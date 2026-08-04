# PLEX market-integration thread

## Institutional sequence

`59 regional books -> cancellation -> empty PLEX snapshot -> global region 19000001 formation`

Verified archive boundary on 2025-07-07 UTC:

- 10:45 regional;
- 11:15 empty;
- 11:45 first observed global;
- 12:15 early global growth.

The treatment must therefore be represented as a sequence, not a single date dummy.

## Data lineage

EVE Ref daily indexes -> pinned URL/size/ETag/file time -> temporary hashed payload -> schema-validated streaming PLEX filter -> compact manifest and summary. Full-market archives are not retained.

## Live questions

1. Do non-mechanical displayed spread and depth improve after early global formation?
2. How quickly did the global book replenish after cancellation?
3. Before pooling, do regional quote gaps follow observable network diffusion beyond fixed-effect and autoregressive benchmarks?
4. Can control items selected solely from pre-event liquidity provide a useful, explicitly imperfect counterfactual?

## Boundaries

Regional dispersion becoming zero is mechanical. Snapshot disappearance does not identify trades. PLEX/ISK is an in-platform executable market, not a USD-investable asset.

