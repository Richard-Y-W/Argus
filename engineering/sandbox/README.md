# Argus research sandbox

This is the lab's fast testing area. It answers “is this idea coherent and technically feasible?” before a full registered experiment is built.

## Rules

1. Use only synthetic data or a documented, pinned local dataset.
2. Put each probe in a dated subdirectory with `question.md`, one runnable script, and machine-readable output.
3. Mark all output **exploratory**. Sandbox results cannot appear as evidence in a conclusion.
4. Check timing, denominator stability, missingness, sample size, and a negative control before interpreting an effect.
5. If a probe is promising, create a sequential HYP/EXP pair, register predictions and design in Git, then rerun from an experiment-owned script.
6. If it fails, keep the probe and add a two-sentence postmortem.

Run infrastructure checks from the repository root:

```powershell
pytest engineering/tests
```

The sandbox is intentionally not notebook-only: every number must come from a runnable script and a saved table.
