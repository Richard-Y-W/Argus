# EXP-011 — Search breadth under a known null

## Verdict

**HYP-011 survives within its simulation scope.** All three registered predictions passed. This is evidence about a stylized research process, not about market regimes or expected returns.

## Results

Across 20,000 Monte Carlo runs, the mean selected training z-statistic rose strictly from 0.013 at K=1 to 2.751 at K=200. The naive one-sided 5% pass share rose from 5.36% to 99.99%. Thus, trying 200 independent null variants made a conventionally “significant” winner almost certain.

The selected candidate's independent test statistic did not move with search breadth. Mean test z ranged from -0.012 to 0.010, positive shares ranged from 49.50% to 50.20%, and naive test pass shares remained near 5%. P1, P2, and P3 all pass.

## Adversarial review and limitations

- The result is mechanically expected from order statistics; its value is calibration, not novelty.
- Candidate statistics are independent Gaussian draws. Real variants are correlated, returns are non-Gaussian, and search is adaptive. Correlation can reduce the effective number of trials; adaptive reuse can worsen the problem.
- An untouched test sample diagnoses the selected null candidate here because it is truly untouched. Calling a repeatedly inspected dataset “out of sample” would invalidate the comparison.
- No economic mechanism, costs, forecasting ability, or alpha was tested.

## What was learned

Search breadth is part of the statistical design. A z-statistic cannot be interpreted without the number and dependence of variants that competed to produce it. EXP-012 tests the governance implication: whether another untouched confirmation layer materially lowers false claims.

## Reproduction

Run `python experiments/EXP-011-search-breadth/analysis.py`. Fixed seed: 20260716. Outputs are in `results/`.

## Connections

`hypotheses/HYP-011-search-breadth.md` · `literature_reviews/2026-07-16-data-snooping-and-holdout-discipline.md` · EXP-012 · White (2000)
