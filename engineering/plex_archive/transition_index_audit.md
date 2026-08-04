# Pre-outcome transition index audit

**Frozen before inspecting PLEX rows in the transition files.**

EVE Ref lists 48 normal-sized snapshots on July 7, 2025. On July 8, files through 12:45 UTC are approximately 19.4 MB compressed. The 13:15 and 13:45 files are approximately 1.05 MB, followed by a return to approximately 19.5 MB at 14:15.

The incomplete-snapshot rule is fixed as:

> Exclude a snapshot from treatment classification when its compressed byte size is less than 50% of the median compressed size for that UTC day.

Under the July 8 index, 13:15 and 13:45 fail this rule. They cannot establish absence, cancellation completion, or first global availability. The initial payload probe found that the otherwise valid 12:45 snapshot was already entirely global, proving that the tiny-file interval was a later archive outage rather than the market-formation boundary. The audit therefore moves backward to the pinned 11:45 and 12:15 snapshots. This update follows observed source content but does not change the incomplete-file rule.

No economic outcome is tested in this audit.
