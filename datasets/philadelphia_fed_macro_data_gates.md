# Philadelphia Fed macro data-gate workbooks

**Acquired:** 2026-09-08 from the Federal Reserve Bank of Philadelphia  
**Use:** exploratory schema and point-in-time feasibility audits only  
**Storage:** raw workbooks remain local and untracked; the deterministic downloader verifies these fingerprints

| Workbook | Official role | SHA-256 |
|---|---|---|
| `SPFmicrodata.xlsx` | SPF individual forecasts, 1968:Q4-present workbook | `d45af2eaebe11e8c7a0635d3f868d5d85897e5bc5cc3d8cb477c243b31faa076` |
| `ROUTPUTQvQd.xlsx` | Real GNP/GDP, quarterly vintages and quarterly observations | `bf0c4c1b6b902283bfb94fe7b7d94e003ff68fb926aebb0169504bbe213a055c` |
| `cpiQvMd.xlsx` | CPI, quarterly vintages and monthly observations | `57d28f99b28ca9a37801fcdd5026fae9b859e58b0f3dc1e150a55c544598bc34` |
| `rucQvMd.xlsx` | unemployment rate, quarterly vintages and monthly observations | `d971e59d3ed5f1322a46631743508fb1ad5eee39bfbe12425a641a277fdd9b9a` |

The source pages are the Philadelphia Fed's [SPF individual forecasts](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/individual-forecasts), [real output](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/routput), [CPI](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/cpi), and [unemployment](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/ruc) pages. The files are mutable public releases. A later download is a new dataset version and must not silently replace these fingerprints.

Reproduce acquisition into an ignored local directory:

```powershell
python -m engineering.sandbox.macro_data_gates.download .tmp/macro_audit
```

## Known semantic limits

- SPF respondent IDs are not guaranteed person-level identities. Before 1990 an ID may have been reused; after the Philadelphia Fed takeover, an ID can follow either a person or firm depending on the forecast's institutional character.
- Core-PCE point forecasts supply a nowcast and four following quarterly horizons. Core-PCE density forecasts supply only current-year and next-year distributions.
- The RTDSM quarterly workbooks are mid-quarter snapshots. They identify an admissible information set on February 15, May 15, August 15, or November 15, but do not by themselves assign every observation an exact agency release timestamp or revision number.
- CPI columns before 1994:Q3 exist in the workbook but are entirely empty. They are schema placeholders, not historical vintages.

## Connections

`source_scouting/2026-09-09-spf-composition-schema-audit.md` · `source_scouting/2026-09-09-rtdsm-vintage-release-map-audit.md` · `engineering/sandbox/macro_data_gates/`
