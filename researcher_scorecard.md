# Researcher Scorecard

*Living document. Updated after every meaningful research cycle. Tracks long-term growth, not short-term productivity.*

**Researcher:** Richard
**Started:** 2026-07-09
**Last updated:** 2026-07-12 (EXP-005 cycle — Argus-executed; researcher absent this cycle)

---

## Baseline (self-reported 2026-07-09)

Solid undergrad core: comfortable with calculus, linear algebra, and probability; limited exposure to econometrics and time series. Levels below are **self-reported and unverified** — each will be confirmed or corrected by the mastery checks in `learning_notes/foundations_curriculum.md`. Data access: free sources (Ken French, FRED, Yahoo) plus academic WRDS/CRSP/Compustat.

First phase chosen by the researcher: **foundations first** (Modules 1–5), capstone = replication of the stylized facts of asset returns (Cont 2001).

## Literature

| Metric | Count | Notes |
|--------|-------|-------|
| Papers read (by researcher) | 0 | declined to read M&P 2016 (2026-07-10) — honest zero |
| Papers digested via Argus summaries | 5 | M&P 2016, HLZ 2016 (partial), J&M 2020, C&Z 2022, CST 2014 (digest pending researcher's return) |
| Papers fully understood | 0 | "Fully understood" = could re-derive the core result and explain it to a skeptic. Researcher independently reconstructed most of M&P's *design logic* (2026-07-09) — close, not counted |
| Papers replicated (by the lab) | 1 | EXP-001: M&P 2016 — executed by Argus, directed by researcher |
| Landmark papers mastered | 0 | |
| Research areas explored | 1 | cross-sectional anomaly decay |

## Mathematics

Mastery scale: `0 — unaware` · `1 — heard of it` · `2 — can follow` · `3 — can apply` · `4 — can derive` · `5 — can extend/teach`

| Topic | Level | Confidence | Weaknesses | Next step |
|-------|-------|-----------|------------|-----------|
| Probability | 3 (self-rep.) | medium | conditional expectation as projection; heavy tails | Module 1 |
| Linear algebra | 3 (self-rep.) | medium | projection geometry of OLS | Module 3 |
| Statistics / inference | 2 (self-rep.) | low | multiple testing, bootstrap, power | Module 2 |
| Time series | 1 (self-rep.) | low | stationarity, unit roots, GARCH | Module 4 |
| Econometrics | 1 (self-rep.) | low | robust/HAC inference, OVB in finance | Module 3 |
| Bayesian inference | 1 (self-rep.) | low | | Phase 2+ |
| Optimization | 2 (self-rep.) | low | | Phase 2+ |
| Statistical learning | 1 (self-rep.) | low | | Phase 2+ |
| Stochastic calculus | 0–1 | — | | later |
| Information theory | 0–1 | — | | later |
| Measure theory | 0–1 | — | | later |

## Experimental Ability

| Metric | Count |
|--------|-------|
| Hypotheses proposed independently | 0 |
| Experiments designed independently | 0 |
| Replications completed | 0 |
| Novel experiments | 0 |
| Robustness analyses | 0 |
| Negative results documented | 1 (EXP-005, lab-level: first `failed_experiments/` entry; researcher not yet author of one) |
| Statistical mistakes caught before execution | 0 |

## Scientific Judgment — Milestone Log

Record dated, concrete examples where the researcher: changed their mind after evidence; rejected an exciting but weak idea; identified overfitting; caught leakage; recognized publication bias; improved an experimental design; connected unrelated literature; generated an original research question.

- **2026-07-09 — First committed pre-literature prediction.** Before reading McLean & Pontiff (2016), predicted the three-window return pattern for published anomalies. Got the story-1 timeline right; blended overfitting (story 2's explanation) with persistence (story 1's prediction) in one answer, and picked the wrong discriminating window (post-publication instead of post-sample-pre-publication). Lesson extracted: *each candidate mechanism must generate its own full set of predictions — a hypothesis is a row in a table, not a single timeline.* Details in `ideas/2026-07-09-anomaly-decay-prior.md`.
- **2026-07-11 — (Argus calibration note, logged here for symmetry.)** Across EXP-002/003, four of Argus's registered predictions failed (EXP-002 P4; EXP-003 P2/P4/P6), all by over-predicting how visibly a mechanism would show up. The researcher should read the failed predictions before the passed ones — they are the honest part of the record, and spotting *why* they failed is this week's best training material. No researcher judgment events this cycle (researcher absent).
- **2026-07-12 — (Argus calibration, continued: the miss pattern is now a standing rule.)** EXP-005 added two more directional misses (P2 volatility sign, P3 citations sign) *and* a subtler failure: P1 passed its registered decision rule yet its mechanism interpretation was overturned by a one-regressor scale diagnostic. Running total: 6 of 16 registered predictions failed, every miss from over-predicting mechanism visibility. Standing rule adopted: no Argus mechanism claim is reported without a scale/composition diagnostic beside it. Teaching value for the researcher: *a registered pass is not a mechanism* — see the EXP-005 digest. No researcher judgment events this cycle (researcher absent).

## Contribution Attribution Ledger

Each research cycle gets one of four levels (defined in the charter §Contribution Attribution): **AI-led** · **Human-directed** · **Collaborative** · **Human-led**. No percentages — the construct is not continuously measurable, and pretending otherwise is false precision. The evidence column carries the claim; the label only summarizes it.

| Date | Work | Level | Evidence |
|------|------|-------|----------|
| 2026-07-09 | Repository + charter initialization | AI-led | Repository initialized by Argus from the charter |
| 2026-07-09 | Anomaly-decay thread selection | Human-directed | Researcher redirected the first cycle away from the math curriculum toward his own question, and committed falsifiable three-window predictions before reading the literature (`ideas/2026-07-09-anomaly-decay-prior.md`) |
| 2026-07-10 | EXP-001 (M&P replication) | Human-directed | Thread chosen by researcher; literature, hypothesis, design, code, and write-up by Argus. Growth risk flagged at the time: delegated execution teaches nothing by itself |
| 2026-07-11 | EXP-002, EXP-003 | AI-led | Researcher requested "two cycles" and was otherwise absent; the EXP-002 design-it-yourself opportunity lapsed unanswered and Argus designed both experiments. One missed day proves nothing; three would be a pattern |
| 2026-07-12 | EXP-005 (rejected: decay is scale-proportional) | AI-led | Researcher requested "another cycle … with something else" and was otherwise absent. EXP-004 worksheet remains empty (day two of the lapse noted above); the reserved human-led slot held. Two prediction questions now await him: the EXP-004 worksheet and the EXP-005 digest's placebo-drift numbers |

**Standing target:** the next cycle (EXP-004, correlation-sorted placebo spillover) is reserved as the first **Human-led or Collaborative** entry — the researcher's prediction, mechanism, design, and postmortem, with Argus as critic and implementer. Worksheet: `experiments/EXP-004-placebo-spillover/researcher-worksheet.md`. An empty worksheet blocks the cycle; Argus does not run EXP-004 without it.
