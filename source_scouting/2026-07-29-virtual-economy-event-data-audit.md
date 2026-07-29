# Event-and-data audit — virtual-economy market access

*Cycle completed 2026-07-29. AI-led follow-up to the collaborative 2026-07-27 domain-selection cycle.*

## Question and promotion rule

This cycle asked whether public records support a claim-bearing test of the idea that lower conversion, transfer, or market-access frictions cause virtual assets to become more liquid or externally priced. Events were collected from institutional documentation without inspecting asset returns. Promotion to `HYP-025` required: an exact effective date, a treated unit and credible comparison, adequate pre/post observations, and prices that are executable or explicitly bounded as non-executable.

## Candidate inventory

`Verified` means the linked issuer or platform record fixes the event and date. It does not mean the event is causally clean or the data are research-ready. `Candidate` means the date or implementation still needs an archived first-party record.

| # | System | Effective date | Institutional change | Variation potentially usable | Price/data status | Audit status |
|---:|---|---|---|---|---|---|
| 1 | EVE Online | 2017-05-09 | Old PLEX split 1:500; Aurum consolidated into PLEX; PLEX Vault introduced | Old/new instrument boundary; market orders cancelled | Official market history restarts under a new type ID; ESI history and monthly reports plausible | Verified; anticipation and type discontinuity severe ([announcement](https://www.eveonline.com/news/view/changes-to-plex-packages-coming-with-may-release)) |
| 2 | EVE Online | 2020-11-10 | Dynamic Bounty System and revised ESS launched | System-level exposure varies with activity and security space | Monthly Economic Reports plus ESI market data; treatment is endogenous | Verified ([patch notes](https://www.eveonline.com/news/view/patch-notes-for-version-18-11)) |
| 3 | EVE Online | 2020-12-01 | DBS equilibrium and cap increased; ESS parameters changed | A common parameter shock with heterogeneous pre-event bounty exposure | Aggregate and system data need reconstruction; simultaneous changes | Verified ([patch notes](https://www.eveonline.com/news/view/patch-notes-for-version-18-11)) |
| 4 | EVE Online | 2021-07 | ESS reserve-bank keys made available | Reserve-bank access shock across systems with accumulated balances | Timing is documented; system-level outcomes may require ESI or proprietary telemetry | Verified at month, exact deployment date to pin ([announcement](https://www.eveonline.com/news/view/the-grand-heist)) |
| 5 | EVE Online | 2021-09-14 | Epic Games Store distribution opened | New external acquisition channel, not asset convertibility | Player counts are weak public proxies; no clean untreated region | Verified ([Gateway announcement](https://www.eveonline.com/news/view/gateway-new-quadrant-starts-today)) |
| 6 | EVE Online | 2022-05-17 | Fiat price of Omega and PLEX raised; package menu restructured | Exogenous official on-ramp price schedule | PLEX/ISK market data plausible; all players treated and announced 25 days early | Verified ([announcement](https://www.eveonline.com/news/view/plex-and-omega-price-changes)) |
| 7 | EVE Online | 2025-07-07 | Regional PLEX order books pooled into one global market | Same asset before/after a direct fragmentation removal | ESI order and trade history is the best public candidate; no untreated PLEX market | Verified; strongest direct market-access event ([announcement](https://www.eveonline.com/news/view/global-plex-market-coming-7-july)) |
| 8 | World of Warcraft | 2015-04-07 US | WoW Token launched as sanctioned real-money-to-gold bridge | Staggered regional launches may offer comparisons | Current token price feeds exist; complete point-in-time regional history and executable quantity are not yet verified | Date supported by launch record; archive needed ([design announcement](https://worldofwarcraft.blizzard.com/en-us/news/18141101/introducing-the-wow-token)) |
| 9 | World of Warcraft | 2017-02-06 US | Token redemption expanded from game time to Battle.net balance | Utility/off-ramp-like expansion within the platform | Regional token price histories are third-party; no order book or volume | Candidate; first-party effective-date archive required |
| 10 | Old School RuneScape | 2021-12-09 | 1% Grand Exchange tax and item sink introduced | Tax thresholds and eligible/ineligible items | Public item price/volume API; no legal fiat exit or executable depth | Verified via preserved official post ([record](https://oldschool.runescape.wiki/w/Update%3AGrand_Exchange_Tax_%26_Item_Sink)); already studied in prior literature |
| 11 | Old School RuneScape | 2023-11-21 | GE tax rate reportedly increased from 1% to 2% | Common tax shock, possible item heterogeneity | Public price/volume; implementation and concurrent update need first-party archive | Candidate; do not use yet |
| 12 | Steam economy | 2015-12 | Mobile-authenticator trade holds introduced | Account-level adoption determines immediate versus delayed transfer | No public account assignment; market aggregates only | Candidate date; unsuitable without microdata |
| 13 | Steam economy | 2016-03-09 | Unauthenticated trade and market holds increased to 15 days; item restoration ended | Authenticated versus unauthenticated accounts; scarcity rule changed simultaneously | Public aggregate listings cannot identify account treatment | Verified in Steam platform record ([announcement](https://store.steampowered.com/news/posts/?enddate=1474405919&feed=steam_blog)); microdata unavailable |
| 14 | Counter-Strike | 2018-03-29 | Seven-day cooldown applied to items received in trades | Recently traded versus seasoned inventory | Public marketplace prices but treatment state is not observed | Candidate; official archived post and microdata needed |
| 15 | Counter-Strike | 2019-10-28 | Newly purchased container keys made non-tradable and non-marketable | Legacy keys versus newly purchased keys | Steam market sees legacy stock, but third-party venue history and item provenance are incomplete | Candidate; promising scarcity event, weak comparison |
| 16 | Rocket League | 2019-12-04 | Crates and keys replaced by blueprints and credits; item-shop purchases account-bound | Legacy tradable items versus newly bound shop items | Third-party trades, no canonical executable history; migration changed many margins | Verified in platform news archive ([conversion record](https://store.steampowered.com/news/posts/?appids=252950&enddate=1576113809)); heavily bundled |
| 17 | Roblox | 2025-09-05 10:00 PT | DevEx rate for newly earned Robux rose from $0.0035 to $0.0038 | Robux earned before/after cutoff has different cash-out rate | Creator-level balances and earnings are private; Robux is not freely cash-convertible for users | Verified ([DevEx help](https://en.help.roblox.com/hc/en-us/articles/13061189551124-Developer-Exchange-Help-and-Information-Page)); no public outcome panel |
| 18 | Roblox | 2026-06-08 | Special $0.0054 DevEx rate added for eligible US 18+ in-game spending | Age/geography/transaction eligibility creates discontinuities | Required creator transaction data are private | Verified ([DevEx help](https://en.help.roblox.com/hc/en-us/articles/13061189551124-Developer-Exchange-Help-and-Information-Page)); potentially strong with platform partnership only |
| 19 | Second Life | 2019-06-24 | Process-credit fees increased | Cash-out cost shock for creators versus users retaining USD credit | LindeX has limit orders, but historical order-book and withdrawal microdata not verified | Verified by Linden staff explanation ([record](https://community.secondlife.com/forums/topic/437799-a-brief-note-on-pricing-changes-which-ran-long/)) |
| 20 | Second Life | 2019-08-01 | Tilia assumed management of USD balances and process credit | KYC/payment-intermediary transition | Public exchange aggregates insufficient for user-level friction | Candidate; official launch archive and historical data access needed |
| 21 | Second Life | 2020 | Identity requirements expanded in parts of LindeX/Tilia flow | User-specific compliance friction | Assignment and transactions are private | Candidate based on contemporaneous reports; not claim-ready |

## Data-source audit

| System | Public institutional timing | Public prices | Volume/depth | Legal cash exit represented by price? | Survivorship/delistings | Verdict |
|---|---|---|---|---|---|---|
| EVE/PLEX | Strong | Transactional in-game market history | Orders and daily volume potentially available through ESI; archive coverage must be tested | No player fiat off-ramp; price is executable in ISK, not USD liquidation | Type-ID change in 2017 must be bridged explicitly | Best public market-design laboratory |
| WoW Token | Strong | Platform-set regional quote | No public volume or order book | One-way real-money bridge; no user cash-out | Region definitions and product utility changed | Descriptive event study only unless better data appear |
| OSRS items | Strong | Public transaction-derived aggregates | Daily volume, no depth or identities | No lawful fiat exit | API coverage and item additions auditable | Good policy laboratory, poor convertibility test |
| Steam/CS items | Strong for major rules | Steam market transaction prices; third-party cash venues | Listings visible now; historical depth/venue survival uncertain | Steam wallet is not cash; third-party cash-out adds counterparty and account risk | Acute | Research-ready only with a vendor/archival dataset |
| Roblox | Strong for current DevEx rules | Issuer-fixed creator cash-out schedule, not a market price | Private | Only eligible earned Robux and approved creators | Cohorts can be defined by issuer records | Excellent natural experiment only with creator/platform microdata |
| Second Life | Moderate | LindeX is a real limit-order exchange into USD balance | Historical depth and user flow not confirmed | Net proceeds can be processed to approved payment rails | Historical records uncertain | Revisit after data-access inquiry |
| Rocket League | Strong | Fragmented third-party prices | Fragmented and survivor-biased | Operationally fragile third-party exit | Acute after platform and trading changes | Reject for first study |

## Identification debate

- **Optimist:** The 2025 EVE global PLEX market is a direct reduction in spatial fragmentation with a precise effective date and a market explicitly designed to pool liquidity.
- **Skeptic:** It affects one asset everywhere, was announced, and coincides with other monetization changes. A before/after fall in spreads cannot isolate integration from anticipation or market-wide trends.
- **Statistician:** A credible test needs either unaffected but similar EVE assets with comparable pre-event liquidity dynamics or order-level regional books whose convergence begins only when pooling occurs. Synthetic controls over unrelated items are weak because PLEX has unique utility and fiat issuance.
- **Market-structure view:** ESI daily history may report completed trades but not preserve the counterfactual regional best quotes needed to measure fragmentation. A global book can mechanically remove observed dispersion while leaving effective player access costs unchanged.
- **Portfolio view:** PLEX/ISK is executable inside EVE, but it is not an investable USD return. Any result is about market design and private money, not a trading strategy.

## Decision

The audit satisfies the requested breadth—21 candidate events across seven systems—but **does not promote `HYP-025`**. No public event currently clears all four promotion requirements. The EVE global PLEX pooling event is the strongest lead and moves to a targeted acquisition audit: determine whether archived regional order books, daily fills, fees, and comparable item histories exist for at least 180 days on each side of 2025-07-07. Roblox's 2026 age/geography DevEx schedule is a better causal design in principle, but the necessary transactions are private.

The negative result is informative: “convertibility” is not one treatment. Official on-ramps, creator cash-out, market pooling, trade delays, wallet convertibility, and third-party liquidation change different margins and should not be pooled into a single event-study coefficient.

## Connections

`ideas/2026-07-27-financialization-of-virtual-economies.md` · `source_scouting/2026-07-27-virtual-economy-financialization.md` · `source_scouting/2026-07-29-developer-policy-credibility-audit.md` · `research_journal/2026-07-29-two-virtual-economy-audits.md` · `ideas/hypothesis_queue.md`
