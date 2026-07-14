# EXP-004 — Registered design: placebo spillover from published predictors

*Registered 2026-07-14 before analysis. Implements HYP-004.*

## Data and timing

Use pinned C&Z placebo and predictor LS portfolios through 2024 plus SignalDoc dates. Apply the EXP-002 placebo quality/date filters and require at least 12 in-sample and 12 post-publication placebo months.

For each placebo, estimate correlations during the 60 months ending December of the year before its publication. Candidate predictors must have publication year strictly earlier than the placebo's year and at least 36 overlapping monthly returns. Primary exposure is the signed correlation of the predictor with the largest absolute correlation. Record its identity and estimation n. Requiring the predictor to be public before the measurement cutoff blocks future-strategy leakage.

## Outcomes and estimators

The predictor-level outcome is placebo post-publication mean minus in-sample mean. Primary HC3 OLS uses standardized exposure plus standardized in-sample mean, publication year, and correlation-estimation months. Terciles use signed exposure.

Negative-control exposure repeats the same selection against predictors published strictly after the placebo. It is structurally related but unavailable to contemporaneous arbitrageurs.

Robustness uses (a) a 120-month window with at least 60 overlaps and (b) correlation with the equal-weighted return of already-published predictors, requiring at least five available predictors per month and 36 months.

## Interpretation limits

This is an exposure design, not holdings evidence. Maximum-correlation selection is noisy and creates winner's-curse magnitude. Shared factors can make the negative control fire. Any positive result is “consistent with spillover,” not causal proof of arbitrage trading.

## Outputs

`exposures.csv`, `regressions.csv`, `terciles.csv`, and a deterministic run log. No plot is required for scoring.

## Connections

`hypotheses/HYP-004-placebo-spillover.md` · EXP-002 · EXP-003 · publication-arbitrage lineage
