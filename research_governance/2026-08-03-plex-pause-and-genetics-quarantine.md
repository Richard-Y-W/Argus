# PLEX pause and genetics quarantine

**Effective:** 2026-08-03  
**Decision owner:** researcher  
**Status:** active, reversible pause

## Decision

Pause the PLEX market-integration program after transition-boundary reconstruction. Preserve its source manifests, extracted observations, code, tests, figures, and conclusions unchanged. Do not run the queued effect estimation, control selection, spatial-diffusion, resilience, or fluid-continuity studies until the researcher explicitly resumes this branch.

This is a prioritization decision, not an evidentiary rejection. The verified PLEX transition sequence remains archived and may be resumed from its existing boundary without rerunning or rewriting it.

## Quarantine boundary

The active financial-genetics program must not use any PLEX-derived:

- observations, timestamps, item or region identifiers, control assets, or archive metadata;
- variables, thresholds, event windows, estimators, figures, or selected metrics;
- empirical findings, outcome-aware design choices, or conclusions.

Genetics artifacts must have independent data provenance, registrations, code paths, configurations, outputs, and interpretation. Shared generic research utilities are permitted only when they contain no PLEX constants or PLEX-derived choices. A PLEX result may be discussed later as an external analogy, but not used to specify or evaluate a genetics experiment.

Likewise, genetics findings must not modify the frozen PLEX design. Resuming PLEX requires a new dated decision and a fresh preregistration boundary.

## Enforcement

`engineering/genetics/check_quarantine.py` scans Python, JSON, YAML, and TOML artifacts in genetics-owned paths for prohibited PLEX markers. Its test is a tripwire, not proof of causal independence; review must still inspect provenance and design choices.

## Genetics evidence boundary

EXP-025 through EXP-027 consumed the existing synthetic AR(1) regime-path family. Their paths, mutation settings, gate thresholds, and outcomes cannot serve as confirmation data or be tuned further. The next experiment must use either:

1. an externally specified benchmark with frozen rules; or
2. point-in-time historical data with an explicit, independently defined sample and untouched evaluation segment.

Any historical dataset previously examined by Argus must be labeled exploratory unless a credible untouched boundary can be demonstrated.

## Resume condition

PLEX work resumes only after an explicit researcher instruction. At that point, record the date and scope here or in a successor governance note before executing new analyses.

## Connections

- `knowledge_graph/plex-market-integration-thread.md`
- `ideas/hypothesis_queue.md`
- `failed_experiments/EXP-025-financial-immune-controller/`
- `failed_experiments/EXP-026-diversity-preserving-immune-controller/`
- `failed_experiments/EXP-027-distance-gated-immune-controller/`

