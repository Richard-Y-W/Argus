# Financial genetics thread

## Research lineage

Richard's financial-DNA proposal separates four objects:

`genome specification -> expressed portfolio phenotype -> environmental selection -> inherited mutation`

The prior-art audit found that evolutionary search, artificial immune systems, and adaptive policy libraries already cover many individual components. The potentially useful contribution is an auditable system in which ancestry, mutation budgets, phenotype diversity, and system-level fitness remain explicit.

## Current evidence

- `HYP-025` registered the first minimal vertical slice.
- `EXP-025` found lower regret from local mutation in one untouched synthetic family but rejected the joint recovery hypothesis.
- Local mutation reduced normalized genome diversity from 0.808 under random restart to 0.213, exposing premature convergence as the next central problem.
- EXP-011/012 establish why every genome evaluated must remain in the search ledger and why untouched confirmation is necessary.
- `EXP-026` rejected a fixed 75% descendants / 25% immigrants hybrid with four phenotype-diversity reserve slots. The reserve raised phenotype diversity by at least 2.37x in every family but significantly underperformed random restart on pooled full-year return.

## Live discriminating question

Can a preregistered environmental-distance gate decide when to use local inheritance, mixed search, dormant memory, or global restart better than any fixed search policy?

The current mechanism map is:

`environmental similarity -> useful inheritance radius -> mutation/global-search allocation -> population phenotype`

EXP-025 suggests local inheritance can help after a related transition; EXP-026 shows that unconditional mixed inheritance is inadequate across large structural breaks. This contrast is hypothesis-generating, not a registered cross-experiment estimate.

`EXP-027` then rejected a generic causal environment-distance gate. The score increased across intended severity and isolated the correlation-break family, but failed every performance, routing, and tail-risk prediction. The missing estimand is not distribution distance; it is the **decision value of inheritance for a particular genome and phenotype**.

Program stop: do not tune more thresholds or component weights on EXP-025–027's consumed synthetic families. Resume only with an externally specified benchmark or point-in-time historical validation.

No market, alpha, or literal biological claim currently survives.
