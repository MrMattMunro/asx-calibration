# Event studies & precursor patterns

> **The trap this file exists to avoid.** Search the lead-up to any big price move and you will
> *always* find a plausible precursor. Hindsight guarantees a story. Analyses that skip a control
> group don't replicate. So nothing here becomes a claim until it has either (a) survived a matched
> control test, or (b) been registered as a forward rule and graded out-of-sample by `score.py`.

**Stated expectation, up front, so it can't be rationalised later:** precursors for *price moves*
mostly wash out. Precursors for *reactions* given a catalyst type — "when X is true, the market
underreacts to good news of type Y" — may hold. This tests which, honestly. Target the **reaction**,
not the **timing** of the catalyst; the latter is close to impossible from public data.

**Efficient-market steer:** expect the *quant-screenable* precursors (anyone can run them, so any
edge is arbitraged) to show little. The *news-synthesis* ones are where an LLM edge, if any, would
survive — so weight effort there.

---

## Two paths, and they have different evidence bars

There are two ways a precursor gets tested here, and it matters which one you are on.

### Path A — backward (an event study). Requires a control group before anything is registered.

You noticed a move, and you're reverse-engineering what preceded it. This is the dangerous
direction, so it carries the heavier bar:

1. **Identify** — a check-in flags a move that looks catalyst-driven (a discrete news event, not
   drift). Record the move, the date, and the apparent catalyst.
2. **Hypothesise** — state the precursor as a *crisp, falsifiable rule about the reaction type*.
   Good: "A defence/gov-contract stock under an unresolved regulatory probe *underreacts* to bullish
   sector news — it still underperforms VAS over the next N days." Bad: "DRO was going to fall."
3. **Control group** — pull **matched control windows**: names with a *similar setup* that did **not**
   produce the move. Aim for ≥3. Assess blind to outcome where practical. Ask the killer question
   explicitly: **would this precursor also appear before the non-movers?**
4. **Separation test** — does the pattern actually distinguish movers from non-movers better than
   chance? If it is equally present in the controls, record it as **non-predictive (hindsight
   artifact)** and stop. This is a common and valid result — log it as such rather than quietly
   dropping it.
5. **Register forward** — *only* if it survives step 4, write a pre-registered entry into
   `predictions.json` with a probability, an objective resolution rule, and `derived_from` set to
   this event-study id.
6. **Grade** — `score.py` grades it like anything else, and can slice `derived_from` predictions to
   show whether precursor-derived rules actually beat cold ones.

### Path B — forward (prospective screening). The screen *is* the control group.

You hunt the universe for names *currently* matching a **pre-committed** rule, and register a
prediction on **every** match before any outcome is known. This is the stronger test, and it does
not need hand-picked controls, because **the non-movers among the matches are the control group** —
measured automatically, with no opportunity to only notice the precursor after it pays off.

Its bar is different, not lower:

- **The rule must be pre-committed** in `precursors.json`. You never author a precursor to fit
  today's matches. That is the whole game.
- **Register the entire cohort**, including the matches that look unpromising. Cherry-picking the
  cohort destroys the control.
- **Multiple-comparisons discipline.** `screen.py --precursors` prints how many precursor × name
  tests were made each run, so the spurious-match risk stays visible rather than hidden.
- **A precursor is only ever called "holds up" on out-of-sample matches** — never on the cases that
  spawned it.

A rule can legitimately be *screened prospectively while still `status: candidate`*, even if the
backward event study that inspired it hasn't passed a control test. Path B generates its own
controls; that is precisely why it is the stronger path.

### Honest limits of mechanical screening

`screen.py` only sees yfinance price and fundamentals data. So most precursors are **hybrid**: a
screenable *quant condition* narrows the universe to a shortlist, then a targeted **news sweep**
confirms the *news condition* on that shortlist. Pure-quant rules auto-complete. Pure-news rules skip
the numeric screen entirely and go straight to a sweep. Don't overpromise mechanical screening the
data cannot support.

---

## The prospective-screen loop (run each check-in)

1. `python screen.py --precursors` → per-rule shortlists + ready-to-paste ledger stubs.
2. For hybrid/news rules, run a **targeted news sweep** over the shortlist to confirm the news leg.
3. Paste the confirmed cohort into `predictions.json` — **the whole cohort**, before any outcome is
   known.
4. `python score.py` grades them forward. The `derived_from` slice shows whether precursor-screened
   predictions beat cold ones.

---

## Registered rules

Live rules are in [`precursors.json`](precursors.json). Status vocabulary:

| Status | Meaning |
| ------ | ------- |
| `candidate` | Pre-committed and being screened, but unproven. |
| `active` | Survived on out-of-sample matches. |
| `retired` | Failed. Kept in the file — retired rules are evidence too. |

---

## Worked example — DRO (2026-07-18)

> ⚠️ **HINDSIGHT — NOT YET REGISTERED AS A FORWARD RULE.** This is a Path A hypothesis that has not
> had its control check. No probability has been registered off the back of it, and nothing in
> `FINDINGS.md` may cite it as a result.

**The move.** DroneShield (DRO) fell −6.6% in week 1 (2026-07-11 → 2026-07-18) **despite** NATO
pledging >US$40bn to counter-drone on 7 Jul — a large, unambiguously bullish sector catalyst.

**What was concurrently true.** An unresolved ASIC investigation disclosed 11 May 2026 (into Nov 2025
disclosures and share sales by the then-CEO/chairman around a contract announced then retracted
hours later), a fresh Jefferies downgrade (Underperform, target ~$2.05), ~43–55% dilution over the
year, and ~12% short interest.

**Candidate precursor.** *An unresolved regulatory/governance overhang suppresses a stock's reaction
to bullish sector news — it underperforms its sector over the reaction window despite the good news.*

**Why this is interesting rather than obvious.** A live bearish precursor sat directly next to a big
bullish one, and bearish won. If the pattern is real, it says something usable about *which* signal
dominates. If it isn't, it's a just-so story about one week of one small cap.

**Controls that must be gathered before this is registered (Path A):** other ASX small/mid defence-tech
names with positive sector news in the same window but **no** governance overhang. If they *also*
underperformed, the overhang explains nothing — the sector news was simply already priced, and this
is a hindsight artifact.

**Status:** hypothesis only. Note that the closely-related *forward* rule
`governance-overhang-suppresses-good-news` is being screened prospectively via Path B, which
generates its own controls — that is a separate, legitimate test, not a shortcut around this one.

---

## Results ledger

*(One row per completed study. Empty until the first control test or forward grade lands.)*

| Study id | Date | Hypothesis | Controls | Separated? | Outcome |
| -------- | ---- | ---------- | -------- | ---------- | ------- |
| `dro-governance-overhang-2026-07-18` | 2026-07-18 | Governance overhang suppresses reaction to bullish sector news | not yet gathered | — | **hypothesis only** |
