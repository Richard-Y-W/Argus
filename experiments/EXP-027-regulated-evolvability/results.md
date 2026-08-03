# EXP-027 results — Regulated evolvability

## Classification

**NOT SUPPORTED.** The observable environmental-distance gate failed all five registered predictions. It identified the largest correlation break but did not reliably distinguish changes by their relevance to the financial genome, beat any fixed search policy, or control tail loss.

## Data boundary

Every return in EXP-027 is synthetic. The code generates multivariate AR(1) paths from parameters frozen in `design.md` and `analysis.py`. No equity, bond, commodity, cryptocurrency, PLEX, broker, exchange, or vendor market return enters this experiment. The result is a computational mechanism test and cannot support a historical-performance or alpha claim.

## Registered outcomes

Twenty-four untouched paths—six in each of four new structural families—were evaluated. Each method tested exactly 576 new genomes per path.

| Prediction | Estimate or diagnostic | 95% family-stratified paired interval | Result |
|---|---:|---:|---|
| P1: gate minus local evolution | 0.00598 | [-0.00828, 0.01989] | **Fail** |
| P2: gate minus global random | -0.00273 | [-0.01292, 0.00722] | **Fail** |
| P3: gate minus fixed hybrid | -0.00116 | [-0.01221, 0.00969] | **Fail** |
| P4: strict global-route ordering | 0, 0, 0, 0.806 | — | **Fail** |
| P5: gate ES minus best fixed ES | 0.1863 | threshold <= 0.05 | **Fail** |

The global-route sequence corresponds to small drift, moderate rotation, mean reversion, and correlation break. Mean observed distances were 1.013, 1.264, 1.745, and 2.801 respectively. The continuous score increased with intended severity, but the fixed thresholds did not create the registered strict route ordering.

## Family diagnostics

| Family / method | Full return | Early return | Volatility | Annualized 5% ES | Turnover |
|---|---:|---:|---:|---:|---:|
| Small drift / evolution | -0.0052 | -0.0017 | 0.0715 | 2.5207 | 27.63 |
| Small drift / random | -0.0103 | -0.0099 | 0.0678 | 2.3957 | 26.52 |
| Small drift / hybrid | -0.0028 | -0.0065 | 0.0705 | 2.4628 | 30.61 |
| Small drift / gate | 0.0098 | -0.0058 | 0.0736 | 2.5599 | 36.96 |
| Moderate rotation / evolution | -0.0034 | 0.0081 | 0.0619 | 2.1775 | 24.84 |
| Moderate rotation / random | 0.0097 | 0.0128 | 0.0664 | 2.2488 | 24.13 |
| Moderate rotation / hybrid | 0.0021 | 0.0097 | 0.0655 | 2.2820 | 26.42 |
| Moderate rotation / gate | -0.0049 | 0.0076 | 0.0674 | 2.3979 | 28.02 |
| Mean reversion / evolution | -0.0182 | -0.0067 | 0.0733 | 2.5065 | 26.76 |
| Mean reversion / random | 0.0119 | 0.0035 | 0.0803 | 2.7572 | 23.82 |
| Mean reversion / hybrid | 0.0153 | 0.0100 | 0.0802 | 2.7810 | 21.88 |
| Mean reversion / gate | 0.0074 | 0.0092 | 0.0847 | 2.8902 | 23.45 |
| Correlation break / evolution | 0.0306 | 0.0322 | 0.0792 | 2.7326 | 14.96 |
| Correlation break / random | 0.0273 | 0.0309 | 0.0840 | 2.8955 | 15.97 |
| Correlation break / hybrid | 0.0178 | 0.0261 | 0.0776 | 2.7522 | 14.70 |
| Correlation break / gate | 0.0155 | 0.0261 | 0.0810 | 2.8344 | 15.17 |

## Mechanism interpretation

The distance score detected statistical distribution change, not the value of inheritance to the portfolio optimizer. Those are different estimands. A large correlation change does not imply that global restart is optimal, while a moderate persistence change may destroy a trend genome even if its omnibus z-distance is smaller.

The gate also pays switching and search variance. In small drift it achieved the highest full return but the highest turnover. In correlation break it routed mostly global even though local evolution had the highest mean return. This directly contradicts the proposed monotone mapping from raw environmental distance to useful mutation radius.

## Strongest adversarial interpretation

The experiment imposed an arbitrary Euclidean aggregation of twelve noisy statistics and two uncalibrated thresholds. It then asked this generic distribution-change score to solve a decision problem: estimate the relative value of local versus global search. The score contains no model of how each environmental component interacts with the genome's phenotype. Failure is therefore unsurprising.

The opposite objection also matters: only six paths per family produce wide performance intervals. The run can reject the registered joint claim and the fixed gate, but it cannot establish that every decision-aware gate is useless.

## Anti-overfitting decision

Do not adjust 1.25/2.50 thresholds, component weights, windows, or family definitions on EXP-027 outcomes. EXP-025–027 have consumed their synthetic families. Three consecutive rejected joint hypotheses trigger a program-level pause on further tuning within this simulator class.

Any successor must change the evidence source, not merely the hyperparameters. Two defensible routes remain:

1. a new externally specified simulator or benchmark where the loss of inheritance is defined independently of Argus's return generator; or
2. historical point-in-time validation across liquid multi-asset data, with rolling-origin splits, untouched eras, realistic costs, and standard adaptive baselines.

## Verification

- Four tests passed: causal and finite distance, threshold routing, deterministic distinct families, and equal candidate/hybrid budgets.
- Candidate budget: 576 per method and path.
- Seed-level SHA-256: `a443c5c6cc737f21d5b12cc2a39cf3f4a8db6ab7fbb636c140fa50fc3312aa10`.
- Figures are generated by `plots.py` from archived CSVs.

## Connections

EXP-025 · EXP-026 · `datasets/2026-08-03-evidence-boundaries.md` · `knowledge_graph/financial-genetics-thread.md`

