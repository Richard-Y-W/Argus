# EXP-030 results — Invariant-restoring financial defense

## Classification

**NOT SUPPORTED, WITH A SURVIVING MECHANISM.** The registered joint claim failed two of seven conditions. Targeted defense materially improved on proportional deleveraging and reduced collateral intervention, but did not beat volatility targeting on safety and did not preserve more terminal equity than liquidation.

## What was tested

Five hundred independently seeded 120-day systems were evaluated under five paired policies, for 2,500 policy paths. The controller observed leverage, liquidity coverage, funding contributions, exposure, and trailing losses—but never the hidden pathology family or culprit label.

This is a designed mechanism benchmark. It contains no historical return, institution, account, or executable market data and cannot establish practical edge or regulatory adequacy.

## Registered decisions

| Condition | Estimate | 95% family-stratified paired interval | Decision |
|---|---:|---:|---|
| Immune minus proportional violation area < 0 | -0.0673 | [-0.0782, -0.0572] | Pass |
| Immune minus volatility-target violation area < 0 | +0.0869 | [+0.0738, +0.1004] | **Fail** |
| Immune no more than 0.02 above liquidation | +0.0164 | [+0.0065, +0.0272] | Pass on registered mean rule |
| Healthy reduction below proportional | -4.76 | [-5.76, -3.76] | Pass |
| Healthy reduction below liquidation | -90.07 | [-95.45, -84.68] | Pass |
| Terminal equity above liquidation | -1.81 | [-2.97, -0.62] | **Fail** |
| False actions below 12 days and breadth >=3/4 | about 2.2 days; 4/4 | — | Pass |

The targeted controller had lower mean violation area than proportional deleveraging in all four non-benign pathology families and also in the benign-volatility family.

## Interpretation

This is the first financial-immune experiment with direct evidence for a narrow defense mechanism. Targeted isolation restored leverage/liquidity health more effectively than proportional deleveraging while cutting healthy-module reduction by 4.76 exposure units on average. It remained close to liquidation's safety while preserving roughly 90 additional units of healthy exposure.

However, volatility targeting achieved still lower violation area by reducing roughly 229–236 of the initial 240 exposure units across stress families. It is effectively a near-system-wide shutdown in this benchmark. Liquidation also preserved 1.81 more terminal-equity units on average because it avoided subsequent severe losses. The immune controller occupied a potentially useful middle part of the safety/collateral-damage frontier, but it did not dominate that frontier.

## Strongest adversarial review

**NOT SUPPORTED.** The experiment does not yet isolate whether the improvement over proportional deleveraging comes from targeted treatment or earlier detection. The immune controller acts at leverage 2.9 or LCR 1.05, whereas proportional deleveraging waits for an actual 3.0/1.0 breach. That asymmetry is a material design confound.

Further limitations:

1. The simulator defines contribution variables that resemble the controller's scoring inputs, potentially making localization artificially easy.
2. The volatility baseline wins safety by almost liquidating the system; the registered scalar endpoint does not fully price opportunity loss.
3. “Benign volatility” can still produce genuine leverage breaches through equity losses, so it is benign only with respect to injected funding pathology.
4. Liquidation mechanics, buffer release, outflow rates, and transaction costs are assumed rather than externally calibrated.
5. Family-stratified bootstrap uncertainty covers stochastic paths, not uncertainty about simulator structure.

## Bounded conclusion

We now know what “working” looks like more clearly. Targeted defense has **mechanism potential** because it delivers substantially less invariant damage than proportional control with much less collateral reduction than liquidation. It does **not yet have system-level support** because a conventional volatility rule is safer and the treatment effect is confounded with earlier triggering.

The minimum next experiment is EXP-031: give targeted and proportional treatments the identical early-warning trigger, then factorially cross detector (`breach` versus `early`) with treatment (`targeted` versus `proportional`). That separates surveillance value from isolation value without changing any pathology, action size, or health threshold after observing EXP-030.

## Verification

Five focused tests passed before execution. Results reproduce deterministically from `analysis.py`; configuration and source hash are stored in `outputs/run_metadata.json`. Figures read only archived CSV outputs.

## Connections

`hypotheses/HYP-030-invariant-restoring-financial-defense.md` · EXP-029 · `knowledge_graph/financial-genetics-thread.md`

