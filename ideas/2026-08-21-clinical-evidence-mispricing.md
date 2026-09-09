# Clinical evidence and discontinuous biotech repricing

**Origin:** Richard observed large vaccine-related stock jumps and proposed medical-research-focused quantitative research. Argus separated predictable scientific information from genuinely new readout information.  
**Stage:** exploration; no return result and no alpha claim

## Candidate A — Pre-readout scientific probability

Can features publicly available before a Phase III readout predict success beyond frozen phase-by-disease base rates?

- Estimand: out-of-sample change in log loss and calibration relative to the base-rate model.
- Falsifier: no improvement on untouched events, or improvement disappears when every feature is timestamp-audited.
- Difficulty/novelty/failure probability: high/high/high.
- Main threat: historical trial records may encode later amendments or results.

## Candidate B — Complexity-conditioned post-readout drift

Conditional on result direction, disclosed effect size and uncertainty, immediate return, firm exposure, liquidity, and confounding news, does announcement complexity predict same-direction CAR over sessions +2 to +20?

- Estimand: complexity coefficient and high-minus-low complexity CAR in a frozen cross-sectional specification.
- Falsifier: coefficient has the wrong sign, is economically negligible, or disappears under exact timestamps and overlapping-event exclusions.
- Difficulty/novelty/failure probability: high/high/high.
- Main threat: complexity is subjective and correlated with bad disclosure, small firms, and low liquidity.

## Candidate C — Exposure explains the jump

Does lead-asset dependence explain immediate absolute repricing beyond trial outcome and firm size?

- Estimand: incremental explanatory power of a point-in-time exposure measure for absolute CAR[0,+1].
- Falsifier: no incremental explanatory power outside company size and development stage.
- Difficulty/novelty/failure probability: medium/low-to-medium/medium.
- Main threat: drug NPV and pipeline dependence are measured with post-event or researcher-imposed assumptions.

## Candidate ranking

Scores are 1–5; higher confounding is worse.

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding |
|---|---:|---:|---:|---:|---:|---:|
| A. Pre-readout scientific probability | 5 | 2 | 4 | 4 | 5 | 5 |
| B. Complexity-conditioned drift | 5 | 3 | 4 | 5 | 5 | 4 |
| C. Exposure explains the jump | 5 | 3 | 2 | 5 | 4 | 4 |

Candidate B is the leading eventual return test because it most directly addresses delayed incorporation. Candidate A is the stronger scientific-information question but requires a more demanding historical evidence reconstruction. Candidate C is a necessary baseline rather than the likely contribution.

## Connections

`source_scouting/2026-08-21-clinical-evidence-mispricing.md` · `papers/2022-singh-et-al-clinical-trial-stock-reactions.md` · `engineering/sandbox/clinical_evidence_mispricing/README.md`
