# EXP-014 — Registered design: coverage-matched US publication decay

*Registered 2026-07-17 before restricted-window outcomes were computed. AI-led.*

Load the pinned C&Z predictor panel using EXP-001's published-predictor, window, and panel-end definitions. Estimate the full-history benchmark and two restrictions beginning 1986-01 and 1990-01. Apply each floor before requiring at least 12 in-sample and 12 post-publication months. Estimate within-predictor post-sample and post-publication coefficients with month-clustered covariance. Repeat the 1986 restriction for `Predictability in OP == 1_clear`.

`analysis.py` writes estimates, eligibility flow, verdicts, and a deterministic run log. No alternative floor, subgroup, or window rule will be added after observing results.

## Connections

`hypotheses/HYP-014-coverage-matched-us-decay.md` · EXP-001 · EXP-013
