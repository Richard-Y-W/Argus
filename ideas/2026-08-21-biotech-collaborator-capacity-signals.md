# Biotech collaborator and capacity signals

**Origin:** Richard proposed looking through collaborators for early operational evidence such as syringe purchases, insurance changes, or other preparation before a clinical announcement.  
**Stage:** exploration and measurement design; no registered hypothesis, return test, or alpha claim

## Sharpened question

Do costly, asset-specific commitments by an outside organization, publicly observable before a pivotal readout, predict clinical success beyond a frozen phase-by-disease base rate?

The testable object is not “any collaborator activity.” It is a public commitment that is difficult to reverse, tied to one medical asset, made by an entity other than the sponsor, and available far enough before the readout to be actionable.

## Candidate signals

| Signal | Interpretation | Main alternative explanation | Initial priority |
|---|---|---|---|
| Asset-specific manufacturing or fill-finish expansion | Outside party commits scarce capacity after technical diligence | Manufacture-at-risk preserves an option; sponsor may reimburse it | High |
| Asset-specific government award or amendment | Public agency shares development or scale-up risk | Preparedness and political demand, not efficacy belief | Medium-high |
| New trial collaborator on a historical registry version | Another institution contributes expertise or resources | Routine trial administration; relationship may predate the visible update | Medium |
| Milestone-bearing license or co-development agreement | Counterparty pays for conditional rights | Deal may reflect commercial fit rather than clinical confidence | High |
| Generic syringes, needles, vials, or cold-chain procurement | System-level preparation for expected demand | Supports multiple candidates and says little about which one succeeds | Negative control / low |
| Insurance disclosure or coverage limit | Potential operational scale or perceived liability | Annual boilerplate, renewal timing, and weak asset specificity | Deprioritized |

## Candidate D — costly external commitment

Let `commitment=1` when at least one independently sourced, costly, asset-specific external commitment becomes public 30–365 calendar days before the readout. Compare its out-of-sample clinical-outcome information with a phase-by-disease base-rate model.

- Primary estimand: change in log loss on untouched events.
- Secondary estimand: calibration slope and Brier-score change.
- Falsifier: no improvement on untouched events, or improvement disappears after COVID, sponsor size, phase, disease area, public funding, and scheduled-readout controls.
- No stock returns are inspected during the feasibility and outcome-prediction stages.

## Candidate E — independent corroboration

Test whether two or more independently published signal families add outcome information beyond one signal. Independence requires different publishing organizations and different underlying commitments; repeated press coverage of one agreement is one signal.

This candidate remains secondary because multi-node corroboration is sparse and invites researcher flexibility.

## Candidate F — collaborator spillovers

Separately ask whether a publicly traded supplier or licensee reprices around the sponsor's readout. This is an event-exposure question, not an early-signal test, and must not be mixed with Candidate D.

## Smallest credible pilot

Construct a return-blind, balanced gold ledger of 30 Phase III readouts, including failures and discontinued or acquired sponsors. For each event:

1. Freeze the readout timestamp and historical sponsor/security lineage.
2. Search only prespecified public source families.
3. Record publication time, availability precision, underlying action date, asset specificity, payer, amount/capacity, reversibility, and source hash.
4. Dual-code whether the signal satisfies the costly external commitment rule.
5. Compare the frozen indicator with the clinical outcome using leave-one-event-out predictions against phase-by-disease base rates.

Thirty events can establish feasibility and coding reliability; it cannot support a tradable claim. A larger development sample and untouched confirmation cohort would still be required.

## Stop rules

- Stop if historical public availability cannot be bounded for at least 80% of candidate signals.
- Stop if asset mapping agreement is below 90% under dual coding.
- Stop if fewer than 10 events in the pilot contain a qualifying commitment; the proposed test would be too sparse.
- Do not create a learned composite score, select windows from returns, or interpret Moderna/COVID as confirmation.

## Current judgment

Building the source ledger is feasible. Predictive value is unknown. Generic syringe procurement is best treated as a preparedness control, and insurance is not currently a credible early signal. The leading hypothesis is the narrower costly, asset-specific, externally made commitment.

