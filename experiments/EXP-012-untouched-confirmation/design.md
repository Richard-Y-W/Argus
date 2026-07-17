# EXP-012 — Registered design: consumed versus untouched holdout

*Registered 2026-07-16 before execution. AI-led.*

In 100,000 Monte Carlo runs, draw independent standard-normal train, validation, and confirmation statistics for 100 null candidates. Select the maximum training candidate. The leaky rule claims discovery when its validation z exceeds the fixed one-sided 5% cutoff. The confirmation rule claims discovery only when that same candidate also exceeds the cutoff on the untouched confirmation statistic.

Report leaky and confirmed false-claim rates, relative reduction, conditional confirmation share, and binomial Monte Carlo standard errors. Decision rules are fixed in HYP-012. The experiment measures null false claims only; it does not assess power, dependence, realistic returns, or adaptive researchers.

`analysis.py` writes `results/summary.csv` and `results/run_log.txt` deterministically.

## Connections

`hypotheses/HYP-012-untouched-confirmation.md` · White (2000) · Bailey et al. (2016) · EXP-011
