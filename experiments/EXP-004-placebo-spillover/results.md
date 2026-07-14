# EXP-004 — Results: correlation-sorted placebo spillover is rejected

*Run 2026-07-14 from the registered design. Status: **HYP-004 rejected**. Attribution: AI-led. Sample: 114 eligible placebos; 113 with primary exposure.*

## Registered results

The primary coefficient of signed pre-publication exposure on placebo post-publication change was **−0.014%/month per exposure SD** (HC3 se 0.034, t = −0.41), controlling for the placebo's in-sample mean and publication year. The registered threshold was <= −0.05 with t <= −2. **P1 fails.** Correlation-estimation months were constant at 60 in the primary sample and therefore correctly omitted as a collinear control.

The raw signed-exposure terciles looked more favorable:

| Tercile | n | Mean exposure | In-sample | Post-publication | Change |
|---|---:|---:|---:|---:|---:|
| Low | 38 | −0.869 | 0.161 | 0.101 | −0.061 |
| Middle | 37 | 0.113 | 0.167 | 0.110 | −0.057 |
| High | 38 | 0.889 | 0.423 | 0.178 | −0.245 |

High minus low change is −0.184%/month, so **P2 passes its raw magnitude rule**. But high-exposure placebos also had 0.262%/month larger in-sample means. The primary controlled regression shows that this sorting pattern is scale/composition, not incremental exposure evidence—the same trap identified in EXP-005.

## Negative control and robustness

- **P3 fails decisively:** exposure to predictors published only *after* the placebo predicts change with +0.076 (t = +2.54). The sign differs from the spillover prediction, but the registered rule required |t| < 2. Future strategies should not explain contemporaneous arbitrage spillover; significance exposes shared structure/composition in the correlation design.
- **120-month max-correlation:** −0.056 (t = −1.58), directionally consistent but not significant.
- **Published-predictor composite:** +0.103 (t = +3.27), significant in the opposite direction. **P4 fails.**

The registered falsifier fires: P1 fails, P3 fires, and the robustness measures disagree.

## Interpretation

There is no reliable evidence here that arbitrage in published predictors spills into correlated placebo portfolios. Maximum return correlation mostly sorts placebos by shared structure and in-sample scale. This does not reject publication-informed arbitrage in EXP-001/003 or McLean–Pontiff; it rejects this indirect proxy for one transmission channel.

Testing actual arbitrage now requires closer-to-the-trade observables: short interest, institutional holdings, turnover, lending fees, price impact, fund flows, or portfolio overlap constructed from security-level weights. Return correlation alone is too downstream and ambiguous.

## Reproducibility

Run `python analysis.py`. Output tables are `results/regressions.csv`, `terciles.csv`, and `exposures.csv`. The predictor and placebo files use different within-month timestamps; the script explicitly normalizes both to calendar month before correlation. That defect was detected before a successful run and is now part of the deterministic pipeline.

## Connections

`hypotheses/HYP-004-placebo-spillover.md` · EXP-002 · EXP-003 · EXP-005 · `literature_reviews/2026-07-14-publication-arbitrage-lineage.md`
