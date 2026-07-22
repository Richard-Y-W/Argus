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
                                               [EXP-004: correlation spillover proxy] ✗
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
                                                       │
                                                       ▼
                                               [EXP-010: paired EW/VW decay] ✗
                                                       │
                                                       ▼
                                               [EXP-013: world-ex-US transport] ✗
                                                       │ comparability attacked by
                                                       ▼
                                               [EXP-014: 1986 coverage floor] ✗
                                               [EXP-015: JKP world vs ex-US] ✓ bounded
                                                       │ direct US repair
                                                       ▼
                                               [EXP-016: standalone JKP US] ✗
                                                       │ return association hardened by
                                                       ▼
                                               [EXP-017–019: dependence, timing,
                                                and breadth robustness] ✓
                                               [EXP-020: equal-factor estimand] ✓
                                               [EXP-021: single-factor influence] ✓
```

## Edge notes

- Researcher prior → M&P: prior predicted full decay; evidence shows partial → prior revised to "correction bounded by arbitrage costs."
- M&P → EXP-001: replication successful; our post-sample estimate (37%) sits at J&M's US number rather than M&P's 26% → decay magnitude is design-dependent (predictor set, window dating).
- C&Z placebos → EXP-002: the unused control group in the public data; sharpest cheap test available to this lab.
- EXP-001 → EXP-002 (2026-07-11): control-group test passed — placebos show no post-sample decline and only −0.11%/mo post-publication drift; DiD γ₂ = −0.26 (t = −3.3) makes the decay predictor-specific. Failed side-prediction P4: screening placebos on positive long-sample mean does *not* induce post-sample decay → the selection that inflates published results operates through t-stat/specification search, not simple mean conditioning.
- EXP-002 → EXP-003: the placebo post-publication drift is an upper bound on a common calendar-time trend (−0.11 of predictors' −0.37); separating event time from calendar time is now the binding threat to the causal story.
- EXP-003 (2026-07-11): the threat is retired — 88% of the publication effect survives era controls; identification via staggered publication years. CST 2014's decimalization attenuation is reframed: in their pre-2001-published anomaly set, calendar break ≡ event time; with staggering, the era effect is +0.02 (t = 0.1). New facts: decay is flat in event time (arrives ≤5y, stays); the only significant era effect is *positive* (1993–2000, +0.22); 2020–24 revival is calendar-shaped but marginal (t = 1.8).
- EXP-003 → EXP-004 (2026-07-14): correlation-sorted placebo spillover rejected. Raw high-minus-low exposure decline (−0.184%/mo) was absorbed by in-sample scale; primary exposure −0.014 (t=−0.41), future-predictor negative control fired, and composite exposure reversed sign. Return correlation is too ambiguous; quantity/holdings evidence is required.
- EXP-003 → EXP-005 (2026-07-12): first rejected hypothesis. Registered heterogeneity tests "passed" (pp × OP-t −0.151, t = −5.1) but a labeled post-hoc showed all characteristic interactions are absorbed by pp × in-sample mean (−0.247, t = −5.2): decay is a ~50% proportional haircut, not characteristic-targeted. Realized-t interaction (−0.201) > OP-t interaction (−0.151) — the ordering shrinkage predicts. Citations interaction *positive* (t = 1.7): famous factors endure, post-treatment caveat both ways. Method lesson of record: levels-interactions confound rate with scale; a registered pass is not a mechanism.
- EXP-005 → EXP-004: placebos have no in-sample edge, so the scale result predicts ~zero placebo decay from shrinkage alone — any drift concentrated in predictor-correlated placebos becomes cleanly attributable to spillover. The researcher's worksheet question is now sharper than when it was posed.
- EXP-005 → M&P re-read flag: their Tables 5–6 heterogeneity (higher in-sample return/t → more decay) may be the same scale confound; check whether they control for in-sample mean when interacting.
- EXP-005 → EXP-006 (2026-07-14): sample length fails as a cheap shrinkage discriminator. Retention-length slope +0.033 (t=0.90); long histories retain 8.1 points less, not 10 points more. This rejects the prediction, not shrinkage in general.
- EXP-005 → EXP-007 (2026-07-14): newest cohort raw decay exceeds oldest by 19.5 points, but the primary controlled year slope is negative and insignificant and robustness signs conflict. Equal-60-month evidence is positive (t=2.45). Filed as not supported/inconclusive.
- EXP-004 → EXP-008 (2026-07-14): direct predictor-composite crowding also fails. Mean correlation change −0.024 (t=−0.98); 120-month change is significantly negative. Registered placebo control was infeasible, so the design is not confirmatory.
- EXP-005 → EXP-009 (2026-07-14): raw VW decay 94.7% versus EW 56.4%, but adjusted VW coefficient +0.152 (t=0.50). Requires within-signal alternative portfolios; between-signal weighting labels are composition-confounded.
- EXP-009 → EXP-010 (2026-07-15): official alternative portfolios remove between-signal composition, but the paired VW-minus-EW decay difference (+0.141, t=1.76) misses the registered inference rule. The levels DiD has the wrong sign and positive breadth is exactly 50%. Weighting remains an unstable proxy; seek direct quantities or external replication.
- EXP-010 → EXP-013 (2026-07-16): JKP world-ex-US external replication rejects transport of the strong US magnitude. Post-publication decay is -0.037 percentage points per month (t=-0.55); the negative second-step contrast is suggestive but its registered joint rule fails.
- EXP-013 → EXP-014 (2026-07-17): imposing JKP's 1986 coverage floor on C&Z strengthens decay from -0.369 to -0.415, firing the falsifier. Simple time-axis truncation cannot explain the external gap.
- EXP-013 → EXP-015 (2026-07-17): with JKP construction fixed, world decay (-0.096, t=-2.17) exceeds world-ex-US (-0.037, t=-0.55). Registered rules pass, but the paired world-minus-ex-US gap has t=-1.27. Evidence is consistent with US concentration, not decisive geography or arbitrage identification.
- EXP-015 → EXP-016 (2026-07-18): standalone JKP US decay is strong (-0.164 pp/month, t=-2.97), but the direct US-minus-world-ex-US gap remains imprecise (-0.131, t=-1.45) and fails its registered rule. Construction mismatch is a weaker explanation; geography is still not statistically distinguished.
- EXP-016 → EXP-020/021 (2026-07-21): equal factor weighting retains -0.154 pp/month decay with 70.9% negative contrasts, and every single-factor deletion leaves the pooled coefficient between -0.170 and -0.159. Unequal histories and single-factor dominance are rejected as explanations; correlated families and direct trading quantities remain unresolved.
