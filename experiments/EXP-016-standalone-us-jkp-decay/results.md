# EXP-016 — Standalone JKP US decay is strong, but the geography gap is imprecise

## Verdict

**HYP-016 is not supported under its registered joint rule.** P1, P2, and P4 pass; P3 fails because the direct US-minus-world-ex-US coefficient does not reach the registered inference threshold. The falsifier does not fire, so the evidence is directionally consistent with US concentration but insufficient to establish the cross-location difference.

## Results

Across 141 eligible standalone US factors, post-publication decay is **-0.164 percentage points per month** (t = -2.97). Post-sample performance is 0.027 pp/month above the in-sample baseline (t = 0.56), making post-publication minus post-sample -0.191 pp/month (t = -3.00). Both primary US predictions pass, and 70.9% of factors decline from in-sample to post-publication means.

The binding paired comparison uses 126 common factors and 56,335 common factor-months. US minus world-ex-US post-publication decay is **-0.131 pp/month**, but t = -1.45 misses P3's absolute 1.65 threshold. Its post-sample-to-post-publication contrast is -0.090 pp/month (t = -1.47). The equal-factor US-minus-world-ex-US change is -0.129 pp/month, and the significant-factor US coefficient is -0.197 pp/month (t = -2.95), so P4 passes.

## Adversarial review

- Standalone US measurement repairs EXP-015's aggregate-subtraction problem, but the direct location gap remains imprecise in a second specification.
- Original papers and sample dates are disproportionately US-centric; the event clock may be better aligned to US portfolios even without differential post-publication trading.
- Factor dependence, annual publication dating, and changing portfolio breadth limit inference.
- No direct trading quantity is observed, so the result does not identify arbitrage, causality, or implementation economics.

## What was learned

JKP construction does reproduce statistically strong US publication decay, reducing concern that the C&Z-versus-JKP construction difference alone explains the earlier external gap. It still does not establish that US decay is statistically different from world-ex-US decay. Repeated paired imprecision in EXP-015 and EXP-016 makes further return-only geography slicing low priority; direct quantities are now the sharper research frontier.

## Reproduction

Run `python experiments/EXP-016-standalone-us-jkp-decay/analysis.py` against the pinned JKP files.

## Connections

HYP-016 · EXP-013 · EXP-014 · EXP-015 · Jensen, Kelly, and Pedersen (2023)
