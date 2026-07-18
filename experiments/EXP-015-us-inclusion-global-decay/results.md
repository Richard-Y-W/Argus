# EXP-015 — US inclusion strengthens standardized global publication decay

## Verdict

**HYP-015 survives its registered rules, with an important inference limitation.** All four predictions pass and the falsifier does not fire, but the direct paired location-gap estimate is imprecise.

## Results

On 126 common factors, JKP `world` post-publication decay is **-0.096 percentage points per month** (t = -2.17), versus -0.037 (t = -0.55) in `world_ex_us`. The -0.059 pp gap clears P1's -0.05 economic threshold. World post-publication minus post-sample is -0.113 pp (t = -2.29), and 66.7% of factors decline. Significant-factor and equal-factor-weight gaps have the registered negative direction.

The direct factor-month `world - world_ex_us` fixed-effect post-publication gap is -0.055 pp but has t = -1.27. P1 did not preregister a significance threshold for this gap, so the hypothesis passes as written; scientifically, the weak paired inference limits confidence.

## Adversarial review

- `world` is an aggregate containing US stocks, not a standalone US portfolio. Its difference from world-ex-US depends on changing country weights.
- Common metadata and construction reduce—but do not eliminate—comparability concerns.
- The result is consistent with US concentration of publication decay; it neither proves geography nor identifies arbitrage.
- No trading quantities, costs, flows, holdings, lending conditions, or price impact are observed.

## What was learned

Combined with EXP-014, the evidence moves away from a simple truncated-history explanation and toward a US-concentrated effect within JKP's standardized construction. The paired uncertainty prevents treating that interpretation as settled. Direct quantities remain the next claim-bearing priority.

## Reproduction

Run `python experiments/EXP-015-us-inclusion-global-decay/analysis.py` against the pinned JKP files.

## Connections

HYP-015 · EXP-013 · EXP-014 · Jensen, Kelly, and Pedersen (2023)
