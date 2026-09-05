# HYP-032 - US publication decay survives equal dependence-cluster weighting

*Registered 2026-09-05 before computing EXP-032 outputs. AI-led.*

## Motivation and prediction

EXP-020 showed a negative equal-factor post-publication-minus-in-sample contrast, but EXP-022/024 showed that nominal factors are strongly dependent and that one large cluster carries much of the equal-factor estimate. If the US publication-decay pattern is broad across empirically inferred dependence families, then weighting each pre-publication cluster equally should retain a materially negative average.

P1: the equal-cluster mean contrast is at most -0.10 percentage points per month. P2: the conventional cluster-level t-statistic is at most -1.65. P3: at least 70% of cluster means are negative. Survival requires all three. A non-negative equal-cluster mean is a falsifier.

## Alternatives and limits

Failure would not erase the factor-level return pattern; it would show that the broadness interpretation is not robust to dependence-cluster weighting. The cluster labels were learned in EXP-022 from pre-publication returns, but the experiment still reuses already inspected EXP-020/022 artifacts. It is therefore a dependent robustness audit, not untouched confirmation.

## Data, debate, and value

Inputs are archived `experiments/EXP-020-factor-balanced-us-decay/results/factor_contrasts.csv` and `experiments/EXP-022-effective-factor-breadth/results/assignments.csv`. The Optimist expects the negative pattern to remain visible across clusters; the Skeptic expects a few accounting/liquidity clusters to dominate; the Statistician treats 13 clusters as the sampling unit; the Economist rejects causal trading interpretation; the Portfolio Manager notes that costs, capacity, and flows remain unobserved.

## Connections

EXP-020 - EXP-022 - EXP-024 - `experiments/EXP-032-cluster-weighted-us-decay/design.md`
