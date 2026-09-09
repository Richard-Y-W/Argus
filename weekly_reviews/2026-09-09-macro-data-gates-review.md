# Adversarial review: SPF and RTDSM data gates

**Verdict:** SUPPORTED WITH LIMITS  
**Claim reviewed:** the public Philadelphia Fed files can support a preregistered quarterly point-disagreement design and a three-target quarterly real-time macro design  
**Promotion:** infrastructure may advance; no economic, forecasting, or asset-pricing claim may be promoted

## Strongest evidence

The pinned SPF workbook supplies 79 surveys with five quarterly core-PCE forecast horizons and 97.30% median within-survey common-horizon coverage. The pinned RTDSM files supply 129 common, nonempty quarterly vintages for real output, CPI, and unemployment with deterministic mid-quarter cutoffs. Tests cover empty vintage columns, density-versus-point horizon separation, and as-of parsing.

## Findings

- **Blocking for density registration:** PRCPCE has two annual density horizons, so the proposed three-horizon density curve is unavailable.
- **Blocking for exact-release work:** full-history RTDSM matrices do not identify every cell's release number or exact source release timestamp.
- **Material:** SPF IDs can change economic meaning across persons and firms; longitudinal ID effects require bounded language.
- **Material:** 12.66% median adjacent-quarter attrition remains large enough for composition to matter despite high same-survey horizon completeness.
- **Material:** the common RTDSM sample begins in 1994:Q3 because earlier CPI columns are empty.
- **Improvement:** the downloader pins current files but official URLs and workbooks are mutable; new releases need new fingerprints rather than overwrite.

## Required wording

Call these outcomes data-feasibility findings. Do not call SPF disagreement uncertainty, de-anchoring, or private information. Do not call an RTDSM-versus-final difference a causal revision effect or a tradable signal.

## Minimum next verification

For SPF, freeze the point-horizon estimand and generate a return-free composition sensitivity table. For RTDSM, attach release status and transformation semantics to the 129 common vintages. Only then preregister experiments.

## Connections

`source_scouting/2026-09-09-spf-composition-schema-audit.md` · `source_scouting/2026-09-09-rtdsm-vintage-release-map-audit.md` · `datasets/philadelphia_fed_macro_data_gates.md`
