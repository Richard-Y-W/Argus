# Data snooping and holdout discipline

## Question

Why do regime filters and strategy variants look persuasive after search, and what does an untouched confirmation sample actually buy?

White (2000) defines data snooping as reusing a dataset for model selection or inference and develops a test of whether the best model found in a specification search beats a benchmark. Hansen (2005) refines this family of tests for superior predictive ability. Bailey et al. (2016) frame backtest overfitting as repeated strategy variation on one historical record and emphasize that ordinary holdout language is insufficient if the holdout is itself consumed by selection.

The immediate Argus gap is narrower than implementing those full corrections. The queued regime-filter sandbox showed that the best of 50 independent noise filters nearly always looks positive in-sample. It did not map the distortion against search breadth, and it did not quantify the protection from requiring a second, genuinely untouched confirmation sample.

## Two registered gaps

1. **Search breadth calibration:** under a known null, estimate how the selected in-sample statistic and naive false-discovery rate change from 1 to 200 tried variants, while checking that an independent test statistic remains centered at zero.
2. **Holdout consumption:** compare reporting a favorable validation result after train-sample selection with requiring the same selected candidate to pass both validation and an untouched confirmation split.

These are simulation studies about research procedure, not market evidence. Independent Gaussian candidate statistics are deliberately favorable: real strategies share returns, have heavy tails, and are often searched adaptively. The experiments therefore isolate multiplicity and holdout reuse rather than claim realistic backtest-overfitting rates.

## Sources

- White, H. (2000), “A Reality Check for Data Snooping,” *Econometrica* 68(5), 1097–1126, DOI 10.1111/1468-0262.00152.
- Hansen, P. R. (2005), “A Test for Superior Predictive Ability,” *Journal of Business & Economic Statistics* 23(4), 365–380, DOI 10.1198/073500105000000063.
- Bailey, D. H., Borwein, J. M., López de Prado, M., Salehipour, A., and Zhu, Q. J. (2016), “Backtest Overfitting in Financial Markets,” UC eScholarship.

## Connections

`engineering/sandbox/2026-07-14-regime-filter-mining/` · `hypotheses/HYP-011-search-breadth.md` · `hypotheses/HYP-012-untouched-confirmation.md`
