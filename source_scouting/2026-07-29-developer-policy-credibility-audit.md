# Design audit — developer monetary-policy credibility

*Cycle completed 2026-07-29. AI-led. This is a design and feasibility audit, not an empirical result.*

## Candidate claim

The queued intuition was: virtual-asset prices should react more strongly to supply, sink, tax, or utility announcements when the developer has a history of discretionary reversals. The concept is attractive because a platform operator simultaneously resembles an issuer, fiscal authority, central bank, exchange owner, and rule-maker. That analogy is also the main threat to validity.

## Literature boundary

- Time-consistency and reputation models make credibility an expectations object, not a synonym for good outcomes. Moscarini's competence model likewise separates the authority's information and objectives from public inference ([American Economic Review](https://pubs.aeaweb.org/doi/10.1257/aer.97.1.37)).
- Private e-money theory shows that issuer market power and public monetary policy interact; importing a central-bank model without the issuer's profit and platform objectives would be incomplete ([Bank of Canada](https://www.bankofcanada.ca/2019/01/staff-working-paper-2019-1/)).
- Virtual-economy interventions are already an empirical literature. The Old School RuneScape tax and item-sink study finds heterogeneous effects and demonstrates that a generic “developer shock moves prices” contribution is occupied ([paper](https://arxiv.org/abs/2210.07970)).
- A randomized virtual-currency endowment experiment shows that issuer-controlled currency supply can change money demand, but it relies on private assignment and purchase data unavailable in the candidate public systems ([study](https://pmc.ncbi.nlm.nih.gov/articles/PMC5646808/)).

## Why the original variable is not identified

“History of discretionary reversals” cannot be coded retrospectively by reading only famous policies. Reversals are more likely to be documented when a policy was salient, unpopular, or economically consequential. Coding credibility after viewing prices would add direct outcome leakage. Developer promises also vary in specificity: a dated numerical commitment, a roadmap aspiration, and flavor text are not comparable promises.

Platforms have objectives absent from a standard central-bank setting: engagement, monetization, fraud control, game balance, new-player accessibility, and content cadence. A reversal may reveal low commitment, new information, or a deliberate state-contingent rule. Those mechanisms predict different price responses.

## Prospective measurement protocol

A future test must freeze a promise ledger before outcomes are inspected. Each communication receives the following fields:

1. timestamp and first-party archived text;
2. policy instrument: faucet, sink, tax, supply cap, utility, transfer, or access;
3. numerical and temporal specificity;
4. conditional versus unconditional language;
5. announced implementation date and actual implementation date;
6. direction and affected assets fixed from mechanics, not returns;
7. later fulfillment, delay, parameter drift, reversal, or abandonment;
8. whether the deviation was explicitly state-contingent;
9. concurrent content, monetization, security, or access changes;
10. market observability: quote, fill, volume, depth, inventory, and user flows.

The credibility score at event `t` may use only ledger entries publicly observable before `t`. Suggested components are a trailing fulfillment rate, median implementation delay, numerical-guidance error, and frequency of unexplained reversals. The components must remain separate in primary analysis; a composite score would require weights chosen before price inspection.

## Candidate event families

| Family | Public policy record | Outcome data | Ex ante credibility history | Primary problem | Decision |
|---|---|---|---|---|---|
| EVE resource scarcity and redistribution, 2019–2022 | Detailed first-party outlooks and patch notes; issuer explicitly described scarcity as temporary ([outlook](https://www.eveonline.com/news/view/the-eve-online-ecosystem-outlook2)) | Monthly Economic Reports and market history | Many dated follow-ups can be archived | Bundled economy-wide changes and endogenous feedback | Best public pilot for ledger construction, not yet a causal test |
| EVE Dynamic Bounty System, 2020–2021 | Formula direction and later parameter changes are dated ([launch](https://www.eveonline.com/news/view/concord-introduces-the-dynamic-bounty-system); [parameter update](https://www.eveonline.com/news/view/patch-notes-for-version-18-11)) | System multipliers and activity may be partly observable | Communications frequent | Policy reacts mechanically to player behavior | Use to validate ledger semantics, not price-response credibility |
| OSRS Grand Exchange tax/item sink | Exact implementation and mechanics | Public prices and volume | Polls and news archive may reveal prior commitments | Prior paper already estimates the intervention; few comparable reversals | Low novelty unless promise formation is reconstructed independently |
| Roblox DevEx schedules | Exact issuer-set exchange rates and cohort rules | Creator transactions private | Terms reserve broad discretion | Public market price absent | Partnership-only design |
| WoW Token | Launch and utility expansions documented | Regional quote, no volume | Sparse numerical forward guidance | Platform algorithm sets price | Insufficient public outcomes |
| Second Life fees/KYC | Policy notices and exchange mechanism | Historical LindeX depth uncertain | Communications can be archived | Regulatory shocks and private user assignment | Data inquiry first |

## Falsifiable designs considered

### Cross-platform announcement response

Regress item-level price or volume responses on pre-event issuer credibility. Rejected: platform identity, communication style, market data quality, and asset utility are inseparable from the credibility score; the effective number of issuers would be tiny.

### Within-EVE promise fulfillment and announcement response

Build a timestamped ledger, then compare responses to similarly classified supply/sink announcements over time. This is feasible as a descriptive pilot. It is not yet causal because policy choice and surprise respond to the same market conditions that drive prices.

### Forecast-error design

Use pre-announcement market-implied expectations, then relate announcement surprises to the prior ledger. This best matches credibility theory, but no reliable prediction market or forward curve exists. Spot pre-trends are not expectations measures.

## Decision

No `HYP-025` is registered. The cycle rejects the naive cross-platform test and narrows the viable work to a **prospective EVE communication ledger** whose first purpose is measurement validation. A claim-bearing credibility experiment requires either (a) player survey forecasts timestamped before announcements, (b) a platform partnership with user expectations and transactions, or (c) repeated quasi-random announcement surprises within one stable market regime.

The queue status changes from “queued behind convertibility audit” to “measurement protocol specified; blocked on expectations or microdata.” This is not evidence that developer credibility has no effect. It is evidence that public spot-price reactions cannot presently distinguish credibility from policy endogeneity and issuer identity.

## Connections

`ideas/2026-07-27-financialization-of-virtual-economies.md` · `source_scouting/2026-07-29-virtual-economy-event-data-audit.md` · `research_journal/2026-07-29-two-virtual-economy-audits.md` · `ideas/hypothesis_queue.md`
