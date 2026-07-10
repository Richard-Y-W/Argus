# 2026-07-10 — The first full research cycle

One day after founding, Argus ran a complete cycle autonomously at the researcher's request: literature → gap identification → registered hypothesis → experiment → honest write-up. The researcher chose the thread (anomaly decay, from his day-zero prior) but delegated execution — the Independent Thinking Index entry reflects that split: human direction, machine execution.

## What happened

- **Literature:** McLean & Pontiff (2016), Chen & Zimmermann (2022), Jacobs & Müller (2020) noted in `papers/`; synthesis with five identified gaps in `literature_reviews/2026-07-10-anomaly-decay.md`. The sharpest gap: post-publication decay is reliably US-only, which fits neither pure data mining nor frictionless arbitrage.
- **HYP-001 registered falsifiable ranges before any code existed.** This mattered psychologically as much as statistically: when the numbers landed (36.8% / 55.1% / 0.333), there was no temptation to reframe, because success had been defined in advance.
- **EXP-001 replicated M&P** on 212 open-source predictors through 2024: partial two-stage decay confirmed, all predictions in range, all six robustness specs agreeing. Full materials in `experiments/EXP-001-anomaly-decay/`.

## What was learned (repository)

The M&P pattern survives a decade more data and twice the predictors. Our post-sample decay (37%) matches Jacobs & Müller's US number, not M&P's 26% — predictor-set composition and window dating move that estimate materially, which is itself informative: "the" decay number is design-dependent. Unplanned: 2020–2024 partially revived published anomalies (panel ending 2019 shows 61% post-pub decay vs 55% through 2024). Parked, not interpreted.

## What was learned (process)

- C&Z data extends *before* each paper's sample start; the pre-sample category doesn't exist in M&P's design and had to be explicitly dropped. Silent inclusion would have contaminated the fixed effects. Lesson: **look at what's in the data beyond what the design names.**
- Annual publication dating attenuates the publication effect — predicted in the design doc before running, observed in the results. Predicting your bias's direction in advance is cheap and buys credibility.

## Open loop for the researcher

EXP-002 candidate is the placebo test (C&Z ships 114 placebo characteristics). The researcher was left with the question: *what should placebos do around their "publication" if decay is publication-caused?* His answer decides whether he designs EXP-002 himself — which would be the first researcher-designed experiment in the lab.

## Connections

`successful_experiments/EXP-001-anomaly-decay.md` · `hypotheses/HYP-001-decay-replication.md` · `questions/why-is-decay-us-only.md` · `researcher_scorecard.md` (updated)
