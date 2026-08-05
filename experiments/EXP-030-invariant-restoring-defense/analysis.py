"""EXP-030 invariant-restoring defense benchmark."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
FAMILIES = ("liquidity_drain", "leverage_cancer", "systemic_correlation", "combined", "benign_volatility")
POLICIES = ("none", "proportional", "vol_target", "liquidate", "immune")
SEEDS = tuple(range(30000, 30100))
DAYS, N = 120, 6
BASE_OUTFLOW = 0.08
BASE_SYSTEM_OUTFLOW = 5.0


def metrics(exposure: np.ndarray, equity: float, buffer: float, multipliers: np.ndarray) -> tuple[float, float]:
    leverage = exposure.sum() / max(equity, 1e-9)
    outflows = BASE_SYSTEM_OUTFLOW + np.sum(BASE_OUTFLOW * exposure * multipliers)
    return float(leverage), float(buffer / max(outflows, 1e-9))


def family_state(family: str, day: int) -> tuple[np.ndarray, np.ndarray, float, float, float, np.ndarray, set[int]]:
    mean = np.zeros(N)
    vol = np.array([0.009, 0.010, 0.011, 0.008, 0.012, 0.010])
    corr, multipliers, drain, growth = 0.20, np.ones(N), 0.0, 0.0
    culprits: set[int] = set()
    if family == "liquidity_drain" and 30 <= day < 60:
        multipliers[0], drain, culprits = 5.0, 0.35, {0}
    elif family == "leverage_cancer" and 20 <= day < 70:
        mean[1], multipliers[1], growth, culprits = 0.0010, 1.8, 0.012, {1}
    elif family == "systemic_correlation" and 40 <= day < 70:
        mean[:] = -0.0030
        vol, corr, drain, culprits = vol * 2.0, 0.85, 0.10, set(range(N))
    elif family == "combined" and 45 <= day < 75:
        mean[:] = -0.0018
        vol, corr, drain = vol * 1.6, 0.70, 0.15
        multipliers[2], culprits = 4.0, {2}
    elif family == "benign_volatility" and 30 <= day < 60:
        vol, corr = vol * 1.8, 0.35
    return mean, vol, corr, drain, growth, multipliers, culprits


def return_path(family: str, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 100_000 * FAMILIES.index(family))
    path = np.empty((DAYS, N))
    for day in range(DAYS):
        mean, vol, corr, *_ = family_state(family, day)
        covariance = np.outer(vol, vol) * (corr + (1 - corr) * np.eye(N))
        normal = rng.multivariate_normal(np.zeros(N), covariance)
        scale = np.sqrt(rng.chisquare(5) / 5)
        path[day] = mean + normal / scale
    return path


def reduce(exposure: np.ndarray, amount: np.ndarray, equity: float, buffer: float,
           stress: float) -> tuple[np.ndarray, float, float, float]:
    actual = np.minimum(exposure, np.maximum(amount, 0.0))
    total = float(actual.sum())
    exposure = exposure - actual
    equity -= 0.002 * (1.0 + stress) * total
    buffer += 0.15 * total
    return exposure, equity, buffer, total


def proportional_action(exposure: np.ndarray, equity: float, buffer: float,
                        multipliers: np.ndarray, target_lev: float, target_lcr: float,
                        stress: float) -> tuple[np.ndarray, float, float, np.ndarray]:
    reductions = np.zeros(N)
    for _ in range(30):
        leverage, lcr = metrics(exposure, equity, buffer, multipliers)
        if leverage <= target_lev and lcr >= target_lcr:
            break
        amount = 0.05 * exposure
        before = exposure.copy()
        exposure, equity, buffer, _ = reduce(exposure, amount, equity, buffer, stress)
        reductions += before - exposure
    return exposure, equity, buffer, reductions


def immune_action(exposure: np.ndarray, equity: float, buffer: float, multipliers: np.ndarray,
                  recent_module_pnl: np.ndarray, stress: float) -> tuple[np.ndarray, float, float, np.ndarray]:
    exp_score = exposure / max(exposure.sum(), 1e-12)
    out = BASE_OUTFLOW * exposure * multipliers
    out_score = out / max(out.sum(), 1e-12)
    losses = np.maximum(-recent_module_pnl, 0.0)
    loss_score = losses / max(losses.sum(), 1e-12)
    ranking = np.argsort(-(exp_score + out_score + loss_score) / 3.0)
    reductions = np.zeros(N)
    cursor = 0
    for _ in range(30):
        leverage, lcr = metrics(exposure, equity, buffer, multipliers)
        if leverage <= 2.85 and lcr >= 1.10:
            break
        idx = int(ranking[min(cursor, N - 1)])
        step = min(0.05 * max(exposure.sum(), 0.0), exposure[idx])
        amount = np.zeros(N)
        amount[idx] = step
        before = exposure.copy()
        exposure, equity, buffer, _ = reduce(exposure, amount, equity, buffer, stress)
        reductions += before - exposure
        if exposure[idx] <= 1e-9:
            cursor += 1
    return exposure, equity, buffer, reductions


def simulate(family: str, seed: int, policy: str) -> tuple[dict[str, float | str | int], list[dict]]:
    returns = return_path(family, seed)
    exposure, equity, buffer = np.full(N, 40.0), 100.0, 32.0
    peak, maximum_drawdown = equity, 0.0
    module_pnl_history: list[np.ndarray] = []
    portfolio_returns: list[float] = []
    violation_area = healthy_reduction = total_reduction = 0.0
    breach_days = false_action_days = 0
    first_breach, recovery_day, healthy_run = None, None, 0
    trace = []
    for day in range(DAYS):
        mean, vol, corr, drain, growth, multipliers, culprits = family_state(family, day)
        if growth:
            exposure[1] *= 1.0 + growth
        pnl_by_module = exposure * returns[day]
        pnl = float(pnl_by_module.sum())
        prior_equity = equity
        equity += pnl
        buffer -= drain + 0.10 * max(-pnl, 0.0) * (corr >= 0.70)
        module_pnl_history.append(pnl_by_module)
        portfolio_returns.append(pnl / max(prior_equity, 1e-9))
        leverage, lcr = metrics(exposure, equity, buffer, multipliers)
        actual_breach = leverage > 3.0 or lcr < 1.0
        violation = max(leverage - 3.0, 0.0) + max(1.0 - lcr, 0.0)
        violation_area += violation
        breach_days += int(actual_breach)
        if actual_breach and first_breach is None:
            first_breach = day
        healthy_run = 0 if actual_breach else healthy_run + 1
        if first_breach is not None and recovery_day is None and healthy_run >= 5:
            recovery_day = day - 4
        reductions = np.zeros(N)
        stress = float(vol.mean() / 0.01)
        if policy == "proportional" and actual_breach:
            exposure, equity, buffer, reductions = proportional_action(
                exposure, equity, buffer, multipliers, 2.90, 1.05, stress)
        elif policy == "liquidate" and actual_breach:
            before = exposure.copy()
            exposure, equity, buffer, _ = reduce(exposure, 0.90 * exposure, equity, buffer, stress)
            reductions = before - exposure
        elif policy == "vol_target" and len(portfolio_returns) >= 20:
            realized = np.std(portfolio_returns[-20:], ddof=1) * np.sqrt(252)
            if realized > 0.18:
                scale = max(0.0, min(1.0, 0.15 / realized))
                before = exposure.copy()
                exposure, equity, buffer, _ = reduce(exposure, (1 - scale) * exposure, equity, buffer, stress)
                reductions = before - exposure
        elif policy == "immune" and (leverage > 2.90 or lcr < 1.05):
            recent = np.sum(module_pnl_history[-10:], axis=0)
            exposure, equity, buffer, reductions = immune_action(
                exposure, equity, buffer, multipliers, recent, stress)
        action = float(reductions.sum())
        false_action_days += int(action > 1e-12 and not actual_breach)
        total_reduction += action
        healthy = np.ones(N, dtype=bool)
        if culprits:
            healthy[list(culprits)] = False
        healthy_reduction += float(reductions[healthy].sum())
        peak = max(peak, equity)
        maximum_drawdown = min(maximum_drawdown, equity / peak - 1.0)
        trace.append({"family": family, "seed": seed, "policy": policy, "day": day,
                      "leverage": leverage, "lcr": lcr, "equity": equity,
                      "violation": violation, "action": action})
    recovery = 0 if first_breach is None else (DAYS - first_breach if recovery_day is None else recovery_day - first_breach)
    outcome = {"family": family, "seed": seed, "policy": policy,
               "violation_area": violation_area, "breach_days": breach_days,
               "recovery_days": recovery, "total_reduction": total_reduction,
               "healthy_reduction": healthy_reduction, "terminal_equity": equity,
               "maximum_drawdown": maximum_drawdown,
               "false_action_days": false_action_days}
    return outcome, trace


def stratified_interval(frame: pd.DataFrame, left: str, right: str, column: str,
                        seed: int, reps: int = 10_000) -> tuple[float, float, float]:
    pivot = frame.pivot(index=["family", "seed"], columns="policy", values=column)
    difference = (pivot[left] - pivot[right]).rename("difference").reset_index()
    by_family = {family: group.difference.to_numpy() for family, group in difference.groupby("family")}
    rng, boot = np.random.default_rng(seed), np.empty(reps)
    for i in range(reps):
        boot[i] = np.mean([rng.choice(values, len(values), replace=True).mean()
                           for values in by_family.values()])
    estimate = float(difference.difference.mean())
    low, high = np.quantile(boot, [0.025, 0.975])
    return estimate, float(low), float(high)


def main() -> None:
    outcomes, traces = [], []
    for family in FAMILIES:
        for seed in SEEDS:
            for policy in POLICIES:
                outcome, trace = simulate(family, seed, policy)
                outcomes.append(outcome)
                if seed == SEEDS[0]:
                    traces.extend(trace)
    frame, trace_frame = pd.DataFrame(outcomes), pd.DataFrame(traces)
    comparisons = []
    specs = [("violation_area", "proportional"), ("violation_area", "vol_target"),
             ("violation_area", "liquidate"), ("healthy_reduction", "proportional"),
             ("healthy_reduction", "liquidate"), ("terminal_equity", "liquidate")]
    for number, (metric, comparator) in enumerate(specs):
        estimate, low, high = stratified_interval(frame, "immune", comparator, metric, 31000 + number)
        comparisons.append({"metric": metric, "comparator": comparator, "estimate": estimate,
                            "ci_low": low, "ci_high": high})
    summary = frame.groupby(["family", "policy"], as_index=False).mean(numeric_only=True)
    breadth = frame.pivot(index=["family", "seed"], columns="policy", values="violation_area").reset_index()
    family_breadth = breadth.groupby("family").apply(
        lambda x: pd.Series({"immune_mean": x.immune.mean(), "proportional_mean": x.proportional.mean(),
                             "immune_lower": x.immune.mean() < x.proportional.mean()}),
        include_groups=False).reset_index()
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "seed_outcomes.csv", index=False)
    trace_frame.to_csv(OUT / "example_traces.csv", index=False)
    summary.to_csv(OUT / "family_summary.csv", index=False)
    pd.DataFrame(comparisons).to_csv(OUT / "comparisons.csv", index=False)
    family_breadth.to_csv(OUT / "family_breadth.csv", index=False)
    config = {"families": FAMILIES, "policies": POLICIES, "seeds": [SEEDS[0], SEEDS[-1]],
              "days": DAYS, "invariants": {"max_leverage": 3.0, "min_lcr": 1.0}}
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / "run_metadata.json").write_text(json.dumps({"config": config, "analysis_sha256": source_hash}, indent=2) + "\n")
    print(pd.DataFrame(comparisons).to_string(index=False))
    print(family_breadth.to_string(index=False))
    print(summary.query("policy == 'immune'").to_string(index=False))


if __name__ == "__main__":
    main()
