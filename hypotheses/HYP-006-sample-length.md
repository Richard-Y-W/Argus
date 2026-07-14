# HYP-006 — Does sample length separate shrinkage from publication correction?

*Registered 2026-07-14, before analysis. Attribution: AI-led.*

## Motivation and prior evidence

EXP-005 found that post-publication decay is approximately proportional to the in-sample mean. That pattern is consistent with both publication-induced arbitrage and statistical shrinkage. Sampling error falls with sample length, so the two accounts diverge if decay is compared across predictors with short and long original samples while holding in-sample scale fixed.

## Hypothesis and mechanism

If sampling error is an important source of the proportional haircut, shorter in-sample histories should have lower post-publication retention. Under a simple independent-observation heuristic, noise falls with the square root of months; publication correction has no equally direct sample-length prediction.

Alternatives: publication cohorts confound length; persistent signals may have shorter histories because their inputs are newer; serial dependence makes calendar months a poor effective-sample-size measure; original authors may use shorter subperiods selectively.

## Registered predictions

- **P1 (primary):** In a cross-predictor regression of retention (`post_pub_mean / in_sample_mean`) on log in-sample months, the coefficient is positive with |t| >= 2 after controlling for publication year and in-sample mean. To limit denominator pathologies, the primary sample requires in-sample mean > 0.10 %/month.
- **P2 (terciles):** Long-sample predictors retain at least 10 percentage points more than short-sample predictors.
- **P3 (levels diagnostic):** In a predictor-month FE regression containing post-publication × in-sample mean, the triple interaction with log sample length is positive with |t| >= 2.
- **Falsifier:** P1 and P3 both fail, or either is significantly negative. That rejects sample-length evidence for shrinkage; it does not prove arbitrage.

## Data, difficulty, and value

Chen–Zimmermann October 2025 predictor portfolios and SignalDoc, already pinned. Difficulty low; novelty modest; expected failure probability 55%. Publication value low alone, learning value high because it directly follows the lab's first rejection.

## Connections

`experiments/EXP-005-decay-heterogeneity/results.md` · `experiments/EXP-006-sample-length/design.md` · EXP-002 P4
