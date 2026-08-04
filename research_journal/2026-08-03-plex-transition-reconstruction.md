# 2026-08-03 — PLEX transition reconstruction

## Stage and attribution

External-data engineering and treatment audit; **Human-directed**.

## Result

**SUPPORTED WITH LIMITS.** Complete EVE Ref snapshots identify a 59-region book at 10:45, zero PLEX orders at 11:15, and a 130-order global book at 11:45 UTC on July 7, 2025. The event is now represented as cancellation plus formation, not a single daily indicator.

## Data integrity

The pipeline records source URL, file time, byte size, ETag, last-modified time, research-download time, and SHA-256. Raw full-market archives are streamed from temporary storage and deleted. Six offline tests cover schema rejection, PLEX filtering, global classification, incomplete-file rejection, fixed-time selection, and time-substitution rejection.

## Boundary

This is treatment semantics, not market-quality evidence. PLEX outcomes were inspected only to classify the regime boundary. Registration awaits pre-event-only controls and tested book metrics.

## Connections

PLEX dataset record · transition audit · extractor · PLEX knowledge graph

