# EXP-029 results — Danger-routed financial immune controller

## Classification

**NOT SUPPORTED.** The controller restored danger sensing, tolerance, localized repair, systemic regeneration, and inherited state, but failed five of six registered conditions. No adaptive-defense edge is established.

## Evidence boundary

The official French 10-industry archive was downloaded and hashed before parsing. Calibration used 120 months from 1995–2004 to fix signal quantiles without portfolio-performance optimization. Primary evaluation contains 240 months from 2005–2024. The 18-month 2025+ check is descriptive and cannot rescue failure.

This panel was previously uninspected, but it overlaps EXP-028's US equity source and industry construction. The result is cross-resolution evidence, not independent geography or tradability evidence.

## Registered decisions

| Condition | Result | Decision |
|---|---:|---|
| Controller minus localized monthly CE | -0.000048, 95% CI [-0.003125, 0.003456] | **Fail** |
| Controller minus random monthly CE | -0.000699, 95% CI [-0.002518, 0.000961] | **Fail** |
| Controller minus all-gene monthly CE | -0.000629, 95% CI [-0.004763, 0.003765] | **Fail** |
| ES no more than 10% worse than best fixed response | 0.4635 vs best 0.4629 | Pass |
| Turnover below every fixed response | 16.70 vs localized 11.01 and all-gene 11.52 | **Fail** |
| Every route used in at least 5% of months | localized 3.75% | **Fail** |

Route shares were 73.33% tolerance, 3.75% localized repair, and 22.92% systemic regeneration. The calibrated detector transferred poorly: concentrated damage occurred less often in evaluation than the registered minimum anticipated.

## Diagnostics

| Period / method | Net log return | Ann. vol. | Ann. 5% ES | Max drawdown | Turnover | New-candidate evaluations |
|---|---:|---:|---:|---:|---:|---:|
| 2005–2024 controller | 2.413 | 0.192 | 0.463 | -0.512 | 16.70 | 4,096 |
| 2005–2024 localized | 2.422 | 0.191 | 0.463 | -0.443 | 11.01 | 15,360 |
| 2005–2024 all-gene | 2.518 | 0.241 | 0.580 | -0.532 | 11.52 | 15,360 |
| 2005–2024 random | 2.546 | 0.194 | 0.471 | -0.473 | 43.15 | 15,360 |
| 2005–2024 minimum variance | 1.837 | 0.149 | 0.356 | -0.369 | 18.33 | 240 |
| 2005–2024 equal weight | 1.995 | 0.187 | 0.457 | -0.525 | 0.00 | 240 |
| 2025+ controller | 0.188 | 0.163 | 0.358 | -0.166 | 1.27 | 320 |
| 2025+ equal weight | 0.224 | 0.152 | 0.332 | -0.165 | 0.00 | 18 |

The controller used only 26.7% as many new candidates as a fixed search policy, which is computationally efficient. That was not a registered performance claim and does not compensate for the failed outcomes. Systemic Dirichlet resets were sufficiently large that infrequent intervention still produced more turnover than localized and all-gene search.

## Adversarial review

**NOT SUPPORTED.** The exact supported claim is limited to computational triage: a frozen danger rule skipped most searches while roughly matching localized risk and return. It did not improve the primary endpoint and did not achieve the intended low-collateral-damage mechanism.

Blocking findings:

1. All three primary superiority intervals include zero and their point estimates are negative.
2. Systemic regeneration created large portfolio changes, contradicting the proposed defense-efficiency mechanism.
3. Local repair almost disappeared out of sample, so the three-level immune architecture did not operate with registered breadth.
4. Equal weight beat the controller with lower volatility and no turnover in the short later-vintage check.

The strongest alternative explanation is ordinary sparse computation: the controller is a change detector that occasionally runs an optimizer. There is no evidence that immune vocabulary contributes beyond that standard control formulation. Damage statistics describe distribution change, not expected intervention value—repeating EXP-027's central lesson in historical data.

## What remains of the original idea

The original idea has not been disproved in full; it is too broad for one experiment. But two core naive assumptions now have negative evidence:

- greater statistical danger does not reliably tell us which adaptation radius is valuable;
- fewer interventions do not guarantee less collateral damage when the systemic response is large.

Further work should stop trying new thresholds on these data. A scientifically distinct continuation would model defense as constrained loss containment rather than return optimization: detect breaches of an explicit system-health invariant, isolate the failing module, and minimize intervention subject to restoring the invariant. That is closer to immunity than evolving portfolios for return.

## Verification

Four focused tests cover routing boundaries, exact preservation of unaffected modules, equal fixed budgets, deterministic loading, and the quarantine. Inputs, thresholds, route shares, and settings are stored in `outputs/run_metadata.json`.

## Connections

`hypotheses/HYP-029-danger-routed-immune-controller.md` · EXP-027 · EXP-028 · `knowledge_graph/financial-genetics-thread.md`

