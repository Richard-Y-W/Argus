# Novelty audit — EVE PLEX global-market integration

*Audited 2026-08-02. Search-based assessment, not proof of universal absence. Sources were checked through public scholarly indexes, working-paper repositories, general web search, EVE developer records, community analyses, and repository/code discovery.*

## Candidate contribution

The candidate study reconstructs PLEX limit-order books across regional EVE markets before the July 2025 transition to a single global PLEX book, then distinguishes mechanical effects of the rule from non-mechanical changes in spread, depth, concentration, resilience, participation, and quote adjustment. A companion design tests whether pre-integration regional quote gaps follow a spatial/network diffusion structure beyond standard panel and autoregressive benchmarks.

## Search boundary

Queries combined variants of:

- `EVE Online`, `PLEX`, `global PLEX market`, `market integration`, `regional price`, `order book`, `liquidity`, `market microstructure`, `arbitrage`, `natural experiment`, and `research`;
- virtual-economy market intervention, game-economy policy, transaction taxes, item sinks, and virtual-currency market structure;
- EVE-specific papers, repositories, practitioner analyses, and post-launch commentary;
- network diffusion, spatial price adjustment, exchange consolidation, and order-book integration.

Searches located adjacent work and descriptive analysis but no public paper or repository executing the candidate design. Unindexed theses, private CCP analysis, work in progress, and unpublished proprietary research remain possible.

## What is already occupied

### Virtual economies as laboratories

This is established. The literature studies inflation, exchange rates, virtual goods, wealth concentration, policy shocks, taxes, and platform governance. The broad statement that game economies permit useful natural experiments has no novelty.

Hogan-Hennessy, Xenopoulos, and Silva study an Old School RuneScape transaction tax and item sink using regression discontinuity, regression kink, and difference-in-differences methods. Their design occupies the generic contribution “developer market intervention in a large virtual economy” ([paper](https://arxiv.org/abs/2210.07970)). Hooper studies EVE wealth concentration and play time, occupying a generic EVE-macroeconomy contribution ([DiGRA paper](https://dl.digra.org/index.php/dl/article/view/1187)).

### Descriptive PLEX launch analysis

CCP stated ex ante that pooling was intended to increase liquidity, reduce price disparities, improve availability, and encourage adoption. It also stated that existing orders would be cancelled and fees reimbursed ([announcement](https://www.eveonline.com/zh/news/view/global-plex-market-and-friction-free-trade)).

A practitioner analysis reported 27.7 million PLEX exchanged in 82,640 transactions over the first 25 days, an average trade size of 335 PLEX, and a 2.9% fall in average price. It also records a PLEX-linked promotion five days after launch, which directly confounds a simple price event study ([The Nosy Gamer](https://nosygamer.blogspot.com/2025/08/eve-onlines-global-plex-market-july-2025.html)). Current market tools expose the global PLEX market, but a data browser is not a causal or historical microstructure study ([isk.gg](https://isk.gg/)).

Therefore a launch summary, price chart, volume chart, or statement that dispersion disappeared would not be new.

### Methods from conventional markets

Exchange consolidation, spatial price integration, order-book liquidity, diffusion, market impact, and resilience are large literatures. Using spread, depth, entropy, a network, or an event study does not create method novelty.

## What appears open

No located public work jointly does the following:

1. reconstructs the regional PLEX books from archived order-level snapshots before pooling;
2. identifies the cancellation and global-book formation sequence at intraday resolution;
3. separates mechanical disappearance of regional books from non-mechanical liquidity outcomes;
4. measures regional quote adjustment when the asset was already stored in a location-independent PLEX Vault;
5. tests a spatial/network model against frozen region fixed-effect, common-factor, and autoregressive benchmarks;
6. separates announcement, implementation, promotions, and longer-run adaptation;
7. preserves the distinction between an executable ISK market and a fiat-investable asset.

This **event × archive × estimand** combination is plausibly original as of the audit date. The wording must remain “we found no public study,” not “no one has studied it.”

## Why the institutional setting may generalize

Before pooling, PLEX was close to locationless in custody because the PLEX Vault reduced physical delivery needs, yet price discovery remained segmented by region. Pooling then removed the venue/search boundary. This is narrower than ordinary geographic integration:

```text
physical transport friction: already reduced
information and venue fragmentation: still present
global pooling: removes the remaining regional book boundary
```

That institutional sequence may reveal search, attention, thin-market, and venue-fragmentation effects without the usual commodity-shipping mechanism. The analogy is imperfect because account access, private structures, contracts, taxes, promotions, and platform rules remain.

## Claims the design cannot earn

- A causal welfare effect from one treated asset and no perfect untreated PLEX.
- A result based on regional dispersion becoming zero; that is encoded by the rule.
- An order-count result across the cancellation boundary without reconstructing migration and relisting.
- A USD return or investability result.
- General market-integration theory from a single issuer-controlled environment.
- Method novelty merely from applying physics language.

## Publication-value assessment

| Version | Novelty | Identification | Likely value |
|---|---|---|---|
| Price/volume before-after chart | Low | Weak | Practitioner note only; partly done |
| Descriptive order-book reconstruction | Moderate | Descriptive | Reusable data/method note |
| Non-mechanical market-quality event study | Moderate-high | Bounded by one event | Strong case study if transition and confounds are handled |
| Pre-event regional diffusion plus intervention | High for this setting | Better cross-sectional content | Best research version |
| Physics-branded universal market model | Low | Weak | Do not pursue |

## Decision

The exact project remains worth pursuing, but novelty depends on the narrow institutional and measurement contribution. The next novelty check should be repeated immediately before a formal manuscript or public claim, including citation chaining from newly located work and repository searches by data-source name (`EVE Ref`, `EveKit`, `Fuzzwork`, `ESI`).

## Connections

`datasets/eve_online_market_archives_2025.md` · `literature_reviews/2026-08-02-bio-physics-methods-in-finance.md` · `ideas/2026-08-02-self-replication-fluid-and-biological-finance.md` · `source_scouting/2026-08-02-digital-assets-and-complex-systems.md`
