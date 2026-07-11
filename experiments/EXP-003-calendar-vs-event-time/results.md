# EXP-003 — Results: Calendar-time vs event-time decomposition

*Run 2026-07-11. Design registered before analysis in `design.md`; predictions in `hypotheses/HYP-003-calendar-vs-event-time.md`. Status: **partially supported — P1 and P3 pass, P2 fails (informatively), P4 and P6 fail narrowly; the falsifier P5 does not fire.** The headline claim — publication decay survives calendar controls — passes more strongly than registered; the secondary claim — calendar eras independently depress returns — is rejected.*

## Headline result (E1: 212 predictors, 136,338 predictor-months, signal FE, month-clustered SEs)

| Term | No era controls | With era controls | Registered | Verdict |
|---|---|---|---|---|
| Post-sample β₁ | −0.247 (t = −3.85) | −0.249 (t = −4.26) | — | unchanged |
| Post-publication β₂ | −0.369 (t = −6.49) | **−0.325 (t = −2.97)** | ≤ −0.148, t ≤ −2 | **P1 ✓** (88% survives) |
| Era 1993–2000 | | **+0.224 (t = 2.49)** | not registered | surprise, see below |
| Era 2001–2010 | | **+0.019 (t = 0.13)** | ≤ 0, t ≤ −2 | **P2 ✗** |
| Era 2011–2019 | | −0.101 (t = −0.87) | — | — |
| Era 2020–2024 | | +0.118 (t = 0.77) | — | — |
| Era 2020–24 minus 2011–19 | | **+0.219 (se 0.121, t = 1.81)** | > 0 (direction only) | **P3 ✓** (marginal) |

Robust across R1 (5-year bins: β₂ = −0.294, t = −3.4), R2 (linear trend ≈ 0, β₂ = −0.348), R3 (winsorized: −0.284), R4 (clear-reproduction only: −0.339). Gross of costs throughout.

## What the failures say (they are the interesting part)

**P2 failed — there is no independent decimalization-era effect in this panel.** We predicted, following Chordia–Subrahmanyam–Tong (2014), that 2001–2010 would depress predictor returns conditional on event time. Coefficient: +0.02 (t = 0.13). Proposed reconciliation (post-hoc, labeled as such): CST's 12 anomalies were all published *before* 2001, so in their sample "post-decimalization" and "post-publication event time" are the same regime — they could not separate the two. The C&Z panel staggers publications across five decades, and when both clocks run, **the predictor's own clock wins**. Their attenuation is real; its attribution to liquidity eras looks like publication event time wearing a calendar costume.

**The one significant era effect has the wrong sign for the calendar story:** predictors earned +0.22 %/mo *more* in 1993–2000 conditional on windows — the dot-com-era anomaly heyday, not a decay force. Unregistered observation, flagged not interpreted.

**P4 failed (narrowly): decay is flat in event time, not deepening.** Profile: years 1–5 = −0.33, years 6–10 = −0.31, years 11+ = −0.40 (all t < −2.3; differences tiny vs SEs). We registered gradual deepening (arbitrage capital ramps); the data say the drop arrives within the first five years and roughly stays. Consistent with M&P's own finding that decay is quick.

**P6 failed on its registered magnitude, ambiguously.** Placebo post-publication drift with era controls: −0.094 (registered: |β| < 0.08), but its t drops from −2.55 to −1.18 — no longer distinguishable from zero, yet the point estimate barely moves. Verdict as registered: fail. Honest reading: this experiment cannot adjudicate spillover vs calendar for the placebo drift; the drift is too small relative to its clustered SE once eras soak up degrees of freedom. The spillover question needs its own design (correlation-sorted placebos — EXP-004 candidate).

## Composition caveat (registered)

Era × window cells are unbalanced by construction: pre-1993 months are 94% in-sample; 2020–24 months are 100% post-publication. Era coefficients lean on the staggered middle (1993–2019). The APC identification caveat from HYP-003 travels with every number here: all statements hold *under the registered binning*.

## Interpretation (bounded by what we ran)

The publication effect is not a calendar artifact: 88% of it survives era controls, and no registered calendar variable (2001 break, linear trend, 5-year bins) absorbs meaningful decay. Combined with EXP-002 (placebos don't show the pattern), the McLean–Pontiff causal chain — selection bias post-sample, information release post-publication — now stands on three legs at this lab: replication, control group, and clock decomposition. The 2020–24 revival is calendar-shaped (P3) but weakly estimated; the US-only puzzle and the spillover question remain open.

## Reproducibility

`analysis.py` (deterministic) then `plots.py`. Environment as EXP-001/002. All reported numbers, including the P3 contrast, are produced by the script. Outputs in `results/`.

---

## Five-minute digest for the researcher

1. **The question you were left with (spillover vs calendar) had a testable half, and we tested it.** If "everything just earns less in recent decades," a calendar variable should eat the publication effect. It ate 12% of it. The decay clock starts when *each* predictor's paper is published — different years for different predictors — and no shared era variable can mimic 212 staggered clocks. That's what "identification by staggering" means, and it's the same trick behind modern diff-in-diff designs.
2. **A famous published result got reframed by our panel.** CST (2014) said anomalies halved after decimalization (2001). True in their data — but all 12 of their anomalies were published before 2001, so their calendar break *is* their event time. With staggered publications, the era effect vanishes (+0.02, t = 0.1). Lesson: when two clocks are collinear in a sample, the sample can't tell you which one rings.
3. **Three of six registered predictions failed this cycle** (P2, P4, P6 — plus P4 in EXP-002). None of them broke the main story; all of them taught us something the passes couldn't. A lab where every prediction passes is a lab that isn't betting.
4. **Question to carry forward (this one is yours before EXP-004 runs):** the placebo drift (−0.11) survived era controls in point estimate but lost significance — we still can't tell spillover from noise. Here's the sharper design: placebos differ in how *correlated* they are with published predictors. If arbitrage spillover is real, placebo decay should line up with that correlation; if not, not. **Predict it: will correlation-with-predictors predict placebo decay, and roughly how strongly?** Commit before we run it.

## Connections

`hypotheses/HYP-003-calendar-vs-event-time.md` (P1 ✓ P2 ✗ P3 ✓ P4 ✗ P5 silent P6 ✗) · predecessors: `experiments/EXP-001-anomaly-decay/results.md`, `experiments/EXP-002-placebo-decay/results.md` · `papers/2014-chordia-subrahmanyam-tong-anomaly-attenuation.md` (reframed by this result) · successor candidate: EXP-004 (correlation-sorted placebo spillover) · `knowledge_graph/anomaly-decay-thread.md`
