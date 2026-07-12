# HYP-005 — Post-publication decay is concentrated in strong, cheap-to-arbitrage signals

*2026-07-12. Status: accepted for testing → EXP-005.*
*(HYP-004 is reserved for the researcher's spillover hypothesis; see `experiments/EXP-004-placebo-spillover/researcher-worksheet.md`. Numbering skips ahead so his slot stays his.)*

## Title
Cross-predictor heterogeneity in post-publication decay: predictors with stronger original-paper evidence decay more, and predictors that are costlier to arbitrage (proxied by long-short strategy volatility) decay less.

## Motivation
EXP-001–003 established *that* published predictors decay (−0.37 %/mo post-publication), that the decay is predictor-specific (placebos don't share it, EXP-002), and that it runs on the publication clock (EXP-003). None of them asked *which* predictors decay. The average conceals the mechanism: a correction driven by arbitrage capital should be largest where the prize is biggest and the frictions smallest; a correction that is mere reversion of in-sample luck should be largest where the in-sample estimate was noisiest. The same panel that answered the first three questions can decompose this one, at zero new data cost. M&P (2016, Tables 5–6) ran this test on their 97 predictors; we extend it to 212 with the event-time framing EXP-003 validated, plus one covariate M&P could not use — Google Scholar citations as a direct attention proxy.

## Prior literature
M&P 2016 (decay larger for higher in-sample return/t-stat predictors; smaller for portfolios concentrated in small, illiquid, high-idiosyncratic-risk stocks); Pontiff 2006 (idiosyncratic risk as the binding holding cost of arbitrage); HLZ 2016 (published t-stats are selected — a t-threshold survivorship that makes strong published evidence partly luck); EXP-002 (screening placebos on in-sample mean does *not* induce decay → the pure selection-on-mean channel is weak in this panel).

## Expected mechanism
Two channels, with partially opposing fingerprints:

1. **Arbitrage correction.** Publication reveals the signal; capital flows toward the biggest, most implementable prizes. Predicts: more decay for high-t signals (more convincing → more capital), less decay for high-volatility strategies (volatility is a holding cost, Pontiff 2006).
2. **Statistical shrinkage.** Published estimates are selected on significance (HLZ); the luck component reverts unconditionally after the sample ends. Predicts: more decay for high-t signals **and** more decay for high-volatility strategies (noisier in-sample estimates carry more luck).

The two channels agree on the t-stat and disagree on volatility — the volatility interaction is the discriminating cell. EXP-002's failed P4 (mean-screened placebos don't decay) already suggests the shrinkage channel is weak here, tilting the volatility prediction toward the arbitrage sign.

## Measurement choices (stated up front)
- **Signal strength = original-paper t-stat** (`T-Stat` in SignalDoc, n=188/212), not our realized in-sample t. The realized in-sample mean sits on both sides of a decay regression and manufactures reversion mechanically. The OP t-stat is not immune (it embeds the same in-sample luck plus publication selection) but it is the pre-registered, externally recorded number. The realized-t version is run as a labeled robustness, and a *gap* between the two is itself informative about shrinkage.
- **Arbitrage cost = in-sample volatility of the long-short return.** We lack holdings, so stock-level idiosyncratic risk is out of reach; strategy-level volatility is the coarse proxy. Log-transformed (right-skewed), z-scored.
- **Attention = log Google Scholar citations (2025-09 snapshot).** Exploratory only: measured after treatment, so causality can run backward (famous because it worked, or cited because it died — both stories exist).

## Falsifiable predictions (registered before running; ranges deliberately conservative — Argus has failed 4/12 predictions to date, every miss from over-predicting mechanism visibility)
P1. The post-publication × OP-t-stat interaction is negative: between −0.05 and −0.30 %/mo per 1 sd of OP t, with |t| ≥ 2 in the joint specification. Equivalent sort statement: the top OP-t tercile's post-publication decline (in-sample mean minus post-pub mean) exceeds the bottom tercile's by at least 50%.
P2. The post-publication × volatility interaction is **not strongly negative**: coefficient in [−0.05, +0.25] %/mo per sd, point prediction positive but small. The bet is the floor: a coefficient below −0.15 with |t| ≥ 2 would mean shrinkage dominates arbitrage costs, contradicting Pontiff's mechanism and EXP-002's P4 evidence, and P2 fails.
P3 (exploratory, direction only, ~60% confidence). Post-publication × log-citations is negative — more-cited predictors decay more. Post-treatment caveat applies regardless of outcome.
P4 (falsifier for the whole design). If **no** characteristic interacts (all |t| < 1 in the joint spec and terciles are flat), decay is homogeneous across signals. That would be genuine news: uniform correction regardless of signal strength or cost looks like broad factor crowding, not signal-by-signal arbitrage — and would demote HYP-005.

## Alternative explanations to guard against
- **Cohort/era composition:** OP t-stats and citations correlate with publication year (older papers accumulate citations; earlier literature faced lower t-hurdles). A pp × X interaction can proxy a pp × era effect. Mitigation: robustness with EXP-003's registered era dummies, and a pp × publication-year control.
- **Mechanical shrinkage in the t measure:** addressed by using OP t as primary and realized t as the labeled contrast (see Measurement choices).
- **Volatility ≠ idiosyncratic risk:** a high-vol LS portfolio can be high-beta rather than high-idio. Accepted as a proxy limitation; wording of conclusions will say "strategy volatility," not "arbitrage cost," unless the sign pattern earns it.
- **Weighting heterogeneity:** 184/212 predictor portfolios are equal-weighted, 28 value-weighted; vol and decay both depend on weighting. Reported as a descriptive check, not a spec.

## Required data
Already cached: `datasets/raw/PredictorPortsFull.parquet`, `SignalDoc.csv` (provenance `datasets/chen_zimmermann_oct2025.md`). No new data.

## Estimates
Difficulty: low-moderate (the panel machinery exists; the subtlety is all in measurement validity). Novelty: low as replication (M&P did the core test), moderate as extension (212 predictors, OP-t vs realized-t contrast, citations, event-time framing). Expected failure probability: ~25% on P1's significance, ~35% on P2's range, ~40% on P3. Learning value: high per unit effort — this is the researcher's first meeting with *interaction terms as mechanism tests* and with post-treatment bias.

## Internal debate (condensed)
- **Statistician:** "Your 'exogenous' OP t-stat is selected on crossing a threshold — conditioning on publication truncates the luck distribution, so P1 confirms bias-plus-correction jointly, not arbitrage alone." — Accepted; P1's interpretation is written as the joint channel, and the vol interaction (P2) carries the discriminating weight.
- **Skeptic:** "P2's range [−0.05, +0.25] is wide. Is it a prediction or an alibi?" — The floor is the content: shrinkage-dominance predicts clearly negative; ruling that out is a real bet after EXP-002 P4, and the registered failure line (−0.15, |t|≥2) can be hit.
- **Economist:** "Citations measured in 2025 are an outcome, not a treatment. Why include them at all?" — Because no one else can either (M&P predate the citation explosion), and a *null* would also be informative. Kept, but demoted to exploratory and fenced with the post-treatment caveat in every mention.
- **Mentor:** "Richard's EXP-004 question is whether correlation with predictors drags placebos down. This experiment quietly estimates the predictor-side analogue — whether capital chases strength. Write the digest so it sharpens his spillover intuition without answering his worksheet for him." — Adopted; the digest's prediction question is chosen accordingly.

## Connections
`hypotheses/HYP-001-decay-replication.md` (baseline effect) · `hypotheses/HYP-002-placebo-decay.md` (P4 shrinkage evidence) · `hypotheses/HYP-003-calendar-vs-event-time.md` (era controls reused) · `papers/2016-mclean-pontiff-does-academic-research-destroy-predictability.md` · → `experiments/EXP-005-decay-heterogeneity/design.md` · feeds `experiments/EXP-004-placebo-spillover/` (mechanism side-view) · `knowledge_graph/anomaly-decay-thread.md`
