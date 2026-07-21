# EXP-017 — US decay survives factor-and-month clustered inference

## Verdict

**HYP-017 survives its registered joint rule.** Both predictions pass and the falsifier does not fire.

## Results

On the frozen 141-factor, 101,920-observation EXP-016 sample, the point estimate remains **-0.164 pp/month**. Two-way clustering by factor and calendar month gives t = **-2.92**, versus -2.97 with month clustering alone. Post-publication minus post-sample is **-0.191 pp/month** with t = **-3.03**. P1 and P2 pass.

## Adversarial review

- Two-way clustering addresses persistent within-factor errors and common monthly shocks, but not uncertainty in factor discovery or publication dates.
- The near-identical standard error is an empirical result, not permission to use weaker covariance estimators elsewhere.
- Factor portfolios overlap, so arbitrary higher-order cross-factor dependence may remain.
- This strengthens inference about a return pattern only; no trading quantity, causal mechanism, cost, or capacity is observed.

## Reproduction and connections

Run `python experiments/EXP-017-dependence-aware-us-decay/analysis.py` against the pinned JKP files. HYP-017 · EXP-016 · EXP-018 · EXP-019
