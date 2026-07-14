# Scout report — retail attention and live-trading failure modes

*Scouted 2026-07-14 from web-indexed Reddit discussions and research pages. Discovery artifact only.*

## Practitioner claims

- r/algotrading repeatedly argues that spreads, slippage, option selection, and latency destroy backtests.
- Posters nominate unusual options volume, skew, and put/call ratios as leading signals, usually without reproducible samples or multiple-testing disclosure.
- Regime conditioning is frequently proposed after a strategy fails, creating post-selection risk.
- Finance communities discuss earnings-call access and public-information timing, suggesting attention questions beyond WallStreetBets sentiment.

Representative URLs:

- https://www.reddit.com/r/algotrading/comments/gr3f6v/estimating_transaction_costs/
- https://www.reddit.com/r/algotrading/comments/1i15y54/algotrading_on_price_data_alone/
- https://www.reddit.com/r/SecurityAnalysis/comments/1i2ls71/2025_analysis_questions_and_discussions_thread/

## Collision with literature

- Hu & Yan associate Reddit attention with returns and retail activity: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4861540
- *The Social Signal* separates attention and sentiment effects: https://www.sciencedirect.com/science/article/pii/S0304405X2400093X
- *Place Your Bets?* reports deterioration in WallStreetBets due-diligence informativeness after GameStop, especially for attention-oriented reports: DOI 10.1093/rfs/hhad098.
- Da, Hua, Hung & Peng distinguish retail attention price pressure from institutional information resolution: DOI 10.1287/mnsc.2023.01294.

The useful gap is not the saturated “does Reddit predict returns?” question. It is content versus attention, decay after community growth, executable costs, and whether results survive frozen timestamped text models.

## Candidate hypotheses

1. High post volume with neutral/dispersed semantic sentiment predicts temporary pressure and reversal; evidence-bearing consensus predicts continuation.
2. A ticker mention's informativeness falls as community membership and outside coverage rise—social-signal publication decay.
3. Unusual-options-flow predictability is concentrated where historical spreads and contract-selection costs erase it.
4. Practitioner regime filters improve random strategies in sample through specification search but fail nested walk-forward tests.

## Decision and limitations

Queue candidate 1; it needs timestamped Reddit data, point-in-time prices, a frozen classifier, and reproducible access. Promote candidate 4 to sandbox calibration because it can be tested synthetically. Search indexing is not a random Reddit sample; removed-post survivorship is material. No identities were collected.
