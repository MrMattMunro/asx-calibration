# Paper Trading Log — $20k Mock Portfolio

> **A mental exercise, not real money.** Goal: test whether stock-picking holds Matt's
> attention/focus over ~1 month of periodic check-ins, and whether an active book of picks
> beats just buying the index. No brokerage account, no real capital at risk.

- **Pretend pot:** $20,000 AUD
- **Started:** 2026-07-11
- **Planned review window:** ~6 weeks (target wrap **~2026-08-26**, extended 2026-07-18 from the
  original ~08-11). **Why extended:** the catalysts that actually grade these picks — the August
  FY-reporting wall (CSL 18 Aug, BHP 17 Aug, QBE 14 Aug, Vicinity/SRG/NST 20 Aug, DRO ~26 Aug) —
  land *after* the original wrap. Ending 11 Aug would cut off right before the evidence arrives.
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

> **EODHD second-source test — NOT RUN (2026-07-18).** The optional automated cross-check needs a free
> API key, which has not been provisioned, so it remains unconfirmed whether plain EOD data for ASX
> works on their free tier. **EODHD is therefore disabled.** The code path is written and
> capability-flagged; enabling it later is a key in `EODHD_API_KEY`, not a code change. Until then the
> layer runs on gates plus manual GOOGLEFINANCE — the intended fallback, not a degraded mode.

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

- Each check-in, add **3–5 factual/event predictions** across the 0.6–0.95 range. Directional stock
  calls can only honestly sit near 0.5, so the upper calibration bands can *only* be populated by
  factual predictions — that's where calibration is actually testable, and it's cheap to generate.
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
