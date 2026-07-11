# HYP-003 — Publication decay survives calendar-time controls; the 2020–24 revival is a calendar effect

*2026-07-11. Status: accepted for testing → EXP-003.*

## Title
The post-publication decline in predictor returns is primarily an event-time (years-since-publication) phenomenon that survives controlling for calendar eras; calendar eras additionally matter, including a positive 2020–2024 era effect.

## Motivation
Both completed experiments leave the same confound standing. EXP-001: post-publication windows cluster in recent calendar decades, so a secular decline in all characteristic returns (Chordia–Subrahmanyam–Tong 2014: anomaly profits halved after 2001 decimalization) could masquerade as a publication effect. EXP-002 bounded the confound — placebos exposed to the same eras drifted only −0.11 %/mo vs predictors' −0.37 — but did not decompose it. The C&Z panel is unusually well suited to the decomposition: publication years are staggered across five decades, so different predictors experience the same era at different event times.

## Prior literature
CST 2014 (calendar story: decimalization, arbitrage capital); M&P 2016 (their robustness includes time controls and the publication effect survives — on their sample and dating); Brogaard–Nguyen–Putniņš–Zhang 2023 WP (both channels contribute); EXP-001/EXP-002 (this lab's estimates).

## Expected mechanism
Publication releases signal-specific information → decay aligned to each predictor's own clock. Era forces (tick size, hedge-fund AUM, quant capital) compress all cross-sectional spreads → decay aligned to the calendar. Both operate; the question is whether the publication effect survives at meaningful size once eras are absorbed.

## Identification caveat (stated up front)
Event time = calendar year − publication year. With signal fixed effects (cohort), event-time and calendar effects are identified only through coarse binning — the age-period-cohort problem. We register the bins in the design and do not refine them after seeing results. Estimates are interpretable under the maintained assumption that era effects are constant within bins.

## Falsifiable predictions (registered before running)
P1. The post-publication coefficient survives era controls: β_pp remains negative with t ≤ −2, at 40–100% of its uncontrolled level (−0.37 %/mo from EXP-002's benchmark run).
P2. Era effects exist: the 2001–2010 era coefficient is negative and significant (t ≤ −2) relative to the pre-1993 base, conditional on window dummies (CST attenuation).
P3. The 2020–2024 revival flagged in EXP-001 (R4) is a calendar effect: the 2020–24 era coefficient exceeds the 2011–19 era coefficient, conditional on event time.
P4 (direction only). Within post-publication event time, decay deepens then flattens: the 6–10-years-after bin is at least as negative as the 1–5-years bin.
P5 (falsifier). If β_pp shrinks to insignificance (|t| < 1) under era controls, the publication-timing interpretation of EXP-001 fails and the thread's causal story must be rebuilt around era forces — despite the placebo evidence, which would then need a spillover-free explanation.
P6 (cross-experiment consistency). Era controls should absorb the *placebo* post-publication drift: placebo β_pp with era dummies moves toward 0 (|β| < 0.08). If it does, EXP-002's residual drift was calendar, not spillover.

## Alternative explanations to guard against
- **Bin artifacts:** era cut points chosen to flatter the hypothesis. Mitigation: cuts fixed now (1993 / 2001 / 2011 / 2020) on external grounds (quant expansion; decimalization per CST; post-GFC quant boom; COVID/meme), plus a registered alternative binning (5-year bins from 1990) and a linear-trend variant.
- **Composition:** later eras contain more (and weaker) recently published predictors; signal FE handle level composition, but era coefficients still average over a changing mix. Report predictor counts per era.
- **Publication-year measurement error** (annual dating) — attenuates event-time estimates, as in EXP-001/002.

## Required data
Already cached: predictor + placebo panels and SignalDoc (provenance `datasets/chen_zimmermann_oct2025.md`). No new data.

## Estimates
Difficulty: moderate (design subtleties, APC identification). Novelty: moderate-high — M&P do a trend control, CST do a break, but an event-time × era decomposition on 212 predictors with a placebo cross-check is not something we've seen published. Expected failure probability: ~30% on magnitudes (P1's 40% floor is a real bet), ~15% that P3 reverses. Learning value: high — the researcher meets the age-period-cohort problem, which recurs everywhere in finance panels.

## Internal debate (condensed)
- **Statistician:** "Age-period-cohort is fundamentally unidentified; you're selling bin restrictions as identification." — Adopted into the caveat paragraph and the alternative-binning robustness; conclusions will be worded as 'under the registered binning.'
- **Skeptic:** "P1's range (40–100%) is wide enough to be unfalsifiable." — Response: the floor is the bet; CST's halving-after-2001 view predicts eras absorb most of it (< 40% survives). The falsifier P5 has real bite, and P6 can genuinely embarrass EXP-002's spillover reading.
- **Economist:** "The 2020–24 revival could be event-time too — old anomalies mean-reverting after being over-arbitraged." — Noted; P3 tests calendar-conditional-on-event-time, which is the right conditional for that debate.
- **Mentor:** "This is the researcher's digest question from EXP-002 answered by machine before he answers it himself. Keep his question open by writing the digest around *how* to tell the stories apart, not just the answer." — Adopted.

## Connections
`experiments/EXP-002-placebo-decay/results.md` (motivating residual) · `papers/2014-chordia-subrahmanyam-tong-anomaly-attenuation.md` · `papers/2016-mclean-pontiff-does-academic-research-destroy-predictability.md` · → `experiments/EXP-003-calendar-vs-event-time/design.md` · `knowledge_graph/anomaly-decay-thread.md`
