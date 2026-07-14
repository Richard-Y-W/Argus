# engineering

Reusable research infrastructure and a fast falsification sandbox.

- `argus_lab/`: small shared statistical primitives.
- `tests/`: synthetic-data unit tests.
- `sandbox/`: exploratory probes that cannot support claims until promoted into a registered experiment.

The current infrastructure is deliberately small. Data loaders and event-window construction should migrate here only after two experiments genuinely share the same semantics.
