#!/usr/bin/env python
"""Compute a measured anchor for an `event-move` prediction.

Why this exists
---------------
Every probability in this ledger is supposed to be anchored to something
COMPUTED, not felt. For a results-day magnitude claim ("|move| exceeds X% on
results day") the anchor is the stock's own history of moving that much on a
results day.

The first attempt at this (2026-08-01 batch) identified past results days as
*the largest-move day* inside each reporting window and then measured that
move. That is selection on the outcome variable and biased the anchor upward by
a measured +1.61pp, leaving 6 of 8 entries over-confident by >0.10.

The corrected method, implemented here and used from 2026-08-02:

  1. Identify each past event day by **maximum VOLUME** inside its reporting
     window. Turnover spikes on results days and is independent of move size,
     so it does not select on the outcome.
  2. Measure the absolute return on that day.
  3. Report the frequency of exceeding the threshold, alongside the
     UNCONDITIONAL daily frequency for context.

Both figures go in the entry's `rationale`. The registered probability is then
shaded DOWN from the event-day figure, because:

  - n is small (16-32 event days over 8 years), and
  - a max-volume day can be an index rebalance or an ex-dividend date rather
    than the result. It is a proxy too. Its one decisive advantage is being
    independent of move size.

Returns are computed on dividend-ADJUSTED closes (auto_adjust=True), so an
ex-dividend drop does not masquerade as a large move. That removes one of the
two contaminants named in the caveat above; index rebalances remain.

Usage
-----
    python anchor.py CSL --threshold 3.0 --months 2,8
    python anchor.py FMG --threshold 3.0 --months 1,4,7,8,10 --years 8
    python anchor.py CBA --threshold 2.0 --months 2,8 --json

`--months` are the calendar months in which that name actually reports. Match
them to the company's real cycle, not a generic Feb/Aug assumption:

    30-Jun FY industrials/healthcare   -> 2,8
    30-Sep FY banks (WBC/NAB/ANZ)      -> 5,11
    quarterly miners (production)      -> 1,4,7,10  (+ 2,8 for results)

Getting these wrong pollutes the sample with non-event days, which drags the
measured frequency DOWN and would make the anchor spuriously conservative.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance not installed. Run: python -m pip install yfinance")


def fetch(ticker: str, years: int):
    """Daily OHLCV on dividend-adjusted closes."""
    sym = ticker if "." in ticker else f"{ticker}.AX"
    df = yf.download(
        sym,
        period=f"{years}y",
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    if df is None or df.empty:
        sys.exit(f"{sym}: no price history returned")
    # yfinance may return MultiIndex columns for a single ticker.
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    df = df.dropna(subset=["Close", "Volume"])
    df["ret"] = df["Close"].pct_change() * 100.0
    return df.dropna(subset=["ret"])


def event_days(df, months: list[int]):
    """One event day per (year, month) window: the max-VOLUME session in it.

    Never the max-move session - that would select on the outcome variable.

    The CURRENT calendar month is skipped. A part-elapsed window has no results
    day in it yet, so its max-volume session is just the busiest ordinary day -
    a non-event that dilutes the measured frequency downward.
    """
    today = date.today()
    out = []
    for (yr, mo), grp in df.groupby([df.index.year, df.index.month]):
        if mo not in months or len(grp) < 5:
            continue
        if (yr, mo) == (today.year, today.month):
            continue
        day = grp["Volume"].idxmax()
        out.append(
            {
                "window": f"{yr}-{mo:02d}",
                "event_day": day.date().isoformat(),
                "abs_move_pct": round(abs(float(grp.loc[day, "ret"])), 3),
                "volume": int(grp.loc[day, "Volume"]),
                "median_window_volume": int(grp["Volume"].median()),
            }
        )
    return sorted(out, key=lambda r: r["window"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ticker")
    ap.add_argument("--threshold", type=float, required=True,
                    help="absolute move %% the claim must exceed, e.g. 2.0")
    ap.add_argument("--months", default="2,8",
                    help="comma-separated reporting months, e.g. 2,8")
    ap.add_argument("--years", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    months = [int(m) for m in a.months.split(",") if m.strip()]
    df = fetch(a.ticker, a.years)
    thr = a.threshold

    uncond_n = len(df)
    uncond_hits = int((df["ret"].abs() > thr).sum())
    uncond = uncond_hits / uncond_n if uncond_n else 0.0

    evs = event_days(df, months)
    ev_hits = sum(1 for e in evs if e["abs_move_pct"] > thr)
    ev_freq = ev_hits / len(evs) if evs else 0.0

    result = {
        "ticker": a.ticker.upper(),
        "threshold_pct": thr,
        "reporting_months": months,
        "years": a.years,
        "history_start": df.index[0].date().isoformat(),
        "history_end": df.index[-1].date().isoformat(),
        "unconditional": {
            "sessions": uncond_n,
            "hits": uncond_hits,
            "freq": round(uncond, 4),
        },
        "event_day": {
            "windows": len(evs),
            "hits": ev_hits,
            "freq": round(ev_freq, 4),
            "median_abs_move_pct": round(
                sorted(e["abs_move_pct"] for e in evs)[len(evs) // 2], 3
            ) if evs else None,
        },
        "elevation_x": round(ev_freq / uncond, 2) if uncond else None,
        "days": evs,
        "computed_on": date.today().isoformat(),
        "method": "event day = max VOLUME in each reporting-month window "
                  "(independent of move size); returns on dividend-adjusted "
                  "closes; SHADE THE REGISTERED PROBABILITY DOWN from event_day.freq "
                  "for small n and for max-volume-day proxy impurity.",
    }

    if a.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n{result['ticker']}  |move| > {thr}%  "
          f"({result['history_start']} to {result['history_end']})")
    print(f"  unconditional : {uncond_hits}/{uncond_n} = {uncond:.1%} of all sessions")
    print(f"  event-day     : {ev_hits}/{len(evs)} = {ev_freq:.1%} "
          f"(windows: months {months})")
    if result["elevation_x"]:
        print(f"  elevation     : x{result['elevation_x']}")
    print(f"  median event-day |move| : {result['event_day']['median_abs_move_pct']}%")
    print("\n  window   event day    |move|%   vol / median-vol")
    for e in evs:
        mult = e["volume"] / e["median_window_volume"] if e["median_window_volume"] else 0
        star = "*" if e["abs_move_pct"] > thr else " "
        print(f"  {e['window']}  {e['event_day']}  {e['abs_move_pct']:7.2f} {star}"
              f"   x{mult:.1f}")
    print("\n  -> SHADE DOWN from the event-day figure when registering.\n")


if __name__ == "__main__":
    main()
