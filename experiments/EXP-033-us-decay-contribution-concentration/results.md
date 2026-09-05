# EXP-033 - Equal-factor US decay is contribution-concentrated

## Verdict

**HYP-033 is rejected.** The archived equal-factor US publication-decay estimate is dominated by one dependence cluster.

## Results

The full archived equal-factor mean is **-0.1535 percentage points per month**. Cluster 2, a 59-factor dependence family, contributes **92.5%** of the signed negative total. Omitting that cluster weakens the retained equal-factor mean to **-0.0198 pp/month**.

The registered rules split sharply. P2 passes because the top two absolute cluster contributions account for **58.1%** of absolute contribution mass, below the 60% threshold. P1 fails because the largest signed contribution exceeds 40%. P3 fails because at least one leave-one-cluster estimate is not below -0.10 pp/month. The 70% dominance falsifier fires.

## Adversarial review

- The concentration result is not an independent market test. It is an accounting ledger over archived EXP-020/022 outputs.
- Signed contribution shares can be large when positive clusters offset negative clusters. That is part of the point: the equal-factor mean is not a diffuse consensus across clusters.
- The result is consistent with EXP-024 and gives a clearer denominator for the concentration objection.
- No trading, crowding, or capacity mechanism is identified.

## What changed

Single-factor deletion stability was too weak a breadth diagnostic. A large correlated family can make every one-factor deletion look stable while still dominating the total signed estimate.

## Reproduction and connections

Run `python experiments/EXP-033-us-decay-contribution-concentration/analysis.py`. HYP-033 - EXP-020 - EXP-022 - EXP-024 - EXP-032
