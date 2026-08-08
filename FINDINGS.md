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

**Eight predictions have resolved.** As at check-in 4 (2026-08-09) the ledger holds **77 predictions** —
8 resolved, 69 live. Primary ledger only; the 13-entry Claude arm is scored separately and never enters
these numbers.

| Track | n | Brier | vs 0.25 baseline | Verdict |
| ----- | - | ----- | ---------------- | ------- |
| Directional | 3 | 0.1980 | **beats it** | **read as LUCK at n=3** — see below |
| Factual | 2 | 0.0772 | n/a | 100% accurate, but see the caveat below |
| Compliance *(excluded from calibration)* | 3 | 0.0037 | n/a | expected; means nothing |

Run `python score.py` for the live numbers.

⚠️ **The directional track flipped from 0.2858 to 0.1980 on a single resolution** (`rmd-results-move-0807`,
P 0.85, TRUE). It now beats the coin-flip baseline. **The standing pre-commitment applies without
amendment: at n=3 this is luck, not edge.** The flip is itself the argument — if one observation can move
the headline number across the baseline in either direction, the headline number is not yet measuring
anything. Recorded prominently because a pre-commitment is only worth writing down if it is honoured when
the numbers turn *favourable*, which is the harder direction.

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

### 🔴 PRE-REGISTERED: the results-reaction batch is expected to be OVER-CONFIDENT

*Written 2026-08-02, before any of the eight entries resolve — the first is due 2026-08-07.*

**The anchor used to price that batch was circular.** Results days were identified as *the largest-move
day* in each reporting window, and then the size of that move was measured. That selects on the outcome
variable and is biased upward by construction.

Re-measured using **volume** to identify the results day — a proxy that is independent of move size,
since results days spike turnover — the max-move anchor overstates the typical results-day move by
**+1.61pp on average** (up to +3.4pp for CSL).

Consequence, stated in advance and per entry:

| | threshold | registered P | volume-identified P | gap |
| --- | --- | --- | --- | --- |
| RMD | 2% | 0.85 | 25% | **+0.60** |
| CSL | 3% | 0.72 | 25% | **+0.47** |
| CBA | 2% | 0.68 | 25% | **+0.43** |
| TCL | 2% | 0.58 | 31% | **+0.27** |
| SUN | 2% | 0.78 | 56% | **+0.22** |
| FMG | 3% | 0.85 | 69% | **+0.16** |
| WOW | 2% | 0.66 | 62% | +0.04 |
| TLS | 2% | 0.65 | 75% | −0.10 |

**6 of 8 are over-confident by more than 0.10; the mean gap is +0.26. If the volume proxy is right this
batch should resolve TRUE about 46% of the time, against the ~72% its probabilities imply.**

**The probabilities stand uncorrected** — the ledger is append-only, and this is exactly the situation
that rule exists for. Recording the expectation instead makes the batch a *sharper* test rather than a
spoiled one: it is now a pre-registered prediction about the system's own miscalibration, and it can fail
in both directions. If the batch resolves near 46%, the self-diagnosis was right and the mechanism
(selection on the outcome variable) is confirmed. If it resolves near 72%, the volume proxy was the
flawed one and the original anchor was sound.

**Caveat, so this is not over-read:** the max-volume day can also be an index rebalance or an ex-dividend
date rather than the result. It is a proxy too. Its one decisive advantage is being *independent of move
size*, which the max-move anchor is not.

**Method fixed for future batches** — see the change log. This is the single most useful thing found so
far, because it is the experiment's own stated purpose (detecting over-confidence) turned on the
experiment's own output, and it caught a real error.

#### 🔴 FOLLOW-UP 2026-08-09 — the table above does not fully reproduce

*Written at check-in 4, with one of the eight resolved.*

The volume-anchor computation was re-run, this time through a committed script (`anchor.py`) rather than
by hand. **Six of the eight figures reproduce within ~6pp. Two do not, and they miss in opposite
directions:**

| | thr | registered P | table above | recomputed | delta |
| --- | --- | --- | --- | --- | --- |
| RMD | 2% | 0.85 | 25% | **60%** | **+35pp** |
| TCL | 2% | 0.58 | 31% | **10%** | **−21pp** |
| CSL | 3% | 0.72 | 25% | 30% | +5pp |
| CBA | 2% | 0.68 | 25% | 30% | +5pp |
| SUN | 2% | 0.78 | 56% | 50% | −6pp |
| FMG | 3% | 0.85 | 69% | 70% | +1pp |
| WOW | 2% | 0.66 | 62% | 60% | −2pp |
| TLS | 2% | 0.65 | 75% | 70% | −5pp |

Recomputation used the same stated method — event day = max-volume session in each Feb/Aug window, n=10
complete windows over 5 years — matching the original's stated n. Three of the original figures being
*exactly* 25% is what prompted the check. RMD was additionally tested on the NYSE line in case the
original had used the wrong listing: that gives 40%, and the ASX line gives 60%. **Neither is 25%, and
the figure is not recoverable from any reading of the method that could be reconstructed.**

**What survives and what does not:**

- ✅ **The batch-level pre-registration survives essentially intact.** Recomputed mean across the eight is
  **47.5%** against a registered mean of 72.1%; the figure recorded above was 46% vs ~72%. The two errors
  very nearly cancel. The falsifiable claim — *this batch should resolve TRUE far below the ~72% its
  probabilities imply* — is unchanged, and remains the thing to judge at the wrap.
- ❌ **The per-entry table does not survive**, and neither does the ranking built on it. RMD was named the
  worst offender at +0.60; on the recomputed anchor it is +0.25, mid-pack. Any wrap-time reading that
  leans on *which* entries were most over-confident is reading a number that cannot be reproduced.
- ⚠️ **RMD has since resolved TRUE** (−8.29% against a ±2% bar). That is one observation and settles
  nothing, but it sits comfortably with a 60% anchor and awkwardly with a 25% one.

**Nothing above was edited.** The append-only rule exists for precisely this case: a pre-registered
expectation that later looks wrong is evidence, not a mistake to tidy away. The correction is recorded
beside it.

**The deeper lesson is about method, not arithmetic.** The corrected anchoring method was documented in
prose and then applied *by hand, per batch*. That is how an unreproducible number entered the record and
sat there for a week, under a heading announcing a methodological fix. A method that exists only as prose
is not a method — it is an intention. It is now `anchor.py`.

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

## Front-loaded registration (2026-08-02) — decoupling the experiment from check-in discipline

**The largest remaining risk was never the code — it was 17 consecutive weekly check-ins.** The sample
only becomes informative near the end, so stopping at week six would bank all the work and produce
nothing. Registering predictions only as check-ins happen makes the entire result hostage to that.

**The structural fix: directional entries grade MECHANICALLY.** No source check, no judgement, no human
step. So they can be registered *now* for events months out and will resolve whether or not anyone shows
up. Only factual claims need a resolution pass.

**As at 2026-08-02: 54 live predictions, of which 41 (76%) grade with no check-in required**, spanning
resolve dates from 21 Aug through 27 Nov.

### The chained index-window sequence

Fourteen VAS entries on **disjoint, end-to-start ~5-trading-day windows** running 14 Aug → 27 Nov, each
asking whether the index return stays better than a threshold. Probabilities are the **measured
non-overlapping base rate** over 872 disjoint windows since 2009 (SE ~1%):

| Threshold | Measured P | Registered | Band filled | Count |
| --- | --- | --- | --- | --- |
| > −1.0% | 76.5% | 0.76 | 0.7–0.8 | 5 |
| > −1.5% | 83.5% | 0.84 | 0.8–0.9 | 5 |
| > −2.5% | 91.7% | 0.92 | 0.9–1.0 | 4 |

Registered **at** the base rate, deliberately unshaded — the 2026-07-19 correction established that a
2–3pp adjustment sits inside the noise band and would be false precision.

**⚠️ The 25 Sep → 1 Oct window is deliberately omitted.** VAS goes ex-distribution on 1 October every
year (verified from the dividend record: 2024-10-01, 2025-10-01, 2023-10-02), worth ~$1.10 on a ~$111
price — a ~1% mechanical drop that would bias any window spanning it. This is the trap flagged in the
2026-07-19 change-log entry, and it is handled with a gap rather than an invented adjustment.

### Serial correlation, measured rather than assumed

Chained windows are disjoint but **not independent** — volatility clusters. Measured on the same 872
windows, the serial correlation of the *outcome* is **+0.030 / +0.085 / +0.076** at the −1.0 / −1.5 /
−2.5 thresholds. The practical form is starker: at −2.5%, P(fail) is 8.3% overall but **15.3% given the
previous window failed**.

This is now encoded as a correlation floor that **decays with the gap** between windows (20-day time
constant). The decay matters: applying the flat figure to all 91 pairs cut the sequence to an effective
7.9, which is far too harsh for windows a quarter apart. Decayed, adjacent windows keep the measured
0.060 and windows 3.5 months apart fall to 0.0006, giving **effective n 10.9 from 14 raw** — close to the
AR(1) expectation of ~12.4 and slightly conservative.

### October–November results-reaction entries — first use of the corrected anchor

Six further `event-move` entries on **company-confirmed** results dates: BOQ 15 Oct, NST 21 Oct,
FMG 22 Oct, WBC 2 Nov, NAB 5 Nov, ANZ 9 Nov. (AGM dates were deliberately excluded — an AGM rarely
moves a price the way a result does.)

These are the first entries priced with the **corrected** anchoring method: past event days identified
by **maximum volume** within each reporting window, never by largest move. Two further improvements over
the August batch:

- **Reporting windows matched to each name's real cycle** rather than a generic Feb/Aug assumption —
  quarterly for the miners, full-year-plus-half-year for the banks, giving n=16–32 historical event days
  over 8 years instead of 10.
- **Shaded down** from the measured figure for small n *and* because a max-volume day can be an index
  rebalance or ex-dividend date rather than the result.

They span P 0.56–0.88 across four bands. The contrast with the August batch is deliberate and will be
readable at the wrap: **if the pre-registered over-confidence expectation holds, the August entries
should underperform their probabilities while these should not.** That is a direct, in-sample test of
whether the methodological fix actually worked.

### Rate decisions

Four policy-rate calls (RBA 29 Sep / 3 Nov, FOMC 16 Sep / 28 Oct — dates confirmed from primary sources,
the RBA via text proxy cross-checked against two independent RBA pages). **Deliberately priced modestly
at 0.58–0.68**, not the ~0.85–0.90 a settled-policy period would justify: the RBA is mid-tightening with
trimmed-mean CPI still above band, the July FOMC carried three dissents preferring a *hike*, and these
sit two-to-three meetings out. Given the over-confidence finding above, an unanchored high number here
would have been the same error repeated.

*(Note: there is no November FOMC meeting in 2026 — the Fed holds only 8, so 28 Oct is the last US
decision before the wrap.)*

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

As at check-in 4 (2026-08-09). Effective n ≈ 5.0 — far below the ~20 needed to say anything firm.
*(The count fell from 6.0 because the two remaining compliance entries were reclassified out of the
table on 2026-08-01, not because anything was un-resolved.)*

| Prob band | Mean predicted | Actual frequency | n |
|-----------|----------------|------------------|---|
| 0.5–0.6 | 0.54 | 1.00 | 1 |
| 0.6–0.7 | 0.61 | 0.50 | 2 |
| 0.7–0.8 | — | — | 0 |
| 0.8–0.9 | 0.85 | 1.00 | 1 |
| 0.9–1.0 | 0.90 | 1.00 | 1 |

Every cell is n ≤ 2. **No cell here supports any inference.** The 0.8–0.9 band opened at check-in 4 with
the RMD results-move resolution. **The 0.7–0.8 band is still empty** after four check-ins — it now holds
13 live entries, the first of which (`rba-holds-11aug`, P 0.70) resolves 11 Aug.

**Where the live sample is heading**, by band, across the 63 live calibration-scored entries (compliance
excluded): 0.5–0.6 → 22, 0.6–0.7 → 11, 0.7–0.8 → 13, 0.8–0.9 → 13, 0.9–1.0 → 4. The 0.5–0.6 band is the
fattest and the *least* informative per entry, because a near-coin-flip claim discriminates weakly; it is
fat because relative directional stock calls cannot honestly sit anywhere else. **Even assuming every
live entry resolves, no band reaches the ≈21 needed to detect even gross miscalibration** — the best case
is 0.5–0.6 at 23, and that is the band where 21 would buy the least. **The wrap should therefore state
"n too small to conclude" as its headline calibration result**, which is the pre-committed outcome, not a
disappointment to be written around.

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
| 2026-08-09 | **`anchor.py` added — the results-day anchoring method is now a script rather than a documented intention.** `python anchor.py TICKER --threshold X --months M,M --years N` reports the unconditional exceedance frequency, the volume-identified event-day frequency, the elevation ratio and the per-window detail. Two substantive improvements over the hand method: returns are computed on **dividend-adjusted** closes, and the **current, part-elapsed calendar month is excluded** as a window. | The 2026-08-02 correction fixed the *method* but left it being applied by hand, per batch. That is exactly how the unreproducible anchor table recorded above got into the record and stayed there for a week under a heading announcing a methodological fix. Adjusted closes remove the ex-dividend contaminant named in the original caveat (index rebalances remain, so the proxy is still impure and figures are still shaded down). Excluding the current month matters because a part-elapsed window holds no results day yet, so its max-volume session is just the busiest ordinary day — including it dragged measured frequencies **down** and would have made new anchors spuriously conservative. |
| 2026-08-09 | **Recomputation of the 2026-08-01 over-confidence table: 6 of 8 reproduce, RMD and TCL do not** (+35pp and −21pp). Recorded as a follow-up beside the original; **nothing edited**. | Three of the original figures were exactly 25%, which prompted the check. The batch-level pre-registration survives — recomputed mean 47.5% vs the recorded 46%, against a registered mean of 72.1% — because the two errors run in opposite directions and cancel. The per-entry table and the "RMD is the worst offender" ranking do not survive. Logged rather than corrected in place because a pre-registered expectation that later looks wrong is evidence, and editing it would destroy the only thing that makes it a test. |
| 2026-08-09 | **Event-move entries now require a COMPANY-CONFIRMED results date** — the company's own key-dates page or an ASX-lodged calendar, never an earnings aggregator. Names whose dates could not be primary-confirmed (BHP, DRO, ORG, GMG, MIN, JBH) were dropped from this batch despite usable anchors. | The date sweep found **REA had already reported on 6 Aug**, before the window it was being considered for. An event-move entry keyed to a wrong date does not measure a wrong forecast — it measures an ordinary trading session, and grades FALSE for reasons unrelated to judgement. Separately, a research pass returned "~24 Aug" for FMG's FY26 statutory result from converging secondary sources; Fortescue's own key-dates page says **20 August**, which is what the two live FMG entries already assume. Both live entries are therefore safe, and the secondary sources were simply wrong. |
| 2026-08-09 | **New `au-macro-data` cluster** for the two ABS entries (July unemployment, July CPI), with their weaker anchors declared inside their own `rationale` fields. | 14 of the ledger's entries are `results-reaction`; adding more inflates raw n while `effective_n` correctly declines to count it. Macro prints are genuinely uncorrelated with company results-day volatility, so they buy real independent sample. The declaration matters as much as the cluster: these two are anchored on a published level plus the series' step size, **not** on a computed distribution of historical monthly changes, which makes them softer than every price-based entry and they should be discounted accordingly at the wrap. |
| 2026-08-09 | **The 0.9+ band was deliberately left unfed**, despite being the thinnest (n=5). | The best measured anchor available this cycle was 87.5% (14/16, NST and WTC at their chosen thresholds), and house rule is to shade **down** from the measured figure for small n and proxy impurity. Shading down from 87.5% cannot honestly reach 0.90. Filling a thin band by inflating a probability to fit it is question selection driving the calibration curve — the identical error that got the date-of-disclosure claims retired on 2026-08-01. The band stays thin and the wrap says so. |
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
| 2026-08-02 | **Front-loaded registration: 18 entries covering Aug–Nov, and `ref_date` support extended to absolute-basis entries** so a SEQUENCE of disjoint end-to-start windows can be registered in advance. | The biggest remaining risk to this experiment was never the code — it was depending on 17 consecutive weekly check-ins for a sample that only becomes informative near the end. Directional entries grade mechanically, so they can be registered now and resolve unattended: **41 of 54 live predictions (76%) now need no check-in at all.** This converts the failure mode from "the run lapses and nothing is learned" into "the run lapses and the mechanical tracks still grade". |
| 2026-08-02 | **Serial-correlation floor added for same-ticker disjoint windows, decaying with the gap** (measured 0.06 adjacent, 20-day time constant). | Chained windows are disjoint but volatility clusters, so they are not fully independent — measured serial rho of the outcome is +0.030/+0.085/+0.076 across the three thresholds, and P(fail) roughly doubles given the previous window failed. Without a floor, `score.py` would have counted 14 chained windows as 14 independent observations. **The decay was necessary, not decorative:** a flat floor across all 91 pairs collapsed the sequence to an effective 7.9, over-penalising windows a quarter apart that share no regime. Decayed, it gives 10.9 from 14 raw. |
| 2026-08-02 | **Results-day anchoring method corrected: identify the event day by VOLUME, never by largest move.** `CHECKIN.md` updated; the eight live entries priced with the old method are left uncorrected with a pre-registered over-confidence expectation recorded above. | The original anchor identified the results day as the largest-move day in each window and then measured that move — **selection on the outcome variable, biased upward by construction.** Re-measured with volume identifying the day (independent of move size), the old anchor overstates by **+1.61pp** on average, leaving 6 of 8 live entries over-confident by >0.10 (mean gap +0.26). Caught before any of them resolved. The probabilities stand — append-only — so the expectation was pre-registered instead, which turns the batch into a falsifiable test of the system's own miscalibration rather than a spoiled sample. |
| 2026-08-01 | **Date-of-disclosure claims retired from calibration.** The 9 "company X reports on date Y" entries are tagged `"scoring": "compliance"`, still graded but excluded from the factual Brier and the calibration table; `CHECKIN.md` forbids new ones. Replaced by `basis: "event-move"` entries — results-day price-reaction claims graded mechanically against a `ref_date` close. | **These were never predictions.** ASX LR 4.3A obliges lodgement within two months of a 30-June balance date and the company publishes the date itself, so the base rate is >97%; the claim tested calendar-reading. Worse, stacked into the 0.9 band they would have manufactured a false "under-confident at the top" result out of question selection alone — 69% of the factual track was this. **The reclassification is self-penalising and that is the check that it is honest:** both resolved compliance entries were TRUE at P 0.95/0.93, so removing them moved the factual Brier from 0.0404 to **0.0772** and cut the 0.9 band from n=3 to n=1. Rule applied uniformly, without reference to outcome. *(Raised by Matt, who pointed out that a company meeting a legally-mandated deadline it announced itself is "things going as expected", not a forecast — and that the valuable question is what is IN the report and whether it moves the price.)* |
| 2026-08-01 | **New schema: `basis: "event-move"` with `ref_date`.** The reference price is the close on a pre-registered future date rather than one stamped at logging; outcome is `abs(return) > threshold_pct` from that close to the `resolve_date` close. `_window()` uses `[ref_date, resolve_date]` for these. | Measuring a *reaction* requires a reference from the session before the event, which only became possible once `get_close_on()` existed. Still tamper-proof: the date is fixed in advance and the close is a public mechanical number, so nothing is selected after the fact. The `_window` change matters for correlation — using `logged` would have made eight different companies' results days look like one overlapping blob and collapsed them to ~1 effective observation; with ref_date windows, same-day pairs correlate at 0.40 and different-day pairs at 0.00, giving effective n 6.67 from 8 raw. Verified on a scratch ledger against known closes: NST moved +2.222% from 28→29 Jul, grading TRUE against a 2% threshold and FALSE against 3%, with a future-dated entry correctly left ungraded. |
| 2026-08-01 | **The small-sample caveat is now unconditional, and per-band n is reported alongside it.** | It previously printed only while effective n was below 20 — meaning the warning that protects every reading of these numbers would **switch itself off exactly as the sample grew**, and the live ledger is now at 21.1. Crossing ~20 does not make a calibration curve readable; it only stops it being hopeless. The per-band thresholds (≈21 gross / ≈62 moderate / ≈97 subtle) are now printed every run so a band with n=3 cannot be mistaken for evidence. |
| 2026-07-31 | **Provenance model changed:** entries logged from this check-in carry `claude-opus-5[1m]`; check-ins 1–2 carry `claude-opus-4-8[1m]`. | Recorded because the provenance table now spans two models mid-experiment. This changes nothing about the standing pre-commitment: **no model-comparison claim will be made at the wrap.** Per-cell n is in the low single digits, the split is confounded with time and with question type, and a flattering cut will always be available. The field exists for description only. |
