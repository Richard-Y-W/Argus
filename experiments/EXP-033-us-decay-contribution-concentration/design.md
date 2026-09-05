# EXP-033 - Dependence-cluster contribution concentration

## Stage and boundary

Stage: dependent robustness audit. Attribution: AI-led.

This experiment audits whether the archived equal-factor US publication-decay estimate is concentrated in one dependence cluster. It reuses inspected artifacts and therefore cannot establish an independent empirical claim.

## Estimand

For each EXP-022 cluster, compute:

- factor count;
- cluster mean post-publication-minus-in-sample contrast;
- cluster sum of factor contrasts;
- share of the signed negative total; and
- share of absolute contribution mass.

The primary question is concentration, not coefficient magnitude.

## Inputs

- `experiments/EXP-020-factor-balanced-us-decay/results/factor_contrasts.csv`
- `experiments/EXP-022-effective-factor-breadth/results/assignments.csv`

## Decision rule

P1: maximum signed negative contribution share <= 40%.

P2: top-two absolute contribution share <= 60%.

P3: every leave-one-cluster-out equal-factor mean <= -0.10 pp/month.

Falsifier: maximum signed negative contribution share >= 70%.

The hypothesis survives only if P1, P2, and P3 all pass and the falsifier does not fire.

## Interpretation limits

The concentration ledger can downgrade breadth language but cannot adjudicate why a cluster decays. Factor construction, publication timing, and eligibility are inherited from prior JKP work.

## Connections

HYP-033 - EXP-020 - EXP-022 - EXP-024
