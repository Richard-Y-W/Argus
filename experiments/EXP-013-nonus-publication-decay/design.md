# EXP-013 — Registered design: non-US publication decay

*Registered 2026-07-16 before publication-window outcomes were computed. AI-led.*

## Sample construction

Read the JKP public `[all_regions]_[all_factors]_[monthly]_[vw]` file and official `factor_details.xlsx`. Retain named factors with a nonmissing `abr_jkp`, parse the first and final four-digit years in `in-sample period` as sample start/end, and parse the final parenthesized four-digit year in `cite` as publication year. Drop metadata rows with ambiguous or missing years, duplicate `abr_jkp`, publication before sample end, or no return match.

For each location, drop observations before sample start. Assign sample-start through sample-end years to `in_sample`, later years through publication year to `post_sample`, and subsequent years to `post_pub`. Require at least 12 in-sample and 12 post-publication months per factor-location. Returns are decimal monthly signed long–short returns; reported coefficients are multiplied by 100 to percentage points.

## Estimation and decision rules

For `world_ex_us`, estimate return on post-sample and post-publication indicators with factor fixed effects. Compute within-factor coefficients and month-clustered covariance using the canonical Argus clustered OLS helper where compatible; otherwise implement and test the same sandwich formula locally. P1 uses the post-publication coefficient. P2 uses the post-publication-minus-post-sample contrast.

Repeat the panel estimator separately for developed and emerging locations for P3. For P4, calculate factor window means and the share with `post_pub - in_sample < 0`. P5 includes (a) the primary panel restricted to metadata `significance == 1`, and (b) factor-level OLS of window changes on an intercept with HC3 covariance, giving every factor equal weight. No calendar-era adjustment is added in this first external replication because the primary question is transport of the registered three-window pattern; calendar decomposition is a successor only if the primary survives.

## Bias controls and outputs

No factor direction is chosen from realized returns. The JKP construction signs factors from original-paper direction. The locations, release, weighting, thresholds, estimators, and decision rules are fixed before execution. No subgroup, alternative year parser, horizon balance, winsorization, or factor exclusion will be added to rescue a result.

`analysis.py` deterministically writes metadata flow, panel estimates, factor window means, verdicts, and a run log under `results/`.

## Connections

`hypotheses/HYP-013-nonus-publication-decay.md` · `datasets/jkp_global_factors_2025.md` · EXP-001 · EXP-003
