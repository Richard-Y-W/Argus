# EXP-006 — Results: sample length does not explain proportional decay

*Run 2026-07-14 from the registered design. Status: **HYP-006 rejected**. Data: C&Z October 2025, 212 predictors before the registered positive-mean floor; 208 in the primary cross-section.*

## Registered results

The primary coefficient of standardized log in-sample months on retention was +0.033 (HC3 se 0.037, t = 0.90), controlling for in-sample mean and publication year. **P1 fails.** Robustness estimates were +0.014 (winsorized), +0.047 (mean > 0.20), and +0.056 (clear-only), all |t| <= 1.31.

Sample-length terciles moved opposite to P2: short / middle / long histories retained 40.1% / 42.4% / 32.0% of their in-sample means. Long minus short = **−8.1 percentage points**, versus the registered prediction of at least +10. **P2 fails.**

The predictor-month FE triple interaction `post-publication × in-sample mean × log length` was −0.134 (se 0.078, t = −1.72). **P3 fails** in sign and significance. The underlying publication decay remains visible; this experiment only rejects sample length as its proposed discriminator.

## Interpretation

Calendar sample length supplies no evidence that the ~50% haircut is sampling-error shrinkage. This does not prove publication-induced arbitrage: months are not effective independent observations, length is endogenous to data availability and author choice, and the retention ratio is noisy. The honest update is narrower: the cheap discriminator proposed after EXP-005 did not work.

## Reproducibility

Run `python analysis.py`. Outputs: `results/cross_regressions.csv`, `terciles.csv`, `panel_regression.csv`, and `predictors.csv`. No resampling or manual exclusions beyond the registered rules.

## Researcher digest

The idea was simple: longer samples contain less luck, so they should shrink less. They did not. All controlled estimates were weak, and the long-sample group actually retained less. A plausible mechanism is not evidence until its unique prediction survives; this one did not.

## Connections

`hypotheses/HYP-006-sample-length.md` · EXP-005 · EXP-002 P4
