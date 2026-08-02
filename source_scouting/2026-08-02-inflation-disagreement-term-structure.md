# Scout report — inflation-disagreement term structure

*Scouted 2026-08-02. AI-led macro/quant discovery cycle. No asset-pricing claim is made.*

## Question

Does the *shape* of disagreement across inflation forecast horizons contain information distinct from consensus inflation expectations, and is that information robust to forecaster composition and probability-bin conventions?

The question is attractive because it connects expectations formation to yields and monetary transmission without requiring rapid execution.

## Prior evidence

- The Philadelphia Fed's Survey of Professional Forecasters (SPF) provides historical individual responses, consensus measures, dispersion, and probability forecasts. It is an unusually transparent public panel, but respondent identifiers are confidential codes and participation changes over time ([SPF data portal](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters)).
- Sill documents substantial SPF forecast dispersion and reviews explanations based on heterogeneous models and information processing ([Philadelphia Fed review](https://www.philadelphiafed.org/the-economy/macroeconomics/forecast-disagreement-in-the-survey-of-professional-forecasters)).
- Cumings-Menon, Shin, and Sill introduce Wasserstein disagreement measures for probabilistic and density forecasts, directly addressing the information lost by comparing point forecasts alone ([Philadelphia Fed WP 21-03](https://www.philadelphiafed.org/the-economy/monetary-policy/measuring-disagreement-in-probabilistic-and-density-forecasts)).
- Barbera, Xia, and Zhu study the term structure of inflation-forecast disagreement and report that cyclical disagreement changes monetary-policy transmission to financial markets ([BIS Working Paper 1114](https://www.bis.org/publ/work1114.htm)).
- Crump, Eusepi, and Moench combine professional forecasts with bond yields and find that term premiums explain much of yield variation, underscoring that disagreement should not be conflated with mean rate expectations ([New York Fed Staff Report 775](https://www.newyorkfed.org/research/staff_reports/sr775.html)).

The core economic claim is therefore occupied. A defensible new contribution would be a measurement and composition audit, possibly followed by external replication—not a regression of yields on one dispersion series.

## Candidate designs

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Composition-robust disagreement curve | 5 | 5 | 4 | 4 | 5 | 3 | Highest macro priority |
| Density-versus-point disagreement comparison | 5 | 5 | 3 | 4 | 5 | 2 | Natural companion |
| Disagreement predicts bond excess returns | 5 | 5 | 2 | 3 | 4 | Defer; occupied/mining risk |
| Disagreement conditions policy-shock transmission | 5 | 3 | 3 | 5 | 5 | 4 | Defer until shock audit |

## Proposed narrow hypothesis

The slope and curvature of the SPF inflation-disagreement curve will survive controls for the consensus forecast but weaken materially after correcting for panel entry, exit, and horizon-specific response selection.

The falsifier is stability of the disagreement curve under a balanced-panel or inverse-response-probability protocol. The design must freeze eligible horizons, distinguish point and density disagreement, retain empty/missing responses, and avoid using future forecast accuracy to weight forecasters. Bootstrap units should preserve forecaster and survey-date dependence.

## Internal debate

- **Optimist:** This is public, conceptually rich, and sized for a first serious panel-data project.
- **Skeptic:** Composition adjustment may be useful housekeeping rather than publishable novelty.
- **Statistician:** Unbalanced participation is endogenous; balanced panels may select persistent institutions. Report multiple estimands rather than declaring one correction true.
- **Economist:** Disagreement can reflect private information, model heterogeneity, stale forecasts, or genuine uncertainty. It is not automatically “de-anchoring.”
- **Portfolio manager:** Even robust disagreement is not a trade. Any later return test needs a frozen release calendar, contemporaneous yields, costs, and a separate holdout.
- **ML researcher:** Wasserstein geometry is justified for density forecasts; embeddings or neural aggregation add no identification at this stage.

## Promotion gate

This is the strongest candidate, but do not register before an SPF schema audit. Promotion requires verified historical availability for at least three comparable inflation horizons, documented respondent-code continuity, and a deterministic rule for probability-bin changes. If those conditions pass, this should receive the next experiment ID ahead of the other three macro branches.

## Connections

`literature_reviews/2026-08-02-macro-quant-research-map.md` · `ideas/hypothesis_queue.md` · `research_journal/2026-08-02-four-macro-quant-discovery-cycles.md`
