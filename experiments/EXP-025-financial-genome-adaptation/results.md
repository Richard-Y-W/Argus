# EXP-025 results — Inherited local mutation

## Classification

**INCONCLUSIVE for the broad mechanism; NOT SUPPORTED under the registered joint rule.**

Local inherited mutation produced lower confirmation regret than equal-budget global random restart, but its recovery-time confidence interval included zero. P1, P3, and P4 passed; P2 and therefore the joint hypothesis failed.

## Registered results

Thirty untouched confirmation paths were scored after a one-year adaptation interval. Each adaptive method evaluated 576 new genomes per path.

| Prediction | Estimate | 95% paired bootstrap interval | Result |
|---|---:|---:|---|
| P1: random minus evolution regret | 0.0183 cumulative log-return | [0.0083, 0.0289] | Pass |
| P2: random minus evolution recovery days | 8.67 days | [-4.73, 27.83] | **Fail** |
| P3: evolution/random realized volatility | 0.961 | registered acceptable range [0.90, 1.10] | Pass |
| P4: evolution minus random annualized 5% ES | -0.0816 | threshold <= 0.0005 | Pass |
| Joint | all four required | — | **Fail** |

The regret advantage was positive in 21 of 30 confirmation paths and ranged from approximately -0.03 to +0.09 across individual paths. The result is not path-universal.

## Method-level diagnostics

| Family / method | Mean regret | Recovery days | Annual return | Annual vol. | Annualized 5% ES | Annual turnover | Genome diversity |
|---|---:|---:|---:|---:|---:|---:|---:|
| Confirmation / evolution | 0.2927 | 16.77 | 0.0111 | 0.0714 | 2.5437 | 19.64 | 0.213 |
| Confirmation / random | 0.3110 | 25.43 | -0.0072 | 0.0742 | 2.6253 | 20.46 | 0.808 |
| Confirmation / static | 0.3117 | 19.73 | -0.0079 | 0.0798 | 2.8374 | 23.14 | 0.854 |
| Development / evolution | 0.2672 | 15.90 | 0.0447 | 0.0832 | 2.7268 | 33.69 | 0.224 |
| Development / random | 0.2933 | 35.40 | 0.0185 | 0.0720 | 2.3245 | 26.34 | 0.809 |
| Development / static | 0.2843 | 35.40 | 0.0276 | 0.0723 | 2.3673 | 24.77 | 0.877 |

Expected shortfall is the negative mean of the worst 5% daily returns multiplied by 252, not a one-year loss quantile. Turnover is annualized one-way absolute weight change.

## Interpretation

The narrow evidence is consistent with local mutation exploiting inherited structure more efficiently than global resampling in this confirmation family. It is not evidence that financial markets possess literal DNA or that mutation is generally superior.

Evolution collapsed genome diversity to roughly one quarter of the random population's level. That is the intended local-search behavior, but also the clearest failure risk: premature convergence. On the development family, evolution earned more but carried higher volatility, expected shortfall, and turnover than random search. The confirmation result therefore does not establish general risk robustness.

## Strongest adversarial interpretation

This experiment compares a local optimizer with a global sampler on synthetic regimes engineered to share the same genome and phenotype vocabulary. The inherited neighborhood may be useful because the simulator is smooth in those parameters, not because biological inheritance transfers to finance. The scored interval begins one year after the regime break and freezes selection; consequently the experiment measures the quality of the surviving population after adaptation, not immediate real-time recovery. The oracle uses future information and only provides a common regret reference.

The confirmation pilot has only 30 independent paths after a disclosed pre-execution feasibility reduction from 200. Bootstrap uncertainty reflects these simulated paths, not uncertainty across plausible market-generating processes. The broad search over possible genome definitions occurred conceptually before registration and is not represented by the reported interval.

## Deviations and engineering audit

1. Before outcome generation, deterministic timing led to a documented reduction from 40/200 development/confirmation seeds and a 2,000-genome oracle pool to 10/30 and 100. This reduces precision.
2. After P1–P4 were generated, annual turnover was found missing from the exported diagnostics. Gross paths were retained and outputs regenerated; decision endpoints reproduced exactly. This post-outcome repair is disclosed in `design.md`.
3. Four unit tests passed, covering causal timing, genome bounds, one-gene mutation, market determinism, and equal candidate budgets.
4. The pre-repair deterministic rerun reproduced SHA-256 `c01359f4...`. The finalized turnover-inclusive `seed_metrics.csv` has SHA-256 `ad7945bdd9271be8d1078fb7d0e9715eaf1a2374aadb0600b01cd452a7a93285`.

## Decision and next discriminating test

Archive the joint hypothesis as rejected. Do not optimize mutation scales on these paths. The next experiment, if pursued, should use a frozen adaptive-radius rule and score immediately after the regime break across multiple structural families. It should compare local mutation, global random search, Bayesian optimization, and a hybrid maintaining both local lineages and global novelty. Population diversity should become a constraint rather than a descriptive diagnostic.

## Reproduction

```powershell
pytest -q experiments\EXP-025-financial-genome-adaptation\test_analysis.py
python experiments\EXP-025-financial-genome-adaptation\analysis.py
```

## Connections

`hypotheses/HYP-025-financial-genome-adaptation.md` · `failed_experiments/EXP-025-financial-genome-adaptation.md` · `ideas/2026-08-02-lineage-aware-financial-immune-system.md` · EXP-011/012

