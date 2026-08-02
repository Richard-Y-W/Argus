# Deep scout — digital-asset data and complex-systems methods

*Scouted 2026-08-02. Human-directed topic, AI-led data audit and method triage. This cycle changes the feasibility verdict but does not report an economic result.*

## Starting point

Prior Argus work inventoried 21 virtual-economy events and ranked the July 2025 EVE PLEX global market as the strongest public market-integration candidate. It withheld registration because archived regional books had not been verified. Richard then asked for deeper digital-asset research and proposed importing ideas from biology and physics where they may create an edge.

## Material new evidence

EVE Ref's machine-readable archive was queried directly on 2026-08-02. Its market-order hierarchy contains daily directories from 2021 through 2026, and the 2025 hierarchy contains the dates around the PLEX event. The service documents two full regional snapshots per hour and provides ETags, byte sizes, and timestamps through JSON indexes ([dataset documentation](https://docs.everef.net/datasets/market-orders); [dataset index specification](https://docs.everef.net/datasets/)).

A two-file probe established content, not just filenames:

- 2025-07-06 12:15:08 UTC: 2,003 PLEX orders across 59 regional books;
- 2025-07-08 14:15:10 UTC: 322 PLEX orders in global region `19000001` only.

CCP's developer notice independently identifies region `19000001` and says current PLEX orders and history would use existing ESI routes ([notice](https://developers.eveonline.com/blog/global-plex-market-and-sde-updates)). EVE Ref also exposes market history back to 2003 and mirrors all twelve CCP Monthly Economic Report archives for 2025. Detailed provenance and hazards are recorded in `datasets/eve_online_market_archives_2025.md`.

The earlier verdict therefore changes from **archive coverage unknown** to **regional and global order books verified; staged acquisition feasible**.

## Research questions now feasible

Scores are 1–5; higher confounding risk is worse.

| Candidate | Falsifiable | Data feasible | Novel | Mechanism | Learning | Confounding risk | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| PLEX integration and displayed market quality | 5 | 5 | 4 | 5 | 5 | 4 | Promote to preregistration after exact transition audit |
| Spatial diffusion of regional PLEX quote gaps | 5 | 5 | 4 | 5 | 5 | 3 | Best physics-informed sandbox |
| Order-book resilience/entropy after pooling | 5 | 5 | 4 | 4 | 5 | 4 | Secondary; benchmark against simple metrics |
| Self-exciting PLEX order flow | 5 | 2 | 3 | 4 | 5 | 4 | Defer; snapshots censor deleted events |
| Ecological competition among virtual assets | 4 | 3 | 4 | 3 | 5 | 5 | Defer; strategy abundance unobserved |
| Critical-transition warning for virtual crashes | 5 | 4 | 3 | 3 | 5 | 5 | Hostile replication only |

## Candidate estimands

### Market-quality discontinuity

Track effective displayed spread, depth within fixed basis-point bands, order-count and quantity concentration, imbalance, quote staleness, and recovery after large book changes. The pre/post comparison should exclude mechanically zero regional dispersion as an “effect.” It should model the announcement window separately and use deployment timestamps derived from the first valid global snapshots.

Controls can include matched liquid EVE items, market-wide snapshot totals, MER activity, day-of-week/time-of-day, and placebo dates. None produces a perfect untreated PLEX, so the result must remain a bounded event-study association unless stronger variation is found.

### Spatial diffusion

Before pooling, define nodes as regions and outcomes as bid/ask gaps from a liquidity-weighted hub. Test whether quote-gap adjustment relates to connectivity, local depth, and prior gaps beyond region fixed effects and common PLEX moves. Freeze hub definition and graph distance without inspecting forecast performance. Use rolling-origin regional holdouts.

This imports a physics mechanism with observable states and topology. It is more defensible than fitting a generic nonlinear dynamical system to the global PLEX price.

### Resilience and entropy

Define shocks mechanically from book changes, not future returns. Compare time to replenish depth and normalize by contemporaneous activity. Entropy measures must beat Herfindahl concentration, spread, depth, and imbalance in held-out recovery forecasts. Otherwise they are relabeled descriptive statistics.

## Internal debate

- **Optimist:** A direct platform rule changes the topology of a real limit-order market. Archived books on both sides make this unusually concrete digital-economy research.
- **Skeptic:** Global pooling mechanically changes displayed books, PLEX is unique, and the announcement invites anticipation. A clean causal welfare statement remains out of reach.
- **Statistician:** Freeze the exact transition from archive content, not the announced date alone. Treat one event as one event; thousands of orders do not create thousands of independent policy shocks.
- **Economist:** Integration may reduce search fragmentation while changing regional access, tax incidence, inventory placement, and speculation simultaneously. Market quality is multidimensional.
- **Portfolio manager:** The outcome is executable in ISK but not a USD liquidation return. Contract trading and fees may sit outside the observed book.
- **Complex-systems researcher:** Network diffusion fits because topology and state variables are observed. Hawkes, ecology, and critical-transition models require event, abundance, or bifurcation structure the current archive does not automatically supply.
- **ML researcher:** A large sequence model would learn the intervention timestamp. Begin with transparent benchmarks and hold out regions or dates before adding nonlinear structure.

## Decision

The data gate for a PLEX study is substantially cleared, but `HYP-025` is not registered in this cycle because the exact transition sequence, incomplete-snapshot rule, control-asset set, and source correction history must be fixed first. The next bounded cycle is now engineering rather than open-ended scouting:

1. pin indexes and ETags for ±60 days;
2. locate the first valid global book and the regional cancellation/migration sequence;
3. select control items from pre-event liquidity only;
4. build streaming extraction and synthetic schema tests;
5. run a sandbox measurement audit with no claim-bearing tests;
6. preregister market-quality and spatial-diffusion predictions before expanding the window.

This is a genuine advance over the July 29 audit: the strongest candidate is no longer blocked on archive existence. It remains blocked on exact treatment semantics and credible inference.

## Connections

`datasets/eve_online_market_archives_2025.md` · `literature_reviews/2026-08-02-bio-physics-methods-in-finance.md` · `source_scouting/2026-07-29-virtual-economy-event-data-audit.md` · `ideas/hypothesis_queue.md` · `research_journal/2026-08-02-digital-assets-complex-systems.md`
