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
                                               [EXP-003: calendar time vs event time]
                                               [candidate: event-time profile, SSRN dates]
                                               [candidate: 2020–24 revival observation]
                                               [candidate: spillover — placebo decay vs
                                                correlation with published predictors]
```

## Edge notes

- Researcher prior → M&P: prior predicted full decay; evidence shows partial → prior revised to "correction bounded by arbitrage costs."
- M&P → EXP-001: replication successful; our post-sample estimate (37%) sits at J&M's US number rather than M&P's 26% → decay magnitude is design-dependent (predictor set, window dating).
- C&Z placebos → EXP-002: the unused control group in the public data; sharpest cheap test available to this lab.
- EXP-001 → EXP-002 (2026-07-11): control-group test passed — placebos show no post-sample decline and only −0.11%/mo post-publication drift; DiD γ₂ = −0.26 (t = −3.3) makes the decay predictor-specific. Failed side-prediction P4: screening placebos on positive long-sample mean does *not* induce post-sample decay → the selection that inflates published results operates through t-stat/specification search, not simple mean conditioning.
- EXP-002 → EXP-003: the placebo post-publication drift is an upper bound on a common calendar-time trend (−0.11 of predictors' −0.37); separating event time from calendar time is now the binding threat to the causal story.
