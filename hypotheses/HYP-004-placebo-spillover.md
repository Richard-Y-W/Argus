# HYP-004 — Predictor-correlated placebos inherit publication decay

*Registered 2026-07-14 before analysis. Attribution: AI-led under the autonomous-lab policy.*

## Mechanism

Published predictor rules attract long–short capital. A placebo portfolio built from overlapping accounting or price ingredients can covary with those trades even though its own paper did not claim predictability. If the placebo and an already-public predictor were positively related before the placebo's publication, correction of the predictor should lower the placebo return in its signed direction; a negative relationship predicts the opposite.

## Alternatives

Common factor exposures, shared construction inputs, a calendar trend, noisy correlation selection, and annual publication dating can generate or obscure the pattern. Correlation is not proof of common positions. Publication dates for predictors, not actual adoption dates, proxy the available strategy set.

## Registered predictions

- **P1 primary:** The placebo post-publication change loads negatively on signed pre-publication predictor exposure: coefficient <= −0.05%/month per exposure standard deviation with t <= −2 after controlling for placebo in-sample mean, publication year, and exposure-estimation months.
- **P2 terciles:** High positive-exposure placebos decline at least 0.10%/month more than low/negative-exposure placebos.
- **P3 negative control:** Exposure measured against predictors published only after the placebo publication does not explain placebo decay (|t| < 2). If it does, the exposure design is detecting shared structure or look-ahead-like composition, not publication spillover.
- **P4 robustness:** P1 remains negative under a 120-month exposure window and when exposure is the correlation with an equal-weighted composite of already-published predictors.
- **Falsifier:** P1 fails and either P2 fails or P3 fires. That rejects this implementation of the spillover mechanism.

## Value and failure probability

Difficulty moderate, novelty moderate, expected failure probability 60%. Publication value is modest alone; learning value is high because it tests a missing link in the lab's causal chain. Practical value is low without holdings or transaction-cost data.

## Connections

EXP-002 placebo drift · EXP-003 event clock · EXP-005 scale result · `literature_reviews/2026-07-14-publication-arbitrage-lineage.md`
