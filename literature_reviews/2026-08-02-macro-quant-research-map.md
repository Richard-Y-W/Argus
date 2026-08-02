# Macro-quant research map: four routes beyond low latency

*Reviewed 2026-08-02. AI-led synthesis of four discovery cycles; source abstracts, methods pages, and data documentation were screened. This is not a claim of full-paper mastery.*

## Why macro research fits Argus

Macro-quant work does not need to mean predicting the next data release milliseconds before the market. The durable research problems are slower and more structural: reconstructing what was knowable, measuring expectations rather than substituting realized data, separating structural shocks from mixtures, and mapping quantities into risk premia.

The four branches screened here share one discipline:

```text
historical information set
          ↓
measurement of news / beliefs / supply
          ↓
identification against competing mechanisms
          ↓
forecast, yield, or return outcome only after the design is frozen
```

## Comparative assessment

| Branch | Core object | Main skill | Public-data outlook | Identification bottleneck | Priority |
|---|---|---|---|---|---:|
| Inflation-disagreement curve | Distribution of beliefs across horizons | Panel data; density geometry; bootstrap | Strong | Changing respondents and bins | 1 |
| Real-time macro vintages | Historically available releases | Time series; ragged edges; forecast evaluation | Strong | Exact release/vintage mapping | 2 |
| Monetary-policy communication | Announcement shock decomposition | Event studies; factor rotations; local projections | Mixed | Intraday instruments and structural labels | 3 |
| Treasury duration supply | Maturity-weighted privately held risk | Fixed income; duration; state-space models | Moderate | Exogenous issuance expectations | 4 |

The priority ordering reflects research readiness, not presumed economic importance or alpha. SPF and RTDSM offer transparent public panels. The two event-study branches may ultimately be more structurally ambitious, but their decisive inputs—intraday quotes and point-in-time expectations—are harder to verify.

## Cross-cutting literature lesson

Three recurring errors connect otherwise different macro literatures:

1. **Final-data leakage:** revised macro series substitute future information for the historical information set.
2. **Label leakage:** a statistical component receives an economic name after researchers inspect downstream asset or macro responses.
3. **Quantity endogeneity:** observed policy or issuance quantities respond to the same state that moves yields.

These are variants of the same identification failure: conditioning today’s interpretation on information or selection that was not fixed at the decision point.

## Program recommendation

Run a two-stage macro program rather than four simultaneous backtests.

First, audit and acquire SPF and RTDSM. If the SPF schema clears its gate, register a composition-robust inflation-disagreement experiment. In parallel, build a reusable “as-of” data contract that maps every observation to reference period, release timestamp, vintage, and revision status. That infrastructure supports later nowcasting, policy, and bond studies.

Second, treat monetary-policy and Treasury-supply questions as institutional data projects. Their next artifacts should be event inventories and provenance records. Do not approximate missing intraday data with daily closes or missing expectations with realized changes merely to keep the pipeline moving.

## What this cycle did not establish

- No macro variable was shown to forecast an asset return.
- No policy shock was identified.
- No disagreement measure was shown to represent de-anchoring or uncertainty.
- No Treasury supply effect was estimated.
- No novelty claim was established beyond candidate-level gaps.

## Researcher growth digest

- **Concept:** macro data have at least three dates—reference period, release date, and vintage date. A valid backtest must model all three.
- **Mathematics to learn next:** forecast-loss comparison under serial dependence; Wasserstein distance for discrete densities; factor-rotation indeterminacy; bond duration and ten-year equivalents.
- **Design habit:** name the competing mechanism and the observable cross-section that distinguishes it before examining outcomes.
- **Best first implementation:** an SPF schema and panel-composition audit, not a return model.

## Connections

`source_scouting/2026-08-02-real-time-macro-vintages.md` · `source_scouting/2026-08-02-monetary-policy-communication-shocks.md` · `source_scouting/2026-08-02-inflation-disagreement-term-structure.md` · `source_scouting/2026-08-02-treasury-supply-duration-risk.md` · `ideas/hypothesis_queue.md`
