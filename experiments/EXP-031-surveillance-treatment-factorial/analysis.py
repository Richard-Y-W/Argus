"""EXP-031 detector-by-treatment factorial on frozen EXP-030 paths."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
BASE_PATH = HERE.parent / "EXP-030-invariant-restoring-defense" / "analysis.py"
SPEC = importlib.util.spec_from_file_location("exp030_frozen", BASE_PATH)
base = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(base)
POLICIES = ("breach_proportional", "breach_targeted", "early_proportional", "early_targeted")


def policy_parts(policy: str) -> tuple[str, str]:
    trigger, treatment = policy.split("_", 1)
    return trigger, treatment


def should_trigger(trigger: str, leverage: float, lcr: float) -> bool:
    if trigger == "early":
        return leverage > 2.90 or lcr < 1.05
    if trigger == "breach":
        return leverage > 3.0 or lcr < 1.0
    raise ValueError(trigger)


def simulate(family: str, seed: int, policy: str) -> dict[str, float | str | int]:
    returns = base.return_path(family, seed)
    exposure, equity, buffer = np.full(base.N, 40.0), 100.0, 32.0
    peak, maximum_drawdown = equity, 0.0
    module_history: list[np.ndarray] = []
    violation_area = healthy_reduction = total_reduction = 0.0
    breach_days = false_action_days = 0
    first_breach, recovery_day, healthy_run = None, None, 0
    trigger, treatment = policy_parts(policy)
    for day in range(base.DAYS):
        mean, vol, corr, drain, growth, multipliers, culprits = base.family_state(family, day)
        if growth:
            exposure[1] *= 1.0 + growth
        pnl_by_module = exposure * returns[day]
        pnl = float(pnl_by_module.sum())
        equity += pnl
        buffer -= drain + 0.10 * max(-pnl, 0.0) * (corr >= 0.70)
        module_history.append(pnl_by_module)
        leverage, lcr = base.metrics(exposure, equity, buffer, multipliers)
        actual_breach = leverage > 3.0 or lcr < 1.0
        violation_area += max(leverage - 3.0, 0.0) + max(1.0 - lcr, 0.0)
        breach_days += int(actual_breach)
        if actual_breach and first_breach is None:
            first_breach = day
        healthy_run = 0 if actual_breach else healthy_run + 1
        if first_breach is not None and recovery_day is None and healthy_run >= 5:
            recovery_day = day - 4
        reductions = np.zeros(base.N)
        if should_trigger(trigger, leverage, lcr):
            stress = float(vol.mean() / 0.01)
            if treatment == "proportional":
                exposure, equity, buffer, reductions = base.proportional_action(
                    exposure, equity, buffer, multipliers, 2.85, 1.10, stress)
            else:
                recent = np.sum(module_history[-10:], axis=0)
                exposure, equity, buffer, reductions = base.immune_action(
                    exposure, equity, buffer, multipliers, recent, stress)
        action = float(reductions.sum())
        total_reduction += action
        false_action_days += int(action > 1e-12 and not actual_breach)
        healthy = np.ones(base.N, dtype=bool)
        if culprits:
            healthy[list(culprits)] = False
        healthy_reduction += float(reductions[healthy].sum())
        peak = max(peak, equity)
        maximum_drawdown = min(maximum_drawdown, equity / peak - 1.0)
    recovery = 0 if first_breach is None else (
        base.DAYS - first_breach if recovery_day is None else recovery_day - first_breach)
    return {"family": family, "seed": seed, "policy": policy,
            "violation_area": violation_area, "breach_days": breach_days,
            "recovery_days": recovery, "total_reduction": total_reduction,
            "healthy_reduction": healthy_reduction, "terminal_equity": equity,
            "maximum_drawdown": maximum_drawdown, "false_action_days": false_action_days}


def interval(frame: pd.DataFrame, left: str, right: str, metric: str, seed: int,
             reps: int = 10_000) -> tuple[float, float, float]:
    return base.stratified_interval(frame, left, right, metric, seed, reps)


def main() -> None:
    rows = [simulate(family, seed, policy)
            for family in base.FAMILIES for seed in base.SEEDS for policy in POLICIES]
    frame = pd.DataFrame(rows)
    comparisons = []
    specs = [
        ("early_targeted", "early_proportional", "violation_area", "treatment_at_early"),
        ("early_targeted", "early_proportional", "healthy_reduction", "treatment_at_early"),
        ("early_targeted", "early_proportional", "terminal_equity", "treatment_at_early"),
        ("breach_targeted", "breach_proportional", "violation_area", "treatment_at_breach"),
        ("breach_targeted", "breach_proportional", "healthy_reduction", "treatment_at_breach"),
        ("early_proportional", "breach_proportional", "violation_area", "early_warning_proportional"),
        ("early_targeted", "breach_targeted", "violation_area", "early_warning_targeted"),
        ("early_targeted", "early_proportional", "false_action_days", "treatment_at_early"),
    ]
    for number, (left, right, metric, estimand) in enumerate(specs):
        estimate, low, high = interval(frame, left, right, metric, 32000 + number)
        comparisons.append({"estimand": estimand, "left": left, "right": right, "metric": metric,
                            "estimate": estimate, "ci_low": low, "ci_high": high})
    summary = frame.groupby(["family", "policy"], as_index=False).mean(numeric_only=True)
    pivot = frame.pivot(index=["family", "seed"], columns="policy", values="violation_area").reset_index()
    breadth = pivot.groupby("family").apply(
        lambda x: pd.Series({"early_targeted_mean": x.early_targeted.mean(),
                             "early_proportional_mean": x.early_proportional.mean(),
                             "targeted_lower": x.early_targeted.mean() < x.early_proportional.mean()}),
        include_groups=False).reset_index()
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "seed_outcomes.csv", index=False)
    summary.to_csv(OUT / "family_summary.csv", index=False)
    pd.DataFrame(comparisons).to_csv(OUT / "comparisons.csv", index=False)
    breadth.to_csv(OUT / "family_breadth.csv", index=False)
    metadata = {"base_analysis_sha256": hashlib.sha256(BASE_PATH.read_bytes()).hexdigest(),
                "analysis_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "families": base.FAMILIES, "seed_range": [base.SEEDS[0], base.SEEDS[-1]],
                "restoration_target": {"max_leverage": 2.85, "min_lcr": 1.10}}
    (OUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(pd.DataFrame(comparisons).to_string(index=False))
    print(breadth.to_string(index=False))


if __name__ == "__main__":
    main()

