#!/usr/bin/env python
"""Multi-factor ASX screener — rank a universe by quality / momentum / growth / value.

Reads universe.json, pulls fundamentals + 6-month price history via yfinance,
scores each name on four factors, and prints ranked candidate tables.

Usage:
    python screen.py                 # full run (~1-2 min, ~80 tickers)
    python screen.py --top 15        # show top 15 (default 12)
    python screen.py --precursors    # hunt current matches for pre-committed precursor rules

Factors (each name is percentile-ranked 0-100 within the universe, then blended):
    Quality  30%  ROE (+), profit margin (+), debt/equity (-)
    Momentum 30%  6-month return (+), position in 52-week range (+)
    Growth   20%  revenue growth (+)
    Value    20%  P/E (- , positive only), P/B (-), dividend yield (+)

This is an IDEA-GENERATION tool, not advice. High scores = worth a look, nothing more.
yfinance is unofficial/free (~20 min delayed); occasional missing fields are handled.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance not installed. Run: python -m pip install yfinance")

HERE = Path(__file__).resolve().parent
UNIVERSE = HERE / "universe.json"
PRECURSORS = HERE / "precursors.json"


def fetch(ticker: str) -> dict | None:
    """Pull the metrics we score on for one ASX ticker."""
    sym = f"{ticker}.AX"
    try:
        t = yf.Ticker(sym)
        info = t.info or {}
        price = info.get("currentPrice")
        hi, lo = info.get("fiftyTwoWeekHigh"), info.get("fiftyTwoWeekLow")
        # 6-month return from history (more reliable than any info field).
        ret6m = None
        hist = t.history(period="6mo")
        if not hist.empty and price:
            start = hist["Close"].dropna().iloc[0]
            if start:
                ret6m = (price / start - 1) * 100
        # Position in 52-week range, 0 (at low) .. 100 (at high).
        rng_pos = None
        if price and hi and lo and hi > lo:
            rng_pos = (price - lo) / (hi - lo) * 100
        if not price:
            return None
        return {
            "ticker": ticker,
            "price": price,
            "mktcap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "de": info.get("debtToEquity"),
            "margin": info.get("profitMargins"),
            "rev_growth": info.get("revenueGrowth"),
            "div_yield": info.get("dividendYield"),
            "ret6m": ret6m,
            "rng_pos": rng_pos,
        }
    except Exception:
        return None


def pctile_ranks(rows: list[dict], key: str, higher_better: bool, positive_only: bool = False) -> dict:
    """Map row index -> percentile (0-100) for a metric. Missing/invalid -> worst (0)."""
    vals = []
    for i, r in enumerate(rows):
        v = r.get(key)
        if not isinstance(v, (int, float)):  # skip None and any stray strings from yfinance
            continue
        if positive_only and v <= 0:
            continue
        vals.append((i, v))
    ranks = {i: 0.0 for i in range(len(rows))}  # default worst
    if len(vals) < 2:
        return ranks
    vals.sort(key=lambda x: x[1], reverse=higher_better)  # best first: largest if higher_better, else smallest
    n = len(vals)
    for pos, (i, _) in enumerate(vals):
        ranks[i] = (1 - pos / (n - 1)) * 100  # best -> 100, worst -> 0
    return ranks


def num(x, fmt="{:.1f}"):
    return fmt.format(x) if isinstance(x, (int, float)) else "n/a"


# --- Precursor screening ------------------------------------------------------
#
# quant_condition in precursors.json is PROSE, for a human reader. The machine
# version lives here, one explicit predicate per precursor id. That is deliberate:
# parsing the prose would be a fragile guess dressed up as automation, and a
# mis-parsed screen silently changes what cohort gets pre-registered.
#
# A precursor with no predicate registered here is NOT skipped and NOT quietly
# matched against everything — it is reported as sweep-only, so the gap is visible.

def _p_governance(r: dict) -> bool:
    # Tightened 2026-07-18 (was: ret6m < 0 and rng_pos < 40, which matched 37/82
    # names and made the follow-up news sweep untargeted). The quant leg is an
    # operational narrowing device only - governance overhang is invisible in
    # price data, so the news_condition carries this rule's actual signal.
    return (
        isinstance(r.get("ret6m"), (int, float))
        and r["ret6m"] < -15
        and isinstance(r.get("rng_pos"), (int, float))
        and r["rng_pos"] < 25
    )


def _p_insider(r: dict) -> bool:
    return isinstance(r.get("rng_pos"), (int, float)) and r["rng_pos"] < 15


def _p_preupgraded(r: dict) -> bool:
    return (
        isinstance(r.get("rng_pos"), (int, float))
        and r["rng_pos"] > 60
        and isinstance(r.get("ret6m"), (int, float))
        and r["ret6m"] > 0
    )


QUANT_PREDICATES = {
    "governance-overhang-suppresses-good-news": _p_governance,
    "insider-buy-after-warning": _p_insider,
    "preupgraded-guidance-into-result": _p_preupgraded,
}


def run_precursors(rows: list[dict]) -> None:
    """Hunt the universe for names currently matching each pre-committed rule."""
    try:
        rules = json.loads(PRECURSORS.read_text(encoding="utf-8"))["precursors"]
    except Exception as exc:
        sys.exit(f"Could not read precursors.json: {exc}")

    today = date.today()
    tests = 0

    print("\n## Precursor screen — current matches\n")
    print(
        "_Rules are **pre-committed** in `precursors.json`. Register the WHOLE cohort below in "
        "`predictions.json`, including matches that look unpromising — the non-movers are the "
        "control group. See paper-trading-event-studies.md._\n"
    )

    for rule in rules:
        if rule.get("status") == "retired":
            continue
        rid = rule["id"]
        pred = QUANT_PREDICATES.get(rid)
        resolve_date = (today + timedelta(days=int(rule["reaction_window_days"]))).isoformat()

        print(f"\n### `{rid}` — status: {rule.get('status')}\n")
        print(f"- **Hypothesis:** {rule['hypothesis']}")
        print(f"- **Reaction window:** {rule['reaction_window_days']}d → resolves {resolve_date}")
        print(f"- **Default probability:** {rule['default_prob']}")

        if rule.get("quant_condition") and pred is None:
            print(
                f"- ⚠️ **No machine predicate registered for this rule id.** Quant condition is "
                f"`{rule['quant_condition']}` — screen it by hand or add a predicate to "
                f"QUANT_PREDICATES in screen.py. Treating as sweep-only.\n"
            )
            shortlist = []
        elif pred is None:
            print("- **Quant condition:** none (pure-news rule) — whole universe goes to sweep.\n")
            shortlist = []
        else:
            print(f"- **Quant condition:** {rule['quant_condition']}")
            shortlist = [r for r in rows if pred(r)]
            tests += len(rows)

        if rule.get("news_condition"):
            print(f"- **News condition (confirm by sweep):** {rule['news_condition']}")

        if pred is None:
            continue

        if not shortlist:
            print("\n**No current matches.** (A zero-match run is a result — log it.)")
            continue

        print(f"\n**{len(shortlist)} quant match(es)** — each is a CANDIDATE until the news leg is confirmed:\n")
        print("| Ticker | Price | 6mo % | 52wk pos | News leg confirmed? |")
        print("|--------|-------|-------|----------|---------------------|")
        for r in sorted(shortlist, key=lambda r: r["ticker"]):
            print(
                f"| {r['ticker']} | ${num(r['price'],'{:.2f}')} | {num(r['ret6m'])} "
                f"| {num(r['rng_pos'],'{:.0f}')} | [ ] |"
            )

        print("\n<details><summary>Ready-to-paste ledger stubs</summary>\n")
        stubs = []
        for r in sorted(shortlist, key=lambda r: r["ticker"]):
            stubs.append(
                {
                    "id": f"{today.isoformat()}-{r['ticker'].lower()}-{rid}",
                    "logged": today.isoformat(),
                    "type": "directional",
                    "ticker": r["ticker"],
                    "claim": f"{r['ticker']} underperforms VAS on price return between "
                    f"{today.isoformat()} and {resolve_date}",
                    "prob": rule["default_prob"],
                    "resolution": f"price: {r['ticker']}.AX price-return < VAS.AX price-return "
                    f"over [logged, resolve_date]",
                    "resolve_date": resolve_date,
                    "ref_price": round(r["price"], 4),
                    "bm_ref": None,
                    "method": "precursor",
                    "cluster": rule.get("cluster"),
                    "rationale": f"Precursor cohort match: {rule['hypothesis']}",
                    "outcome": None,
                    "resolved_on": None,
                    "source": None,
                    "derived_from": rid,
                    "provenance": {
                        "model": "unverified",
                        "surface": "claude-code-main",
                        "effort": "default",
                        "web_search": False,
                        "generated_by": f"precursor-screen-{today.isoformat()}",
                    },
                }
            )
        print("```json")
        print(json.dumps(stubs, indent=2))
        print("```")
        print(
            "\n⚠️ Before pasting: **stamp `bm_ref`** with the VAS price from the same fetch, set "
            "`provenance.model` to the model you actually configured, and check the claim direction "
            "matches the hypothesis (stubs default to *underperforms*).\n"
        )
        print("</details>")

    print(f"\n---\n\n**Multiple-comparisons footer:** {tests} precursor × name tests this run "
          f"across {len([r for r in rules if r.get('status') != 'retired'])} live rule(s) over "
          f"{len(rows)} names. The more tests, the more spurious matches you should expect — this "
          f"count exists so that risk stays visible rather than hidden.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument(
        "--precursors",
        action="store_true",
        help="hunt the universe for names matching pre-committed precursor rules",
    )
    args = ap.parse_args()

    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))["tickers"]
    print(f"Screening {len(universe)} ASX names via yfinance… (~1-2 min)\n", file=sys.stderr)

    rows = []
    for i, tk in enumerate(universe, 1):
        r = fetch(tk)
        print(f"  [{i}/{len(universe)}] {tk} {'ok' if r else 'skip'}", file=sys.stderr)
        if r:
            rows.append(r)

    if not rows:
        sys.exit("No data fetched — yfinance may be rate-limiting. Try again shortly.")

    # Precursor mode is a different job from factor ranking: it needs only the raw
    # price/momentum fields, so it branches before the percentile blending.
    if args.precursors:
        run_precursors(rows)
        return

    # Factor percentiles.
    roe = pctile_ranks(rows, "roe", True)
    margin = pctile_ranks(rows, "margin", True)
    de = pctile_ranks(rows, "de", False)          # lower debt better
    ret6 = pctile_ranks(rows, "ret6m", True)
    rng = pctile_ranks(rows, "rng_pos", True)
    growth = pctile_ranks(rows, "rev_growth", True)
    pe = pctile_ranks(rows, "pe", False, positive_only=True)   # lower PE better, positive only
    pb = pctile_ranks(rows, "pb", False)
    dy = pctile_ranks(rows, "div_yield", True)

    for i, r in enumerate(rows):
        q = (roe[i] + margin[i] + de[i]) / 3
        m = (ret6[i] + rng[i]) / 2
        g = growth[i]
        v = (pe[i] + pb[i] + dy[i]) / 3
        r["q"], r["m"], r["g"], r["v"] = q, m, g, v
        r["score"] = 0.30 * q + 0.30 * m + 0.20 * g + 0.20 * v

    ranked = sorted(rows, key=lambda r: r["score"], reverse=True)

    def table(title, subset, sort_key):
        print(f"\n### {title}\n")
        print("| # | Ticker | Price | Score | Qual | Mom | Grow | Val | PE | ROE% | Rev g% | 6mo% | 52wk pos |")
        print("|---|--------|-------|-------|------|-----|------|-----|----|----|--------|------|----------|")
        for n_, r in enumerate(subset, 1):
            roe_pct = r["roe"] * 100 if isinstance(r["roe"], (int, float)) else None
            rg_pct = r["rev_growth"] * 100 if isinstance(r["rev_growth"], (int, float)) else None
            print(
                f"| {n_} | {r['ticker']} | ${num(r['price'],'{:.2f}')} | {r['score']:.0f} "
                f"| {r['q']:.0f} | {r['m']:.0f} | {r['g']:.0f} | {r['v']:.0f} "
                f"| {num(r['pe'])} | {num(roe_pct)} | {num(rg_pct)} | {num(r['ret6m'])} | {num(r['rng_pos'],'{:.0f}')} |"
            )

    table(f"Top {args.top} — blended (quality + momentum + growth + value)", ranked[: args.top], "score")
    table("Top 6 — pure momentum", sorted(rows, key=lambda r: r["m"], reverse=True)[:6], "m")
    table("Top 6 — pure value", sorted(rows, key=lambda r: r["v"], reverse=True)[:6], "v")

    print(
        "\n_Idea-generation only. Scores are relative ranks within this universe, not advice. "
        "Verify anything interesting before acting._"
    )


if __name__ == "__main__":
    main()
