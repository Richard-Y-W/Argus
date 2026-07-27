# EXP-023 — Family-level inference rejects broad decay

## Verdict

**HYP-023 is rejected on every registered rule.** Family-aware inference does not support a broad negative decay contrast.

## Results

The equal-weight mean across 13 empirical families is **-0.0698 percentage points per month**, short of the -0.10 threshold. Eight of 13 family means are negative rather than the required nine. Exhaustive enumeration of all 8,192 sign assignments gives a two-sided exact **p = 0.2058**, above 0.05.

Family means span -0.339 to +0.200 pp/month. The largest 59-factor family is strongly negative, while a 24-factor family is positive (+0.157). This heterogeneity explains why equal-factor breadth and equal-family breadth tell different stories.

## Adversarial review

- This rejects the registered family-breadth claim, not the existence of a pooled negative association.
- Exact sign inference assumes family-level sign symmetry and has only 13 units.
- Cluster membership was learned without post-publication returns, but the 13-cluster partition remains one frozen empirical taxonomy.

## Reproduction and connections

Run EXP-022 first, then `python experiments/EXP-023-family-level-decay-inference/analysis.py`. HYP-023 · EXP-020 · EXP-022
