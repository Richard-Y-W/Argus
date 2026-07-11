# EXP-002 — Results: Placebo test of publication-timed decay

*Run 2026-07-11. Design registered before analysis in `design.md`; predictions in `hypotheses/HYP-002-placebo-decay.md`. Status: **hypothesis supported — P1, P2, P3 pass; P4 (a mechanism side-prediction) fails and is documented below.***

## Headline result (114 placebos, 69,712 signal-months; predictor benchmark = EXP-001 sample)

| Quantity (levels, %/mo) | Placebos | Predictors | Registered | Verdict |
|---|---|---|---|---|
| In-sample mean LS | 0.209 | 0.670 | — | — |
| Post-sample change β₁ | **+0.082** (t = 1.19) | −0.247 (t = −3.85) | \|β₁\| < 0.15 | **P3 ✓** |
| Post-publication change β₂ | **−0.110** (t = −2.55) | −0.369 (t = −6.49) | \|β₂\| < 0.20 and < half of predictors' | **P1 ✓** |
| DiD: extra predictor post-pub decline γ₂ | **−0.259** (t = −3.32) | | ≥ 0.15, t ≥ 2 | **P2 ✓** |
| DiD: extra predictor post-sample decline γ₁ | **−0.328** (t = −2.90) | | not registered | supports selection channel |

Estimator: signal fixed effects, SEs clustered by month; DiD pools both panels (326 signals, 206,050 rows). Gross of transaction costs throughout.

**Reading:** characteristics published *without* a predictability claim show **no post-sample decline at all** (point estimate is positive) and only a small post-publication drift. The two declines that define the predictor decay pattern are almost entirely specific to predictors — which is what the M&P causal story (selection bias + publication-informed arbitrage) requires. The falsifier P5 (placebos decay like predictors → publication is not the cause) does not fire.

## Robustness (registered)

| Spec | n | β₁ post-sample (t) | β₂ post-pub (t) |
|---|---|---|---|
| Primary | 114 | +0.08 (1.2) | −0.11 (−2.6) |
| R1a indirect only | 100 | +0.04 (0.7) | −0.12 (−2.7) |
| R1b `4_not` only (descriptive, underpowered) | 14 | +0.37 (1.7) | **−0.06 (−0.6)** |
| R2 winsorized 1/99 | 114 | +0.07 (1.1) | −0.11 (−2.7) |
| R3 end 2019 | 114 | +0.07 (1.0) | −0.15 (−3.4) |
| R4 selected on positive in-sample mean | 78 | **−0.03 (−0.5)** | −0.26 (−5.2) |
| R5 balanced ≥36m windows | 104 | +0.05 (0.6) | −0.14 (−3.2) |

The winsorized DiD is essentially unchanged (γ₂ = −0.237, t = −3.30).

## The failed side-prediction (P4), reported with the same care as the passes

**P4 predicted** that artificially selecting placebos on positive in-sample mean (R4) would *create* a post-sample decline — selection bias made visible. **It did not:** β₁ = −0.03 (t = −0.5). Best available explanation, formed after seeing the result (so it is a hypothesis, not a finding): conditioning on a positive mean over a 25–40-year sample is *weak* selection — the sampling error of a long-sample mean is small relative to cross-signal dispersion, so the condition mostly picks signals whose *true* mean is positive, and there is little inflation to revert. Publication selection is different in kind: it selects on t-statistics near thresholds from a large space of tried specifications (the HLZ channel), which a simple mean>0 screen does not mimic. Implication for the thread: the predictors' post-sample decline (γ₁ = −0.33) is real and predictor-specific, but our R4 exercise says its source is sharper than "any conditioning on in-sample performance."

## The one result that keeps the confound alive

Placebos do drift down slightly after "publication" (−0.11 %/mo, robust across R1a–R5). Two candidate explanations, not separable in this data, both declared in advance:
1. **Arbitrage spillover** — many `indirect` placebos are correlated with true predictors; trading the predictor moves the placebo. Consistent with the `4_not` subgroup (least correlated with claims, by construction) showing no significant decline.
2. **A mild calendar-time trend** hitting everything in later decades — post-publication windows are concentrated in recent years, so any secular decline in cross-sectional return spreads loads onto the post-pub dummy.

Explanation 2 is exactly the confound EXP-001 flagged and deferred. It is now the most important open threat to the causal interpretation of the whole thread → **EXP-003** (calendar time vs event time) is the mandatory next experiment, not an optional extension.

## Interpretation (bounded by what we ran)

The publication-decay pattern of EXP-001 passes its control-group test: no predictive claim → no post-sample decline and (at most) a small post-publication drift attributable to spillover or a common trend. This materially strengthens the causal reading of EXP-001 but does not complete it — the calendar-time confound remains unmodeled, and the placebo drift is an upper bound on its size (−0.11 of the predictors' −0.37).

## Reproducibility

`analysis.py` (deterministic) then `plots.py`. Same environment as EXP-001 (Python 3.11.15, pandas 3.0.3, statsmodels 0.14.6). Data: `datasets/chen_zimmermann_oct2025.md` (PlaceboPortsFull acquired 2026-07-11). Outputs in `results/`.

---

## Five-minute digest for the researcher

1. **What a control group buys you.** EXP-001 showed predictors decay after publication. A skeptic says: "everything decays in recent decades; publication timing is coincidence." The placebos are 114 characteristics that went through the *same journals, same data, same decades* — but carried no predictability claim. They didn't decay post-sample at all. The skeptic's story just got much harder to tell.
2. **Difference-in-differences in one sentence:** instead of asking "did predictors fall after publication?" ask "did predictors fall *more than placebos* after publication?" — the second question subtracts anything that hits both groups (eras, costs, regimes). Answer: yes, by 0.26%/mo (t = −3.3).
3. **An honest miss:** I predicted that cherry-picking placebos with positive in-sample means would fake a post-sample decline (selection bias demo). It didn't — selecting on a long-sample mean is too weak a filter. The selection that inflates published results is nastier: thousands of tried specifications, t-stat thresholds, referee filters. Weak selection ≠ no selection bias elsewhere; my demo was underpowered *by design of the filter*, and that's on me.
4. **Question to carry forward (answer before reading EXP-003):** placebos still drifted down a little (−0.11%/mo) after their papers appeared. Two stories: (a) they're correlated cousins of real predictors and got dragged down by arbitrage spillover; (b) *everything* — predictor or not — earns less in recent decades, and "post-publication" secretly means "recent." What evidence would distinguish (a) from (b)? Hint: one of them predicts the decline should line up in *calendar* time, the other in *event* time.

## Connections

`hypotheses/HYP-002-placebo-decay.md` (P1–P3 pass, P4 fails, P5 falsifier does not fire) · predecessor: `experiments/EXP-001-anomaly-decay/results.md` (benchmark) · successor: EXP-003 (calendar vs event time — now mandatory) · `papers/2022-chen-zimmermann-open-source-asset-pricing.md` (placebo construction) · `knowledge_graph/anomaly-decay-thread.md`
