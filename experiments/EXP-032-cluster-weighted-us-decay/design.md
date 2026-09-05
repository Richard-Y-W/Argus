# EXP-032 - Cluster-weighted US publication decay

## Stage and boundary

Stage: dependent robustness audit. Attribution: AI-led.

This experiment was registered on 2026-09-05 before computing its outputs, but after the underlying EXP-020 factor contrasts and EXP-022 dependence clusters were already known to the repository. It can test the robustness of prior language about breadth; it cannot provide untouched confirmation of a market effect.

## Estimand

The estimand is the equal-weighted mean across 13 pre-publication dependence clusters of each cluster's average post-publication-minus-in-sample factor contrast, measured in percentage points per month.

## Inputs

- `experiments/EXP-020-factor-balanced-us-decay/results/factor_contrasts.csv`
- `experiments/EXP-022-effective-factor-breadth/results/assignments.csv`

No raw JKP files are required for this audit. That is a limitation, not a feature: the analysis inherits every eligibility, parsing, and publication-clock choice embedded in the archived upstream outputs.

## Decision rule

P1: equal-cluster mean <= -0.10 pp/month.

P2: conventional cluster-level t-statistic <= -1.65.

P3: negative cluster share >= 70%.

Falsifier: equal-cluster mean >= 0.

The hypothesis survives only if P1, P2, and P3 all pass and the falsifier does not fire.

## Leakage and dependence

Cluster assignments were estimated from pre-publication returns in EXP-022, so they do not use post-publication outcomes directly. However, the archived artifacts and prior family-influence conclusions have already been inspected. The result must be described as a stress test of interpretation, not a fresh discovery.

## Connections

HYP-032 - EXP-020 - EXP-022 - EXP-024
