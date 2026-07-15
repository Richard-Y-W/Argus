# EXP-010 — Results: within-signal weighting does not identify stronger VW decay

*Run 2026-07-15. Status: **HYP-010 rejected**. AI-led.*

## Result

The primary paired sample contains 152 signals. Mean `VW decay - EW decay` is **+0.141** (SE 0.080, t = 1.76, 95% CI [−0.017, +0.300]). The estimate clears the registered +0.10 economic threshold but not the t >= 2 inference threshold, so P1 fails and the falsifier fires.

The rest of the registered evidence is weaker than the primary mean suggests:

- **P2 fails with the wrong sign.** The levels difference-in-differences is +0.051% per month (t = +1.54), whereas stronger VW deterioration required a negative estimate.
- **P3 fails.** Exactly 50.0% of signals have greater proportional decay under VW, below the registered 55% breadth threshold.
- **P4 passes only directionally.** The winsorized mean is +0.151 (t = 2.46) and the clear-only mean is +0.136 (t = 1.57). Both are positive, as registered, but this does not override the primary falsifier.

The correct conclusion is rejection, not “marginal support.” Pairing repairs EXP-009's between-signal composition problem, yet it does not produce broad or conventionally precise evidence that value-weighted implementations decay more after publication.

## Sample flow and adversarial review

There are 212 eligible predictor metadata records, 179 signals common to both alternative-portfolio files, and 152 after requiring common in-sample/post-publication histories plus both in-sample means above 0.10% per month. The clear-only robustness sample has 122 signals.

The median paired decay difference is only +0.021 and the positive share is exactly one half. Large opposing tails drive much of the mean: the five lowest differences range from −1.97 to −3.91, while the five highest range from +2.10 to +4.54. Winsorization improves inference, but choosing it over the preregistered raw primary would be outcome-dependent. Cross-signal dependence could also make the conventional paired t-statistic optimistic.

## What was learned

The raw EXP-009 gap (94.7% VW versus 56.4% EW across different signals) was not recovered as a broad within-signal fact. Weighting is therefore not a reliable proxy for publication-arbitrage intensity in this panel. This leaves direct quantities—holdings, flows, turnover, short interest, lending fees, or price impact—as the more credible next mechanism evidence.

The experiment says nothing about net implementability. Both series are gross decile spreads; EW can load on microcaps and VW can weaken characteristic exposure. Annual publication timing and 33 signals missing from the paired alternative files further limit generalization.

## Reproduction

Run `python experiments/EXP-010-within-signal-weighting-decay/analysis.py`. Dataset fingerprints are in `datasets/manifest.json`. Machine-readable outputs are in `results/`.

## Connections

`hypotheses/HYP-010-within-signal-weighting-decay.md` · EXP-009 · EXP-001 · `knowledge_graph/anomaly-decay-thread.md` · Chen–Zimmermann October 2025 release
