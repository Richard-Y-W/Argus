# 2026-07-16 — Search breadth and the consumable holdout

Two AI-led cycles completed the queued regime-filter calibration branch without making a market claim.

EXP-011 mapped the best-of-noise effect across a preregistered search grid. The naive one-sided pass rate rose from 5.36% with one candidate to 99.99% with 200, while the selected candidate's independent test statistic stayed centered at zero. The lesson is sharper than “overfitting is bad”: the number of attempted variants belongs beside the reported statistic.

EXP-012 tested the governance consequence. After train-sample selection, treating a favorable validation result as a claim produced a 5.145% false claim rate under the complete null. Requiring an untouched confirmation pass reduced that to 0.274%, a 94.67% reduction. The word “untouched” carries the result. If the lab modifies the strategy after inspecting confirmation, the protection is spent.

Both hypotheses survived, but they are intentionally modest. Independent Gaussian statistics make the answer nearly analytic and omit candidate dependence, fat tails, adaptive search, and power. These cycles improve the lab's process discipline; they do not expand its evidence about publication decay or tradability. The next claim-bearing priority remains direct trading quantities or a second market/data family.

## Human growth digest

- **Concept:** a holdout is consumed when it influences model choice, even if no parameter is fit on it.
- **Quantitative anchor:** the maximum of 200 null z-statistics averaged 2.75 in EXP-011.
- **Mistake to avoid:** reporting the best strategy's ordinary p-value as though it were the only strategy tried.
- **Question to carry forward:** how should effective search breadth be measured when candidate strategies are strongly correlated?

## Connections

EXP-011 · EXP-012 · `knowledge_graph/data-snooping-thread.md` · `researcher_scorecard.md`
