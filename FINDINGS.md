# Findings

> **Status: open.** The experiment began 2026-07-18 and wraps **2026-11-28** (extended 2026-08-01 from
> the original 2026-08-26 — see the pre-commitment below). This file is updated at each check-in and
> finalised at the wrap. **Null results are reported, not buried.**

## Pre-commitment on the extension (written 2026-08-01, before any further result)

The run was extended from 2026-08-26 to **2026-11-28**. **Extending an experiment after seeing early
results is a questionable research practice** — it is optional stopping run backwards, and it is exactly
how a null result gets quietly converted into a positive one. So the reasoning is fixed here, in advance:

1. **The trigger was a power calculation, not a result.** At n≈28 no band could reach the ~21 needed to
   detect even *gross* miscalibration. The extension targets a stated sample size, computed before the
   extra data exists, and would have been made identically had the early results been flattering.
2. **The extension cannot help the numbers look better.** The directional Brier currently sits at 0.2858
   — *worse* than the 0.25 baseline — and the pre-committed expectation is that it converges *to* 0.25.
   More sample makes the unflattering result firmer, not softer.
3. **Every pre-committed expectation stands unchanged** — see "The pre-committed expectation" above. None
   was revised when the run was extended.
4. **No further extension will be made on the basis of what the numbers say.** 2026-11-28 is the end. If
   the sample is still too thin then, the wrap reports "n too small to conclude", which remains a valid
   pre-committed outcome.
5. **The wrap reports whatever it finds on that date**, including a directional Brier at or above 0.25,
   including an over-confident factual track, including nulls on all three precursor rules.

Also fixed now, so it cannot be tuned later: from 2026-08-01 each check-in targets **8–10 factual
predictions**, biased toward genuinely uncertain claims rather than published-calendar reads.

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

**Six predictions have resolved.** As at check-in 3 (2026-07-31) the ledger holds **34 predictions** —
6 resolved, 28 live. The first cluster came due 29–30 July and graded cleanly.

| Track | n | Brier | vs 0.25 baseline | Verdict |
| ----- | - | ----- | ---------------- | ------- |
| Directional | 2 | 0.2858 | **does NOT beat it** | no directional skill — **as pre-committed** |
| Factual | 4 | 0.0404 | n/a | 100% accurate, but see the caveat below |

Run `python score.py` for the live numbers.

### The directional track is behaving exactly as predicted

The first two directional resolutions produced a Brier of **0.2858 — worse than the 0.25 coin-flip
baseline**, and worse than the base-rate baseline too. This is the outcome written down on 2026-07-18
before anything resolved. It is reported here as a headline rather than buried, because a result that
confirms an unflattering pre-commitment is the one most likely to be quietly de-emphasised.

`nst-underperform` (P 0.60) is the instructive failure: it was wrong on **mechanism as well as
direction**. The thesis was "gold momentum reversing into the quarterly." What actually happened is that
NST had cut FY26 guidance twice and fallen ~40% in three months on KCGM execution problems, then beat an
already-lowered bar on 29 Jul. The stock moved on its own operational story, not on gold. A confident
narrative about a sector was applied to a stock whose price was being driven by something else entirely.

### 🚫 Date-of-disclosure claims were not predictions at all — retired 2026-08-01

The sharper version of the "too easy" problem below, and it needed a stronger remedy than shading
probabilities. **"Company X releases its results on date Y" is not a forecast — it is a compliance
event.** ASX Listing Rule 4.3A obliges a 30-June-balance-date company to lodge within two months, the
company publishes the date itself, and the base rate is >97%. The claim tests whether the system can
read a calendar.

**It was also actively corrupting the measurement, not merely diluting it.** Stack near-certainties into
the 0.9 band and it reads ~100% actual against ~0.93 predicted — an apparent "under-confident at the
top" finding manufactured entirely by question selection. That is a false result. **69% of the factual
track (9 of 13 entries) was this**, with four more at P ≥ 0.80 queued to land in the upper bands.

**Remedy.** All nine are tagged `"scoring": "compliance"`, still graded and reported, but **excluded from
the factual Brier and the calibration table** — the same treatment the eight grandfathered watch-calls
received. `CHECKIN.md` now forbids registering more.

**The honesty test this had to pass:** both already-resolved compliance entries resolved TRUE at P 0.95
and P 0.93. Removing them makes the record **worse**, not better — the factual Brier went **0.0404 →
0.0772** and the 0.9–1.0 band collapsed from n=3 to n=1. A reclassification that costs the score is not
motivated reasoning. The rule was applied uniformly to every date-of-disclosure claim without reference
to outcome.

### ✅ What replaced them: measured results-day reaction claims

The valuable question is not *when* a report lands but **what it does to the price** — which no source
states in advance. Eight `event-move` entries were registered 2026-08-01 against the confirmed August
reporting dates, asking whether each stock moves more than a threshold on its results day, graded
mechanically from price with no source check and no self-grading.

**Every probability is anchored to a computed figure.** Over 5 years of daily closes, two things were
measured per name: the unconditional frequency of exceeding the threshold, and a proxy for results-day
moves (the largest single-day move in each of 10 Feb/Aug reporting windows). The proxy is an **upper
bound** — the window max is usually but not always the result itself — so every registered probability
is shaded *down* from it.

A first attempt measured only a **×1.39** "in-season" elevation and was discarded as misleading: a 21-day
window contains ~1 results day, so the effect is diluted roughly 20:1. Measuring the event directly gives
a far larger elevation — e.g. WOW moves >2% on just **4.6%** of ordinary days but on **80%** of proxy
results days.

The batch spans P 0.58–0.85 and lands **1 / 3 / 2 / 2** across the 0.5–0.6, 0.6–0.7, 0.7–0.8 and 0.8–0.9
bands — filling the two that were empty, with genuinely uncertain claims rather than calendar reads.
**Deliberately nothing above 0.9**: the data does not support a near-certain move at any threshold worth
asking about, and inventing one would repeat the exact mistake being corrected.

### ⚠️ The factual track is currently too easy — the Brier flatters it

The factual Brier of 0.0404 at 100% accuracy should **not** be read as evidence of forecasting skill.
Three of the four resolved factual entries are of the form *"will company X report on the date its own
investor calendar already publishes?"*, verified from a primary source **at the time of logging**. Dates
do sometimes move, so these are real forecasts — but weak ones, and they are close to free.

If the upper calibration band is built entirely from published-calendar reads, the wrap will be able to
conclude only that the system can read a calendar. The `fomc-holds-29jul` entry (P 0.62) is the one
resolved factual call with genuine two-sided uncertainty, and the 9–3 vote with three dissenters
preferring a *hike* confirms the uncertainty was real rather than theatrical.

**Corrective adopted at check-in 3:** new factual entries are weighted toward claims with real
uncertainty and placed to fill the empty 0.7–0.8 and 0.8–0.9 bands, rather than padding the 0.9 band.
`tavneos-ec-pending-26aug` (P 0.62) is the model of what is wanted — no source states the answer in
advance. This must be read at the wrap: the factual Brier is a **mixture** of a hard sub-track and an
easy one, and the mixture proportion moved during the experiment.

### An under-confident entry, left standing

`rba-holds-11aug` was pre-registered at **P 0.70 on 18 July**. The 29 July Q2 CPI print (headline 3.8%,
trimmed mean 3.6%) then dropped market-implied odds of an August hike to ~4%, and Westpac withdrew its
last-standing hike call. On today's information the honest number would be ~0.95. **The pre-registered
0.70 stands uncorrected** — the ledger is append-only. If it resolves TRUE it should be read at the wrap
as a visibly *under*-confident call, which is as much a calibration failure as over-confidence and is
rarer to catch in the wild.

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

## Measured: how much independent information the ledger actually holds

*Added 2026-08-01.*

**Finding: the directional ledger carries close to its full nominal sample.** 13 of 16 directional
entries resolve on a single day (2026-08-26), and 12 share an identical start date, end date and
benchmark — a structure that looks alarmingly redundant. It measures as almost entirely independent, and
the reason is structural rather than lucky: a *relative* claim carries the benchmark on both sides, so
the common market factor cancels out of the quantity actually being predicted.

*(This was measured because the shared-window structure prompted a concern that effective n might be as
low as ~2. The data did not support that. The concern is recorded because the check changed the scorer —
see below — not because the worry was correct.)*

**The measurement.** 508 sessions of daily ASX data to 2026-07-31, 15 names, 105 pairs:

| Correlation of… | ρ̄ |
| --- | --- |
| Raw daily returns | **+0.084** ← the market factor |
| Daily **excess** returns vs VAS | **+0.002** |
| The **actual outcome** (39-day beat / not-beat) | **−0.020** |

**The suspicion was wrong, and wrong in the direction that flattered it.** The market factor is real, but
a relative claim — "X beats VAS" — carries the benchmark on *both* sides, so the common factor cancels
and what remains is idiosyncratic. Twelve relative calls on different names over one shared window are
worth very nearly twelve independent bets, not two.

**What IS correlated, and was being missed entirely.** The old estimator discounted by *sector tag* at
ρ=0.7 — a guess, and one the data says is far too aggressive for relative calls. Meanwhile it gave a
**zero** discount to the genuinely near-duplicate pairs, because they happened to carry different tags:

| Pair | Old ρ | Measured/modelled ρ |
| --- | --- | --- |
| Two VAS index calls, identical window | 0.7 (same `market-beta` tag) | **0.85** |
| The two live CSL price calls | **0.0** — different tags | **0.68** |
| The two live DRO price calls | 0.7 | **0.74** |
| CBA vs WDS — different names, different sectors | 0.0 | **0.00** ✓ |
| An NST price call vs an NST reporting-date fact | 0.0 | **0.40** |

So the estimator was simultaneously too harsh on the thing that was fine and blind to the thing that
wasn't. Replaced (see change log) with a model keyed on **same ticker × window overlap**, differentiated
by track. Net effect on the live ledger: raw 34 → effective **21.1**.

### How much sample would actually be needed — and does a longer run help?

Power, computed rather than asserted:

| To detect | Needed **in that band** |
| --- | --- |
| Gross miscalibration (claims 0.90, truly 0.70) | ≈ **21** |
| Moderate (0.90 vs 0.80) | ≈ **62** |
| Subtle (0.60 vs 0.50) | ≈ **97** |

And on the directional Brier, the 95% CI around 0.25 is **[0.10, 0.40] at n=16** — worthless — narrowing
to [0.196, 0.304] at n=120 and only [0.224, 0.276] at n=500. **The directional track can therefore never
demonstrate an edge at any realistic sample size. It can only ever rule out a large one** — which it has
already provisionally done, and which was the pre-committed expectation anyway.

**Does extending the run help? Yes — materially, and more than first thought**, precisely because the
correlation measurement shows sample accumulates almost independently. Each additional relative call is
worth close to a full observation, not a fraction of one. At ~9 new predictions per weekly check-in from
a base of 28:

| Wrap moved to | Approx. raw n |
| --- | --- |
| 2026-08-26 (current) | 28 |
| late Sep | ~64 |
| **late Oct** | **~100** |
| late Nov | ~145 |

**The binding constraint is not total n — it is per-band n, and specifically the FACTUAL predictions.**
Directional stock calls can only honestly sit at 0.50–0.60, so they all pile into the bottom band; the
0.7/0.8/0.9 bands can only ever be filled by factual entries, which arrive at ~5 per check-in spread over
several bands. Reaching ≈21 in each of the three upper bands takes roughly **13 more weeks**.

**Conclusion: ~late October buys a readable aggregate; ~late November buys a readable calibration curve
at the gross-miscalibration level. Nothing buys the subtle level.** Extending past November is not worth
the effort it costs.

## Precursor / event-study track

Seeded, grading continues past the wrap by design (most precursor rules resolve in September).

- **Check-in 2 (2026-07-26):** all three rules screened; 51 quant candidates → **1 confirmed** on the
  news condition (`csl-insider-buy-after-warning`, registered, resolves 24 Sep). `governance-overhang`
  and `preupgraded-guidance-into-result` produced **0 confirmed matches** — a real, reported outcome,
  not a failed run. The ~2% confirmation rate is the intended effect of a demanding, pre-committed news
  condition. With a single confirmed name there is no cohort and no control group this run. ~~**51
  name×rule comparisons** this run~~ — **see the correction below; this figure was wrong.**

- **Check-in 3 (2026-07-31):** 83 names screened (SVW skipped, delisted); 50 shortlisted after the
  research budget → **4 confirmed**, the largest cohort yet.
  - **`governance-overhang` → 2 confirmed (DRO, WTC)** — the first matches this rule has ever produced.
    Both legs primary-checked: DRO's ASIC investigation of 12 May still open, against a defence /
    counter-drone sector rally; WTC's AFP investigation plus ASIC probe into ~A$229m of chair share
    trading, against an ASX IT sector rally. 13 of 15 failed leg A outright.
  - **`preupgraded-guidance` → 2 confirmed (CPU, MIN)** — both with two dated *company-issued* guidance
    upgrades. **Direction flipped from the stub default**, as for CSL at check-in 2: the rule
    hypothesises these names *beat* VAS, but `screen.py` emits every stub as "underperforms", so
    registering as emitted would test the rule backwards.
  - **`insider-buy-after-warning` → 0 confirmed** for the second run running.
  - Strictness is the point, and it bit in both directions: Harvey Norman was rejected because its ASIC
    matter was **resolved** by judgment on 28 Jul (fails "unresolved"); ARB was rejected because its
    genuine on-market director purchase followed a January warning, outside the 45-day window.
    "Reaffirmed", "narrowed", "guided to the top end" and results merely *beating* prior guidance were
    all rejected as non-upgrades.

- **⚠️ CORRECTION to the multiple-comparisons record (made 2026-07-31).** Check-in 2 logged **51**
  name×rule comparisons. That was wrong: 51 was the count of quant **matches** (15+15+21), not tests
  **performed**. `screen.py` accumulates `tests += len(rows)` for every rule, giving 82 names × 3 rules
  = **246** tests, and the file has not changed since 2026-07-19 — before check-in 2 ran. So that run's
  true multiple-comparisons exposure was also ~246, and the logged figure **understated it by roughly
  5×**. Check-in 3's count is **246**. Recorded prominently because the error ran in the direction that
  flattered the method, and the whole purpose of this footer is to keep that risk visible.

## Calibration table

As at check-in 3 (2026-07-31). Effective n ≈ 6.0 — far below the ~20 needed to say anything firm.

| Prob band | Mean predicted | Actual frequency | n |
|-----------|----------------|------------------|---|
| 0.5–0.6 | 0.54 | 1.00 | 1 |
| 0.6–0.7 | 0.61 | 0.50 | 2 |
| 0.7–0.8 | — | — | 0 |
| 0.8–0.9 | — | — | 0 |
| 0.9–1.0 | 0.93 | 1.00 | 3 |

Every cell is n ≤ 3. **No cell here supports any inference.** The 0.7–0.8 and 0.8–0.9 bands were still
empty at this check-in and were deliberately targeted by the predictions registered on 2026-07-31.

**Known reporting constraint:** the bands start at 0.5, so a prediction carrying P < 0.5 would count in
the Brier score but appear in **no** band — vanishing from this table without trace. The house convention
is therefore to phrase every claim so its probability is ≥ 0.5 (state the complement instead). A guard
added at check-in 3 makes any breach print a loud warning rather than fail silently. No entry has
breached it to date.

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
| 2026-07-19 | **Index-level predictions added** (`basis: "absolute"`). Three VAS entries: positive return to the wrap (P 0.58), positive to 30 Jul (P 0.54), and no worse than −5% to the wrap (P 0.88). All tagged `cluster: market-beta`. | Every directional entry until now was framed *relative* to VAS, so the ledger held no calibration data on the market's own direction — the index was only ever the yardstick, never the subject. Required a schema change: `score.py` computed `beat = ret > bm_ret`, so an entry whose subject **is** the benchmark would compare VAS to itself and resolve FALSE by construction, silently mis-grading every such call. Absolute-basis entries now grade against a pre-registered `threshold_pct` and carry a null `bm_ref`. Probabilities are anchored to self-computed base rates (ASX200, 2001–2026, n≈6,430: 61.1% of ~27-day and 56.9% of ~8-day price returns positive; 90.0% better than −5%), shaded down only slightly for in-window event risk (29 Jul CPI, 11 Aug RBA in a live tightening cycle). **The small deviation from base rate is deliberate** — a large one would be the overconfidence this experiment exists to detect. The −5% entry is placed specifically to populate the upper calibration band, which directional stock calls can never reach. |
| 2026-07-19 | **Correction to the base rates cited above — the sample sizes were overstated.** The n≈6,430 figures come from *overlapping* rolling windows and are not independent observations; the true independent count is ~239 at the 27-day horizon and ~806 at 8 days. Recomputed on **non-overlapping** windows: 27-day positive **64.9%** (SE 3.1pp, 95% CI 59–71%), 8-day positive **55.3%** (SE 1.8pp), better-than-−5% **90.0%** (SE 1.9pp) — the last identical to the overlapping estimate. | Point estimates held up (the −5% figure to three decimals), so the anchors are sound, but the *precision* was illusory. This matters for interpretation: the 27-day base rate is only known to about ±6pp, so the 2–3pp shading applied for macro headwinds is **well inside the noise band and is not a measurable adjustment**. It also means `vas-positive-to-wrap` (P 0.58) sits ~7pp below the better central estimate of 64.9%, not the ~3pp intended. **The pre-registered `prob` and `rationale` stand uncorrected — they are append-only.** This note is the correction, and the entry should be read at wrap as a call that was more bearish than its own stated reasoning justified. |
| 2026-07-19 | Verified the `--resolve` write path on absolute-basis entries before any is due (forced past-due on a scratch copy). Outcomes wrote back correctly against `threshold_pct`. | The write path had never been exercised for the new basis. Discovering it broken on 30 July, when the first entry is actually due, would have meant debugging a grader while an outcome was already known — the worst possible time. Noted: the rule is a strict `>`, so an exactly-flat return resolves FALSE. |
| 2026-07-19 | Verified no VAS ex-distribution date falls inside the prediction window. | VAS distributes quarterly (1 Jan/Apr/Jul/Oct). An ex-date inside a window mechanically drops the price and would bias *both* the new absolute entries and — by dragging the benchmark leg — every existing "beats VAS" call. 1 Jul has passed and the next is 1 Oct, so the window is clean. **Any future window spanning 1 October breaks this assumption and must adjust for it.** |
| 2026-07-26 | **Check-in 2: pre-registered 5 factual predictions** (FOMC 29-Jul hold 0.62; BHP report-date 0.68; IAG/RIO/NST report-dates 0.90–0.95) and **1 precursor match** (`csl-insider-buy-after-warning`, 0.55, out of 51 quant candidates across 3 rules). No rule or scorer change. | Routine check-in: fill the thin upper calibration band with primary-sourced reporting-date facts, and seed the precursor track with the one name that passed its pre-committed news condition. Direction on the insider-buy precursor was flipped from the stub default to *outperform* to match the rule's hypothesis. |
| 2026-07-18 | **REVERTED the above. Rule restored to its original pre-committed form; a separate `screen_budget` added instead.** | The tightening was defensible (no cohort registered, no outcomes existed) but defensible is not the standard — the rule stays pre-committed. The actual mistake was conflating two different things: **the rule**, which must never be tuned, and **how many names can be researched per run**, which is pure logistics. Separating them fixes it with no compromise. `screen_budget` caps the sweep at the 15 most beaten-down matches, ranked by a pre-move characteristic applied blind to outcomes, and **reports every dropped name** rather than discarding it silently. The control-group property survives because the cohort is still chosen by a stated rule applied before any outcome is known. |
| 2026-07-31 | **`score.py` crash fix — read-only runs died as soon as anything resolved.** The provenance table and precursor slice read `int(e["outcome"])` back off the ledger dict, but a directional entry that has just come due is graded *in memory* and only has `outcome` written under `--resolve`. Fixed by threading `(entry, outcome)` pairs through to the reporting layer. | Pure defect, no grading change. Worth logging because of *when* it surfaced: the command documented as "safe to run any time" was broken from the moment the first prediction came due — i.e. it had never actually been exercised on the path that matters. A gate that has never run is not a gate. |
| 2026-07-31 | **Grading now uses the close ON `resolve_date`, not the price on the day the check-in is run.** Added `prices.get_close_on()` (last session on or before `resolve_date`); `--resolve` additionally writes a `graded_on` block recording the session used, the subject return and the bar. | **This was a silent rule violation, not a rounding error.** `prices.py` had no historical lookup at all, so a check-in run late measured a longer window than the rule pre-registered. NST's rule specifies `[2026-07-18, 2026-07-29]`; grading it on 31 Jul prices measured 13 days, not 11. **Verified outcome-neutral before adoption** — both entries due today grade identically old and new (NST 0, VAS 1), so this cannot be a grader retro-fitted to flatter the score, and that verification is *why* it was done today rather than later. The exposure is concentrated: **14 of 15 live directional entries resolve on 2026-08-26, which is the wrap date itself** — running the wrap one day late would have mis-windowed every one of them. |
| 2026-07-31 | **Guard added for probabilities below 0.5.** The calibration bands start at 0.5, so a P < 0.5 entry would count in the Brier score but appear in no band. `score.py` now prints a loud warning naming any such entry. Convention restated: phrase claims so P ≥ 0.5, stating the complement where needed. | Found while drafting a genuinely-uncertain entry that naturally wanted P ≈ 0.4. Nothing had breached it yet, so this is a fix made *before* the failure rather than after — the cheap case. Also drove the wording of `tavneos-ec-pending-26aug`, phrased as a positive read of a published status field rather than an argument from absence, which is the flaw already logged against the `dro-asic-live` rule. |
| 2026-07-31 | **Precursor cluster tagged by correlation, not by rule, for one entry.** `dro-governance-overhang…` is tagged `cluster: "defence"` rather than `"governance"`. | It is nearly the same bet as the live `dro-underperform` call — same stock, same direction, overlapping window — and that same-stock correlation is far stronger than its link to the other cohort member (WTC) through the rule. Tagging `defence` makes `score.py` discount it against the existing DRO entries, **lowering** effective n. The conservative choice, taken at the cost of the tag-by-rule convention, and recorded here because it is a deviation. **Related observation, uncorrectable:** the six existing reporting-date factual entries are all tagged `cluster: "independent"`, which counts them at full weight. They are independent *events*, but the *errors* are highly correlated — same question type, same evidence source, same failure mode if published calendars turn out unreliable. Those tags are pre-registered and stand; new reporting-date entries share `cluster: "reporting-dates"` instead. Effective n on the factual track is therefore **overstated** for the earlier entries. |
| 2026-08-01 | **`effective_n` rewritten: correlation is now MEASURED, and keyed on ticker × window overlap rather than on sector tag.** Old model: same-cluster ⇒ ρ=0.7, everything else ⇒ 0. New model: `n_eff = n²/Σρᵢⱼ`, with same-ticker ⇒ 0.85 and same-cluster ⇒ 0.40, both scaled by the fraction of the shorter measurement window the pair shares; differentiated by track (factual pairs correlate by method, not ticker; cross-track same-subject pairs get the cluster rho as an unmeasured conservative middle). | The old ρ=0.7 was an admitted guess and the data contradicts it: measured correlation of the *outcome being predicted* across names is **−0.020**, because the benchmark leg cancels the market factor in a relative claim. So the old model over-penalised the cross-sectional book while giving a **zero** discount to genuinely near-duplicate pairs that happened to carry different tags — the two live CSL price calls were being counted as fully independent. Net effect on the live ledger: raw 34 → effective 21.1. **Prompted by a concern that the shared-window structure had collapsed effective n to ~2; the measurement did not support that, and the estimator was rewritten anyway because the check exposed the same-ticker blind spot.** ⚠️ Note this is a scoring-method change made mid-experiment; it alters no `prob`, no `outcome` and no pre-registered field, only the *reported* effective n. |
| 2026-08-01 | **Date-of-disclosure claims retired from calibration.** The 9 "company X reports on date Y" entries are tagged `"scoring": "compliance"`, still graded but excluded from the factual Brier and the calibration table; `CHECKIN.md` forbids new ones. Replaced by `basis: "event-move"` entries — results-day price-reaction claims graded mechanically against a `ref_date` close. | **These were never predictions.** ASX LR 4.3A obliges lodgement within two months of a 30-June balance date and the company publishes the date itself, so the base rate is >97%; the claim tested calendar-reading. Worse, stacked into the 0.9 band they would have manufactured a false "under-confident at the top" result out of question selection alone — 69% of the factual track was this. **The reclassification is self-penalising and that is the check that it is honest:** both resolved compliance entries were TRUE at P 0.95/0.93, so removing them moved the factual Brier from 0.0404 to **0.0772** and cut the 0.9 band from n=3 to n=1. Rule applied uniformly, without reference to outcome. *(Raised by Matt, who pointed out that a company meeting a legally-mandated deadline it announced itself is "things going as expected", not a forecast — and that the valuable question is what is IN the report and whether it moves the price.)* |
| 2026-08-01 | **New schema: `basis: "event-move"` with `ref_date`.** The reference price is the close on a pre-registered future date rather than one stamped at logging; outcome is `abs(return) > threshold_pct` from that close to the `resolve_date` close. `_window()` uses `[ref_date, resolve_date]` for these. | Measuring a *reaction* requires a reference from the session before the event, which only became possible once `get_close_on()` existed. Still tamper-proof: the date is fixed in advance and the close is a public mechanical number, so nothing is selected after the fact. The `_window` change matters for correlation — using `logged` would have made eight different companies' results days look like one overlapping blob and collapsed them to ~1 effective observation; with ref_date windows, same-day pairs correlate at 0.40 and different-day pairs at 0.00, giving effective n 6.67 from 8 raw. Verified on a scratch ledger against known closes: NST moved +2.222% from 28→29 Jul, grading TRUE against a 2% threshold and FALSE against 3%, with a future-dated entry correctly left ungraded. |
| 2026-08-01 | **The small-sample caveat is now unconditional, and per-band n is reported alongside it.** | It previously printed only while effective n was below 20 — meaning the warning that protects every reading of these numbers would **switch itself off exactly as the sample grew**, and the live ledger is now at 21.1. Crossing ~20 does not make a calibration curve readable; it only stops it being hopeless. The per-band thresholds (≈21 gross / ≈62 moderate / ≈97 subtle) are now printed every run so a band with n=3 cannot be mistaken for evidence. |
| 2026-07-31 | **Provenance model changed:** entries logged from this check-in carry `claude-opus-5[1m]`; check-ins 1–2 carry `claude-opus-4-8[1m]`. | Recorded because the provenance table now spans two models mid-experiment. This changes nothing about the standing pre-commitment: **no model-comparison claim will be made at the wrap.** Per-cell n is in the low single digits, the split is confounded with time and with question type, and a flattering cut will always be available. The field exists for description only. |
