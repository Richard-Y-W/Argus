# EBA 2025 EU-wide stress-test public release

**Audited:** 2026-08-11  
**Use status:** schema and feasibility only; not admitted as claim-bearing input  
**Provider:** European Banking Authority

## Official release

Landing page: <https://www.eba.europa.eu/eu-wide-stress-test-2025>

The landing page identifies 64 banks from 17 EU/EEA countries and links the following full-database files under release identifier `763451`:

| File | Bytes | SHA-256 observed 2026-08-11 |
|---|---:|---|
| `TRA_OTH.csv` | 6,223,488 | `e7a48b99984d8728b5b24285d9b00aed94b605a7855705f04b41c5b21da5378a` |
| `TRA_CRE_IRB.csv` | 62,215,416 | `38087207191702dde669df6b1e7b29aa8f082e57d59646467334437f1214c6d0` |
| `TRA_CRE_STA.csv` | 70,053,968 | `ae94e02a6c6d4290dfde02cbae65e9a60ad1cefde3facf5cffbaf8ccef13cec7` |
| `Data_Dictionary.xlsx` | 27,210 | `46ea6eb59eec41e57ed6fb4c327aa147ce49d4fed6c99d29c537be7f5d94fa22` |
| `Metadata_TR.xlsx` | 114,960 | `5f3fab231e4a3d254abfdf246e701f1860e12f6850bec29b771dbd52436e6274` |

The raw files were inspected in a temporary directory and are not committed. They can be reacquired from `https://www.eba.europa.eu/assets/st25/full_database/763451/<FILE>` and checked with `engineering/sandbox/eba_2025_schema_audit.py`.

## Observed schema

- `TRA_OTH.csv`: 64,128 rows; 64 banks; 154 reported items across summary, capital, risk-exposure amount, profit-and-loss, and capital-measure templates.
- `TRA_CRE_IRB.csv`: 534,600 rows; credit exposures, risk exposure amounts, IFRS 9 stages, provisions, and coverage ratios across portfolio, exposure class, geography, and performance status.
- `TRA_CRE_STA.csv`: 595,826 rows; analogous standardised-approach and securitisation fields.
- Starting values generally use December 2024 and scenario code 11. Baseline/adverse projections use scenario codes 2/3 for December 2025–2027.
- The dictionary contains 168 items. No LCR, funding, deposits, or operational liquidity endpoint is present. The only label matching a broad liquidity search is an accounting reserve within accumulated other comprehensive income.

The EBA describes the exercise as constrained bottom-up with a static-balance-sheet assumption. Projected credit tables provide outcomes under common scenarios, not observations of alternative balance-sheet interventions.

## Research boundary

These files can support external calibration of bank-level solvency stress and descriptive exposure heterogeneity. They do not identify how capital, losses, funding, or lending capacity would respond if a researcher selectively removed exposures. Such a response requires an imposed model; a targeted-versus-proportional comparison would inherit that model rather than test it.

The 2025 release is therefore unsuitable for EXP-032 as originally conceived. It remains a potential calibration input if a future design obtains an independently validated response model and reserves another release or jurisdiction for confirmation.

## Connections

`source_scouting/2026-08-11-eba-2025-schema-audit.md` · EXP-031 · `engineering/sandbox/eba_2025_schema_audit.py`
