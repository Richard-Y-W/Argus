# EXP-013 — Non-US publication decay is not established

## Verdict

**HYP-013 is rejected.** The world-ex-US post-publication estimate was directionally negative but far smaller and less precise than the preregistered primary rule. Four of five predictions failed and the falsifier fired.

## Results

The eligible world-ex-US sample contains 126 factors and 56,335 factor-months. Relative to the original in-sample window, the factor-fixed-effect post-publication coefficient was **−0.037 percentage points per month** (month-clustered SE 0.068, t = −0.55). P1 required at most −0.10 and |t| at least 2.0; it fails.

The post-sample/pre-publication coefficient was +0.038 (t = 0.68), while the post-publication-minus-post-sample contrast was −0.076 (SE 0.040, t = −1.91). The second step clears P2's contrast magnitude and inference thresholds, but P2 fails because the registered two-stage pattern required a negative post-sample coefficient.

Developed and emerging post-publication coefficients were both negative (−0.048 and −0.053) but imprecise (t = −0.67 and −0.79), so P3 fails. Only 53.97% of factors had lower post-publication than in-sample means, below P4's 55% rule. P5 passes narrowly on signs: the significant-factor panel estimate was −0.052 and the equal-factor-weight change was −0.015, but neither was precise and P5 cannot rescue the primary rejection.

## Adversarial review

- The result is not evidence that arbitrage is absent. A non-US aggregate can dilute country-specific correction, publication information can diffuse globally at different speeds, and the public file does not observe trading quantities.
- The negative post-publication-minus-post-sample contrast (t = −1.91) is the strongest suggestive feature, but promoting it would violate the registered joint rule and ignore the positive post-sample coefficient.
- JKP coverage begins mainly in 1986, so 27 of the 153 named factors do not meet the primary window requirements. Classic early anomalies have truncated or absent original-sample histories outside the US.
- Standardized JKP portfolios and C&Z portfolios differ in weighting, breakpoints, universes, and metadata. A smaller estimate may reflect construction rather than geography.
- Factors share stocks and themes. Month clustering addresses common time shocks but not every cross-factor dependence structure.
- Returns are gross; this says nothing about executable alpha, costs, capacity, holdings, shorting, or price impact.

## What was learned

The strong US publication-decay magnitude does not automatically transport to the JKP world-ex-US aggregate. This narrows Argus's current claim: publication-timed decay is well supported in the C&Z US panel, while external validity remains unresolved. Direct trading quantities remain valuable, but the international failure makes a universal arbitrage narrative less credible than it was before EXP-013.

## Reproduction

Acquire the files fingerprinted in `datasets/manifest.json`, then run `python experiments/EXP-013-nonus-publication-decay/analysis.py`. Outputs are under `results/`.

## Connections

`hypotheses/HYP-013-nonus-publication-decay.md` · `datasets/jkp_global_factors_2025.md` · EXP-001 · EXP-003 · Jensen, Kelly, and Pedersen (2023)
