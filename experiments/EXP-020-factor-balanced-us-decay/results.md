# EXP-020 — Factor-balanced US publication decay is broad

## Verdict

**HYP-020 survives all registered rules.** Equal weighting across factors preserves both the magnitude and breadth of the US decay estimate.

## Results

Across 141 eligible factors, the equal-factor post-publication-minus-in-sample contrast is **-0.154 percentage points per month** (t = **-5.62**). The median is -0.163 pp/month, and **70.9%** of factor contrasts are negative. The interquartile range is -0.350 to +0.039 pp/month. The diagnostic post-publication-minus-post-sample mean is -0.149 pp/month (t = -3.90).

All three frozen rules pass: the mean is below -0.10, the cross-factor t-statistic is below -2.0, and negative breadth exceeds 55%. The non-negative-mean falsifier does not fire.

## Adversarial review

- Equal-factor summaries address unequal history length but discard differences in estimation precision.
- The conventional t-statistic treats factors as sampling units; correlated factor families can make it optimistic.
- A 70.9% negative share is broad but not universal, and the upper quartile is slightly positive.
- This robustness result does not observe trading, costs, flows, short interest, or price impact.

## Reproduction and connections

Run `python experiments/EXP-020-factor-balanced-us-decay/analysis.py`. HYP-020 · EXP-016 · EXP-021
