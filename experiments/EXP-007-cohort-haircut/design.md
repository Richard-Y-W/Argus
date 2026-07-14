# EXP-007 — Registered design: cohort stability of proportional decay

*Registered 2026-07-14 before analysis. Implements HYP-007.*

## Sample

Use the same predictor construction and minimum-window rules as EXP-006. Primary predictor-level sample requires in-sample mean > 0.10 %/month. Compute proportional decay and post-publication months from data available through December 2024.

## Estimands

1. HC3 OLS: proportional decay on standardized publication year, log post-publication months, and standardized in-sample mean.
2. Registered cohort table for <=1989, 1990–2000, and 2001+: count, in-sample mean, post-publication mean, proportional decay, and post-publication months.
3. Newest-minus-oldest difference with a heteroskedastic two-sample standard error.

## Robustness

- R1: winsorize proportional decay at 5th/95th percentiles.
- R2: clear reproductions only.
- R3: denominator floor 0.20 %/month.
- R4: equalize horizon by recomputing each post-publication mean from its first 60 available months, requiring 60 months.

The horizon-equalized estimate is diagnostic because it changes both composition and horizon. It cannot silently replace the primary estimate.

## Interpretation limits

Publication cohort is observational and entangled with predictor composition. Recent cohorts are right-truncated. Controls and R4 address obvious manifestations but do not create causal identification.

## Connections

`hypotheses/HYP-007-cohort-haircut.md` · EXP-003 · EXP-005
