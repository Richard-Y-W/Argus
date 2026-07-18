# HYP-015 — US inclusion strengthens publication decay in standardized global factors

*Registered 2026-07-17 before `world` publication-window outcomes were computed. AI-led.*

## Motivation and predictions

EXP-013 found weak decay in JKP `world_ex_us`. The same release provides `world`, holding factor definitions, metadata, dates, weighting convention, and code fixed while adding US stocks. If geography rather than JKP construction drives the gap, US inclusion should make publication decay more negative.

- **P1 primary:** `world` post-publication decay is negative with |t| at least 2.0 and at least 0.05 percentage points more negative than `world_ex_us`.
- **P2:** the world post-publication-minus-post-sample contrast is negative with |t| at least 1.65.
- **P3 breadth:** more than 55% of world factors have lower post-publication than in-sample means.
- **P4 robustness:** the direction of the world-minus-world-ex-US gap remains negative among significant factors and in equal-factor-weight window changes.
- **Falsifier:** world decay is nonnegative or no more negative than world-ex-US in either panel or equal-factor-weight estimates.

## Internal debate

- **Optimist:** this is the closest available construction-controlled geographic bridge.
- **Skeptic:** `world` is not a US portfolio; changing inclusion also changes aggregate weights.
- **Statistician:** use identical eligibility and paired factor support, and cluster the location difference by month.
- **Economist:** a gap supports US concentration but does not identify publication arbitrage.
- **Portfolio manager:** no holdings, costs, or flows are observed.
- **ML researcher:** no country decomposition or alternate mapping after execution.

Expected failure probability is 50%. Interpretation is explicitly limited to US inclusion in a standardized aggregate.

## Connections

`experiments/EXP-015-us-inclusion-global-decay/design.md` · EXP-013 · HYP-014
