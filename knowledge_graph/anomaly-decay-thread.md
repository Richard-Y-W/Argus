# Knowledge graph: anomaly-decay thread

*Started 2026-07-10. Nodes and edges of the lab's first research thread.*

```
[researcher prior: markets patch holes]  (ideas/2026-07-09-anomaly-decay-prior.md)
        │ tested by
        ▼
[M&P 2016: 26% OOS / 58% post-pub, partial]───────────┐
        │ bias channel formalized by                   │ replicated by
        ▼                                              ▼
[HLZ 2016: multiple testing, t>3]              [EXP-001: 37% / 55%, post-pub 0.33%/mo > 0] ✓
        │ challenged by                                │ enabled by
        ▼                                              ▼
[J&M 2020: decay US-only]                      [C&Z 2022 open data, Oct 2025 release]
        │                                              │
        ▼                                              ▼
[Q: why US-only?] (questions/)                 [EXP-002: placebo decay] ✓
                                                       │ residual placebo drift −0.11 escalates
                                                       ▼
                                               [EXP-003: calendar vs event time] ✓ partial
                                                       │ event time wins; CST reframed;
                                                       │ placebo drift still unresolved
                                                       ▼
                                               [EXP-004 candidate: spillover — placebo decay
                                                vs correlation with published predictors]
                                               [candidate: event-time profile, SSRN dates]
                                               [2020–24 revival: calendar-shaped per EXP-003
                                                P3 (+0.22, t=1.8) — weakly resolved]
                                                       │
                                                       ▼
                                               [EXP-005: which predictors decay?] ✗ rejected
                                                       │ decay ∝ in-sample scale (~50% haircut);
                                                       │ no characteristic-specific mechanism
                                                       ▼
                                               [candidate: sample-length sort — split
                                                proportional arbitrage from shrinkage]
                                               [candidate: VW/EW correction gap, registered,
                                                C&Z alt ports (descriptive: 94% vs 55%)]
                                                       │
                                                       ▼
                                               [EXP-006: sample-length discriminator] ✗
                                               [EXP-007: cohort strengthening] ?/✗
```

## Edge notes

- Researcher prior → M&P: prior predicted full decay; evidence shows partial → prior revised to "correction bounded by arbitrage costs."
- M&P → EXP-001: replication successful; our post-sample estimate (37%) sits at J&M's US number rather than M&P's 26% → decay magnitude is design-dependent (predictor set, window dating).
- C&Z placebos → EXP-002: the unused control group in the public data; sharpest cheap test available to this lab.
- EXP-001 → EXP-002 (2026-07-11): control-group test passed — placebos show no post-sample decline and only −0.11%/mo post-publication drift; DiD γ₂ = −0.26 (t = −3.3) makes the decay predictor-specific. Failed side-prediction P4: screening placebos on positive long-sample mean does *not* induce post-sample decay → the selection that inflates published results operates through t-stat/specification search, not simple mean conditioning.
- EXP-002 → EXP-003: the placebo post-publication drift is an upper bound on a common calendar-time trend (−0.11 of predictors' −0.37); separating event time from calendar time is now the binding threat to the causal story.
- EXP-003 (2026-07-11): the threat is retired — 88% of the publication effect survives era controls; identification via staggered publication years. CST 2014's decimalization attenuation is reframed: in their pre-2001-published anomaly set, calendar break ≡ event time; with staggering, the era effect is +0.02 (t = 0.1). New facts: decay is flat in event time (arrives ≤5y, stays); the only significant era effect is *positive* (1993–2000, +0.22); 2020–24 revival is calendar-shaped but marginal (t = 1.8).
- EXP-003 → EXP-004 candidate: placebo drift survived in point estimate (−0.09) but not significance under era controls — spillover vs noise is unresolved; the discriminating design is correlation-sorted placebo decay.
- EXP-003 → EXP-005 (2026-07-12): first rejected hypothesis. Registered heterogeneity tests "passed" (pp × OP-t −0.151, t = −5.1) but a labeled post-hoc showed all characteristic interactions are absorbed by pp × in-sample mean (−0.247, t = −5.2): decay is a ~50% proportional haircut, not characteristic-targeted. Realized-t interaction (−0.201) > OP-t interaction (−0.151) — the ordering shrinkage predicts. Citations interaction *positive* (t = 1.7): famous factors endure, post-treatment caveat both ways. Method lesson of record: levels-interactions confound rate with scale; a registered pass is not a mechanism.
- EXP-005 → EXP-004: placebos have no in-sample edge, so the scale result predicts ~zero placebo decay from shrinkage alone — any drift concentrated in predictor-correlated placebos becomes cleanly attributable to spillover. The researcher's worksheet question is now sharper than when it was posed.
- EXP-005 → M&P re-read flag: their Tables 5–6 heterogeneity (higher in-sample return/t → more decay) may be the same scale confound; check whether they control for in-sample mean when interacting.
- EXP-005 → EXP-006 (2026-07-14): sample length fails as a cheap shrinkage discriminator. Retention-length slope +0.033 (t=0.90); long histories retain 8.1 points less, not 10 points more. This rejects the prediction, not shrinkage in general.
- EXP-005 → EXP-007 (2026-07-14): newest cohort raw decay exceeds oldest by 19.5 points, but the primary controlled year slope is negative and insignificant and robustness signs conflict. Equal-60-month evidence is positive (t=2.45). Filed as not supported/inconclusive.
