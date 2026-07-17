# Jensen, Kelly, and Pedersen (2023) — Is There a Replication Crisis in Finance?

## Main question and framework

Jensen, Kelly, and Pedersen reconstruct 153 published characteristics using a common methodology across 93 countries. The design replaces a collection of author-specific implementations with standardized, signed long–short portfolios and directly studies replication across samples and geographies.

The public Global Factor Data release supplies monthly factor returns for world, world excluding the United States, developed, emerging, and frontier aggregates. Portfolios are signed according to the original paper's expected-return direction. The July 2026 download extends through December 2025 and is licensed CC BY-NC 4.0.

## Why it matters for Argus

Argus's strongest result is publication-timed decay in the US Chen–Zimmermann panel. The JKP library creates a meaningful external test: do the same broad published ideas weaken after their original sample ends and after publication in a standardized non-US portfolio family?

This is not a perfect replication. Factor definitions, weighting, country aggregation, metadata, and coverage differ from C&Z. Non-US returns may still reflect globally transmitted information and arbitrage originating in the United States. Publication year is an annual proxy, and the public aggregate file does not expose holdings, costs, flows, or price impact.

## Identification limits and criticism

- A post-publication break is consistent with arbitrage, investor learning, data mining, changing risk premia, and implementation changes.
- Cross-country coverage begins mainly in 1986, eliminating early in-sample observations for many classic factors.
- Factors share stocks and economic themes, so factor-level observations are dependent.
- Standardized reconstruction improves comparability but does not reproduce every original paper exactly.
- Gross long–short returns do not establish tradability.

## Connections

`datasets/jkp_global_factors_2025.md` · `hypotheses/HYP-013-nonus-publication-decay.md` · Jensen, Kelly, and Pedersen (2023), *Journal of Finance* 78(5), 2465–2518
