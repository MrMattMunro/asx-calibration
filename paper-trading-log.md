# Paper Trading Log — $20k Mock Portfolio

> **A mental exercise, not real money.** Goal: test whether stock-picking holds Matt's
> attention/focus over ~1 month of periodic check-ins, and whether an active book of picks
> beats just buying the index. No brokerage account, no real capital at risk.

- **Pretend pot:** $20,000 AUD
- **Started:** 2026-07-11
- **Planned review window:** target wrap **2026-11-28**, extended 2026-08-01 from ~2026-08-26 (itself
  extended 2026-07-18 from the original ~08-11).
  - **Why extended the first time:** the catalysts that actually grade these picks — the August
    FY-reporting wall (CSL 18 Aug, BHP 17 Aug, QBE 14 Aug, Vicinity/SRG/NST 20 Aug, DRO ~26 Aug) —
    land *after* the original wrap. Ending 11 Aug would cut off right before the evidence arrives.
  - **Why extended again (2026-08-01):** a power calculation, not a result. At n≈28 no probability band
    could reach the ≈21 resolved entries needed to detect even *gross* miscalibration, so the wrap could
    only ever have said "n too small". ~2026-11-28 puts the three upper bands within reach.
    ⚠️ **Extending after seeing early results is a questionable research practice**, so the reasoning and
    the pre-commitments are fixed in `FINDINGS.md` under "Pre-commitment on the extension" — including
    that **no further extension will be made on the basis of what the numbers say**. Note the extension
    cannot flatter the record: the directional Brier is currently 0.2858, *worse* than baseline, and more
    sample is expected to make that firmer rather than softer.
- **Check-in cadence:** every few days / each weekend — flexible, we're watching engagement
- **Benchmark:** $20,000 hypothetically all-in on VAS (Vanguard ASX300 ETF) on day one.
  The whole point — did the picks beat just buying the whole market?

*(Not financial advice — a learning exercise. Entry prices are latest available closes as of
2026-07-11; real fills would differ. Brokerage/tax deliberately ignored for the paper run.)*

---

## Holdings (entry 2026-07-11, re-baselined to yfinance)

> **Prices re-baselined 2026-07-11.** The original entry prices came from web-search snippets
> and were unreliable for several names (NWL, VSL especially — off by 20–30%). All entries and
> watch-list refs below are reset to **yfinance closes on 2026-07-11**, now the single source of
> truth. Day zero therefore = 0%. Prices auto-pulled by `quote.py`.

| Ticker | Company | Tier | Entry price | Allocation | Shares (implied) | Exit rule |
|--------|---------|------|-------------|-----------|------------------|-----------|
| BHP | BHP Group | Blue-chip (resources) | $58.28 | $5,000 | 85.79 | Anchor/income — review month-end; cut if −15% |
| CSL | CSL Ltd | Blue-chip (healthcare) | $122.89 | $5,000 | 40.69 | Contrarian quality — take profit +20% / review −15% |
| QBE | QBE Insurance | Financial (quality+momentum) | $25.47 | $4,000 | 157.05 | +20% take profit / −15% cut |
| VSL | Vulcan Steel | Mid-cap cyclical (steel distribution) | $4.70 | $3,500 | 744.68 | +20% take profit / −15% cut |
| DRO | DroneShield | **Speculative** (counter-drone defence-tech) | $2.29 | $2,500 | 1091.70 | The punt — trim +50% / hard stop −25% |
| | | | | **$20,000** | | |

**Benchmark yardstick (not part of the pot):** $20,000 in **VAS** @ $109.10 → 183.32 units.

---

## Theses (why each is in the book)

- **BHP — $5,000 (blue-chip anchor).** Diversified global miner (iron ore + copper). Recently
  rallied as iron ore/copper firmed. Here as the stable, dividend-paying ballast — low drama,
  shows how a mega-cap behaves vs the spicier names.
- **CSL — $5,000 (contrarian blue-chip).** Global blood-plasma/biotech leader trading well
  below its historic highs (~$126 vs much higher a couple of years ago). The bet: quality name
  at a beaten-down price. Tests whether "buy the dip on a great company" pays.
- **NWL — $4,000 (mid-cap growth).** Wealth-management platform, funds-under-administration
  growth story. Just announced a **Morgan Stanley partnership (7 Jul 2026)** that popped it ~6%
  — a live catalyst to watch. Classic "growth with momentum" mid-cap.
- **VSL — $3,500 (mid-cap cyclical/value).** Steel distribution across AU/NZ. Analyst consensus
  target ~$7.16 vs ~$6.84 entry (modest upside), pays a dividend. A cyclical value counterweight
  to the growth names.
- **DRO — $2,500 (the speculative punt).** DroneShield — counter-drone defence tech, contract-
  driven, wildly volatile (52-wk range **$1.63–$6.70**, currently near the low end ~$2.57). This
  is the "mate's hot tip" slot: big upside if contracts land, real chance of a large drawdown.
  Sized small (12.5%) on purpose — this is the one that teaches nerve.

**Tier weighting:** blue-chips 50% / mid-caps 37.5% / speculative 12.5%.

---

## Calibration experiment (from 2026-07-18)

**The exercise changed shape on 2026-07-18.** It started as "can a book of picks beat the index."
That question is close to unanswerable over six weeks with five stocks — noise swamps any signal, and
a lucky run looks identical to skill. So the primary question was replaced with two that *are*
measurable at this size:

1. **Is the factual research accurate?** When a checkable claim is asserted ("CSL reports 18 Aug"),
   how often is it true?
2. **Is it calibrated?** When it says 65%, does the thing happen about 65% of the time?

Calibration is the interesting one, because it is what makes a predictor usable at all. A
badly-calibrated 90% is worse than an honest 55%. And unlike returns, the habit transfers: write down
a probability and an objective resolution rule *before* the outcome is known, then grade mechanically.

**Money P&L is now the secondary metric** — it stays because it's the part that holds attention,
which was the original point of the exercise. Calibration is the primary output.

### The two tracks

| Track | How it resolves | What it's testing |
| ----- | --------------- | ----------------- |
| **Directional** | `score.py` computes the outcome from price data. No human judgement enters. | Forecasting. Expected: **no skill** — public news is priced in. |
| **Factual** | Against a citable primary source, URL recorded at resolution. | Research accuracy. Expected: reliable, but watch for over-confidence. |

Reporting them separately is the whole point. Blending "CSL reports on 18 Aug" (verifiable) with "NST
beats VAS" (near coin-flip) hides where the reliability actually lives.

### How it's scored

**Brier score** = mean((probability − outcome)²); lower is better. Two baselines:

- **Always-0.5** → Brier 0.25 by construction. Beating this is the bar for *any* directional skill.
- **Base rate** → always predict the observed outcome frequency p̄; Brier = p̄(1−p̄).

Brier alone conflates calibration with resolution, so a **calibration table** sits beside it: per
probability band, mean predicted vs actual frequency vs n.

**Sample size is reported as *effective* n, not raw count.** Fifteen gold miners is one gold bet
cloned fifteen times, and a single macro outcome would swing the whole score. Every prediction carries
a `cluster` tag and same-cluster entries get down-weighted. This is why the expansion below went into
banks, energy, telco, consumer staples, infrastructure and healthcare rather than more gold or AI
names — new sectors buy independent information; same-theme names mostly inflate the raw count.

### The safeguards, and why they exist

The failure mode here is not subtle: the same system writes the thesis, seeds the risks, *and* judges
whether it came true. So:

- **Pre-registration.** Probability *and* objective resolution rule are written before the outcome is
  known. `ref_price` and `bm_ref` are stamped from the same fetch at logging time and locked — if the
  benchmark baseline were filled in later it would silently drift to whenever the script happened to
  run, biasing every directional grade.
- **Append-only.** Entries are never edited after logging, only resolved. No goalpost-moving.
- **Mechanical grading.** Directional outcomes are computed, not judged. Factual outcomes are binary
  and must cite a resolving URL — no prose "I was basically right."
- **Integrity-gated prices.** A grade never runs on a suspect price (see below).
- **Small-n honesty.** `score.py` prints n beside every metric. **"n too small to conclude" is a
  valid, pre-committed result, not a failure.**

**The 8 existing watch-calls are grandfathered.** They stay graded YES/no as a labelled
"pre-calibration cohort" and are **excluded** from the ledger. Retro-assigning probabilities to calls
made a week ago, with the price action already visible, would inflate calibration and defeat the
experiment.

### Provenance — which AI, exactly

Every entry records the exact model, the surface (main session vs delegated subagent), whether live
web search informed it, and a batch tag. This matters because the seed calls below came from the main
session while the new-industry batch came from a Sonnet subagent — different context, different system
prompt, genuinely different systems. Without recording it they'd be silently pooled under one
"Claude" number.

**This is for attribution, not comparison.** Total sample will be ~20–40; split by model and surface
and track, per-cell n is in the low single digits. `score.py` prints the breakdown under an explicit
*descriptive only* header, and the pre-commitment is that **no model-comparison claim is made at this
wrap**, whatever the cells show.

### Price-data integrity

The risk that matters is not a small cross-source difference — it's a **silently broken price**
producing a confident wrong grade. There is no clean, free, automated, *independent* ASX feed (Stooq
is bot-gated now; most free tiers are US-only; every ASX-capable finance MCP just re-wraps yfinance,
so it adds no independence). So the backbone is internal plausibility gates in `prices.py`:
missing/NaN/zero, stale-unchanged across N sessions, outlier single-day moves. **A flagged price
blocks grading** until a human adjudicates, with `=GOOGLEFINANCE("ASX:XXX","closeyest")` as the
one-glance tie-breaker.

> **EODHD second-source test — PASSED, and it is now ENABLED (2026-07-18).** A free-tier key returned
> **real ASX end-of-day closes** for BHP, CSL and VAS (`.AU` suffix), matching yfinance to the cent on
> the 2026-07-17 close. So the free tier is not US-demo-only, and the automated cross-check is live.
>
> **What that exact agreement does and doesn't prove.** Official ASX closing prices are a single
> canonical number, so agreeing to the cent is *expected* — it is **not** evidence that the two feeds
> are genuinely independent, and it would look identical if both re-wrapped the same upstream. What the
> reconcile actually buys is **detection of feed breakage**: if yfinance goes stale or returns garbage,
> EODHD won't move with it. It cannot catch a bad upstream common to both. That is a real but bounded
> guarantee, and it is the one the gates were designed around anyway.
>
> **How it runs:** the free tier is ~20 calls/day, so `score.py` reconciles a **rotating 3 tickers per
> run** via a persisted cursor — every name gets covered over several check-ins. A yfinance-vs-EODHD
> gap above 1.5% raises a `divergence` flag, which (like any flag) **blocks grading** until adjudicated.
> The key lives in the `EODHD_API_KEY` environment variable and is never committed.

### Seed predictions — pre-registered 2026-07-18

All logged **before** any post-logging price move, at yfinance prices from a single fetch
(VAS `bm_ref` = $108.92). Probabilities are the honest ask, not tuned to look decisive.

**Directional — main session** (`claude-opus-4-8[1m]`, from the news sweep):

| ID | Claim | P | Ref | Cluster | Resolves |
|----|-------|---|-----|---------|----------|
| `nst-underperform` | NST underperforms VAS | 0.60 | $19.24 | gold | 2026-07-29 |
| `gnc-underperform` | GNC underperforms VAS | 0.58 | $5.02 | independent | 2026-08-26 |
| `vsl-gives-back` | VSL underperforms VAS | 0.55 | $5.07 | steel | 2026-08-26 |
| `dro-underperform` | DRO underperforms VAS | 0.55 | $2.14 | defence | 2026-08-26 |
| `csl-beats-vas` | CSL beats VAS | 0.52 | $123.32 | independent | 2026-08-26 |
| `wbt-rebounds` | WBT beats VAS | 0.50 | $5.84 | ai-infra | 2026-08-26 |

`wbt-rebounds` at exactly 0.50 is deliberate — a "no edge" marker, to test whether a stated coin-flip
really behaves like one.

**Factual — main session:**

| ID | Claim | P | Resolves |
|----|-------|---|----------|
| `csl-reports-18aug` | CSL FY26 results released 2026-08-18 | 0.85 | 2026-08-18 |
| `qbe-reports-14aug` | QBE H1 results released 2026-08-14 | 0.70 | 2026-08-14 |
| `rba-holds-11aug` | RBA holds the cash rate on 2026-08-11 | 0.70 | 2026-08-11 |
| `dro-asic-live` | The ASIC investigation into DroneShield is real and unresolved | 0.90 | 2026-07-18 |

QBE sits at 0.70 rather than 0.85 specifically because the research agent flagged that date as
medium-confidence from a secondary source. That gap is the calibration signal.

**Directional — new-industry batch** (`claude-sonnet-5`, subagent; six uncorrelated sectors picked for
independence, not conviction):

| ID | Claim | P | Ref | Cluster |
|----|-------|---|-----|---------|
| `cba-underperform` | CBA underperforms VAS | 0.55 | $171.78 | bank |
| `wds-beats-vas` | WDS beats VAS | 0.57 | $30.46 | energy |
| `tls-beats-vas` | TLS beats VAS | 0.52 | $5.04 | telco |
| `wow-beats-vas` | WOW beats VAS | 0.54 | $39.20 | consumer |
| `tcl-beats-vas` | TCL beats VAS | 0.51 | $14.69 | infra |
| `rmd-underperform` | RMD underperforms VAS | 0.54 | $28.75 | healthcare |

All sit between 0.51 and 0.57. That is the correct shape for public-news directional calls, and should
be read as honesty rather than fence-sitting.

**12 distinct clusters across 16 predictions.** All start at `outcome: null`.

### Cadence to the wrap

- Each check-in, add **8–10 factual/event predictions** across the 0.6–0.95 range *(raised from 3–5 on
  2026-08-01)*. Directional stock calls can only honestly sit near 0.5, so the upper calibration bands
  can *only* be populated by factual predictions — that's where calibration is actually testable.
- **Bias toward genuinely uncertain claims, not published-calendar reads.** A reporting date already on
  the company's investor calendar is a near-free 0.9: it fills a band but tests almost nothing. The test
  before logging is *could I have looked this up?* — if yes, ration it. Keep one or two per run for the
  top band rather than five. See the FINDINGS note on the factual track being too easy.
- Prefer **short-horizon** predictions that resolve in days; they compound sample faster.
- Only add directional calls genuinely independent of live ones; otherwise share the `cluster` tag.

### How to score

```
python score.py            # read-only, safe any time
python score.py --resolve  # writes outcomes for predictions past resolve_date (use at the wrap)
```

Precursor/event-study methodology lives in `paper-trading-event-studies.md`; the pre-committed rule
set is `precursors.json`, hunted each check-in with `python screen.py --precursors`.

---

## Check-in log

Each check-in: I look up live prices, mark the book to market, compare vs the VAS benchmark,
and — just as important — note whether Matt would've *held or bailed*, and whether it's still
grabbing his attention.

### 2026-07-11 — Opened / baseline
- Book established at $20,000, re-baselined to yfinance closes (see note above). Benchmark VAS
  $109.10. Everything at 0% — clean day zero. Watch-list refs also set. Automated via
  `quote.py` from now on.

### 2026-07-18 — Check-in 1 (week 1)

| Ticker | Entry | Current | Value | P&L $ | P&L % |
|--------|-------|---------|-------|-------|-------|
| BHP | $58.28 | $57.54 | $4,936.51 | $-63.49 | -1.3% |
| CSL | $122.89 | $123.32 | $5,017.50 | $17.50 | +0.3% |
| QBE | $25.47 | $24.99 | $3,924.62 | $-75.38 | -1.9% |
| VSL | $4.70 | $5.07 | $3,775.53 | $275.53 | +7.9% |
| DRO | $2.29 | $2.14 | $2,336.24 | $-163.76 | -6.6% |

- **Book total:** $19,990.40 vs $20,000 cost → **−0.05%**
- **Benchmark (all-VAS):** $19,967.00 → **−0.2%**
- **Verdict:** picks beating the index by ~0.1 pt — a dead heat, nothing proven at 1 week.
- **Movers:** VSL (+7.9%, +$276) is carrying the whole book; without it the book is red. DRO
  (−6.6%) is the expected spec drag, nowhere near its −25% stop. BHP/QBE small drags, CSL flat.
- **No exit rules triggered — hold-and-watch week.** Would Matt have held? Yes on all — nothing dramatic.

**Watch-list calls (7 of 8 wrong so far):**

| Ticker | Call | Ref | Current | Move | vs VAS | Right so far? |
|--------|------|-----|---------|------|--------|---------------|
| GNC | down | $4.86 | $5.02 | +3.3% | +3.5% | no |
| NST | up | $20.48 | $19.24 | −6.1% | −5.9% | no |
| WBT | up | $7.83 | $5.84 | −25.4% | −25.3% | no |
| NXT | up | $13.94 | $13.12 | −5.9% | −5.7% | no |
| PWR | up | $0.985 | $0.91 | −7.6% | −7.4% | no |
| SRG | up | $3.58 | $3.50 | −2.2% | −2.1% | no |
| VCX | up | $2.64 | $2.62 | −0.8% | −0.6% | no |
| NWL | down | $23.86 | $23.48 | −1.6% | −1.4% | **YES** |

- **Swap control:** NWL→QBE swap validated so far — NWL down 1.6% since the drop (right direction),
  though QBE is also down, so "less wrong," not yet "right." WBT cratered −25% (the spicy chip
  minnow did exactly what "high reversal risk" warned — glad it was a watch-thesis, not the book).

**News sweep (5 parallel research agents, 2026-07-18) — direction-change flags + catalyst calendar.**

Two findings that change the read:
1. **DRO — new governance overhang (the real flag).** Unresolved **ASIC investigation** disclosed
   **11 May 2026** into DroneShield's Nov 2025 disclosures + share sales by the then-CEO/chairman
   around a contract announced then retracted hours later. Plus a fresh **Jefferies** downgrade
   (Underperform, target ~$2.05), ~43–55% share dilution over the year, and **~12% short interest**.
   Tell: DRO *fell* this week despite NATO pledging **>US$40bn** to counter-drone (7 Jul) — market is
   weighting governance/dilution over the sector tailwind. Not near the −25% stop, and the big short
   base means any good surprise could squeeze hard — but the punt's risk profile is materially worse
   than at entry. **Watch closest.**
2. **VSL rose +8% on NO identifiable catalyst.** No company announcement in 2 weeks; the only bullish
   VSL story (new CEO/acquisition) is from **March**, stale. Move ran *against* a falling small-cap
   materials index → more likely flow/short-covering that partially unwinds than a real trend. Since
   VSL is carrying the whole book, our "win" may be softer than it looks.

Thesis corrections:
- **RBA is TIGHTENING** — cash rate 4.35% after 3 hikes in 2026; ~78% hold / ~22% *hike* priced for
  11 Aug. No rate cuts coming to rescue the rate-sensitive names. (NXT/NST notes already flagged the
  hawkish risk — direction was right.)
- **GNC bearish call stands** — the +3% is noise, not a crop story. ABARES *cut* the 2026-27 winter
  crop forecast 21%; El Niño developing (dry). Don't abandon the thesis on a beaten-down-base bounce.
- **CSL carries live regulatory risk into 18 Aug** — EU CHMP recommended revoking its TAVNEOS drug
  (26 Jun); a final EC ruling could land in-window (~$145m sales at risk; binary-sentiment fuel).
- **Gold momentum looks to be REVERSING** — ~$4,000, −3% on the week, ~26% off its Jan record high →
  supports the *bearish* reversal risk on NST, not the bullish "up" watch-call we logged. FOMC 28–29
  Jul is the next swing factor.

**Predictable catalyst calendar (knowable now — this is the "predict before it happens" deliverable):**

| Date | Event | Hits | Confidence |
|------|-------|------|-----------|
| 28–29 Jul | US FOMC rate decision | gold→NST, USD/AUD, AI trade→NXT/WBT | High (Fed primary) |
| 29 Jul | Northern Star Q4 production report | NST | High (NST calendar) |
| 11 Aug | RBA decision ~2:30pm | VCX, NXT, QBE, gold-via-AUD | Med-high (date not primary-verified) |
| 13 Aug | IAG results | QBE read-through | Medium |
| 14 Aug | QBE half-year results | QBE | Medium |
| 17 Aug | BHP FY26 results | BHP | Medium |
| 18 Aug | CSL FY26 results | CSL | High (CSL primary) |
| 20 Aug | Vicinity + SRG + Northern Star FY results | VCX, SRG, NST | High VCX; SRG pattern-based |
| ~26 Aug | DroneShield half-year results | DRO | Unverified |

Biggest single in-window event = **FOMC 28–29 Jul** (sets USD, gold, AI-trade tone at once). Most
reporting dates are single-secondary-sourced — reconfirm against each company's IR page before
grading. Live quotes remain ground truth over any price in search snippets.

### 2026-07-26 — Check-in 2 (week 2)

**Money book (secondary metric):**

| Ticker | Entry | Current | Value | P&L $ | P&L % |
|--------|-------|---------|-------|-------|-------|
| BHP | $58.28 | $58.85 | $5,048.90 | $48.90 | +1.0% |
| CSL | $122.89 | $114.22 | $4,647.25 | $-352.75 | -7.1% |
| QBE | $25.47 | $24.85 | $3,902.63 | $-97.37 | -2.4% |
| VSL | $4.70 | $5.27 | $3,924.47 | $424.47 | +12.1% |
| DRO | $2.29 | $2.04 | $2,227.07 | $-272.93 | -10.9% |

- **Book:** $19,750.32 (−1.2%) vs **benchmark** all-VAS $19,891.84 (−0.5%) → picks **lagging** by 0.7 pts.
- Movers: VSL still carrying the book (+12%); CSL (−7%) and DRO (−11%) the drags. Exactly the "no
  stock-picking edge" result the design predicts — money is the engagement metric, not the point.

**Calibration state:** 1 resolved (`dro-asic-live`, factual, Brier 0.0100, n=1 — means nothing).
15 directional + 8 factual live. Calibration table still empty except the one 0.9–1.0 cell.
**Nothing was due to resolve today** — the first cluster (NST quarterly, RIO H1, FOMC, the two
short-horizon VAS calls) comes due **29–30 Jul**. So `score.py --resolve` was a no-op, correctly.

**Research sweep (4 parallel Sonnet subagents): primary-sourced findings**

- **FOMC 29 Jul** — meeting date confirmed (federalreserve.gov). Current range **3.50–3.75%**, held
  since 17 Jun (Fed press release). A cut is priced ~0%; the live debate is **hold vs 25bp hike**,
  hike odds up ~12%→~38% by 24 Jul (CBS citing CME FedWatch) on an oil>US$100 reinflation narrative.
- **NST June-Q report 29 Jul** — CONFIRMED, NST's own 2 Jul ASX Production Update.
- **RIO H1 results 29 Jul** — CONFIRMED, RIO IR results page + SEC 6-K + RNS. (A snippet conflating
  13 Aug — the interim-dividend ex-date — with the results date was rejected.)
- **IAG FY26 results 13 Aug** — CONFIRMED, IAG's lodged "2026 Calendar of Key Dates" ASX PDF.
- **BHP FY26 results ~18 Aug** — UNVERIFIED (bhp.com bot-blocked). Secondary sources split 18 Aug
  (Motley Fool AU, matches BHP's Tuesday pattern) vs 17 Aug (aggregators, off-pattern).
- **Disconfirming sweep on live theses:** CSL regulatory risk **unchanged** — EU EC still hasn't ruled
  on TAVNEOS, thesis stands into 18 Aug. DRO got a **mild disconfirm** — Fidelity/FMR raised its stake
  to 9.93% on 20 Jul (buying into the risk window), though short interest reportedly also at highs;
  consistent with the near-coin-flip framing, no change. Gold choppy (dipped <$4,000 then bounced) →
  NST reversal thesis inconclusive pending the 29 Jul quarterly. **No live prediction changed.**

**Pre-registered this check-in (5 factual, before any outcome known) — spread 0.62–0.95:**

| ID | Claim | P | Resolves | Basis |
|----|-------|---|----------|-------|
| `fomc-holds-29jul` | FOMC holds at 3.50–3.75% on 29 Jul | 0.62 | 30 Jul | market-implied hold; genuinely two-sided |
| `bhp-reports-18aug` | BHP FY26 results on 18 Aug | 0.68 | 18 Aug | date unverified (17 vs 18); honest mid-band |
| `iag-reports-13aug` | IAG FY26 results on 13 Aug | 0.90 | 13 Aug | confirmed primary; "subject to change" caveat |
| `rio-reports-29jul` | RIO H1 results on 29 Jul | 0.93 | 29 Jul | confirmed primary |
| `nst-reports-29jul` | NST June-Q report on 29 Jul | 0.95 | 29 Jul | confirmed primary |

Two genuinely-uncertain calls (FOMC 0.62, BHP 0.68) plus three confirmed reporting dates placed to
populate the thin 0.9+ band — which directional stock calls can never reach. Provenance:
`claude-opus-4-8[1m]` / `claude-code-main`, web_search true.

**Precursor screen:** run (`screen.py --precursors`) across all three live rules. The quant leg
produced **51 candidate stubs** (governance-overhang 15, insider-buy-after-warning 15,
preupgraded-guidance-into-result 21). Each name's **news condition** was then verified by a targeted
sweep (3 parallel Sonnet subagents). **Result: exactly 1 of 51 confirmed —**

- **`csl-insider-buy-after-warning` → REGISTERED** (P 0.55, beats VAS, resolves 24 Sep). Both legs
  confirmed against primary CSL PDFs: guidance cut/impairments 11 May 2026 + director Gordon Naylor's
  on-market Appendix 3Y purchase 26 May. Direction flipped from the stub default to *outperform* per
  the rule's hypothesis. Flagged as correlated with the live `csl-beats-vas` call (discount at wrap).
- **governance-overhang: 0 confirmed.** DRO (ASIC) and WTC (AFP probe + chair resignation 7 Jul) had
  genuine overhangs but no matching bullish *sector* catalyst inside the 14-day window (gold was
  correcting, not rallying → NST/RMS/RRL fail part b). HVN cannot-verify.
- **preupgraded-guidance: 0 confirmed.** The "2+ guidance upgrades" bar is demanding; CDA (29 Apr)
  and CPU (10 Feb) had exactly one qualifying upgrade each, the rest fewer/none.

**Multiple-comparisons count: 51 name×rule tests this run.** A ~2% confirmation rate is the intended
behaviour of a demanding, pre-committed news condition — most quant matches are not real pattern
matches. With one confirmed name there is no cohort and no control group this run; it is a single
seed for the insider-buy rule, resolving post-wrap by design. Zero-confirmed on the other two rules
is itself a loggable outcome, not a failed run.

### 2026-07-31 — Check-in 3 (week 3) — **first resolutions**

**Money book (secondary metric):**

| Ticker | Entry | Current | Value | P&L $ | P&L % |
|--------|-------|---------|-------|-------|-------|
| BHP | $58.28 | $60.31 | $5,174.16 | $174.16 | +3.5% |
| CSL | $122.89 | $123.06 | $5,006.92 | $6.92 | +0.1% |
| QBE | $25.47 | $24.73 | $3,883.78 | $-116.22 | -2.9% |
| VSL | $4.70 | $5.25 | $3,909.57 | $409.57 | +11.7% |
| DRO | $2.29 | $1.70 | $1,850.44 | $-649.56 | -26.0% |

- **Book:** $19,824.87 (−0.9%) vs **benchmark** all-VAS $20,362.97 (+1.8%) → picks **lagging by 2.7 pts**,
  widened from 0.7 pts at check-in 2. DRO (−26%) is the drag; VSL (+11.7%) still the only real winner.
  The gap widening while the index rises is the expected shape of "no stock-picking edge."

**Two grader defects found and fixed — both latent until something actually came due.**

1. **`score.py` crashed on a read-only run.** The provenance table read `outcome` back off the ledger
   dict, but a newly-due directional entry is graded *in memory* and only written under `--resolve`.
   So the first time anything resolved, the command documented as "safe to run any time" died with a
   `TypeError`. Fixed by carrying `(entry, outcome)` pairs through to the reporting layer.
2. **Grading used the price on the day the check-in was RUN, not the close on `resolve_date`.**
   `prices.py` had no historical lookup at all. NST's rule pre-registers the window
   `[2026-07-18, 2026-07-29]`, but running this check-in on the 31st silently measured a two-day-longer
   window. Added `get_close_on()` (last session on or before `resolve_date`) and switched grading to it;
   `--resolve` now also writes a `graded_on` audit block recording which session priced the grade.

   **Verified outcome-neutral before adoption** — both entries resolving today grade identically either
   way (NST 0, VAS 1), so the fix cannot be a grader tuned to flatter the score. Done now because the
   exposure is concentrated: **14 of the 15 live directional entries resolve on 2026-08-26, the wrap date
   itself.** Running the wrap even one day late would have mis-windowed every one of them.

**Resolved this check-in — 5 entries (first directional resolutions in the experiment):**

| ID | P | Outcome | Basis |
|----|---|---------|-------|
| `nst-underperform` | 0.60 | **FALSE** | NST +7.59% vs VAS +2.66% at the 29 Jul close — it *out*performed |
| `vas-positive-to-30jul` | 0.54 | **TRUE** | VAS +1.84% at the 30 Jul close |
| `fomc-holds-29jul` | 0.62 | **TRUE** | Fed held 3.50–3.75%, 9–3, three dissents wanting a *hike* |
| `nst-reports-29jul` | 0.95 | **TRUE** | NST quarterly PDF cover page, 29 July 2026 |
| `rio-reports-29jul` | 0.93 | **TRUE** | Rio's own investor page, "Announced on Wednesday 29 July 2026" |

- **Directional Brier 0.2858 (n=2)** — worse than the 0.25 coin-flip baseline. This is the
  pre-committed expected result, arriving on schedule.
- **Factual Brier 0.0404, accuracy 100% (n=4).**
- Calibration table: 0.9–1.0 band now 3/3 at mean P 0.93; 0.6–0.7 band 1/2 at mean 0.61.

**Resolution notes worth keeping:**

- **NST was wrong on mechanism as well as direction.** The thesis was "gold momentum reversing." The
  research sweep found NST's July strength was an *oversold operational bounce* — the stock had cut FY26
  guidance twice and fallen ~40% in three months on KCGM execution problems, then beat an already-lowered
  bar on 29 Jul. NST is a noisy proxy for gold sentiment because it carries its own idiosyncratic story.
- **RIO is TRUE only on the ASX-facing date.** The release was a single simultaneous global event at
  ~22:30 UTC — 29 Jul in Sydney, **28 Jul in London**. An LSE/RNS-framed reading of the identical event
  resolves this FALSE. The rule's wording selects the ASX framing, so TRUE stands, but future
  dual-listed reporting-date claims must name the exchange and timezone.
- **FOMC carried a retrieval flag, chased down rather than waved through.** The verifying sweep found the
  July press-release *index* page didn't list the statement. Re-checked independently against the
  official FOMC calendar, which links the 29 Jul statement HTML, PDF, implementation note and press
  conference. Index omission was a summariser artifact, not a missing document.

**Research sweep (4 parallel Sonnet subagents): primary-sourced findings**

- **Q2 CPI (ABS, primary):** headline **+3.8%** y/y, trimmed mean **+3.6%** — still above the 2–3% band.
  Cash rate **4.35%**, unchanged since 17 Jun. Post-print an Aug hike is priced ~4% and **Westpac withdrew
  its last-standing hike call**. ⚠️ **rba.gov.au 403s automated fetch** (same as ato.gov.au) — rate level
  came via proxy plus cross-check, not a clean primary read. Westpac's own note quotes headline CPI as
  3.9% against the ABS's 3.8%; ABS is primary.
- **Reporting dates confirmed from company calendars:** RMD 6 Aug (US), CBA 12 Aug, SUN 12 Aug,
  TLS 13 Aug, TCL 13 Aug, CSL 18 Aug, FMG 20 Aug, WOW 26 Aug.
- ⚠️ **An aggregator claimed Telstra reports 20 Aug; Telstra's own key-dates page says 13 Aug.** The
  "primary beats snippet" rule earned its keep again this run.
- **CSL:** CHMP recommended **revoking** the TAVNEOS EU marketing authorisation on 25 Jun 2026 over
  ADVOCATE data-integrity concerns. **EC decision still pending with no published date** — a live
  unresolved overhang into the 18 Aug result.
- **DRO:** the 28 Jul HY26 update cut FY26 revenue guidance to **$250–270m vs ~$328m consensus**, gross
  margin 60% vs 65% — the mechanism behind the −21% move. ASIC matter still open.
- **WBT:** the ~26% fall followed a guidance *upgrade* (20 Jul, FY26 revenue to ≥A$13.5m). Post-rally
  profit-taking and doubts about revenue quality, not a broken thesis. Its FY26 result (28 Aug) lands
  *after* resolution, so no catalyst can rescue the call.
- **Prices: our own feed was vindicated.** Aggregators quoted VSL anywhere from $5.25 to $7.16; `quote.py`'s
  $5.25 matched the only correctly-dated source. Several "current" GNC/VSL articles were 2023–25 vintage
  resurfaced with recent-looking wrappers.
- **No live prediction was changed by the sweep.**

**Pre-registered this check-in (5, before any outcome known) — spread 0.56–0.94:**

| ID | Claim | P | Resolves | Why this probability |
|----|-------|---|----------|----------------------|
| `rmd-reports-6aug` | ResMed Q4 FY26 on 6 Aug (US) | 0.94 | 08-08 | company press release, read directly |
| `fmg-reports-20aug` | Fortescue FY26 on 20 Aug | 0.85 | 08-21 | **primary says 20 Aug, aggregators say 24 Aug** |
| `dro-reports-26aug` | DroneShield H1 on 26 Aug | 0.72 | 08-27 | **no primary exists**; convergent aggregators only |
| `tavneos-ec-pending-26aug` | No EC decision on TAVNEOS by 26 Aug | 0.62 | 08-26 | ~67-day norm lands ~31 Aug, just outside |
| `vas-positive-to-14aug` | VAS positive 31 Jul → 14 Aug | 0.56 | 08-14 | non-overlapping base rate 55.3% |

Chosen deliberately to fill the **empty 0.7–0.8 and 0.8–0.9 bands** rather than pad the 0.9 band with
another calendar read. See the FINDINGS note on the factual track being too easy. New entries share
`cluster: "reporting-dates"` so they discount against each other.

Provenance: **`claude-opus-5[1m]`** / `claude-code-main` — note the model changed from
`claude-opus-4-8[1m]` used at check-ins 1–2.

**Precursor screen:** run across all three live rules. 83 names screened (SVW skipped — delisted).
The quant leg shortlisted 50 after the research budget (governance 15 of 34 matched, 19 dropped and
listed by name; insider-buy 10; preupgraded 25). Each name's news condition was verified by targeted
sweep (4 parallel Sonnet subagents). **Result: 4 of 50 confirmed.**

- **`governance-overhang` → 2 confirmed: DRO, WTC** (both legs primary-checked). First time this rule
  has produced any match. DRO: ASIC investigation of 12 May still open + defence/counter-drone sector
  rally. WTC: AFP investigation and ASIC probe into ~A$229m of chair share trading + ASX IT sector rally.
- **`preupgraded-guidance` → 2 confirmed: CPU, MIN.** Both had two dated *company-issued* upgrades.
  **Direction FLIPPED from the stub default** — the rule hypothesises these names *beat* VAS, but
  `screen.py` emits every stub as "underperforms"; registering as emitted would test the rule backwards.
- **`insider-buy-after-warning` → 0 confirmed.** Two instructive near-misses: ARB has a genuine on-market
  director purchase (16 Jun) but its profit warning was January, outside the 45-day window; DRO has a real
  guidance cut (28 Jul) but no director purchase in the three days since.
- Rejections were strict and are the point: Harvey Norman's ASIC matter was **resolved** by judgment on
  28 Jul, so it fails "unresolved"; "reaffirmed", "narrowed", "guided to the top end" and results
  *beating* prior guidance were all rejected as non-upgrades.
- **DRO cluster choice, stated openly:** tagged `defence`, not `governance`. It is nearly the same bet as
  the live `dro-underperform` call — same stock, same direction, overlapping window — and that
  correlation is far stronger than its link to WTC via the rule. Tagging `defence` makes `score.py`
  discount it against the existing DRO entries, lowering effective n. The conservative choice, taken at
  the cost of the tag-by-rule convention.

**Multiple-comparisons count: 246 name×rule tests this run** (82 names × 3 rules). ⚠️ **This corrects the
record: check-in 2 logged "51 name×rule comparisons", but 51 was the count of quant MATCHES (15+15+21),
not tests performed.** `screen.py` computes `tests += len(rows)` per rule and has not changed since
19 Jul, so that run's true exposure was also ~246. The earlier figure understated multiple-comparisons
risk by ~5×.

### 2026-08-09 — Check-in 4 — **the anchor table does not reproduce**

**Housekeeping first: this log skipped two sessions.** The 1–2 Aug front-loading (18 predictions, the
circular-anchor catch, the run extension to 28 Nov) and the 8 Aug second-predictor arm were written into
`predictions.json`, `FINDINGS.md` and the commit messages, but **never into this file** — check-in 3 on
31 Jul is the last entry above. `CHECKIN.md` step 4 says new predictions go in the human record as well
as the JSON, and that did not happen. Noted here rather than backdated: those entries are dated where
they actually are, in the ledger.

**Money book (secondary metric):**

| Ticker | Entry | Current | Value | P&L $ | P&L % |
|--------|-------|---------|-------|-------|-------|
| BHP | $58.28 | $62.97 | $5,402.37 | $402.37 | +8.0% |
| CSL | $122.89 | $132.19 | $5,378.39 | $378.39 | +7.6% |
| QBE | $25.47 | $24.42 | $3,835.10 | $-164.90 | -4.1% |
| VSL | $4.70 | $5.60 | $4,170.21 | $670.21 | +19.1% |
| DRO | $2.29 | $2.18 | $2,379.91 | $-120.09 | -4.8% |

- **Book:** $21,165.98 (+5.8%) vs **benchmark** all-VAS $21,026.58 (+5.1%) → picks **ahead by 0.7 pts**,
  recovered from −2.7 pts at check-in 3. DRO's drag halved as it bounced; BHP and CSL did the work. Two
  reversals in three weeks on a five-name book is noise and should be read as noise.

**Resolved this check-in — 2 entries:**

| ID | P | Outcome | Basis |
|----|---|---------|-------|
| `2026-08-01-rmd-results-move-0807` | 0.85 | **TRUE** | RMD moved −8.29% on results day vs a ±2.0% bar |
| `2026-07-31-rmd-reports-6aug` [compliance] | 0.94 | **TRUE** | ResMed IR release, 6 Aug 2026 4:05pm EDT |

- **Directional Brier 0.1980 (n=3)** — beats the 0.25 coin-flip baseline. Per the standing
  pre-commitment this reads as **luck at n=3**, not edge, and the previous check-in's 0.2858 flipping to
  0.1980 on a single resolution is the clearest possible illustration of why.
- **Factual Brier 0.0772, accuracy 100% (n=2).** Compliance track 0.0037 (n=3, 6 live).
- Calibration effective n ≈ 5.0. The 0.7–0.8 band is still **empty**.
- **SEC EDGAR 403s automated fetches**, so the RMD compliance grade rests on ResMed's own IR release
  rather than an 8-K cross-check. Recorded in the entry's `resolution_note`. Add EDGAR to the list of
  primary sources that block us, alongside ato.gov.au and several ASX IR sites.

#### 🔴 The pre-registered over-confidence table does not reproduce

The 2026-08-02 entry in `FINDINGS.md` pre-registered that the eight 1 Aug event-move entries were
over-confident by a mean of +0.26, per a table of "volume-identified" probabilities. **Recomputing that
table this check-in, six of the eight land within ~6pp — and two do not:**

| | thr | registered P | FINDINGS said | recomputed | delta |
| --- | --- | --- | --- | --- | --- |
| RMD | 2% | 0.85 | 25% | **60%** | **+35pp** |
| TCL | 2% | 0.58 | 31% | **10%** | **−21pp** |
| CSL | 3% | 0.72 | 25% | 30% | +5pp |
| CBA | 2% | 0.68 | 25% | 30% | +5pp |
| SUN | 2% | 0.78 | 56% | 50% | −6pp |
| FMG | 3% | 0.85 | 69% | 70% | +1pp |
| WOW | 2% | 0.66 | 62% | 60% | −2pp |
| TLS | 2% | 0.65 | 75% | 70% | −5pp |

Three of the original figures were exactly 25%, which is what prompted the re-check. RMD was tested on
both the ASX and NYSE lines in case the original had used the wrong one — 60% and 40% respectively,
neither of them 25%. **The 25% is not recoverable from any reading of the method I could construct.**

**What this does and does not overturn:**

- ❌ It does **not** overturn the batch-level pre-registration. The recomputed mean across the eight is
  **47.5%** against the registered mean of 72.1% — the FINDINGS figure was 46% vs ~72%. The two errors
  run in opposite directions and very nearly cancel. **The headline expectation stands almost exactly.**
- ✅ It **does** overturn the per-entry table, and specifically the worst-offender ranking. RMD was
  listed as the single most over-confident entry at +0.60. On the recomputed anchor it is +0.25, mid-pack.
- ⚠️ **RMD is also the one that has now resolved — TRUE.** One resolution proves nothing either way, but
  it is consistent with the recomputed 60% and awkward for the recorded 25%.

Nothing was edited. The ledger is append-only and a pre-registered expectation is exactly what that rule
protects; the recomputation is recorded alongside it rather than over it.

**`anchor.py` added** so this cannot recur. The corrected volume-anchoring method was being applied
ad-hoc, by hand, per batch — which is how an unreproducible number entered the record and stayed there.
It is now a script: `python anchor.py NST --threshold 1.5 --months 2,8 --years 8`. Two improvements over
the hand method: returns are computed on **dividend-adjusted** closes, so an ex-dividend drop can no
longer masquerade as a large move (removing one of the two contaminants named in the original caveat);
and the **current, part-elapsed calendar month is excluded** as a window, since it holds no results day
yet and its max-volume session is just the busiest ordinary day.

**Pre-registered this check-in — 11 predictions, P 0.60–0.86:**

| ID | P | Type | Resolves |
|----|---|------|----------|
| `qbe-results-move-0814` | 0.60 | event-move | 14 Aug |
| `rba-retains-tightening-bias-11aug` | 0.62 | factual | 12 Aug |
| `iag-insurance-profit-in-guidance-fy26` | 0.68 | factual | 14 Aug |
| `col-results-move-0825` | 0.74 | event-move | 25 Aug |
| `csl-impairment-ge-1bn-fy26` | 0.78 | factual | 19 Aug |
| `sto-reaffirms-fy26-production-guidance` | 0.78 | factual | 21 Aug |
| `nst-results-move-0820` | 0.80 | event-move | 20 Aug |
| `wtc-results-move-0826` | 0.82 | event-move | 26 Aug |
| `abs-unemployment-jul-ge-4p3` | 0.85 | factual | 21 Aug |
| `sun-hazard-above-allowance-fy26` | 0.85 | factual | 13 Aug |
| `abs-cpi-jul-ge-3p4` | 0.86 | factual | 27 Aug |

Design notes:

- **All four event-move dates are COMPANY-CONFIRMED** from the company's own key-dates page, not a
  calendar aggregator. Made a hard requirement after the date sweep found REA had **already reported on
  6 Aug** — an event-move entry on REA would have measured an ordinary session and graded FALSE for a
  reason having nothing to do with the forecast. BHP, DRO, ORG, GMG, MIN and JBH could not be
  primary-confirmed (several IR sites 403 or time out) and were therefore **not** used, despite good
  anchors on some of them.
- **Two ABS entries deliberately sit in a new `au-macro-data` cluster.** 14 ledger entries are already
  `results-reaction`; piling on more inflates raw n while `effective_n` correctly refuses to count it.
  Macro prints are genuinely independent of company results-day volatility.
- **Their anchors are weaker and each entry says so in its own `rationale`.** The ABS claims are reasoned
  from the published level plus the series' step size, not from a computed distribution of historical
  monthly changes. The price-based entries are computed; these are argued. Discount them at the wrap.
- **The 0.9+ band was left alone on purpose.** It is the thinnest band (5 entries) and the temptation was
  to feed it, but the best measured anchor available this cycle was 87.5% (14/16, NST and WTC), and
  shading *down* from 87.5% cannot honestly produce a 0.90. Manufacturing one would repeat exactly the
  question-selection error that got the date-of-disclosure claims retired.

**FMG's results date was checked directly and the ledger is right.** A research pass returned "~24 Aug"
for the FY26 statutory result from secondary sources, which would have made both live FMG entries measure
a non-event day. Fortescue's own key-dates page says **"20 August 2026 FY26 Full Year Results"**. The
secondary source was wrong; the standing rule about not stating snippets as fact earned its keep again.

**Second predictor arm:** 13 pairs, 0 resolved, first pair resolves 12 Aug (SUN, CBA). Worth recording
that the arm **correctly contains no RMD entry** — RMD resolved on 7 Aug and the arm was registered on
the 8th, so mirroring it would have been a prediction made after the outcome was knowable.

**Precursor screen:** ran — **246 name×rule tests** across 3 live rules over 82 names (SVW skipped, no
data). 15-name cohorts emitted for the governance and pre-upgraded-guidance rules, with 10 further
matches dropped by the operational budget cap. **No new cohort was registered**, because the news leg was
not confirmed by sweep this session and `CHECKIN.md` only permits registering a *confirmed* cohort. Said
plainly rather than left as a silent gap: this is a deferred step, not a completed one. The 5 precursor
entries already live resolve 30 Aug, 14 Sep and 24 Sep and are unaffected.

---

<!-- Template for future entries:
### YYYY-MM-DD — Check-in N
| Ticker | Entry | Current | Value | P&L $ | P&L % |
|--------|-------|---------|-------|-------|-------|
| ...    |       |         |       |       |       |
- Book total: $X (vs $20,000 cost) → +/−X%
- Benchmark (all-VAS): $Y → +/−Y%
- Verdict: picks are beating / lagging the index by Z%
- Notes: catalysts, what I'd have done, engagement level
-->

---

## Watch-list — theses to grade (not in the pot)

Predictions logged with a reference price and a rationale, to check later. No money on them —
purely "was the call right?"

| Ticker | Company | Logged | Ref price | Direction called | Grade at month-end |
|--------|---------|--------|-----------|------------------|--------------------|
| GNC | GrainCorp | 2026-07-11 | $4.86 | **DOWN / underperform** | TBD |
| NST | Northern Star | 2026-07-11 | $20.48 | **UP / outperform** | TBD |
| WBT | Weebit Nano | 2026-07-11 | $7.83 | **UP / outperform** (spicy) | TBD |
| NXT | NextDC | 2026-07-11 | $13.94 | **UP / outperform** (quality) | TBD |

*(Refs re-baselined to yfinance 2026-07-11 closes; thesis prose above may cite the original
web-search figures — the table refs are what get graded. Grading is **vs VAS**: an "up" call is
right if it beats VAS, a "down" call if it lags VAS.)*

### Method bake-off — which *approach* finds winners?

Rather than more random picks, these test different **idea-generation methods** head to head. One
candidate per method, logged as a watch-thesis, graded vs VAS at month-end. The point is to learn
which *style* suits Matt — worth more than any single stock.

| Method | Ticker | Company | Ref | Call | The signal |
|--------|--------|---------|-----|------|-----------|
| **Insider buying** | PWR | Peter Warren Auto | $0.985 | UP | Founder bought ~$5.7M of own stock on-market right after a profit warning + took Exec Chair. Biggest $ director buy on the ASX that quarter. Near 14-yr lows. **Spicy** — betting against a real, recent downgrade, not just noise. |
| **Reporting catalyst** | SRG | SRG Global | $3.58 | UP | Engineering/services firm that **pre-upgraded FY26 guidance twice** (top of $164–168m EBITDA) on $1.85bn contract wins, and guided FY27 above consensus. Reports **~20 Aug** — note that's *just after* the month-end checkpoint, so the catalyst may land late; may need to hold this one longer. |
| **Turnaround** | *(CSL — already held)* | CSL Ltd | $122.89 | UP | The turnaround method is **already live in the book**: an independent research pass picked CSL as its #1 beaten-down-quality name (down ~55% from ~$275; damage mostly non-cash impairment + transitory destocking; still global #1 in plasma). Nice cross-validation of holding it. *(Spicier alt if wanted: Bapcor (BAP), down ~75%, but value-trap-adjacent — not logged.)* |
| **Screener / quant** | VCX | Vicinity Centres | $2.64 | UP | **Top blended score** in the multi-factor ASX screen (`screen.py`): quality + value, near its 52-wk high, PE ~9, ROE ~12%. The "the numbers picked it, not me" entry. Screen runners-up: RIO, RRL, QBE. |

*Screen run 2026-07-11 over 83 liquid ASX names. Full top-15 / momentum / value tables are
reproducible any time via `python screen.py`.*

### Swap decision — NWL → QBE (2026-07-12), with a control

Post-research, **NWL was swapped out of the book for QBE** (day-zero re-baseline, before any moves):
- **Why out (NWL):** PE ~104, falling (−6% 6mo, near 52-wk low), rate-sensitive into 11 Aug RBA,
  its Morgan Stanley catalyst reports 26 Aug (past window). Hardest holding to defend.
- **Why in (QBE):** adds a financial (book had none); ROE ~19%, cheap at PE ~12, strong momentum.
  **Honest caveat:** QBE is *at* its 52-wk high ($25.47 vs $25.61) — extended, so this is partly
  momentum-chasing. That's exactly why we track the control.
- **The control:** NWL stays on the watch-list (ref $23.86). **The swap was right if NWL
  underperforms QBE (and VAS); wrong / impulsive if NWL beats QBE.** This tests the decision
  itself — skill vs churn — not just the stocks.

**GNC thesis (bearish, 2026-07-11):** July/Aug is the Aussie winter-crop weather window — the
seasonal driver for grain handlers. In 2025 (good rainfall) GNC was the ag winner and rallied
into spring. This year is **inverted**: El Niño developing (61–80% prob moderate-strong),
below-average rainfall forecast for eastern Australia, USDA sees Aussie wheat down ~19%. GNC is
a *volume* handler, so drought = less grain to handle = pressure regardless of price. Stock has
**already dropped ~⅓ YTD** (from ~$7 to $4.77) pricing this in. Call: the "buy ag into spring"
pattern does **not** repeat in 2026 — expect GNC to stay weak / underperform VAS through the dry
window. China 55% beef tariff adds pressure to the ag complex; lifted barley tariff is a minor
offset. **Grade:** at month-end, did GNC fall (or lag VAS)? If it *rose*, the seasonal pattern
beat the weather macro — a lesson either way.

**NST thesis (bullish, 2026-07-11):** Gold miners are the standout recent-news momentum theme.
Chain: Middle East risk-off (Trump dismissed Iran talks, warned of strikes) + soft US payrolls
cooling Fed-hike fears + weaker USD → gold at/near record highs, J.P. Morgan targets ~US$6,000/oz
by Q4 2026. ASX gold index (XGD) jumped 8.3% in one session on strong quarterlies (Genesis +16%,
Catalyst +19%). Northern Star as the sector bellwether — notably it's **pulled back to $19.70**
(off its $31.96 March high, −5.6% on the week) *despite* the sector rally, so this is a bet on
the gold theme continuing / NST catching up. **Caveat baked in:** the trade is crowded and has
already run — if the Middle East de-escalates, gold and miners can reverse fast. That's exactly
why it's a watch-thesis, not a position. **Grade:** at month-end, did NST rise (and beat VAS)?
Watch for the de-escalation reversal risk. Note the **RBA decision on 11 Aug** (≈ month-end) as
a macro cross-current — a hawkish outcome lifts AUD, a mild headwind for AUD gold prices.

**WBT thesis (bullish, spicy — 2026-07-11):** The fresh tech breakthrough theme is **AI "Memflation"**
— the AI boom drove DRAM/memory prices up ~125%, and NVIDIA + SK hynix announced a multi-year
next-gen memory partnership. Memory is the new AI bottleneck. Weebit Nano is the ASX name most
directly levered (ReRAM next-gen memory): upgraded guidance, qualified at foundry DB HiTek, test
chips with onsemi, Texas Instruments deal, raised A$80m. Already **up ~118% over 90 days** to
$8.32 — so this is momentum-chasing a highly speculative, low-revenue, royalty-model name. **Call:
UP** on theme continuation, but **high reversal risk** — spicy by design. **Grade:** did WBT beat
VAS at month-end? Expect big swings either way.

**NXT thesis (bullish, quality — 2026-07-11):** The "real business" version of the same AI theme.
NextDC = AI data-centre infrastructure; just lifted senior debt facilities to **$8.7bn** to fund
expansion into AI-driven demand (big tech spending ~US$750bn on AI infra in 2026). Ref $13.83.
Cleaner/less lottery-ticket than the chip minnows. **Cross-current baked in:** NXT is long-duration
/ rate-sensitive — a hawkish **RBA on 11 Aug** (≈ month-end) is the main downside, and Nasdaq
weakness reads straight through to ASX tech. **Call: UP** on structural AI-infra demand. **Grade:**
did NXT beat VAS? Watch the RBA outcome as the swing factor.

**Tech watch note:** these two test the *same* AI theme at opposite risk tiers — WBT (spicy chip
minnow) vs NXT (quality infra). Comparing their month-end grades shows whether the AI trade paid
better via the lottery ticket or the blue-chip-ish infra name. Both share the RBA-11-Aug rate risk.

---

## How to check in (automated)

Run:

```
python quote.py
```

It reads `portfolio.json`, pulls live-ish ASX prices via yfinance
(~20 min delayed, free), and prints a ready-to-paste markdown check-in block — book marked to
market, P&L per position, book vs VAS, and every watch-call graded. Paste the output under
"Check-in log" above. (yfinance was `pip install`ed 2026-07-11; Python 3.12 on this machine.)

**Then the calibration score — this is the primary metric now:**

```
python score.py
```

Reads `predictions.json`, grades what has come due, and prints Brier scores vs baselines, the
calibration table, effective n, provisional standings, and any factual entries needing a source
check. Read-only; `--resolve` writes outcomes back and is for the wrap.

**The check-in rhythm is therefore:** `quote.py` (money + grandfathered calls) → `score.py`
(calibration) → log any **new** pre-registered predictions into `predictions.json` *before* their
outcomes are known → optionally `screen.py --precursors` for prospective precursor cohorts.

**Idea generation — the screener:**

```
python screen.py --top 15
```

Ranks a universe of ~83 liquid ASX names (`universe.json`) on four factors
(quality / momentum / growth / value), each percentile-ranked and blended. Prints top-blended,
top-momentum and top-value tables. Idea generation only — verify anything before acting. Edit
`universe.json` to add/remove names.

## Monthly research playbook — how we built this (repeat next month)

The angles we researched to generate the book + calls, so a future month is a re-run, not a
restart. Each: **what → why → how.**

1. **Balanced book across risk tiers** → spread $20k over blue-chip / mid-cap / speculative + a
   VAS benchmark → picked names per tier, priced via yfinance (NOT web search — see gotcha).
2. **Seasonality / annual-cycle sectors** (agriculture: GNC/ELD/NUF/SHV) → some sectors have
   recurring calendar rhythms (winter-crop weather window mid-year) → WebSearch last-year's
   July/Aug window *and* this-year's macro (ENSO El Niño, China tariffs). **Lesson: a macro shift
   can invert a seasonal pattern** — 2025's good-rain ag rally flipped bearish under 2026 drought.
3. **Recent world news (last ~2 weeks)** → catalysts with a directional tilt → WebSearch markets/
   commodities/rates. Surfaced gold-miner momentum (Middle East risk-off) + the RBA-11-Aug event.
4. **Tech breakthroughs** → fresh themes → WebSearch AI/semis/quantum, then map to ASX proxies
   (AI-memory "Memflation" → WBT; AI data centres → NXT).
5. **Idea-generation method bake-off** → test which *approach* finds winners, not just stocks:
   - **Insider buying** (ASX Appendix 3Y on-market director purchases) — bullish conviction signal.
   - **Reporting-season catalyst** — Aug reporting season; names that pre-upgraded guidance.
   - **Beaten-down quality turnaround** — great business, temporary/fixable problem.
   - **Quant screener** — `screen.py` multi-factor rank.
   How: spun up **3 parallel Sonnet research subagents** (insider / reporting / turnaround) +
   the screener for the quant leg.

**Discipline baked in (keep these):** re-baseline every price to ONE source (yfinance) so day
zero = 0%; log an exit rule *at entry*; unproven ideas go on the **watch-list**, not the book;
when swapping a holding, keep the dropped name as a **control** to grade the decision itself.

**Repeat cadence:** best run just before **August reporting season** each year (the biggest
recurring ASX catalyst). Re-run `screen.py` for fresh candidates; re-do steps 2–5 with the
month's live macro.

## Notes / open items

- **Entry prices re-baselined (2026-07-11):** the original web-search entries were unreliable —
  NWL was ~$30.64 vs a real ~$23.86, VSL ~$6.84 vs ~$4.70. Building the quote script surfaced it
  immediately (showed a fake −11% on day one). Now everything runs off yfinance, one source.
- Nobody's on margin, nothing's real. The only thing being spent is attention.
