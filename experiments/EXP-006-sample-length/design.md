# EXP-006 — Registered design: sample length and proportional decay

*Registered 2026-07-14 before analysis. Implements HYP-006.*

## Sample and variables

Reuse EXP-001 filters: clear/likely predictors, no pre-sample observations, at least 12 in-sample and 12 post-publication months, panel through 2024. For each predictor compute in-sample mean, post-publication mean, and in-sample month count. Primary cross-section additionally requires in-sample mean > 0.10 to stabilize the retention denominator. Sample length is log months, standardized.

## Estimands

1. OLS across predictors: retention on standardized log sample length, standardized in-sample mean, and standardized publication year; HC3 standard errors.
2. Means by sample-length tercile, including retention and absolute decay.
3. Predictor-month fixed-effects OLS with month-clustered errors: post-sample and post-publication indicators; their interactions with in-sample mean; and post-publication × in-sample mean × standardized log length. Include the lower-order post-publication × log-length term.

## Robustness

- R1: retention outcome winsorized at 5th/95th percentiles.
- R2: require in-sample mean > 0.20.
- R3: clear reproductions only.
- R4: add calendar-era controls to the panel regression.

No model selection after results. P1–P3 are scored exactly as written in HYP-006. All return units are percent/month, as stored by C&Z.

## Leakage and limitations

All characteristics are measured using registered in-sample windows. Publication year is metadata, not estimated from returns. Sample length is not randomized and can proxy for cohort, data availability, or researcher choice; therefore even a pass is evidence consistent with shrinkage, not causal identification.

## Connections

`hypotheses/HYP-006-sample-length.md` · EXP-005 · EXP-003 era controls
