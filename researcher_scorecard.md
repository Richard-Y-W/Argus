# Researcher Scorecard

*Living document. Updated after every meaningful research cycle. Tracks long-term growth, not short-term productivity.*

**Researcher:** Richard
**Started:** 2026-07-09
**Last updated:** 2026-07-09 (baseline set from self-report; unverified until module mastery checks)

---

## Baseline (self-reported 2026-07-09)

Solid undergrad core: comfortable with calculus, linear algebra, and probability; limited exposure to econometrics and time series. Levels below are **self-reported and unverified** — each will be confirmed or corrected by the mastery checks in `learning_notes/foundations_curriculum.md`. Data access: free sources (Ken French, FRED, Yahoo) plus academic WRDS/CRSP/Compustat.

First phase chosen by the researcher: **foundations first** (Modules 1–5), capstone = replication of the stylized facts of asset returns (Cont 2001).

## Literature

| Metric | Count | Notes |
|--------|-------|-------|
| Papers read | 0 | |
| Papers fully understood | 0 | "Fully understood" = could re-derive the core result and explain it to a skeptic |
| Papers replicated | 0 | |
| Landmark papers mastered | 0 | See `papers/landmark_reading_list.md` once created |
| Research areas explored | 0 | |

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
| Negative results documented | 0 |
| Statistical mistakes caught before execution | 0 |

## Scientific Judgment — Milestone Log

Record dated, concrete examples where the researcher: changed their mind after evidence; rejected an exciting but weak idea; identified overfitting; caught leakage; recognized publication bias; improved an experimental design; connected unrelated literature; generated an original research question.

- **2026-07-09 — First committed pre-literature prediction.** Before reading McLean & Pontiff (2016), predicted the three-window return pattern for published anomalies. Got the story-1 timeline right; blended overfitting (story 2's explanation) with persistence (story 1's prediction) in one answer, and picked the wrong discriminating window (post-publication instead of post-sample-pre-publication). Lesson extracted: *each candidate mechanism must generate its own full set of predictions — a hypothesis is a row in a table, not a single timeline.* Details in `ideas/2026-07-09-anomaly-decay-prior.md`.

## Independent Thinking Index

Estimate: what fraction of the current research direction originates from the human?

| Date | Human-originated direction | Evidence |
|------|---------------------------|----------|
| 2026-07-09 | ~0% (day zero) | Repository initialized by Argus from the charter |
| 2026-07-09 (later) | ~15% | Researcher redirected the first cycle away from the math curriculum toward his own question (anomaly decay) and committed to falsifiable predictions before reading the literature |
