# Check-in runbook

The repeatable ritual, run every few days to the wrap. **The order is not cosmetic** — it is what
keeps pre-registration honest. Doing step 4 before step 2 would mean writing new predictions while
already knowing how the current ones are going, which is the single easiest way to fake a good
calibration score.

```
1. Record   →  2. Resolve  →  3. Research  →  4. Pre-register  →  5. Screen  →  6. Commit
```

---

## 1. Record the current state

```bash
python quote.py     # money book + grandfathered binary cohort
python score.py     # calibration: Brier, calibration table, effective n
```

Paste both into `paper-trading-log.md` under a new `### YYYY-MM-DD — Check-in N` heading.

**If `score.py` prints anything under "Held — not graded", stop and deal with it.** A held entry means
either a price integrity flag or incomplete pre-registration. Adjudicate with the printed
`=GOOGLEFINANCE("ASX:XXX","closeyest")` line before going further. Never grade around a held entry.

## 2. Resolve what has come due

**Directional** — mechanical. Nothing to judge:

```bash
python score.py --resolve
```

Writes `outcome` and `resolved_on` only for entries past `resolve_date`.

**Factual** — the dangerous one, because a human decides. `score.py` lists everything due under
"Needs source check." For each:

- Find the **primary** source — company IR page, ASX announcement, RBA statement, regulator release.
  Fetch and read the actual document. A search-result snippet is not a source; snippets garble dates
  and figures routinely.
- Record the **URL** in `source` and set `outcome` to 1 or 0.
- **"CANNOT VERIFY" is a valid outcome — leave it unresolved.** Never resolve TRUE because the claim
  sounds right or because it was probably right. This is the system grading its own homework; the
  citation requirement is the only thing holding it honest.
- If the resolution rule turns out to be unsatisfiable as written, resolve on the closest achievable
  evidentiary standard and **write down that you did**, in a `resolution_note`. Do not silently
  reinterpret the rule.

**Never edit a pre-registered field** (`claim`, `prob`, `resolution`, `resolve_date`, `ref_price`,
`bm_ref`, `rationale`, `provenance`). If one contains an error, the error stays and the correction
goes in `resolution_note`. The append-only rule costs something — that is the point of it.

**Second predictor arm** — after resolving, score it and run the paired comparison:

```bash
python score.py --ledger predictions_claude.json
python compare_arms.py
```

`predictions_claude.json` holds Claude's probabilities on a mirrored subset of the event-move claims
— identical claim text, resolution rule and dates, so difficulty is held constant and only the
probability differs. It is a **separate file on purpose**: it must never enter the primary Brier or
calibration table. The arm resolves off the *primary* ledger's outcomes, so there is nothing extra to
grade — just run the two commands.

## 3. Research

A news sweep across the live positions and the calendar ahead. Parallel agents work well: one per
theme or sector, each reporting catalysts, direction-change flags and dated events.

Two standing cautions:
- **Never state a search snippet as fact.** Prices, dates, salaries and consensus figures come back
  garbled. Fetch the primary source or label it unverified.
- **Live quotes from `prices.py` are ground truth** over any price appearing in search results.

## 4. Pre-register new predictions — before any outcome is known

Append to `predictions.json`. This is the step the whole experiment exists for.

**Target 8–10 factual/event predictions per check-in, spread across 0.6–0.95** *(raised from 3–5 on
2026-08-01)*. Directional stock calls can only honestly sit near 0.5, so the upper calibration bands
can *only* be populated by factual predictions. Miss this repeatedly and the calibration curve has no
upper half and the wrap can say nothing.

### 🚫 Do NOT register date-of-disclosure claims

**"Company X releases its results on date Y" is not a prediction.** It is a compliance event: ASX Listing
Rule 4.3A obliges a 30-June-balance-date company to lodge within two months, the company publishes the
date itself, and the base rate is >97%. Such a claim tests whether you can read a calendar.

Worse, it **corrupts the band it lands in**. Stack near-certainties into the 0.9 band and it reads
~100% actual against ~0.93 predicted — an apparent "under-confident at the top" finding manufactured
entirely by question selection. That is a false result, not a weak one.

The nine already in the ledger are tagged `"scoring": "compliance"`, still graded, and **excluded from
the factual Brier and the calibration table**. Do not add more.

**Test before logging: *could I have simply looked this up?*** If yes, it does not belong in the
calibration track.

### ✅ What to register instead — content and consequence

The valuable question is not *when* a report lands but **what is in it, and whether it moves the price**:

1. **Content claims** — resolvable from the released report itself. *"NST's first FY27 production
   guidance midpoint is below X Moz"*, *"CBA declares a FY26 final dividend of at least $Y"*,
   *"Woolworths FY26 Australian Food EBIT is below FY25"*. Genuinely uncertain, objectively checkable,
   and they test judgement about a business rather than a calendar.
2. **Price-reaction claims** — graded mechanically from price, no source check and no self-grading.
   Use `basis: "event-move"` with a `ref_date` (the session before the event) and a `threshold_pct`:
   *"CSL's absolute move on FY26 results day exceeds ±2%"*. Direction claims (*"closes higher"*) are
   honest but pin near 0.50; **magnitude claims are how the upper bands get filled legitimately**,
   because the probability can be anchored to that stock's measured realised volatility.
3. **Pending decisions with no published date** — `tavneos-ec-pending-26aug` (P 0.62) is the shape.

**Anchor every probability to something computed, not felt.** For a magnitude claim, measure the stock's
historical frequency of exceeding the threshold and state it in the `rationale`; shade for the event and
say by how much. An unanchored number is the over-confidence this experiment exists to detect.

🔴 **NEVER identify a past event day by "the biggest move in the window."** That selects on the outcome
variable and biases the anchor upward — measured at **+1.61pp** on the 2026-08-01 batch, which left 6 of
its 8 entries over-confident by >0.10 with a mean gap of +0.26. **Identify the event day by VOLUME**
(results days spike turnover), which is independent of move size, *then* measure the move on that day.

Two further cautions on the volume method: a max-volume day inside a window can also be an index
rebalance or an ex-dividend date, so state it as a proxy; and where the actual historical results dates
can be obtained from the company's own archive, use those in preference to any proxy at all.

**Per-band n is what governs whether any of this means anything.** Detecting gross miscalibration (a
claimed 0.90 that is really 0.70) needs ≈21 resolved entries **in that band**; moderate (0.90 vs 0.80)
needs ≈62; subtle (0.60 vs 0.50) needs ≈97. Spread new entries toward whichever bands are thinnest —
`score.py` prints the count for each.

- Prefer **short-horizon** predictions that resolve in days — they compound sample far faster than
  hold-to-wrap calls.
- Only add directional calls **genuinely independent** of live ones. Otherwise share the `cluster`
  tag, so `score.py` discounts them in effective n rather than letting a theme masquerade as sample.
- Every entry needs: `prob` (P the claim is TRUE), an **objective** `resolution` rule, `resolve_date`,
  `cluster`, and `provenance`.
- **`ref_price` and `bm_ref` are stamped from the same fetch, now, and locked.** Never null on a
  directional entry.
- **`provenance.model` records what was actually configured** — the exact ID (`claude-opus-4-8`,
  `claude-sonnet-5`, …), never a family name, never a guess. A subagent cannot reliably self-report
  its own model; the orchestrating session sets it. If genuinely unknown, `"unverified"`.

Write honest probabilities. A 0.50 is a legitimate, informative entry. Inflating confidence to look
decisive is the failure mode this experiment is built to detect — and it will detect it.

## 5. Precursor screen (optional but cheap)

```bash
python screen.py --precursors
```

- Confirm each shortlisted name's **news condition** with a targeted sweep. The quant leg only
  narrows; it does not establish the pattern.
- **Register the whole confirmed cohort**, including the unpromising ones — the non-movers are the
  control group. Cherry-picking destroys it.
- Fill `bm_ref` and `provenance.model` in the emitted stubs before pasting.
- Note the multiple-comparisons count in the log. It is there to stay visible.
- **Never author a new precursor to fit today's matches.** Rules are pre-committed. If a rule needs
  changing, log the change, the date, and why — and treat any change made after seeing matches as
  suspect even when it is defensible.

## 6. Update the record and commit

- `FINDINGS.md` — update the results tables. **Report null and unflattering results plainly.**
- Any method change goes in the FINDINGS change log with its reason.
- Commit and push. Check `git status` for stray secrets first; the key lives in `EODHD_API_KEY` and
  is never committed.

---

## Standing pre-commitments

Written down so they cannot be quietly abandoned when the numbers arrive:

- **Directional Brier ≈ 0.25 is the expected result.** If it beats 0.25 at this sample size, the
  honest reading is luck, not edge.
- **No model-comparison claim at this wrap**, whatever the provenance table shows. Per-cell n is far
  too small and a flattering cut is always available.
- **"n too small to conclude" is a valid, pre-committed outcome**, not a failure to be written around.
- A precursor is only ever called "holds up" on **out-of-sample** matches, never on the cases that
  inspired it.
- **The Claude arm is frozen at 13 paired entries, registered 2026-08-08.** Its probabilities are a
  documented mechanical function of measured history, not a judgement, and they are never re-derived
  once logged — even if the method is later found wanting. A re-derivation after any outcome is known
  is not a prediction.
- **The arm cannot be used to justify spending on market data.** 13 pairs is below the primary run's
  own ~21 threshold for detecting even gross miscalibration. A favourable result means "worth a
  larger arm next time", never "the estimates are good enough to trade on". The whole reason this
  arm exists is that "can Claude predict markets" was being settled by argument instead of measurement;
  settling it by an underpowered measurement is the same error wearing a lab coat.
