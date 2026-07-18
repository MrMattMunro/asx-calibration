# Findings

> **Status: open.** The experiment began 2026-07-18 and wraps ~2026-08-26. This file is updated at
> each check-in and finalised at the wrap. **Null results are reported, not buried.**

## The pre-committed expectation

Written down on 2026-07-18, before any prediction resolved, so it cannot be rationalised afterwards:

- **Directional track:** Brier ≈ 0.25 — that is, *no skill*. Public news is priced in. If the
  directional Brier beats 0.25 at this sample size, the honest reading is **luck**, not edge, until a
  much larger sample says otherwise.
- **Factual track:** low Brier — the model should be reliable on checkable facts. The thing to watch is
  **over-confidence**: a 0.90 that should have been a 0.75.
- **Sample size is the binding limitation.** ~10 seeds plus a handful per check-in gives roughly 20–40
  predictions by the wrap. That is enough to *illustrate* calibration, not to *prove* skill.
  **"n too small to conclude" is a valid, pre-committed outcome.**

## Results

*(Nothing has resolved yet. The first directional prediction to resolve is `2026-07-29-nst-underperform`
at the Northern Star quarterly on 29 July 2026.)*

| Track | n | Brier | vs 0.25 baseline | Verdict |
| ----- | - | ----- | ---------------- | ------- |
| Directional | — | — | — | pending |
| Factual | — | — | — | pending |

Run `python score.py` for the live numbers.

## Calibration table

*(pending — needs resolved predictions)*

## Provenance

**Descriptive only.** Per-cell n will be in the low single digits. **No model-comparison claim will be
made at this wrap**, whatever the numbers look like — see the README section on provenance.

## Log of method changes

| Date | Change | Why |
| ---- | ------ | --- |
| 2026-07-18 | Exercise reframed from "beat the market" to a calibration experiment; probability ledger opened; money P&L demoted to a secondary engagement metric. | The original question was near-unanswerable at this n; calibration is measurable and transfers. |
| 2026-07-18 | 8 pre-existing binary up/down calls grandfathered — kept, relabelled, excluded from the ledger. | Retro-assigning probabilities after a week of price action would contaminate calibration. |
| 2026-07-18 | EODHD enabled as an automated second price source after its free tier was confirmed to return real ASX closes. | Reconcile catches feed breakage. It agrees with yfinance to the cent, which is expected for canonical closes and is *not* evidence of independence. |
| 2026-07-18 | **Precursor `governance-overhang-suppresses-good-news` quant leg tightened** (`ret6m < 0, rng_pos < 40` → `ret6m < -15, rng_pos < 25`), cutting matches from 37/82 to 16/82. | The original shortlist was so wide the follow-up "targeted news sweep" wasn't targeted. **Flagged for skepticism:** the rule was changed *after* seeing its match list, which this project otherwise forbids. Defensible only because no cohort had been registered and no outcome existed — nothing to fit to. Residual bias cannot be fully excluded and is recorded in `precursors.json`. |
