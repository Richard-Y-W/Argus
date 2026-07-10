# Literature Review: Post-Publication Anomaly Decay

*Argus, 2026-07-10. Papers noted individually in `papers/`. This review synthesizes and identifies gaps.*

## The question

When an academic paper documents a cross-sectional return predictor, what happens to that predictor's returns afterward — and what does the answer reveal about how markets process information?

## The evidence, in one paragraph

McLean & Pontiff (JF 2016) replicated 97 published US predictors and compared returns in-sample, post-sample-pre-publication, and post-publication: returns fall ~26% out-of-sample (statistical bias) and ~58% post-publication, implying a ~32-point publication effect — but they do not reach zero, and decay is smallest where arbitrage is costliest. Harvey, Liu & Zhu (RFS 2016) supply the statistical-bias theory: with hundreds of factors mined from the same data, conventional t > 2 is far too lenient; they argue for t > 3 and conclude most published factors are likely false. Jacobs & Müller (JFE 2020) then break the comfortable synthesis: across 39 markets, the post-publication decline is reliable **only in the United States**, while the anomalies themselves mostly *do* work abroad — hard to square with pure data mining (noise shouldn't travel), and equally hard to square with frictionless global arbitrage (correction shouldn't stop at the border). Chen & Zimmermann (CFR 2022) make the whole literature auditable with open code and data for ~200 predictors, including publication metadata and placebo characteristics.

## Where the stories stand

| Explanation | Supported by | Contradicted by |
|---|---|---|
| Statistical bias (never real) | ~26% OOS decay (M&P); factor-zoo multiple testing (HLZ) | anomalies work internationally (J&M); placebos vs. predictors distinction (C&Z) |
| Arbitrage correction | extra ~32% post-pub decay; volume/short-interest rises (M&P) | correction incomplete; absent outside US (J&M) |
| Risk premium | persistence of residual returns | decay itself; concentration in hard-to-arbitrage stocks |

The mature view: published predictors were **partly overstated, partly real mispricing that informed capital corrects — but only up to the cost of correcting it, and apparently only in the US**.

## Gaps and live questions (the point of this review)

1. **Why is decay US-only?** (J&M's puzzle.) Candidate decompositions — arbitrage capital home bias, shorting frictions abroad, local dissemination of research — are untested. This is the most interesting open question in the thread.
2. **Decay dynamics, not just levels.** Most work estimates a step (pre/post dummies). Is decay gradual? Does it begin *before* publication (working-paper circulation, SSRN posting dates)? Event-time profiles are underexplored relative to their identification value.
3. **Crowding and interaction.** M&P found post-publication correlation among anomalies rises. Does each additional published (or replicated-in-open-data) predictor decay faster than earlier ones — an "arbitrage capacity" story?
4. **The placebo test nobody runs.** C&Z ship placebo characteristics. If decay is publication-caused, placebos (never claimed to predict) should show *no* post-"sample" decay pattern. Cheap, sharp, rarely done.
5. **Construction sensitivity.** Decay estimates use one portfolio construction per predictor. How much do the 26%/58% numbers move under deciles/VW/liquidity screens (all available in C&Z alt-ports)?

## What Argus does next

EXP-001 replicates the M&P three-window result on the C&Z October 2025 release (data through 2024-12 — a decade more post-publication data than M&P had, and ~2× the predictors). Success criterion is *matching the qualitative pattern and rough magnitudes*, not the exact numbers (different predictor set, longer sample, approximate publication dating). Gaps 2 and 4 are candidate follow-ups (EXP-002+).

## Connections

- `papers/2016-mclean-pontiff-does-academic-research-destroy-predictability.md`
- `papers/2020-jacobs-muller-anomalies-across-the-globe.md`
- `papers/2022-chen-zimmermann-open-source-asset-pricing.md`
- `hypotheses/HYP-001-decay-replication.md` → `experiments/EXP-001-anomaly-decay/`
- `ideas/2026-07-09-anomaly-decay-prior.md` (the researcher's prior that started the thread)
