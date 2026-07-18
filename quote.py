#!/usr/bin/env python
"""Mark the paper-trading book to market and grade the watch-list calls.

Reads portfolio.json (the machine-readable source of truth), pulls live-ish ASX
prices via prices.py (~20 min delayed, free), and prints a ready-to-paste
markdown check-in block for paper-trading-log.md.

NOTE: money P&L is the SECONDARY metric in this repo. The primary output is
calibration - see predictions.json and score.py.

Usage:
    python quote.py

Notes:
- All price fetches route through prices.py so plausibility gates run and any
  suspect price is flagged rather than silently used.
- ASX tickers get an .AX suffix for Yahoo (e.g. BHP -> BHP.AX).
- Shares are derived from alloc/entry so rounding never drifts.
- yfinance is unofficial and can occasionally fail for a ticker; those rows
  show "n/a" rather than crashing the run.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Windows consoles default to cp1252 and mangle unicode (e.g. em-dash). Force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from prices import Quote, describe_flags, get_price as fetch_quote

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "portfolio.json"

# Every Quote fetched this run, so integrity flags can be surfaced at the end.
QUOTES: list[Quote] = []


def get_price(ticker: str) -> float | None:
    """Latest price for an ASX ticker via prices.py, or None if unavailable.

    Flags are collected rather than raised: this script reports the money book,
    where a flagged price is worth showing with a warning. score.py is the one
    that refuses to *grade* on a flagged price.
    """
    q = fetch_quote(ticker)
    QUOTES.append(q)
    return q.price


def money(x: float) -> str:
    return f"${x:,.2f}"


def pct(x: float) -> str:
    return f"{x:+.1f}%"


def main() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    today = datetime.now().strftime("%Y-%m-%d")

    # --- Benchmark ---
    bm = cfg["benchmark"]
    bm_price = get_price(bm["ticker"])
    pot = cfg["pot"]
    bm_units = pot / bm["entry"]
    bm_val = bm_units * bm_price if bm_price else None
    bm_ret = (bm_val / pot - 1) * 100 if bm_val else None

    # --- Holdings ---
    rows = []
    book_val = 0.0
    for h in cfg["holdings"]:
        price = get_price(h["ticker"])
        shares = h["alloc"] / h["entry"]
        if price is None:
            rows.append((h["ticker"], h["entry"], None, None, None, None))
            continue
        val = shares * price
        book_val += val
        pnl = val - h["alloc"]
        pnl_pct = (price / h["entry"] - 1) * 100
        rows.append((h["ticker"], h["entry"], price, val, pnl, pnl_pct))

    book_ret = (book_val / pot - 1) * 100

    # --- Output: ready-to-paste markdown ---
    out = []
    out.append(f"### {today} — Check-in")
    out.append("")
    out.append("| Ticker | Entry | Current | Value | P&L $ | P&L % |")
    out.append("|--------|-------|---------|-------|-------|-------|")
    for tk, entry, price, val, pnl, pnl_pct in rows:
        if price is None:
            out.append(f"| {tk} | ${entry:g} | n/a | n/a | n/a | n/a |")
        else:
            out.append(f"| {tk} | ${entry:g} | ${price:,.2f} | {money(val)} | {money(pnl)} | {pct(pnl_pct)} |")
    out.append("")
    out.append(f"- **Book total:** {money(book_val)} vs {money(pot)} cost -> **{pct(book_ret)}**")
    if bm_val:
        out.append(f"- **Benchmark (all-VAS):** {money(bm_val)} -> **{pct(bm_ret)}**")
        edge = book_ret - bm_ret
        verb = "beating" if edge > 0 else "lagging"
        out.append(f"- **Verdict:** active picks are **{verb}** the index by {abs(edge):.1f} pts")
    else:
        out.append("- **Benchmark (all-VAS):** n/a (price fetch failed)")
    out.append("")

    # --- Watch-list grading ---
    out.append("**Watch-list calls (pre-calibration cohort — binary, grandfathered):**")
    out.append("")
    out.append("| Ticker | Call | Ref | Current | Move | vs VAS | Right so far? |")
    out.append("|--------|------|-----|---------|------|--------|---------------|")
    for w in cfg["watchlist"]:
        price = get_price(w["ticker"])
        if price is None:
            out.append(f"| {w['ticker']} | {w['call']} | ${w['ref']:g} | n/a | n/a | n/a | n/a |")
            continue
        move = (price / w["ref"] - 1) * 100
        vs_vas = move - bm_ret if bm_ret is not None else None
        # "up/outperform" call is right if it beat VAS; "down/underperform" if it lagged VAS.
        if vs_vas is None:
            right = "?"
        elif w["call"] == "up":
            right = "YES" if vs_vas > 0 else "no"
        else:
            right = "YES" if vs_vas < 0 else "no"
        vs_str = pct(vs_vas) if vs_vas is not None else "n/a"
        out.append(
            f"| {w['ticker']} | {w['call']} | ${w['ref']:g} | ${price:,.2f} | {pct(move)} | {vs_str} | {right} |"
        )
    out.append("")
    out.append(
        "- These 8 calls predate the calibration ledger and carry no probability. They are kept "
        "and graded YES/no exactly as originally logged, but are **excluded** from calibration "
        "scoring — retro-fitting a probability after the fact would contaminate it."
    )
    out.append(
        "- Calibration-scored predictions (from 2026-07-18) live in `predictions.json` — run `score.py`."
    )
    out.append("- Notes: ")

    out.extend(describe_flags(QUOTES))

    print("\n".join(out))


if __name__ == "__main__":
    main()
