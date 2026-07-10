# EXP-001 — Results: Three-window replication of McLean & Pontiff (2016)

*Run 2026-07-10. Design registered before analysis in `design.md`; hypothesis and prediction ranges in `hypotheses/HYP-001-decay-replication.md`. Status: **replication successful — all registered predictions pass.***

## Headline result (primary spec: 212 predictors, 136,338 predictor-months, 1926–2024)

| Quantity | Estimate | M&P 2016 | Registered range | Verdict |
|---|---|---|---|---|
| Mean in-sample LS return | 0.670 %/mo | ~0.58 %/mo | — | comparable |
| Post-sample decline | **36.8%** (t = −3.85) | 26% | 10–45% | **P1 ✓** |
| Post-publication decline | **55.1%** (t = −6.49) | 58% | 40–75%, > P1 | **P2 ✓** |
| Post-publication mean | **0.333 %/mo** (t = 7.64) | > 0 | > 0, p < .05 | **P3 ✓** |
| Implied publication effect | 18.3 pts | 32 pts | — | smaller; see below |

Estimator: pooled panel with predictor fixed effects, standard errors clustered by month (M&P's specification). Returns are **gross of transaction costs**; nothing here speaks to exploitability.

Cross-predictor medians tell the same story with honest dispersion: median in-sample 0.58 → post-sample 0.37 → post-publication 0.23 %/mo; a quarter of predictors have post-publication means below 0.06 %/mo (see `results/fig2_is_vs_postpub.png`).

## Robustness (all registered in advance; none moved the conclusion)

| Spec | Post-sample decline | Post-pub decline | Post-pub mean (t) |
|---|---|---|---|
| Primary | 36.8% | 55.1% | 0.333 (7.6) |
| R1 clear-reproduction only (165) | 36.1% | 57.4% | 0.348 (6.8) |
| R2 positive in-sample mean only (208) | 36.6% | 54.7% | 0.345 (7.6) |
| R3 winsorized 1/99 | 35.4% | 52.5% | 0.341 (8.5) |
| R4 panel ends 2019-12 | 37.0% | 61.1% | 0.301 (6.7) |
| R5 ≥36 months in all windows (187) | 34.6% | 53.7% | 0.337 (7.3) |

## Deviations from M&P, and what they explain

1. **Our post-sample decay (37%) is larger than M&P's 26%** — but nearly identical to Jacobs & Müller's US estimate (38%). Likely causes: 2× the predictor count (including weaker post-2000 discoveries), a different replication of each predictor, and annual (not issue-date) window boundaries that leak some early post-publication months into the post-sample window.
2. **Our implied publication effect (55 − 37 ≈ 18 pts) is smaller than M&P's 32.** The annual publication dating attenuates it (registered in advance as the expected direction), and pre-publication working-paper circulation blurs the boundary in the same direction.
3. **R4 (ending 2019) shows deeper post-publication decay (61%) than the full panel (55%)** → anomaly returns in 2020–2024 were *better* than the earlier post-publication average. Decay is not monotone in calendar time; the recent period partially revived published predictors. Unplanned observation, flagged for follow-up — not a conclusion.

## Interpretation (bounded by what we ran)

The two-stage partial-decay pattern replicates on independent, open, longer data: roughly a third of published in-sample performance does not survive the sample's end (statistical bias upper bound), publication removes more, and what remains is a statistically solid ~0.33%/month gross — consistent with mispricing that informed capital corrects only up to the cost of correcting it. Nothing here identifies mechanism beyond the timing design; the US-only puzzle (Jacobs & Müller) remains untouched by this experiment.

## What remains unknown / follow-up candidates

- **EXP-002 candidate (placebo test):** C&Z placebo characteristics should show no publication-timed decay if the effect is publication-caused. Sharp, cheap, rarely run.
- **Event-time profile:** does decay begin before publication (working-paper circulation)? Requires SSRN posting dates.
- The 2020–2024 revival observation (above).
- Value-weighted / decile constructions (C&Z alt-ports) to check construction sensitivity.

## Reproducibility

`analysis.py` (deterministic, no resampling) then `plots.py`. Python 3.11.15, pandas 3.0.3, numpy 2.4.6, statsmodels 0.14.6, openassetpricing (Oct 2025 release). Data provenance: `datasets/chen_zimmermann_oct2025.md`. Outputs in `results/` (CSVs, figures, run log).

---

## Five-minute digest for the researcher

1. **Your day-zero prior scored well.** Markets *do* "catch and patch" — we measured it: returns drop an extra ~18–32 points of their in-sample mean after publication, volume and short interest rise (M&P). But the patch is incomplete (~0.33%/mo remains, gross) and the patching apparently stops at the US border (Jacobs & Müller) — efficiency is bounded by the cost of enforcing it.
2. **The single most important design idea:** the post-sample-pre-publication window separates "it was never real" from "it was real and got traded away." You now know why — you derived most of it yourself yesterday.
3. **What made this a *credible* experiment:** the prediction ranges were registered before the code existed (HYP-001), the exclusions and robustness checks were fixed in the design doc, and the one surprising unplanned finding (2020–24 revival) is labeled as unplanned. That discipline is the difference between research and storytelling.
4. **Question to carry forward:** if publication causes decay, what should happen to characteristics that were published but *never claimed to predict returns* (placebos)? Answer it in your head before we run EXP-002.

## Connections

`hypotheses/HYP-001-decay-replication.md` (all predictions pass) · `literature_reviews/2026-07-10-anomaly-decay.md` (gaps 2, 4 now have a pipeline) · `papers/2016-mclean-pontiff-...md` · `papers/2020-jacobs-muller-...md` · `questions/why-is-decay-us-only.md` · successor: EXP-002 (placebo decay)
