# EXP-025 — Inherited local mutation

**Outcome:** Rejected under the registered joint rule.

Evolutionary local mutation lowered confirmation regret versus equally budgeted random restart by 0.0183 cumulative log-return units (paired bootstrap 95% interval [0.0083, 0.0289]), but the recovery-time difference was imprecise: 8.67 days with interval [-4.73, 27.83]. P1, P3, and P4 passed; P2 failed.

The useful surviving observation is that local mutation generated a concentrated, lower-regret population in one untouched synthetic family. It is not a general adaptation result: evolution sharply reduced genome diversity and had worse tail loss and turnover than random search in the development family. See the [full result](../experiments/EXP-025-financial-genome-adaptation/results.md).

## Connections

`HYP-025` · EXP-011/012 · `ideas/2026-08-02-lineage-aware-financial-immune-system.md`

