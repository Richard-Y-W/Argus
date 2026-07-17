# JKP Global Factor Data — April 2026 release

## Source and license

Official public factor portfolios from Jensen, Kelly, and Pedersen's Global Factor Data site, downloaded 2026-07-16. Data are licensed CC BY-NC 4.0; source code is MIT licensed. Raw files remain ignored from Git.

- Factor returns: `[all_regions]_[all_factors]_[monthly]_[vw].zip`
- Metadata: `factor_details.xlsx` from the official `bkelly-lab/jkp-data` repository
- Documentation: Global Factor Data documentation PDF
- Coverage observed before registration: 153 factors in world, world-ex-US, developed, and emerging aggregates; frontier has 135. World-ex-US begins 1986-01 and all aggregates end 2025-12.

The returns file provides `location`, factor `name`, frequency, weighting, original-paper direction, country count, date, and signed long–short return. The official documentation states that the factor is long the tercile identified by the original paper as having the highest expected return and short the lowest.

## Research use and limitations

EXP-013 uses only aggregate value-weighted monthly factor returns and bibliographic/sample-period metadata. It does not use or redistribute stock-level licensed inputs. Country composition changes through time; factors share securities; aggregate returns are gross of costs; and annual publication dating is coarse. Checksums are recorded in `datasets/manifest.json` after acquisition.

## Connections

`papers/2023-jensen-kelly-pedersen-replication-crisis.md` · `hypotheses/HYP-013-nonus-publication-decay.md` · Jensen, Kelly, and Pedersen (2023)
