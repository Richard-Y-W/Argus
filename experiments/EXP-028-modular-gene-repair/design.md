# EXP-028 — Registered design: modular gene repair

**Registered:** 2026-08-03 before parsing return outcomes  
**Stage:** historical mechanism confirmation with later-vintage check  
**Attribution:** Human-directed

## Data and timing

Use the official French five-industry value-weighted daily returns. Fit only on the trailing 252 observations available before each calendar-month rebalance. The frozen December 2024 archive supplies all history through 2024. Primary confirmation is 2015-01-01 through 2024-12-31. The current file supplies only 2025-01-01 onward as a separately reported later-vintage check.

## Genome and phenotype

The genome is five real logits; softmax maps it to long-only, fully invested industry weights. The phenotype is the realized weight vector. Initial weights are equal. Fitness on the lagged window is annualized certainty-equivalent return, `252*mean - 1.5*252*variance`, minus 10 basis points per unit one-way turnover from the incumbent.

## Equal-budget treatments

At each rebalance every stochastic treatment evaluates the incumbent plus 63 new candidates:

1. `localized`: calculate a lagged damage score for every industry from the absolute 63-day versus preceding-189-day mean shift, standardized by pooled standard error, plus the absolute log-volatility shift. Transfer a uniformly drawn feasible amount of weight between only the two highest-scoring industries; the other three weights remain exactly fixed. This pre-execution implementation choice avoids softmax normalization contaminating nominally unchanged genes.
2. `all_gene`: mutate all five incumbent logits with the same Normal(0, 0.35) marginal noise.
3. `random`: draw 63 weights from Dirichlet(1,1,1,1,1).

`min_variance` is the deterministic conventional baseline: long-only SLSQP minimum variance on the same 252-day window. `equal_weight` is a non-adaptive reference. All realized strategies pay 10 basis points per unit one-way turnover at the first observation after rebalancing.

Seeds are method- and rebalance-specific and frozen at 28032026. Candidate sets are not shared.

Pre-execution deviation: the first implementation proposed two-logit Normal mutations, but a unit-test review showed softmax normalization would move all five phenotype weights. Before parsing any outcomes, the localized operator was replaced by the two-industry weight transfer above. No endpoint or observed return informed this correction.

Schema deviation: the first loader expected `Hlth` without padding, while the official CSV header contains `Hlth `. Execution stopped before return parsing or results. The loader now strips header whitespace; the sample and analysis are unchanged.

## Outcomes

Aggregate daily net returns to calendar months. Primary endpoint is monthly realized certainty equivalent, `monthly return - 1.5*monthly variance`. Secondary outcomes are cumulative net log return, annualized volatility, 5% historical expected shortfall, turnover, maximum drawdown, and fraction of months in which localized certainty equivalent exceeds each comparator.

Use 10,000 paired moving-block bootstrap resamples of monthly differences with 12-month circular blocks. Report percentile 95% intervals.

## Registered decision rule

Classify this implementation as `SUPPORTED WITH LIMITS` only if, in 2015–2024:

- localized minus all-gene mean monthly certainty equivalent has a 95% interval strictly above zero;
- localized minus random mean monthly certainty equivalent has a 95% interval strictly above zero;
- localized expected shortfall is no worse than the better of all-gene and random by more than 10%; and
- localized turnover is lower than all-gene turnover.

If any condition fails, classify `NOT SUPPORTED` or `INCONCLUSIVE` according to interval width. Minimum variance and equal weight are interpretation baselines, not part of the joint pass rule; if either clearly dominates localized, practical potential must be described as weak even if the joint rule passes.

The 2025+ check cannot rescue a failed primary rule and receives no parameter tuning.

## Risks and limits

Five industries are a coarse, coupled decomposition. French portfolios are revised research series, gross of implementation frictions beyond the stated stylized cost, and not directly tradable. One US history does not identify biological mechanism, capacity, or alpha. The experiment has three planned stochastic contrasts but one joint claim; all contrasts are reported.

## Connections

`hypotheses/HYP-028-modular-financial-gene-repair.md` · `datasets/french_5_industry_daily.md` · EXP-027
