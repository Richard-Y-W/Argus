# EXP-011 — Registered design: search breadth under a known null

*Registered 2026-07-16 before execution. AI-led.*

For each of 20,000 runs, draw 200 independent standard-normal training z-statistics and 200 independent test z-statistics. For each K in 1, 5, 20, 50, and 200, select the largest training statistic among the first K candidates and carry that candidate's untouched test statistic forward. Report means, Monte Carlo standard errors, positive shares, and naive one-sided 5% pass shares.

P1 requires strict monotonicity of mean selected training z. P2 and P3 use the bounds registered in HYP-011. No alternative grid, seed, threshold, or subgroup will be introduced after execution. This is a stylized multiple-testing calibration, not a return simulation or market claim.

`analysis.py` writes `results/summary.csv` and `results/run_log.txt` deterministically.

## Connections

`hypotheses/HYP-011-search-breadth.md` · White (2000) · regime-filter sandbox
