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

**One prediction has resolved.** The first directional one is `2026-07-18-nst-underperform` at the
Northern Star quarterly on 29 July 2026.

| Track | n | Brier | vs 0.25 baseline | Verdict |
| ----- | - | ----- | ---------------- | ------- |
| Directional | 0 | — | — | pending (12 live) |
| Factual | 1 | 0.0100 | n/a | **n=1 — no verdict possible** |

Run `python score.py` for the live numbers.

### Resolved: `dro-asic-live` (P 0.90 → TRUE)

Claim: *an ASIC investigation into DroneShield is on foot and unresolved as at 2026-07-18.*
Resolved against the primary ASX announcement "Notice of ASIC Investigation" (12 May 2026), fetched
and read directly — [source](https://announcements.asx.com.au/asxpdf/20260512/pdf/06zhn945gfstrq.pdf).

**Three honesty notes, because a first result that flatters the system is exactly where scrutiny
should be highest:**

1. **The "unresolved" half rests on absence of disclosure, not an affirmative statement.** The complete
   official ASX index for DRO through 10 July 2026 shows no closure announcement. For a listed company
   a closure would very likely trigger continuous disclosure, so the silence is meaningful — but it is
   an inference. No ASIC-side source exists; ASIC does not comment on live investigations.
2. **The pre-registered rationale contains a factual error, left uncorrected.** It gives the disclosure
   date as 11 May 2026; the primary source says 12 May. Pre-registered fields are append-only, so the
   error stands on the record. It doesn't affect the claim, which concerned existence and status.
3. **n=1 means nothing.** A single 0.90 resolving TRUE is exactly what a *badly* calibrated system
   would also produce. This is one data point in the top band, not evidence of anything.

**Method lesson:** this entry's resolution rule asked a source to "confirm … has not concluded," which
is close to unsatisfiable affirmatively. Future factual rules should specify an achievable evidentiary
standard — e.g. "no closure announcement on the official record as at DATE."

## Calibration table

| Prob band | Mean predicted | Actual frequency | n |
|-----------|----------------|------------------|---|
| 0.5–0.6 | — | — | 0 |
| 0.6–0.7 | — | — | 0 |
| 0.7–0.8 | — | — | 0 |
| 0.8–0.9 | — | — | 0 |
| 0.9–1.0 | 0.90 | 1.00 | 1 |

## Provenance

**Descriptive only.** Per-cell n will be in the low single digits. **No model-comparison claim will be
made at this wrap**, whatever the numbers look like — see the README section on provenance.

## Log of method changes

| Date | Change | Why |
| ---- | ------ | --- |
| 2026-07-18 | Exercise reframed from "beat the market" to a calibration experiment; probability ledger opened; money P&L demoted to a secondary engagement metric. | The original question was near-unanswerable at this n; calibration is measurable and transfers. |
| 2026-07-18 | 8 pre-existing binary up/down calls grandfathered — kept, relabelled, excluded from the ledger. | Retro-assigning probabilities after a week of price action would contaminate calibration. |
| 2026-07-18 | EODHD enabled as an automated second price source after its free tier was confirmed to return real ASX closes. | Reconcile catches feed breakage. It agrees with yfinance to the cent, which is expected for canonical closes and is *not* evidence of independence. |
| 2026-07-18 | ~~Precursor `governance-overhang-suppresses-good-news` quant leg tightened~~ (`ret6m < 0, rng_pos < 40` → `ret6m < -15, rng_pos < 25`). | Attempted because the original matched 37/82 names, making the follow-up "targeted news sweep" untargeted. **Made after seeing the match list — which this project forbids.** |
| 2026-07-18 | **REVERTED the above. Rule restored to its original pre-committed form; a separate `screen_budget` added instead.** | The tightening was defensible (no cohort registered, no outcomes existed) but defensible is not the standard — the rule stays pre-committed. The actual mistake was conflating two different things: **the rule**, which must never be tuned, and **how many names can be researched per run**, which is pure logistics. Separating them fixes it with no compromise. `screen_budget` caps the sweep at the 15 most beaten-down matches, ranked by a pre-move characteristic applied blind to outcomes, and **reports every dropped name** rather than discarding it silently. The control-group property survives because the cohort is still chosen by a stated rule applied before any outcome is known. |
