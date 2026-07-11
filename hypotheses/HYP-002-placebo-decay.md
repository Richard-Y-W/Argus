# HYP-002 — Publication-timed decay requires a predictive claim: placebos should not decay

*2026-07-11. Status: accepted for testing → EXP-002.*

## Title
Characteristics published *without* a claim of return predictability (C&Z placebos) show little or no post-sample or post-publication decline, unlike predictors.

## Motivation
EXP-001 established that predictors lose ~37% of in-sample returns post-sample and ~55% post-publication. Both M&P mechanisms — selection bias and publication-informed arbitrage — are *specific to claimed predictors*. Selection bias requires selection on in-sample performance; arbitrage requires a published claim to trade on. The C&Z placebos were selected for having been *discussed* in the literature, not for performing, and their papers made no clear predictability claim. If they nonetheless decay on the same publication-timed schedule, the causal reading of EXP-001 is wrong and something else (most plausibly a calendar-time trend common to all characteristics) is doing the work. This is the sharpest cheap falsification test available to this lab, and it is rarely run in the literature.

## Prior literature
M&P 2016 (mechanisms); C&Z 2022 §data (placebo construction: signals from published papers where predictability was not the demonstrated claim — `indirect`, n=100 — or was explicitly rejected — `4_not`, n=14); EXP-001 (predictor benchmark numbers).

## Expected mechanism
- **Channel 1 (selection bias) should be near-absent:** placebos were not selected on in-sample t-stats, and C&Z sign them by the paper's implied direction, not realized performance (verified during data feasibility: 68% positive in-sample means vs ~98% for predictors; `4_not` group in-sample mean ≈ 0.06%/mo). No selection → no mechanical post-sample reversion.
- **Channel 2 (publication-informed arbitrage) should be weak:** nobody allocates capital to a signal the paper didn't claim works.
- **Known contamination, stated in advance:** many `indirect` placebos are constructed from the same accounting objects as true predictors (leverage, distress, investment variants) and are correlated with them. Arbitrage against the real predictors can spill over onto correlated placebos. This biases the experiment *against* HYP-002 (toward finding placebo decay), so a clean null is strong evidence; a partial decline is ambiguous between spillover and confound.

## Falsifiable predictions (registered before running; levels, not percentages, because placebo in-sample means are too small for stable ratios)
P1. Placebo post-publication level decline `|β₂_placebo| < 0.20 %/mo` (predictor benchmark from EXP-001: 0.37 %/mo), and point estimate below half the predictors'.
P2. Difference-in-differences: in the pooled predictor+placebo panel, the extra post-publication decline of predictors over placebos `γ₂ ≥ 0.15 %/mo` with t ≥ 2.
P3. Placebo post-*sample* decline also small: `|β₁_placebo| < 0.15 %/mo` (predictors: 0.25 %/mo in levels). Channel 1 needs selection, which placebos lack.
P4 (registered direction, mechanism demo): if we *artificially* select placebos on positive in-sample mean (R4), a post-sample decline should appear where none was — selection bias made visible in data that has no publication story.
P5 (falsifier). If placebos decline as much as predictors on publication timing (γ₂ ≈ 0), publication is not the cause of predictor decay; escalate the calendar-time confound to a dedicated experiment (EXP-003 candidate).

## Alternative explanations to guard against
- **Calendar-time trend mimicking decay** — the same confound as EXP-001; here it works in our favor: the DiD (P2) differences it out to the extent it hits predictors and placebos equally.
- **Placebo in-sample means are near zero, so "no decline" could be a floor effect.** Mitigation: levels not ratios; and R4's selected subsample has room to fall.
- **Correlation spillover** (above) — declared; interpretive limit, not fixable with this data.

## Required data
`datasets/raw/PlaceboPortsFull.parquet` (acquired 2026-07-11, provenance in `datasets/chen_zimmermann_oct2025.md`), `SignalDoc.csv` placebo rows (all 114 have `Year`, `SampleStartYear`, `SampleEndYear`), plus the EXP-001 predictor panel for the pooled DiD.

## Estimates
Difficulty: low (pipeline exists from EXP-001). Novelty: moderate — placebo decay tests are rarely reported; a clean result is a genuine contribution to the thread. Expected failure probability: ~25% that P2 fails via spillover-contaminated placebos; ~10% that P3 fails if C&Z's placebo choice embeds more performance selection than documented. Learning value: high — this is the researcher's first exposure to control groups and difference-in-differences in a panel.

## Internal debate (condensed)
- **Skeptic:** "Placebos with near-zero in-sample means can't fall, so the test is rigged to pass." — Adopted: primary estimands in levels; P4/R4 creates a selected placebo subsample with room to fall, making the selection channel testable rather than assumed; and the `indirect` group's in-sample mean (~0.27%/mo) is not zero — there *is* room to decline.
- **Statistician:** "The DiD needs the two panels pooled with signal fixed effects and month clustering, not two separate regressions compared informally." — Adopted as E2, the primary test for P2.
- **Economist:** "Indirect placebos are correlated with real predictors; arbitrage spillover will produce some decay and you'll wrongly reject." — Adopted as a declared contamination direction: it biases against HYP-002, so the test is conservative for a null result and ambiguous only for intermediate outcomes. The 14 `4_not` placebos are reported separately as the cleanest (but underpowered) control.
- **Mentor:** "Richard was left this design as an open question and didn't answer before this cycle ran. Record the design reasoning explicitly so he can diff his instinct against it after the fact." — Adopted: see "Five-minute digest" in results doc.

## Connections
`hypotheses/HYP-001-decay-replication.md` (benchmark numbers) → `experiments/EXP-002-placebo-decay/design.md` · `papers/2022-chen-zimmermann-open-source-asset-pricing.md` (placebo construction) · `knowledge_graph/anomaly-decay-thread.md` · possible successor: EXP-003 (calendar-time confound) via P5
