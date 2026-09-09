# Biotech alpha candidates: literature and data lineage

**Stage:** scouting and prioritization  
**Decision:** replicate failure reversal first; develop scientific-quality drift second

## Primary findings inspected

- Overgaard et al. (2000), DOI 10.1177/108155890004800207, report +27% versus -4% average price changes from days -120 to -3 for Phase III winners and losers across 98 products. The paper interprets this as indirect evidence of insider trading; it does not show that public signals generated the divergence.
- Singh et al. (2022), DOI 10.1371/journal.pone.0272851, analyze 13,807 outcomes and find large residual variation after trial properties and sponsor classification. This supports an omitted-feature question, not predictability.
- Hwang (2013), DOI 10.1371/journal.pone.0071966, finds asymmetric immediate reactions in 24 large-firm events and notes that negative effects persisted longer than positive effects.
- Sahin et al. (2025), DOI 10.1016/j.frl.2025.108139, report underreaction to large-firm failures, overreaction to small-firm failures, and a roughly 40–50% 100-day strategy return in 92 Phase III events. The magnitude and long window make exact replication, delisting treatment, and execution accounting mandatory.
- The 2024 PLOS biopharma-news study, DOI 10.1371/journal.pone.0296927, reports stronger biotech sensitivity and possible leakage in longer clinical-news windows, reinforcing the need for exact announcement timestamps and short horizons.
- Alliance research covering 276 biotech-pharma codevelopment agreements finds returns vary with governance, partner capability, and competitive environment. Alliance presence alone is therefore an inadequate construct.

## Public data routes

- SEC EDGAR submission APIs provide real-time filing histories for 8-K, 6-K, 10-Q, 10-K, and ownership forms without API keys. They can anchor announcement, agreement, financing, and Form 4 availability.
- ClinicalTrials.gov provides current public study data with daily weekday refreshes. Historical versions remain necessary for registry-derived predictors.
- FINRA short interest is a twice-monthly position snapshot with a publication lag; daily short-sale volume is a different object and must not be substituted.
- Survivorship-safe returns, delisting returns, historical market capitalizations, option quotes, and borrow costs remain unresolved acquisition requirements.

## Multiple-testing boundary

The eight candidate families are a scouting menu. They are not eight independent chances to discover significance. Only failure reversal and scientific-quality drift are promoted for sequential design. A later registration must allocate an untouched period and specify how the second test proceeds conditional on the first.

## Connections

`ideas/2026-08-21-biotech-alpha-candidate-map.md` · `papers/2022-singh-et-al-clinical-trial-stock-reactions.md` · `datasets/hwang_2013_clinical_events.md`

