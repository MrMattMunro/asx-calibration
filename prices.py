#!/usr/bin/env python
"""Single choke-point for price fetches, with plausibility gates.

Every price used to *grade* a prediction goes through here. The point is not to
chase a perfectly accurate price - it is to notice when the feed is silently
broken, because a mechanical grade run on a broken price is confidently wrong,
which is worse than no grade at all.

Design (see README "Price-data integrity"):
  - yfinance is PRIMARY. There is no clean, free, automated, independent ASX
    feed to cross-check it against, and every ASX-capable finance MCP just
    re-wraps yfinance (same upstream, zero independence).
  - So the backbone is internal PLAUSIBILITY GATES, which need no dependency:
        missing   - None / NaN / zero
        stale     - identical close across the last N sessions (feed frozen)
        outlier   - absolute 1-day move above a threshold
  - EODHD is an OPTIONAL second source behind EODHD_API_KEY. Absent a key it is
    silently skipped and the gates still run.
  - GOOGLEFINANCE is the zero-cost manual tie-breaker when a gate trips.

A flagged price is NOT rejected here - it is returned with its flags, and the
caller decides. score.py refuses to grade a flagged prediction and lists it for
human adjudication instead.

Usage:
    from prices import get_price, Quote, googlefinance_recipe
    q = get_price("BHP")
    if q.ok:  ...
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance not installed. Run: python -m pip install yfinance")

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "portfolio.json"

# Fallbacks if portfolio.json carries no "integrity" block.
DEFAULT_INTEGRITY = {
    "stale_sessions": 3,
    "outlier_pct": 20.0,
    "divergence_pct": 1.5,
}


def _integrity_config() -> dict:
    cfg = {}
    try:
        cfg = json.loads(CONFIG.read_text(encoding="utf-8")).get("integrity", {})
    except Exception:
        pass
    return {**DEFAULT_INTEGRITY, **{k: v for k, v in cfg.items() if k in DEFAULT_INTEGRITY}}


@dataclass
class Quote:
    """A price plus everything needed to decide whether to trust it."""

    ticker: str
    price: float | None
    flags: list[str] = field(default_factory=list)
    detail: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True only if we have a price AND nothing tripped a gate."""
        return self.price is not None and not self.flags

    def flag_str(self) -> str:
        return ", ".join(self.flags) if self.flags else "-"


def _fetch_yf(ticker: str) -> tuple[float | None, list[float]]:
    """Return (latest price, recent closes). Either may be empty on failure."""
    sym = f"{ticker}.AX"
    price, closes = None, []
    try:
        t = yf.Ticker(sym)
        # fast_info is quickest; history is the robust fallback and also feeds the gates.
        p = t.fast_info.get("last_price") if hasattr(t, "fast_info") else None
        if p:
            price = float(p)
        hist = t.history(period="1mo")
        if not hist.empty:
            closes = [float(c) for c in hist["Close"].dropna().tolist()]
            if price is None and closes:
                price = closes[-1]
    except Exception:
        pass
    return price, closes


def get_price(ticker: str, *, reconcile: bool = False) -> Quote:
    """Fetch a price and run the plausibility gates.

    reconcile=True additionally cross-checks against EODHD when a key is
    available. Callers should reconcile only a rotating handful of tickers per
    run so a free tier is not exhausted.
    """
    cfg = _integrity_config()
    price, closes = _fetch_yf(ticker)
    q = Quote(ticker=ticker, price=price)

    # --- Gate 1: missing -------------------------------------------------
    if price is None or price != price or price == 0:  # price != price catches NaN
        q.price = None
        q.flags.append("missing")
        return q

    # --- Gate 2: stale ---------------------------------------------------
    n = int(cfg["stale_sessions"])
    if len(closes) >= n:
        window = closes[-n:]
        if max(window) == min(window):
            q.flags.append("stale")
            q.detail["stale_window"] = window

    # --- Gate 3: outlier single-day move ---------------------------------
    if len(closes) >= 2 and closes[-2]:
        move = (closes[-1] / closes[-2] - 1) * 100
        q.detail["last_move_pct"] = round(move, 2)
        if abs(move) > float(cfg["outlier_pct"]):
            q.flags.append("outlier")

    # --- Optional second source ------------------------------------------
    if reconcile:
        other = get_price_eodhd(ticker)
        if other is not None:
            q.detail["eodhd"] = other
            diff = abs(other / price - 1) * 100
            q.detail["divergence_pct"] = round(diff, 2)
            if diff > float(cfg["divergence_pct"]):
                q.flags.append("divergence")

    return q


def _eodhd_key() -> str | None:
    """Env var first; a gitignored .secrets.json is the local fallback."""
    key = os.environ.get("EODHD_API_KEY")
    if key:
        return key
    secrets = HERE / ".secrets.json"
    if secrets.exists():
        try:
            return json.loads(secrets.read_text(encoding="utf-8")).get("EODHD_API_KEY")
        except Exception:
            return None
    return None


def get_price_eodhd(ticker: str) -> float | None:
    """Independent second source. Returns None (silently) if unavailable.

    STATUS as at 2026-07-18: NOT ENABLED. No free key has been provisioned, so
    the free-tier prerequisite test has not been run and it is still unconfirmed
    whether plain EOD data for ASX (.AU) works on the free tier at all. Until
    that test passes this always returns None and the layer runs on gates plus
    the manual GOOGLEFINANCE tie-breaker - which is the intended fallback, not a
    degraded mode. See paper-trading-log.md.
    """
    key = _eodhd_key()
    if not key:
        return None
    try:
        import urllib.request

        url = (
            f"https://eodhd.com/api/eod/{ticker}.AU"
            f"?api_token={key}&fmt=json&period=d&order=d&limit=1"
        )
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if isinstance(data, list) and data:
            close = data[0].get("close") or data[0].get("adjusted_close")
            return float(close) if close else None
    except Exception:
        return None
    return None


def googlefinance_recipe(ticker: str) -> str:
    """The manual tie-breaker: paste this into a spreadsheet and eyeball it."""
    return f'=GOOGLEFINANCE("ASX:{ticker}","closeyest")'


class Rotator:
    """Persist a cursor so reconciliation covers all names over several runs.

    EODHD's free tier is ~20 calls/day, so we reconcile a few tickers per run
    rather than the whole book, and rotate which ones.
    """

    def __init__(self, path: Path | None = None, size: int = 3):
        self.path = path or (HERE / ".reconcile-cursor.local.json")
        self.size = size

    def pick(self, tickers: list[str]) -> set[str]:
        if not tickers:
            return set()
        start = 0
        try:
            start = int(json.loads(self.path.read_text(encoding="utf-8")).get("cursor", 0))
        except Exception:
            pass
        chosen = {tickers[(start + i) % len(tickers)] for i in range(min(self.size, len(tickers)))}
        try:
            self.path.write_text(
                json.dumps({"cursor": (start + self.size) % len(tickers)}), encoding="utf-8"
            )
        except Exception:
            pass
        return chosen


def describe_flags(quotes: list[Quote]) -> list[str]:
    """Markdown lines describing any tripped gates, with the adjudication recipe."""
    flagged = [q for q in quotes if q.flags]
    if not flagged:
        return []
    lines = ["", "**Price integrity flags:**", ""]
    for q in flagged:
        px = f"${q.price:,.2f}" if q.price is not None else "n/a"
        lines.append(f"- **{q.ticker}** {px} -> `{q.flag_str()}` {q.detail or ''}")
        lines.append(f"  - adjudicate: `{googlefinance_recipe(q.ticker)}`")
    lines.append("")
    lines.append("_A flagged price is not graded until a human adjudicates it._")
    return lines


if __name__ == "__main__":
    # Smoke test: python prices.py BHP CSL
    for tk in (sys.argv[1:] or ["BHP"]):
        q = get_price(tk)
        print(f"{q.ticker}: {q.price} flags={q.flag_str()} detail={q.detail}")
