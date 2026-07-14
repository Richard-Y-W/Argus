# EXP-009 — Registered design: weighting and decay

*Registered 2026-07-14 before analysis.*

Reuse EXP-007 predictor-level construction. Primary sample requires in-sample mean > 0.10, at least 12 in-sample and post-publication months, and Stock Weight in EW/VW. HC3 OLS outcome is proportional decay; regressors are VW, standardized in-sample mean, publication year, and log post-publication months. Secondary HC3 OLS uses post-publication mean with the same controls. Robustness winsorizes proportional decay 5/95 and restricts to `1_clear` reproductions. Report group counts and raw means. This tests association, not causation or implementability.
