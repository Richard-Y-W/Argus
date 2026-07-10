# HYP-001 — Published predictor decay is partial and two-stage

*2026-07-10. Status: accepted for testing → EXP-001.*

## Title
Published US cross-sectional predictors lose part of their returns after their sample ends and more after publication, but remain positive on average.

## Motivation
Direct test of the researcher's day-zero prior (`ideas/2026-07-09-anomaly-decay-prior.md`) and replication of McLean & Pontiff (2016) on independent, open, longer data. Replication of a landmark result is the correct first experiment for a new lab: it validates our pipeline against known numbers before we trust it for anything novel.

## Prior literature
M&P 2016 (target); HLZ 2016 (bias channel); Jacobs & Müller 2020 (international non-replication); Chen & Zimmermann 2022 (data).

## Expected mechanism
Two additive channels: (1) sampling/selection bias inflates in-sample means → post-sample returns drop even with no information release; (2) publication releases the signal to arbitrageurs → additional drop, bounded away from full correction by arbitrage costs.

## Falsifiable predictions (registered before running)
P1. Pooled mean long-short return: post-sample < in-sample, decline between ~10% and ~45% (M&P point estimate 26%).
P2. Post-publication decline from in-sample between ~40% and ~75% (M&P: 58%), strictly larger than P1's.
P3. Post-publication mean return remains significantly > 0 (partial decay).
P4 (falsifier). If post-sample ≈ post-publication (no additional publication effect) or post-publication ≈ 0 (full correction), the two-stage story fails as described.

## Alternative explanations to guard against
- Secular decline in trading costs mimicking publication effects (post-pub windows cluster in recent decades). Mitigation: note it; a calendar-time control is follow-up work, as in M&P's own robustness.
- Construction mismatch inflating "in-sample" means (reproduction error, not bias). Mitigation: restrict to C&Z's clearly-reproduced predictors as a robustness check.
- Publication-year coarseness (we date publication to Dec 31 of publication year vs. M&P's actual dates) — attenuates the measured publication effect.

## Required data
C&Z Oct 2025: `PredictorPortsFull` (LS returns), `SignalDoc` (SampleStartYear, SampleEndYear, publication Year, quality flags). Already acquired; provenance in `datasets/chen_zimmermann_oct2025.md`.

## Estimates
Difficulty: low-moderate (data is clean; inference details matter). Novelty: low — it's a replication; the value is calibration and pipeline validation. Expected failure probability: ~20% that magnitudes fall outside registered ranges (longer post-pub sample and more predictors could yield deeper decay than M&P measured). Learning value: high (panel inference, clustered SEs, event windows, honest replication practice).

## Internal debate (condensed)
- **Skeptic:** "You know the answer; this is confirmation theater." — Response: registered ranges make it falsifiable; a decade of new data and 2× predictors give genuine room to fail; and P3 in particular could fail if post-2015 crowding completed the correction.
- **Statistician:** "Pooled means across predictors with wildly different volatilities and window lengths are not innocent." — Adopted: report both the cross-predictor mean of window means (equal weight per predictor) and the M&P-style panel regression with predictor fixed effects and month-clustered SEs; require ≥12 months per window.
- **Economist:** "Dec-31 publication dating biases the publication effect toward zero — say so up front." — Adopted into design.
- **Optimist:** "Ten extra years of data means we can *extend*, not just replicate — decay among post-2010 publications." — Deferred to follow-up; scope discipline.
- **PM:** "Returns are gross of costs; don't interpret residual post-pub returns as exploitable." — Adopted into results language.

## Connections
`literature_reviews/2026-07-10-anomaly-decay.md` → `experiments/EXP-001-anomaly-decay/design.md`
