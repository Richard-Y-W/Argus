# engineering

Reusable research infrastructure and a fast falsification sandbox.

- `argus_lab/`: small shared statistical primitives.
- `tests/`: synthetic-data unit tests.
- `cycles/`: preregistered engineering plans and completed audit records.
- `sandbox/`: exploratory probes that cannot support claims until promoted into a registered experiment.

The current infrastructure is deliberately small. Shared JKP metadata parsing, event-window construction, eligibility, and estimation live in `argus_lab/jkp_decay.py`; EXP-016–021 now share those semantics. Synthetic tests run without licensed data, while the EXP-016 golden comparison runs when the pinned local JKP release is present and skips explicitly otherwise.
