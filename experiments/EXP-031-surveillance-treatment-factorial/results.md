# EXP-031 results — Surveillance × treatment factorial

## Classification

**NOT SUPPORTED for targeted-treatment superiority. SUPPORTED WITH LIMITS for early surveillance.** Holding trigger timing fixed, targeted isolation did not reduce invariant damage relative to proportional treatment. It did consistently reduce collateral intervention without materially changing terminal equity.

## Registered treatment decisions

| Condition | Estimate | 95% family-stratified paired interval | Decision |
|---|---:|---:|---|
| Early targeted minus early proportional violation area < 0 | +0.00289 | [-0.00070, +0.00679] | **Fail** |
| Early targeted minus early proportional healthy reduction < 0 | -7.27 | [-8.23, -6.30] | Pass |
| Early targeted equity noninferior, margin -0.5 | +0.0209 | [-0.1749, +0.2193] | Pass |
| Breach targeted minus breach proportional violation area < 0 | +0.00018 | [-0.00464, +0.00508] | **Fail** |
| Breach targeted minus breach proportional healthy reduction < 0 | -6.42 | [-7.58, -5.25] | Pass |
| Early targeted lower violation in >=3/4 pathology families | 1/4 | — | **Fail** |
| Early targeted no more than one extra false-action day | -0.23 | [-0.31, -0.15] | Pass |

The joint treatment claim fails three of seven conditions.

## Surveillance contrasts

Holding proportional treatment fixed, early warning reduced violation area by 0.0456, 95% CI [-0.0539, -0.0378]. Holding targeted treatment fixed, early warning reduced it by 0.0429, 95% CI [-0.0509, -0.0355]. Earlier intervention therefore explains EXP-030's safety improvement.

## Mechanism interpretation

Two separable components survive:

1. **Surveillance efficacy:** acting near the boundary rather than after breach reduces health damage under either treatment.
2. **Localization efficiency:** at identical timing and restoration targets, targeted treatment changes 6–7 fewer healthy-exposure units with no detected terminal-equity penalty.

What does not survive is the stronger claim that localization itself restores safety more effectively. Its violation-area point estimates are slightly worse at both triggers and both intervals include zero.

## Adversarial review

**NOT SUPPORTED** for superiority. EXP-031 removes EXP-030's timing confound, and the targeted safety advantage disappears. Calling the overall controller “better” would therefore be misleading.

The collateral result is credible within this simulator but partly structural: targeted treatment is defined to avoid broad reductions, and the simulator labels healthy modules using its own pathology construction. More importantly, no noninferiority margin for violation area was registered. The narrow intervals suggest similar safety, but a post hoc “equally safe” claim cannot be promoted.

Early surveillance is also not a free-standing forecasting result. It observes the health ratios approaching known boundaries in a designed system. It demonstrates the value of buffer zones, not novel crisis prediction.

## Bounded conclusion

The minimal immune decomposition is now:

`early boundary surveillance (supported internally) + targeted containment (less collateral, not safer) + recovery target`

That is more precise and less grandiose than the original metaphor. The next test, if continued, should preregister a safety-noninferiority margin and optimize collateral action subject to that margin. It must use a structurally different benchmark or historical balance-sheet/stress data; further reuse of these pathology paths would only refine a consumed simulator.

## Verification

Four focused tests passed before execution. All 2,000 factorial policy paths reuse the exact EXP-030 return-path function and frozen source hash. Outputs and hashes are archived under `outputs/`.

## Connections

`hypotheses/HYP-031-surveillance-treatment-factorial.md` · EXP-030 · `knowledge_graph/financial-genetics-thread.md`

