# EXP-031 — Registered design: surveillance × treatment factorial

**Registered:** 2026-08-05 before execution  
**Stage:** synthetic mechanism decomposition  
**Attribution:** Human-directed

## Frozen benchmark

Reuse EXP-030's six-module state equations, 120-day horizon, five pathology families, 100 seeds per family, Student-t return paths, invariants, costs, buffer release, pathology timing/intensity, observable contributor score, 5% action increments, and outputs without modification.

## Factorial policies

Cross two triggers with two treatments:

| | Proportional treatment | Targeted treatment |
|---|---|---|
| Actual breach: leverage >3 or LCR <1 | `breach_proportional` | `breach_targeted` |
| Early warning: leverage >2.9 or LCR <1.05 | `early_proportional` | `early_targeted` |

Every triggered treatment acts until the same restoration target is reached: leverage <=2.85 and LCR >=1.10. Proportional treatment reduces every module by 5% steps. Targeted treatment uses EXP-030's frozen observable ranking and reduces ranked modules in 5%-of-system-exposure steps. No policy observes the pathology or culprit label.

This changes EXP-030's proportional target solely to make the factorial treatment comparison exact; the change was registered before EXP-031 outcomes.

## Endpoints and inference

Reuse invariant-violation area, healthy-module exposure reduction, terminal equity, false-action days, breach days, recovery, total reduction, and drawdown. Use 10,000 family-stratified paired bootstrap resamples.

## Joint treatment decision rule

Classify targeted isolation as `SUPPORTED WITH LIMITS` only if:

1. early-targeted minus early-proportional violation area has a 95% interval below zero;
2. early-targeted minus early-proportional healthy reduction has a 95% interval below zero;
3. early-targeted terminal equity is noninferior to early-proportional with margin -0.5 and a 95% lower bound above -0.5;
4. breach-targeted minus breach-proportional violation area has a 95% interval below zero;
5. breach-targeted minus breach-proportional healthy reduction has a 95% interval below zero;
6. early-targeted has lower mean violation area than early-proportional in at least three of four non-benign pathology families; and
7. early-targeted averages no more than one additional false-action day relative to early-proportional.

Separately report early-minus-breach contrasts within each treatment. Those diagnose surveillance and cannot rescue a failed treatment claim.

## Limits

This is a decomposition inside the already inspected EXP-030 simulator. It removes a known confound but is not external confirmation. A pass supports the internal value of localization conditional on this benchmark only.

## Connections

`hypotheses/HYP-031-surveillance-treatment-factorial.md` · EXP-030

