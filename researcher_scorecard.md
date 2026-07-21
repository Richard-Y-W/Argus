# Researcher Scorecard

*Living document. Updated after every meaningful research cycle. Tracks long-term growth, not short-term productivity.*

**Researcher:** Richard
**Started:** 2026-07-09
**Last updated:** 2026-07-21 (EXP-017–019 — Argus-executed)

---

## Baseline (self-reported 2026-07-09)

Solid undergrad core: comfortable with calculus, linear algebra, and probability; limited exposure to econometrics and time series. Levels below are **self-reported and unverified** — each will be confirmed or corrected by the mastery checks in `learning_notes/foundations_curriculum.md`. Data access: free sources (Ken French, FRED, Yahoo) plus academic WRDS/CRSP/Compustat.

First phase chosen by the researcher: **foundations first** (Modules 1–5), capstone = replication of the stylized facts of asset returns (Cont 2001).

## Literature

| Metric | Count | Notes |
|--------|-------|-------|
| Papers read (by researcher) | 0 | declined to read M&P 2016 (2026-07-10) — honest zero |
| Papers digested via Argus summaries | 9 | Prior eight plus Jensen, Kelly, and Pedersen 2023; no new researcher reading claimed |
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
| Negative results documented | 9 (EXP-004/005/006/007/008/009/010/014/016 at lab level; researcher not yet author of one) |
| Statistical mistakes caught before execution | 0 |

## Scientific Judgment — Milestone Log

Record dated, concrete examples where the researcher: changed their mind after evidence; rejected an exciting but weak idea; identified overfitting; caught leakage; recognized publication bias; improved an experimental design; connected unrelated literature; generated an original research question.

- **2026-07-09 — First committed pre-literature prediction.** Before reading McLean & Pontiff (2016), predicted the three-window return pattern for published anomalies. Got the story-1 timeline right; blended overfitting (story 2's explanation) with persistence (story 1's prediction) in one answer, and picked the wrong discriminating window (post-publication instead of post-sample-pre-publication). Lesson extracted: *each candidate mechanism must generate its own full set of predictions — a hypothesis is a row in a table, not a single timeline.* Details in `ideas/2026-07-09-anomaly-decay-prior.md`.
- **2026-07-11 — (Argus calibration note, logged here for symmetry.)** Across EXP-002/003, four of Argus's registered predictions failed (EXP-002 P4; EXP-003 P2/P4/P6), all by over-predicting how visibly a mechanism would show up. The researcher should read the failed predictions before the passed ones — they are the honest part of the record, and spotting *why* they failed is this week's best training material. No researcher judgment events this cycle (researcher absent).
- **2026-07-12 — (Argus calibration, continued: the miss pattern is now a standing rule.)** EXP-005 added two more directional misses (P2 volatility sign, P3 citations sign) *and* a subtler failure: P1 passed its registered decision rule yet its mechanism interpretation was overturned by a one-regressor scale diagnostic. Running total: 6 of 16 registered predictions failed, every miss from over-predicting mechanism visibility. Standing rule adopted: no Argus mechanism claim is reported without a scale/composition diagnostic beside it. Teaching value for the researcher: *a registered pass is not a mechanism* — see the EXP-005 digest. No researcher judgment events this cycle (researcher absent).
- **2026-07-14 — Two more mechanism bets mostly fail.** EXP-006 rejected all three registered predictions; EXP-007 passed one magnitude-only prediction but failed its primary and robustness predictions. The lab correctly resisted promoting the positive cohort contrast. No researcher judgment event: researcher absent.
- **2026-07-15 — A paired repair still rejects the mechanism proxy.** EXP-010 replaced EXP-009's between-signal EW/VW comparison with official within-signal pairs. The primary mean cleared its economic threshold but not its inference rule; the levels sign and 50% breadth contradicted the story. The lab treated the preregistered threshold as binding despite a significant winsorized check. No researcher judgment event: researcher absent.
- **2026-07-16 — Search and holdout calibration.** EXP-011/012 quantified how search breadth inflates naive significance and how an untouched confirmation layer controls null false claims. Both survived their registered synthetic bounds; the lab explicitly withheld market and alpha interpretations. No researcher judgment event: researcher absent.
- **2026-07-16 — External replication rejects transport.** EXP-013 found small, imprecise negative post-publication estimates in world-ex-US, developed, and emerging factor aggregates. The lab rejected the hypothesis despite a suggestive post-publication-minus-post-sample contrast because the registered joint rule failed. No researcher judgment event: researcher absent.
- **2026-07-17 — Coverage rejected; geographic bridge survives cautiously.** EXP-014's falsifier fired because a 1986 floor strengthened US decay. EXP-015 passed all written rules, while the lab foregrounded its unregistered-but-more-direct paired gap's t = -1.27 rather than allowing the pass label to imply settled geography. No researcher judgment event: researcher absent.
- **2026-07-18 — Standalone US level survives; geography difference does not.** EXP-016 found US decay of -0.164 pp/month (t=-2.97), yet rejected the joint hypothesis because the registered paired US-minus-world-ex-US t-statistic was -1.45 rather than the required -1.65. No researcher judgment event: researcher delegated the cycle.
- **2026-07-21 — Three robustness objections tested prospectively.** EXP-017 retained the US result under factor-and-month clustering; EXP-018 retained it outside a publication ±1-year donut; EXP-019 found that within-factor stock-count controls did not absorb it. These harden the return pattern but were not promoted as mechanism evidence. No researcher judgment event: researcher delegated the cycles.

## Contribution Attribution Ledger

Each research cycle gets one of four levels (defined in the charter §Contribution Attribution): **AI-led** · **Human-directed** · **Collaborative** · **Human-led**. No percentages — the construct is not continuously measurable, and pretending otherwise is false precision. The evidence column carries the claim; the label only summarizes it.

| Date | Work | Level | Evidence |
|------|------|-------|----------|
| 2026-07-09 | Repository + charter initialization | AI-led | Repository initialized by Argus from the charter |
| 2026-07-09 | Anomaly-decay thread selection | Human-directed | Researcher redirected the first cycle away from the math curriculum toward his own question, and committed falsifiable three-window predictions before reading the literature (`ideas/2026-07-09-anomaly-decay-prior.md`) |
| 2026-07-10 | EXP-001 (M&P replication) | Human-directed | Thread chosen by researcher; literature, hypothesis, design, code, and write-up by Argus. Growth risk flagged at the time: delegated execution teaches nothing by itself |
| 2026-07-11 | EXP-002, EXP-003 | AI-led | Researcher requested "two cycles" and was otherwise absent; the EXP-002 design-it-yourself opportunity lapsed unanswered and Argus designed both experiments. One missed day proves nothing; three would be a pattern |
| 2026-07-12 | EXP-005 (rejected: decay is scale-proportional) | AI-led | Researcher requested "another cycle … with something else" and was otherwise absent. EXP-004 worksheet remains empty (day two of the lapse noted above); the reserved human-led slot held. Two prediction questions now await him: the EXP-004 worksheet and the EXP-005 digest's placebo-drift numbers |
| 2026-07-14 | EXP-006/007 (sample length rejected; cohort strengthening not supported) | AI-led | Researcher requested two more cycles; Argus selected, registered, implemented, and interpreted both. EXP-004's human-led gate remained untouched. |
| 2026-07-14 | Autonomous-lab policy, sandbox, lineage review, and EXP-004 | AI-led | Researcher explicitly removed worksheet gates and directed Argus to investigate arbitrage and keep testing. Argus designed and executed the spillover test and infrastructure; the intellectual contribution is therefore AI-led within a human-directed topic. |
| 2026-07-14 | EXP-008/009 and senior-quant review | AI-led | Researcher requested more cycles and an institutional-quality review; Argus selected, registered, executed, and judged both tests. |
| 2026-07-14 | Autonomous source-discovery pipeline and regime-filter sandbox | Human-directed | Researcher defined the autonomous-research objective and suggested Reddit/practitioner sources; Argus designed the evidence hierarchy, hypothesis queue, collector, and calibration probe. |
| 2026-07-15 | EXP-010 within-signal EW/VW decay | AI-led | Researcher requested another Argus cycle; Argus selected the queued priority, preregistered, executed, adversarially reviewed, and rejected it. |
| 2026-07-16 | EXP-011/012 search breadth and untouched confirmation | AI-led | Researcher requested a couple more cycles; Argus selected the queued methodological branch, reviewed the literature, preregistered both simulations, executed them, and bounded the interpretation. |
| 2026-07-16 | EXP-013 non-US publication-decay replication | AI-led | Researcher asked Argus to keep running while retaining focus; Argus acquired the JKP public global factor family, preregistered the external test before computing windows, executed it, and rejected transport of the strong US magnitude. |
| 2026-07-17 | EXP-014/015 coverage and US-inclusion bridge tests | AI-led | Researcher requested more cycles and delegated selection, design, execution, and interpretation. Argus rejected history truncation, found a preregistered US-inclusion pattern, and bounded it by the imprecise paired gap. |
| 2026-07-18 | EXP-016 standalone US JKP decay | AI-led | Researcher requested another cycle and repository update; Argus selected, preregistered, acquired, executed, and rejected the joint geography hypothesis on its paired inference rule. |
| 2026-07-21 | EXP-017 dependence-aware inference | AI-led | Researcher requested multiple cycles; Argus selected, preregistered, executed, and interpreted the covariance robustness test. |
| 2026-07-21 | EXP-018 publication-clock donut | AI-led | Argus selected and preregistered both donut widths before execution; researcher delegated design and interpretation. |
| 2026-07-21 | EXP-019 portfolio-breadth control | AI-led | Argus selected the observed composition proxy, fixed the linear specifications before execution, and bounded the result away from direct-trading claims. |

**Operating target:** research proceeds autonomously when the researcher is busy. Human input is welcomed but never required; contribution labels must continue to distinguish topic direction from hypothesis design and execution.
