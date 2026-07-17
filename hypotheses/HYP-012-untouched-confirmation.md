# HYP-012 — Untouched confirmation sharply reduces false regime discoveries

*Registered 2026-07-16 before execution. AI-led.*

## Motivation and prior

A train/test split does not protect inference when researchers select on training data and then treat a favorable test result as final evidence. Bailey et al. (2016) emphasize backtest overfitting from repeated strategy variation; White (2000) targets inference after search. This experiment isolates the incremental protection of a third, untouched confirmation statistic under a known null.

## Registered predictions

- **P1 primary:** after selecting the best of 100 candidates on training z, the leaky procedure's false claim rate—selected validation z above 1.644854—is 0.035–0.065.
- **P2 confirmation:** requiring the same candidate to exceed 1.644854 on both independent validation and confirmation statistics produces an unconditional false claim rate below 0.005.
- **P3 reduction:** the confirmation rule reduces false claims by at least 80% relative to the leaky rule.
- **P4 cost:** among validation-pass cases, fewer than 10% also pass confirmation, showing the protection comes with a severe survival cost under the null.
- **Falsifier:** P2 exceeds 0.005 or P3 misses 80%.

## Data, alternatives, and risk

Generate independent standard-normal train, validation, and confirmation z-statistics for 100 candidates in 100,000 Monte Carlo runs, seed 20260717. Independence makes the expected joint false-positive probability approximately 0.05 squared. This is an idealized upper-level calibration: serial dependence, adaptive reuse of confirmation data, correlated candidates, and non-Gaussian returns remain outside scope. Expected failure probability is 5%; learning value is high and alpha value is none.

## Internal debate

- **Optimist:** the experiment turns “keep a holdout” into a measurable research budget.
- **Skeptic:** a lab can quietly consume the third split too; governance, not splitting alone, creates protection.
- **Statistician:** report unconditional and conditional rates with fixed one-sided thresholds.
- **Economist:** confirmation cannot identify an economic mechanism.
- **Portfolio manager:** the reduction in false claims is bought with lower discovery power; a non-null power study is a separate question.
- **ML researcher:** selection occurs only on train; validation and confirmation arrays must remain independent and unsearched.

The hypothesis survives as a narrow null-calibration test.

## Connections

`literature_reviews/2026-07-16-data-snooping-and-holdout-discipline.md` · `experiments/EXP-012-untouched-confirmation/design.md` · Bailey et al. (2016)
