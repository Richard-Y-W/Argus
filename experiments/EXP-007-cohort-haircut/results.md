# EXP-007 — Results: cohort strengthening is inconclusive

*Run 2026-07-14 from the registered design. Status: **HYP-007 not supported; mixed evidence, filed as failed rather than successful.** Primary cross-section n = 208.*

## Registered results

The primary standardized publication-year slope on proportional decay was **−0.151** (HC3 se 0.241, t = −0.63) after controlling for post-publication horizon and in-sample mean. This is insignificant and opposite the predicted sign. **P1 fails.** Winsorization gave +0.010 (t = 0.19); clear-only gave −0.291 (t = −0.53); the 0.20 denominator floor gave −0.166 (t = −0.67).

The registered cohorts were:

| Publication cohort | n | In-sample | Post-publication | Proportional decay | Mean post-pub months |
|---|---:|---:|---:|---:|---:|
| through 1989 | 12 | 0.755 | 0.345 | 49.0% | 513 |
| 1990–2000 | 36 | 0.737 | 0.459 | 34.9% | 340 |
| 2001+ | 160 | 0.692 | 0.265 | 68.5% | 192 |

Newest minus oldest = **+19.5 percentage points** (se 13.1, t = 1.50), so **P2 passes its magnitude-only rule**, weakly. P3 fails because winsorized and clear-only slopes do not both remain positive.

The registered 60-month equal-horizon diagnostic produced a positive year slope of +0.172 (se 0.070, t = 2.45). That is real supporting evidence, but it is a robustness result on a changed sample and cannot replace the failed primary.

## Interpretation

Recent predictors look worse in raw cohort means and in the equal-horizon sample, but no monotonic cohort effect survives the primary controls or the preregistered robustness set. The oldest bin has only 12 predictors, ratio outcomes have high variance, and cohort changes predictor composition. The correct conclusion is inconclusive heterogeneity, not a stronger modern arbitrage claim.

## Reproducibility

Run `python analysis.py`. Outputs: `results/regressions.csv`, `cohorts.csv`, `cohort_contrast.csv`, and `predictors.csv`.

## Researcher digest

This is a classic temptation: the newest cohort's 68.5% decay looks compelling beside the oldest cohort's 49.0%. But the controlled test—the one registered as primary—points the other way with huge uncertainty. A robustness test revives the story, so the question stays open; it does not earn a positive claim.

## Connections

`hypotheses/HYP-007-cohort-haircut.md` · EXP-003 · EXP-005 · EXP-006
