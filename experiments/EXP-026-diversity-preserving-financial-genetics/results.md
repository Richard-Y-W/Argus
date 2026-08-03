# EXP-026 results — Diversity-preserving financial genetics

## Classification

**NOT SUPPORTED.** The diversity mechanism changed the population as intended but did not improve immediate post-change adaptation. P4 and P5 passed; P1–P3 and the joint rule failed.

## Registered outcomes

The confirmation set contained 36 untouched paths: 12 each from rotation, correlation-flip, and mean-reversion families. Every method evaluated 576 new candidates per path.

| Prediction | Estimate | 95% family-stratified paired interval | Result |
|---|---:|---:|---|
| P1: diverse hybrid minus evolution, full year | -0.00172 | [-0.01235, 0.00908] | **Fail** |
| P2: diverse hybrid minus random, full year | -0.00836 | [-0.01500, -0.00141] | **Fail** |
| P3a: diverse hybrid minus evolution, first 126 days | 0.00195 | [-0.00614, 0.01072] | **Fail** versus -0.005 floor |
| P3b: diverse hybrid minus random, first 126 days | -0.00243 | [-0.00688, 0.00199] | **Fail** versus -0.005 floor |
| P4: weakest-family phenotype-diversity ratio versus evolution | 2.371 | — | Pass |
| P5: ES gap versus better baseline | 0.0192 | threshold <= 0.05 | Pass |

The hybrid did not merely fail to establish superiority over random restart: its pooled full-year return was significantly lower under the registered interval.

## Family diagnostics

| Family / method | Full return | Early return | Volatility | Annualized 5% ES | Turnover | Genome diversity | Phenotype diversity |
|---|---:|---:|---:|---:|---:|---:|---:|
| Rotation / evolution | 0.0293 | 0.0124 | 0.0819 | 2.7672 | 27.55 | 0.237 | 0.069 |
| Rotation / random | 0.0292 | 0.0114 | 0.0773 | 2.6226 | 23.01 | 0.808 | 0.229 |
| Rotation / hybrid quality | 0.0162 | 0.0063 | 0.0803 | 2.7807 | 26.85 | 0.370 | 0.096 |
| Rotation / hybrid diverse | 0.0149 | 0.0070 | 0.0797 | 2.7165 | 29.37 | 0.603 | 0.168 |
| Correlation flip / evolution | -0.0157 | -0.0286 | 0.0824 | 2.9208 | 23.74 | 0.205 | 0.058 |
| Correlation flip / random | -0.0065 | -0.0196 | 0.0802 | 2.8435 | 20.67 | 0.778 | 0.195 |
| Correlation flip / hybrid quality | -0.0204 | -0.0281 | 0.0846 | 3.0506 | 22.26 | 0.495 | 0.135 |
| Correlation flip / hybrid diverse | -0.0189 | -0.0254 | 0.0764 | 2.7783 | 22.05 | 0.605 | 0.161 |
| Mean reversion / evolution | -0.0498 | -0.0457 | 0.0709 | 2.5232 | 34.85 | 0.199 | 0.058 |
| Mean reversion / random | -0.0389 | -0.0407 | 0.0686 | 2.3963 | 26.34 | 0.764 | 0.192 |
| Mean reversion / hybrid quality | -0.0431 | -0.0428 | 0.0687 | 2.4296 | 28.23 | 0.344 | 0.080 |
| Mean reversion / hybrid diverse | -0.0374 | -0.0378 | 0.0675 | 2.4251 | 26.06 | 0.511 | 0.137 |

## What the ablation identifies

The quality-only hybrid also failed to improve on the baselines. Therefore the negative result cannot be attributed solely to reserving four slots for diversity. Mixing 25% immigrants with 75% descendants was itself insufficient under the registered selection rule.

The diversity reserve nevertheless worked mechanically. Diverse-hybrid phenotype diversity was more than twice evolution's in every family, and its genome diversity sat between evolution and random search. In correlation-flip and mean-reversion paths it reduced volatility or expected shortfall relative to evolution. Diversity acted more like a robustness regularizer than a source of higher return.

## Strongest adversarial interpretation

The experiment may simply show that inheritance is not valuable after large discontinuities in a five-parameter trend/risk genome. Global random search covers the small bounded genome space cheaply; local descendants spend scarce evaluations near parents fitted to the obsolete regime. Reserving diversity after fitness selection cannot repair a mutation kernel whose locality is wrong for the environmental distance.

Conversely, these synthetic families are structurally hostile to inherited trend parameters. The result does not show that inheritance is useless under gradual drift, modular genomes, or environments with recurring structure. It shows that the fixed EXP-025 mutation kernel plus a fixed 25% immigration rate is not an adequate general solution.

## Engineering and deviations

- Four preregistered mechanical tests passed: equal candidate budgets and hybrid composition, deterministic distinct families, causal phenotype signatures, and reserve fitness-floor compliance.
- The numerical run completed and wrote both CSVs, after which JSON serialization failed on NumPy booleans. The finalizer was repaired to cast native booleans and operate on the already computed seed-level CSV. No numerical experiment was rerun or altered.
- Final seed-level SHA-256: `f4533c532f5dba5536240fe7c23d5674f1104d5e2d60fc79db6766c0a661fd9e`.

## Research decision

Reject the fixed hybrid. Do not tune immigrant fractions or reserve sizes on these consumed paths.

The next research problem is **conditional evolvability** rather than unconditional diversity: estimate whether the new environment is close enough to prior environments for local inheritance to be useful. A future experiment should freeze a regime-distance gate before execution:

- small detected shift -> local mutation;
- intermediate or uncertain shift -> mixed local/global search;
- large structural break -> global restart or dormant specialist reactivation.

That gate must compete with always-local, always-global, and generic change-point allocation under an equal search budget.

## Reproduction

```powershell
pytest -q experiments\EXP-026-diversity-preserving-financial-genetics\test_analysis.py
python experiments\EXP-026-diversity-preserving-financial-genetics\analysis.py
```

## Connections

EXP-025 · `failed_experiments/EXP-026-diversity-preserving-financial-genetics.md` · `knowledge_graph/financial-genetics-thread.md`

