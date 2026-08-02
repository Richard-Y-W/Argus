# Scout report — Treasury supply, duration risk, and term premia

*Scouted 2026-08-02. AI-led macro/quant discovery cycle. No yield or return effect is estimated.*

## Question

Can publicly observable changes in the maturity composition of Treasury debt isolate a duration-supply channel in term premia, distinct from expected short rates, deficits, inflation news, and Federal Reserve holdings?

This is macro-finance research rather than yield forecasting. The aim is to understand how quantities and investor habitat enter asset prices.

## Prior evidence

- Li and Wei estimate an arbitrage-free term-structure model with yield and supply factors. Their preferred-habitat mechanism maps privately held ten-year-equivalent duration into term premia ([Federal Reserve FEDS 2012-37](https://www.federalreserve.gov/pubs/feds/2012/201237/)).
- D'Amico, English, Lopez-Salido, and Nelson distinguish local scarcity and aggregate duration channels in large-scale asset purchases and locate much of the response in nominal, especially real, term premia ([Federal Reserve FEDS](https://www.federalreserve.gov/econres/feds/the-federal-reserve39s-large-scale-asset-purchase-programs-rationale-and-effects.htm)).
- D'Amico and King use security-level Federal Reserve purchases and find local flow and stock effects concentrated in nearby maturity sectors, supplying evidence for imperfect substitutability ([Federal Reserve FEDS 2012-44](https://www.federalreserve.gov/pubs/feds/2012/201244/)).
- Crump, Eusepi, and Moench show why a yield-level regression is insufficient: survey-based expected short rates and term premia are distinct, with the latter accounting for much yield variation ([New York Fed Staff Report 775](https://www.newyorkfed.org/research/staff_reports/sr775.html)).
- Recent work on open-ended purchases argues that communicated goals and implementation can change flow versus stock effects, so a quantity shock cannot be interpreted independently of the policy regime ([New York Fed Staff Report 1183](https://www.newyorkfed.org/research/staff_reports/sr1183.html)).

The generic supply-effect claim is mature and crowded. A new Argus project needs cleaner variation or a careful reproducibility audit, not another aggregate levels regression.

## Candidate designs

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Auction-announcement maturity-composition shocks | 5 | 4 | 4 | 5 | 5 | 4 | Priority institutional audit |
| Public replication of ten-year-equivalent supply | 5 | 4 | 3 | 4 | 5 | 3 | Strong learning replication |
| Deficit-to-yield predictive regression | 4 | 5 | 1 | 2 | 3 | 5 | Reject |
| Cross-country debt-maturity panel | 5 | 2 | 4 | 4 | 5 | 5 | Defer |

## Proposed narrow hypothesis

Unexpected changes in announced maturity-weighted issuance will move the corresponding yield-curve segment more than distant maturities after controlling for contemporaneous macro news, with larger effects when intermediary risk-bearing capacity is constrained.

The design must define “unexpected” using only pre-announcement issuance expectations; otherwise fiscal conditions and debt-management responses contaminate the shock. Local-maturity effects are the key discriminator. An aggregate ten-year-yield response is compatible with too many stories. State dependence must be preregistered using an external capacity proxy, not mined from many stress indicators.

## Internal debate

- **Optimist:** The question links macro policy, fixed-income mathematics, state-space models, event studies, and institutional detail.
- **Skeptic:** Treasury debt management reacts to deficits, demand, and market conditions. Public expectations may be too weak for credible shocks.
- **Statistician:** Announcement events are few and clustered in policy regimes. Conventional asymptotics and many state splits would be unreliable.
- **Economist:** Preferred habitat predicts local substitution patterns; fiscal-risk and inflation stories predict broader changes. The cross-maturity response is more informative than the average yield move.
- **Portfolio manager:** On-the-run rolls, futures conversion factors, repo specialness, and bid-ask effects matter before any tradability claim.
- **ML researcher:** A black-box yield forecast would obscure the institutional shock. Start with duration accounting and transparent local projections.

## Promotion gate

Do not register. First create an event inventory of Quarterly Refunding announcements, auction schedules, historical issuance expectations, security-level terms, SOMA holdings, and contemporaneous macro releases. Promotion requires a point-in-time expectations proxy and enough unanticipated maturity-composition variation to support a local-maturity test.

## Connections

`literature_reviews/2026-08-02-macro-quant-research-map.md` · `ideas/hypothesis_queue.md` · `research_journal/2026-08-02-four-macro-quant-discovery-cycles.md`
