# asx-calibration

**Is an LLM's market research any good — and does it know what it doesn't know?**

This repo is a small, pre-registered forecasting experiment run against the ASX. It started life
as a $20,000 *paper* portfolio (mock money, no brokerage account) and was deliberately reframed on
2026-07-18, because "can an AI beat the market" is close to unanswerable at this sample size,
while two adjacent questions are genuinely measurable:

1. **Factual research accuracy** — when the model asserts a checkable fact ("CSL reports on 18 Aug"),
   how often is that true?
2. **Calibration** — when it says 65%, does the thing happen about 65% of the time?

Calibration is the interesting one. It is the property that makes a predictor *usable*: a
badly-calibrated 90% is worse than an honest 55%. It is measurable at small n in a way that
"skill" is not. And it transfers — the habit of writing down a probability and an objective
resolution rule *before* the outcome is known works for any high-stakes call, not just stocks.

> **Not financial advice.** Nothing here is a recommendation. The pot is imaginary, the picks are a
> methodology demo, and the honest expected result is that the directional track shows *no skill*.

---

## The experiment in one page

**Two tracks, scored separately.**

| Track | Resolves against | Expectation |
| ----- | ---------------- | ----------- |
| **Directional** | Price. `score.py` computes the outcome from yfinance — no human judgement. | Little or no skill. Public news is priced in. Brier ≈ 0.25. |
| ↳ *relative* (default) | The subject's price return vs the benchmark's, both legs stamped at logging time. | Strips out market direction — tests stock selection, not beta. |
| ↳ *absolute* (`basis: "absolute"`) | The subject's own return vs a pre-registered `threshold_pct`; `bm_ref` is null. | Used where the subject **is** the benchmark. Anchored to a computed base rate, so a large deviation from it is itself the signal worth catching. |
| **Factual** | A citable primary source, URL recorded at resolution. | Reliable, but watch for over-confidence — a 0.90 that should have been 0.75. |

Splitting them is the whole point: it exposes *where* reliability lives (probably the research)
versus where it doesn't (probably the forecasting).

**The metric.** [Brier score](https://en.wikipedia.org/wiki/Brier_score) = mean((probability − outcome)²).
Lower is better. Two baselines to beat:

- **Always-0.5** → Brier 0.25 by construction. Beating this is the bar for *any* directional skill.
- **Base rate** → always predict the observed outcome frequency p̄; Brier = p̄(1−p̄).

Brier alone conflates calibration with resolution, so a **calibration table** sits next to it:
per 10-point probability band, mean predicted vs actual frequency vs n.

**Effective sample size, not raw count.** Fifteen gold miners is one gold bet cloned fifteen times.
Every prediction carries a `cluster` tag; `score.py` reports raw n *and* a crude effective n that
down-weights same-cluster predictions. This is why the ledger deliberately spans banks, energy,
telco, consumer staples, infrastructure and healthcare rather than more of the same theme.

---

## Anti-bias safeguards

The failure mode this design exists to prevent is the obvious one: the same system writes the
thesis, seeds the risks, *and* judges whether it came true.

1. **Pre-registration.** Every entry is written with its probability **and its objective resolution
   rule** before the outcome is known. `ref_price` and `bm_ref` are stamped at logging time and locked.
2. **Append-only.** Entries are never edited after logging — only resolved (`outcome`, `resolved_on`,
   `source` filled in). No goalpost-moving.
3. **Mechanical grading.** Directional outcomes are *computed*, not judged. Factual outcomes are
   binary and must cite a resolving URL — no prose "I was basically right."
4. **Grandfathering.** Eight binary up/down calls predate the ledger. They stay graded the old way as a
   labelled "pre-calibration cohort" and are **excluded** from the probability ledger — retro-assigning
   a probability after a week of price action would contaminate calibration.
5. **Integrity-gated prices.** A mechanical grade must never run on a silently-broken price. See below.
6. **Pre-committed precursor rules.** Precursor patterns are never fitted backward; see
   [`paper-trading-event-studies.md`](paper-trading-event-studies.md).
7. **Small-n honesty.** `score.py` prints n beside every metric and caveats below ~20. "n too small to
   conclude" is a valid pre-committed result, not a failure.

---

## Provenance — which AI, exactly

An experiment whose headline is *"is this AI calibrated"* is uninterpretable without saying **which
AI**. The model changes during the run, and predictions come from more than one surface (a main
session, and delegated research subagents with their own context and system prompt). So every entry
carries a `provenance` block: exact model ID, surface, effort, whether live web search informed it,
and a batch tag.

**This is recorded for attribution and reproducibility — not as a hypothesis.** Total sample is
~20–40. Split by model *and* surface *and* track and per-cell n is in the low single digits.
`score.py` prints a per-`(model, surface)` table under an explicit *descriptive only* header, and the
pre-commitment is: **no model-comparison claim is made at this wrap, whatever the numbers look like.**
A deliberate comparison needs its own design — the same predictions posed to two models
independently — which is a follow-on experiment, not something to reverse-engineer out of this ledger.

---

## Price-data integrity

The real risk is not a small cross-source difference; it is a **silently broken price** producing a
confident wrong grade. Research (2026-07-18) found no clean, free, automated, *independent* ASX feed:
Stooq is now bot-gated, Twelve Data / Finnhub / FMP free tiers are US-only or gate ASX to paid, Alpha
Vantage is unreliable for ASX at 25 req/day, and every ASX-capable finance MCP just re-wraps yfinance
(same upstream, zero independence). So:

- **yfinance stays primary.**
- **Plausibility gates** (`prices.py`) catch the failure modes that actually mis-grade — missing/NaN/zero,
  stale-unchanged across N sessions, outlier single-day move. No new dependency needed.
- **EODHD** is an automated second source behind `EODHD_API_KEY` — **tested and enabled 2026-07-18**
  (its free tier does return real ASX closes, not US-demo-only). `score.py` reconciles a **rotating 3
  tickers per run** via a persisted cursor to stay inside the ~20 calls/day free tier; a gap above 1.5%
  raises a `divergence` flag. Absent a key it is silently skipped and the gates still run.
  *Scope note:* it agrees with yfinance to the cent, which is expected for canonical ASX closes and is
  **not** proof of independence. It catches **feed breakage**, not a bad upstream common to both.
- **`=GOOGLEFINANCE("ASX:BHP","closeyest")`** is the zero-cost manual tie-breaker when a gate trips.

**A tripped, unadjudicated flag blocks grading.** `score.py` lists the prediction under
*held: integrity flag* rather than assigning an outcome.

---

## Files

| File | What it is |
| ---- | ---------- |
| `predictions.json` | The append-only, pre-registered prediction ledger. The heart of it. |
| `score.py` | Resolves what it can and prints Brier, calibration table, baselines, effective n. |
| `prices.py` | Single choke-point for price fetches + plausibility gates. |
| `quote.py` | Marks the paper book to market; grades the grandfathered binary cohort. |
| `screen.py` | Multi-factor idea screener; `--precursors` hunts pre-committed precursor patterns. |
| `precursors.json` | Pre-committed precursor rule-set (never authored to fit today's matches). |
| `portfolio.json` | The mock book, benchmark, and integrity thresholds. |
| `universe.json` | ~83 liquid ASX names the screener ranks. |
| `paper-trading-log.md` | The narrative log — every check-in, in the open. |
| `paper-trading-event-studies.md` | Precursor / event-study protocol + worked examples. |
| `CHECKIN.md` | The repeatable check-in runbook. The step order is what keeps pre-registration honest. |
| `FINDINGS.md` | The evolving honest findings report. Null results included. |

## Running it

```bash
python -m pip install yfinance
python quote.py       # mark the book to market + grade the grandfathered cohort
python score.py       # calibration scoring (read-only)
python score.py --resolve   # write outcomes back for predictions past resolve_date
python screen.py --top 15   # idea generation
python screen.py --precursors   # hunt current precursor matches
```

Python 3.12. `yfinance` is the only third-party dependency.

---

## Pre-publish scrub checklist

This repo is public and developed alongside a private workspace. Before any commit:

- [ ] **No content pulled in from the private workspace's personal-context files** — specifically
      `MEMORY.md`, `context/*.md`, `strategy.md`, `current-data.md`, or any personal plan. This is the
      firewall: it guards against pulling personal context *in*, not against publishing the experiment.
- [ ] No real account balances, net worth, salary, or superannuation figures.
- [ ] No house-deposit, health, property-purchase or career framing.
- [ ] No API keys, tokens, or `.secrets.json` / `.env` staged (`git status` before committing).
- [ ] The $20,000 stays framed as an abstract experiment budget; picks stay framed as a methodology
      demo; the not-financial-advice disclaimer stays in place.
