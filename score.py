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

from prices import Quote, Rotator, describe_flags, get_price

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "predictions.json"

# Same-cluster predictions are treated as ~70% redundant when computing an
# effective sample size. This is a deliberately crude honesty adjustment, not a
# rigorous estimator - the point is that 15 gold miners must not be able to
# masquerade as 15 independent bets.
CLUSTER_RHO = 0.7

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


def effective_n(entries: list[dict]) -> float:
    """Raw n discounted for correlation within clusters.

    A cluster of k predictions counts as roughly 1 + (k-1)*(1-rho) independent
    bets. Untagged entries and anything tagged 'independent' count in full.
    """
    by_cluster: dict[str, int] = {}
    loose = 0
    for e in entries:
        c = e.get("cluster")
        if not c or c == "independent":
            loose += 1
        else:
            by_cluster[c] = by_cluster.get(c, 0) + 1
    eff = float(loose)
    for k in by_cluster.values():
        eff += 1 + (k - 1) * (1 - CLUSTER_RHO)
    return eff


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
    bm_q = get_price(bm_ticker)

    final_dir: list[tuple[float, int]] = []
    final_dir_entries: list[dict] = []
    provisional: list[tuple[dict, float, float, bool]] = []
    held: list[tuple[dict, str]] = []
    resolved_writes = 0

    for e in preds:
        if e["type"] != "directional":
            continue
        if e.get("outcome") is not None:
            final_dir.append((e["prob"], int(e["outcome"])))
            final_dir_entries.append(e)
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
            outcome = 1 if truth else 0
            final_dir.append((e["prob"], outcome))
            final_dir_entries.append(e)
            if args.resolve:
                e["outcome"] = outcome
                e["resolved_on"] = now.isoformat()
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
    out.append("")

    # --- Small-n caveat ---------------------------------------------------
    eff_all = effective_n(final_dir_entries + factual_entries)
    if eff_all < SMALL_N:
        out.append(
            f"> ⚠️ **Small sample.** Effective n ≈ {eff_all:.1f} (raw {len(all_scored)}), "
            f"below the ~{SMALL_N} needed to say anything firm. These numbers *illustrate* "
            f"calibration; they do not establish skill. \"n too small to conclude\" is a "
            f"valid, pre-committed result."
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
    for e in final_dir_entries + factual_entries:
        pv = e.get("provenance") or {}
        key = (pv.get("model", "unverified"), pv.get("surface", "unverified"))
        cells.setdefault(key, []).append((e["prob"], int(e["outcome"])))
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
    derived = [e for e in final_dir_entries + factual_entries if e.get("derived_from")]
    cold = [e for e in final_dir_entries + factual_entries if not e.get("derived_from")]
    if derived:
        out.append("#### Precursor-derived vs cold predictions")
        out.append("")
        d_b = brier([(e["prob"], int(e["outcome"])) for e in derived])
        c_b = brier([(e["prob"], int(e["outcome"])) for e in cold])
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
