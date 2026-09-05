# EXP-032 - Cluster-weighted US publication decay is not broad enough

## Verdict

**HYP-032 is rejected.** The archived US decay estimate does not survive equal weighting across EXP-022 dependence clusters.

## Results

Across 13 pre-publication dependence clusters covering 141 factors, the equal-cluster post-publication-minus-in-sample mean is **-0.070 percentage points per month**. The conventional cluster-level t-statistic is **-1.34**, and 8 of 13 clusters are negative (**61.5%**).

All three registered survival rules fail: the mean is not below -0.10 pp/month, the t-statistic is not below -1.65, and negative cluster breadth is below 70%. The non-negative-mean falsifier does not fire.

## Adversarial review

- This is dependent evidence because the analysis reuses already inspected EXP-020 and EXP-022 artifacts.
- The result does not overturn the archived equal-factor mean; it overturns the stronger claim that the estimate is broad across independent-ish factor families.
- Cluster construction is itself an estimate from pre-publication returns. Thirteen clusters are too few to support precise distributional inference.
- The audit still observes returns only. It says nothing direct about publication arbitrage, crowding, costs, capacity, flows, or implementation.

## What changed

The appropriate language is now: US publication decay is a robust archived factor-level association, but its breadth is materially weaker once dependence clusters are treated as the unit of evidence.

## Reproduction and connections

Run `python experiments/EXP-032-cluster-weighted-us-decay/analysis.py`. HYP-032 - EXP-020 - EXP-022 - EXP-024 - EXP-033
