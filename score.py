#!/usr/bin/env python
"""Calibration scorer for the pre-registered prediction ledger.

Reads predictions.json, resolves what can be resolved mechanically, and prints a
ready-to-paste markdown block: Brier scores against baselines, a calibration
table, effective sample size, provisional standings, and the factual entries
still needing a source check.

Usage:
    python score.py              # read-only, safe to run any time
    python score.py --resolve    # ALSO write outcome/resolved_on back for
                                 # directional predictions past resolve_date

Design commitments encoded here (see README):
  - Directional outcomes are COMPUTED from price, never judged.
  - Grading uses the ref_price / bm_ref stamped at logging time. An entry
    missing either is HELD, not graded against an improvised baseline.
  - A price carrying an unresolved integrity flag is HELD, not graded.
  - Factual entries cannot be auto-resolved; they are listed for a source check
    and only scored once a human sets outcome AND cites a source URL.
  - The provenance table is DESCRIPTIVE ONLY. No model comparison at this n.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from prices import Quote, Rotator, describe_flags, get_close_on, get_price

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "predictions.json"

# --- Correlation model for effective sample size ------------------------------
#
# MEASURED, not assumed (2026-07-31, 508 sessions of ASX daily data to 2026-07-31,
# 15 names, 105 pairs). What matters is the correlation of the OUTCOME actually
# being predicted, not of the underlying prices:
#
#     raw daily returns .............. rho = +0.084   <- the market factor
#     daily EXCESS returns vs VAS .... rho = +0.002
#     39-day beat/not-beat outcome ... rho = -0.020
#
# The market factor is real but CANCELS between the two legs of a relative call
# ("X beats VAS"), because it sits on both sides. So two relative calls on
# different names over the same window are very nearly independent bets, and the
# old model - which discounted them 70% for sharing a sector tag - was wrong.
#
# The correlation that IS real, and that the old model missed entirely:
#   1. SAME TICKER across two entries. Nearly the same bet, and it slipped
#      through whenever the two carried different cluster tags (e.g. the two live
#      CSL entries, which shared no tag and so were counted in full).
#   2. WINDOW OVERLAP. Two calls on one ticker over disjoint periods are far more
#      independent than two over identical periods.
#
# Same-cluster is kept as a modest residual allowance for theme/method
# correlation the cross-sectional measurement cannot see (e.g. reporting-date
# entries share a failure mode, not a market factor).
SAME_TICKER_RHO = 0.85
SAME_CLUSTER_RHO = 0.40

SMALL_N = 20
BANDS = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0001)]


def today() -> date:
    return datetime.now().date()


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def brier(items: list[tuple[float, int]]) -> float | None:
    """items = [(prob, outcome)]. Mean squared error of the probability."""
    if not items:
        return None
    return sum((p - o) ** 2 for p, o in items) / len(items)


def _window(e: dict) -> tuple[date, date] | None:
    """The measurement window [logged, resolve_date], if both are present."""
    try:
        return parse_date(e["logged"]), parse_date(e["resolve_date"])
    except Exception:
        return None


def _overlap_fraction(a: dict, b: dict) -> float:
    """Fraction of the SHORTER window that the two entries share, in [0, 1].

    Returns 1.0 when either window is unknown - the conservative default, since
    assuming no overlap would inflate effective n.
    """
    wa, wb = _window(a), _window(b)
    if not wa or not wb:
        return 1.0
    lo = max(wa[0], wb[0])
    hi = min(wa[1], wb[1])
    shared = (hi - lo).days
    if shared <= 0:
        return 0.0
    shortest = min((wa[1] - wa[0]).days, (wb[1] - wb[0]).days)
    if shortest <= 0:
        return 1.0
    return min(1.0, shared / shortest)


def pair_rho(a: dict, b: dict) -> float:
    """Estimated correlation between two predictions' outcomes.

    The driver differs by track, because the two tracks fail differently:

      - DIRECTIONAL: the ticker dominates. Two price calls on one name over
        overlapping windows are close to the same bet. Two price calls on
        DIFFERENT names are very nearly independent once the benchmark leg
        cancels the market factor (measured rho = -0.020), so they get only the
        modest residual cluster allowance.
      - FACTUAL: the ticker is close to irrelevant and the METHOD is what
        correlates. "Does NST report on the 29th" and "does NST beat VAS" share
        a subject but almost no information; whereas two reporting-date claims on
        unrelated companies share a real failure mode - published calendars being
        less reliable than assumed. So factual pairs correlate by cluster.
      - CROSS-TRACK on the same subject: correlated only through shared
        company-specific information. This one is a judgement call, NOT measured;
        it is set to the cluster rho as a deliberately conservative middle.
    """
    if a is b:
        return 1.0
    ta, tb = a.get("type"), b.get("type")
    same_ticker = bool(a.get("ticker")) and a.get("ticker") == b.get("ticker")
    ca, cb = a.get("cluster"), b.get("cluster")
    same_cluster = bool(ca) and ca == cb and ca != "independent"

    if ta == "factual" and tb == "factual":
        # Point-in-time events: no windows to overlap, method is the driver.
        return SAME_CLUSTER_RHO if same_cluster else 0.0

    if ta != tb:
        return SAME_CLUSTER_RHO if same_ticker else 0.0

    # Both directional.
    if same_ticker:
        base = SAME_TICKER_RHO
    elif same_cluster:
        base = SAME_CLUSTER_RHO
    else:
        return 0.0
    return base * _overlap_fraction(a, b)


def effective_n(entries: list[dict]) -> float:
    """Effective sample size under the estimated correlation structure.

    Uses the standard n_eff = n^2 / sum_ij(rho_ij), which reduces to the familiar
    n / (1 + (n-1)*rho) when every pair shares one correlation. Reported instead
    of raw n so that near-duplicate bets cannot masquerade as independent sample.
    """
    n = len(entries)
    if n == 0:
        return 0.0
    total = 0.0
    for i, a in enumerate(entries):
        for j, b in enumerate(entries):
            total += 1.0 if i == j else pair_rho(a, b)
    if total <= 0:
        return float(n)
    return min(float(n), n * n / total)


def claim_is_beat(e: dict) -> bool:
    """Does this directional claim assert OUT-performance vs the benchmark?"""
    res = (e.get("resolution") or "").lower()
    if "price-return >" in res:
        return True
    if "price-return <" in res:
        return False
    # Fall back to the claim text if the resolution rule is phrased unusually.
    return "beats" in (e.get("claim") or "").lower()


def fmt_pct(x: float | None) -> str:
    return f"{x:+.1f}%" if isinstance(x, (int, float)) else "n/a"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--resolve",
        action="store_true",
        help="write outcome/resolved_on back for directional predictions past resolve_date",
    )
    args = ap.parse_args()

    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    preds = data["predictions"]
    bm_ticker = data.get("benchmark_ticker", "VAS")
    now = today()

    out: list[str] = []
    out.append(f"### {now.isoformat()} — Calibration score (predictions.json)")
    out.append("")

    # --- Price fetches (one per distinct ticker, plus the benchmark) -------
    tickers = sorted({e["ticker"] for e in preds if e["type"] == "directional" and e.get("ticker")})

    # EODHD's free tier is ~20 calls/day, so only a rotating few tickers are
    # cross-checked each run; the cursor persists so every name gets covered over
    # several check-ins. Without a key this is a no-op and the gates still run.
    reconciled = Rotator(size=3).pick(tickers)
    quotes: dict[str, Quote] = {tk: get_price(tk, reconcile=tk in reconciled) for tk in tickers}
    # The benchmark can now also be a directional SUBJECT (absolute-basis index
    # calls), in which case it is already in `quotes` — reuse it rather than
    # spending a second fetch, and a second EODHD reconcile call, on it.
    bm_q = quotes.get(bm_ticker) or get_price(bm_ticker)

    final_dir: list[tuple[float, int]] = []
    final_dir_entries: list[dict] = []
    # (entry, outcome) for everything graded this run. Kept separately because a
    # directional entry that came due is graded IN MEMORY and only gets its
    # `outcome` written back under --resolve; reading e["outcome"] downstream
    # would hit None on a read-only run.
    graded: list[tuple[dict, int]] = []
    provisional: list[tuple[dict, float, float, bool]] = []
    held: list[tuple[dict, str]] = []
    resolved_writes = 0

    for e in preds:
        if e["type"] != "directional":
            continue
        if e.get("outcome") is not None:
            final_dir.append((e["prob"], int(e["outcome"])))
            final_dir_entries.append(e)
            graded.append((e, int(e["outcome"])))
            continue

        # Pre-registration completeness is a hard gate. Absolute-basis entries
        # (the subject IS the benchmark, so a relative comparison is degenerate)
        # need ref_price and threshold_pct instead of bm_ref.
        absolute = e.get("basis") == "absolute"
        if absolute:
            if e.get("ref_price") in (None, 0) or e.get("threshold_pct") is None:
                held.append(
                    (e, "incomplete pre-registration (missing ref_price or threshold_pct)")
                )
                continue
        elif e.get("ref_price") in (None, 0) or e.get("bm_ref") in (None, 0):
            held.append((e, "incomplete pre-registration (missing ref_price or bm_ref)"))
            continue

        q = quotes.get(e["ticker"])
        if q is None or q.price is None:
            held.append((e, "price unavailable"))
            continue
        if q.flags:
            held.append((e, f"integrity flag: {q.flag_str()}"))
            continue
        if not absolute and (bm_q.price is None or bm_q.flags):
            held.append((e, f"benchmark price unusable ({bm_q.flag_str()})"))
            continue

        ret = (q.price / e["ref_price"] - 1) * 100
        if absolute:
            # No benchmark leg: the claim is about the subject's own return
            # clearing a pre-registered threshold. Comparing the benchmark to
            # itself would make `beat` False by construction and silently
            # mis-grade every entry, so that path is never taken here.
            bm_ret = e["threshold_pct"]
            beat = ret > bm_ret
        else:
            bm_ret = (bm_q.price / e["bm_ref"] - 1) * 100
            beat = ret > bm_ret
        truth = beat if claim_is_beat(e) else (not beat)

        if now >= parse_date(e["resolve_date"]):
            # Grade at the CLOSE ON resolve_date, not at today's price. Running a
            # check-in late must not lengthen the measurement window - the rule
            # was pre-registered over [logged, resolve_date] and grading on a
            # later price silently measures something else.
            rd = parse_date(e["resolve_date"])
            px, px_on = get_close_on(e["ticker"], rd)
            if px is None:
                held.append((e, f"no close on/before resolve_date {e['resolve_date']}"))
                continue
            r_ret = (px / e["ref_price"] - 1) * 100
            if absolute:
                r_bm_ret = e["threshold_pct"]
            else:
                bpx, _ = get_close_on(bm_ticker, rd)
                if bpx is None:
                    held.append(
                        (e, f"no {bm_ticker} close on/before resolve_date {e['resolve_date']}")
                    )
                    continue
                r_bm_ret = (bpx / e["bm_ref"] - 1) * 100
            r_beat = r_ret > r_bm_ret
            r_truth = r_beat if claim_is_beat(e) else (not r_beat)
            outcome = 1 if r_truth else 0
            final_dir.append((e["prob"], outcome))
            final_dir_entries.append(e)
            graded.append((e, outcome))
            if args.resolve:
                e["outcome"] = outcome
                e["resolved_on"] = now.isoformat()
                # Audit trail: which session actually priced the grade, and the
                # two numbers compared. Makes a late-run check-in inspectable.
                e["graded_on"] = {
                    "session": px_on.isoformat() if px_on else None,
                    "subject_return_pct": round(r_ret, 4),
                    "bar_pct": round(r_bm_ret, 4),
                }
                resolved_writes += 1
        else:
            provisional.append((e, ret, bm_ret, truth))

    # --- Factual ----------------------------------------------------------
    factual_scored: list[tuple[float, int]] = []
    factual_entries: list[dict] = []
    factual_pending: list[dict] = []
    for e in preds:
        if e["type"] != "factual":
            continue
        if e.get("outcome") is not None and e.get("source"):
            factual_scored.append((e["prob"], int(e["outcome"])))
            factual_entries.append(e)
            graded.append((e, int(e["outcome"])))
        else:
            factual_pending.append(e)

    # --- Directional results ---------------------------------------------
    out.append("#### Directional track (graded mechanically from price)")
    out.append("")
    b = brier(final_dir)
    if b is None:
        out.append(f"- No directional predictions have resolved yet ({len(provisional)} live).")
    else:
        n = len(final_dir)
        base_rate = sum(o for _, o in final_dir) / n
        base_brier = base_rate * (1 - base_rate)
        eff = effective_n(final_dir_entries)
        out.append(f"- **Brier: {b:.4f}** (n={n}, ≈ effective n {eff:.1f})")
        out.append(f"- Always-0.5 baseline: **0.2500** — {'BEATS' if b < 0.25 else 'does NOT beat'} it")
        out.append(
            f"- Base-rate baseline (p̄={base_rate:.2f}): **{base_brier:.4f}** — "
            f"{'beats' if b < base_brier else 'does not beat'} it"
        )
        verdict = (
            "shows no directional skill (as expected — public news is priced in)"
            if b >= 0.25
            else "beats the coin-flip baseline — treat as LUCK at this sample size, not edge"
        )
        out.append(f"- **Verdict:** {verdict}.")
    out.append("")

    # --- Factual results --------------------------------------------------
    out.append("#### Factual track (graded against a cited source)")
    out.append("")
    fb = brier(factual_scored)
    if fb is None:
        out.append(f"- No factual predictions resolved yet ({len(factual_pending)} awaiting source check).")
    else:
        n = len(factual_scored)
        acc = sum(o for _, o in factual_scored) / n
        eff = effective_n(factual_entries)
        out.append(f"- **Brier: {fb:.4f}** · accuracy {acc:.0%} (n={n}, ≈ effective n {eff:.1f})")
    out.append("")

    # --- Calibration table ------------------------------------------------
    out.append("#### Calibration table (all resolved predictions)")
    out.append("")
    all_scored = final_dir + factual_scored
    if not all_scored:
        out.append("_Nothing resolved yet — the table populates as predictions come due._")
    else:
        out.append("| Prob band | Mean predicted | Actual frequency | n |")
        out.append("|-----------|----------------|------------------|---|")
        for lo, hi in BANDS:
            bucket = [(p, o) for p, o in all_scored if lo <= p < hi]
            if not bucket:
                out.append(f"| {lo:.1f}–{min(hi,1.0):.1f} | — | — | 0 |")
                continue
            mp = sum(p for p, _ in bucket) / len(bucket)
            af = sum(o for _, o in bucket) / len(bucket)
            out.append(f"| {lo:.1f}–{min(hi,1.0):.1f} | {mp:.2f} | {af:.2f} | {len(bucket)} |")
        # The bands start at 0.5, so a sub-0.5 probability would be counted in
        # the Brier score but vanish from this table without trace. The house
        # convention is to phrase every claim so its probability is >= 0.5
        # (state the complement instead); this makes a breach loud rather than
        # silent.
        low = [p for p, _ in all_scored if p < 0.5]
        if low:
            out.append("")
            out.append(
                f"> ⚠️ **{len(low)} resolved prediction(s) carry P < 0.5 "
                f"({', '.join(f'{p:.2f}' for p in sorted(low))}) and are NOT shown in any band "
                f"above** — they are still in the Brier score. Convention: phrase claims so P ≥ 0.5."
            )
    out.append("")

    # --- Small-n caveat ---------------------------------------------------
    # ALWAYS printed. This caveat used to appear only while effective n was below
    # SMALL_N, which meant the warning protecting every reading of these numbers
    # would switch itself off exactly as the sample grew - and crossing ~20 does
    # NOT make a calibration curve readable. It only stops it being hopeless.
    # Per-band n is what governs whether a band means anything, so that is now
    # reported alongside, and the caveat is unconditional.
    eff_all = effective_n(final_dir_entries + factual_entries)
    band_ns = [len([1 for p, _ in all_scored if lo <= p < hi]) for lo, hi in BANDS]
    biggest = max(band_ns) if band_ns else 0
    if eff_all < SMALL_N:
        out.append(
            f"> ⚠️ **Small sample.** Effective n ≈ {eff_all:.1f} (raw {len(all_scored)}), "
            f"below the ~{SMALL_N} floor. These numbers *illustrate* calibration; they do not "
            f"establish skill. \"n too small to conclude\" is a valid, pre-committed result."
        )
    else:
        out.append(
            f"> ⚠️ **Sample caveat (always shown).** Effective n ≈ {eff_all:.1f} "
            f"(raw {len(all_scored)}) is past the ~{SMALL_N} floor, but that floor only marks "
            f"where the numbers stop being hopeless — it is not a licence to draw conclusions."
        )
    out.append(
        f"> **Per-band n is the binding constraint, and the largest band holds {biggest}.** "
        f"Detecting *gross* miscalibration (a claimed 0.90 that is really 0.70) needs ≈21 in "
        f"that band; moderate (0.90 vs 0.80) needs ≈62; subtle (0.60 vs 0.50) needs ≈97. "
        f"Read any band below those thresholds as decorative."
    )
    out.append("")

    # --- Provisional standings -------------------------------------------
    out.append("#### Provisional standings — NOT FINAL (live directional predictions)")
    out.append("")
    if not provisional:
        out.append("_None live._")
    else:
        out.append("| ID | Claim | P | Move | Bar (VAS or threshold) | On track? | Resolves |")
        out.append("|----|-------|---|------|------------------------|-----------|----------|")
        for e, ret, bm_ret, truth in provisional:
            bar = f"{fmt_pct(bm_ret)} (abs)" if e.get("basis") == "absolute" else fmt_pct(bm_ret)
            out.append(
                f"| `{e['id']}` | {e['claim'][:52]}… | {e['prob']:.2f} | {fmt_pct(ret)} | "
                f"{bar} | {'yes' if truth else 'no'} | {e['resolve_date']} |"
            )
    out.append("")

    # --- Held -------------------------------------------------------------
    if held:
        out.append("#### Held — not graded (needs adjudication)")
        out.append("")
        for e, why in held:
            out.append(f"- `{e['id']}` — {why}")
        out.append("")

    # --- Factual needing source check ------------------------------------
    out.append("#### Needs source check (factual, unresolved)")
    out.append("")
    if not factual_pending:
        out.append("_None._")
    else:
        for e in factual_pending:
            due = "DUE" if now >= parse_date(e["resolve_date"]) else "not yet due"
            out.append(f"- `{e['id']}` (P {e['prob']:.2f}, {e['resolve_date']}, {due}) — {e['claim']}")
            out.append(f"  - resolve by: {e['resolution']}")
    out.append("")

    # --- Provenance (descriptive only) ------------------------------------
    out.append("#### Provenance breakdown")
    out.append("")
    out.append(
        "> **DESCRIPTIVE ONLY — n is far too small for model comparison. "
        "Do not read this as a ranking.**"
    )
    out.append("")
    cells: dict[tuple[str, str], list[tuple[float, int]]] = {}
    for e, o in graded:
        pv = e.get("provenance") or {}
        key = (pv.get("model", "unverified"), pv.get("surface", "unverified"))
        cells.setdefault(key, []).append((e["prob"], o))
    if not cells:
        out.append("_No resolved predictions yet._")
    else:
        out.append("| Model | Surface | n | Brier | Note |")
        out.append("|-------|---------|---|-------|------|")
        for (model, surface), items in sorted(cells.items()):
            note = "n < 5 — not interpretable" if len(items) < 5 else ""
            out.append(f"| `{model}` | {surface} | {len(items)} | {brier(items):.4f} | {note} |")
    out.append("")

    # --- Precursor slice --------------------------------------------------
    derived = [(e, o) for e, o in graded if e.get("derived_from")]
    cold = [(e, o) for e, o in graded if not e.get("derived_from")]
    if derived:
        out.append("#### Precursor-derived vs cold predictions")
        out.append("")
        d_b = brier([(e["prob"], o) for e, o in derived])
        c_b = brier([(e["prob"], o) for e, o in cold])
        out.append(f"- Precursor-derived: Brier {d_b:.4f} (n={len(derived)})")
        out.append(
            f"- Cold: Brier {c_b:.4f} (n={len(cold)})" if c_b is not None else "- Cold: none resolved"
        )
        out.append("")

    # --- Integrity flags --------------------------------------------------
    out.extend(describe_flags(list(quotes.values()) + [bm_q]))

    print("\n".join(out))

    if args.resolve and resolved_writes:
        LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\n[--resolve] wrote outcomes for {resolved_writes} prediction(s).", file=sys.stderr)
    elif args.resolve:
        print("\n[--resolve] nothing was past its resolve_date; ledger unchanged.", file=sys.stderr)


if __name__ == "__main__":
    main()
