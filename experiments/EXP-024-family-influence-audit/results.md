# EXP-024 — One empirical family carries most equal-factor decay

## Verdict

**HYP-024 is rejected.** Although all 13 deletion estimates remain negative, the magnitude and influence rules fail.

## Results

The full equal-factor contrast is -0.1535 pp/month. Deleting cluster 2, a 59-factor family spanning many investment, issuance, liquidity, risk, and growth constructions, weakens it to **-0.0198 pp/month**. The **0.1337 pp/month** shift exceeds the registered 0.03 bound more than fourfold. Deletion estimates range from -0.2171 to -0.0198.

P1 passes because every deletion remains negative. P2 fails because the least-negative estimate is above -0.10. P3 fails on influence. The non-negative falsifier does not fire, but survival requires all three predictions.

## Adversarial review

- The large family may be economically heterogeneous; its size is itself evidence that the empirical partition is coarse.
- This establishes sensitivity to a frozen correlated block, not that any named mechanism explains the block.
- The honest conclusion is concentration, not absence: pooled decay remains negative but is not broadly independent across families.

## Reproduction and connections

Run EXP-022 first, then `python experiments/EXP-024-family-influence-audit/analysis.py`. HYP-024 · EXP-021 · EXP-022
