from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
EXP26_PATH = HERE.parent / "EXP-026-diversity-preserving-financial-genetics" / "analysis.py"
SPEC = importlib.util.spec_from_file_location("exp026_base", EXP26_PATH)
E = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = E
SPEC.loader.exec_module(E)
B = E.B

OUT = HERE / "results"
START, MID, END = 252, 378, 504
REFERENCE = slice(126, 252)
RECENT = 63
LOW, HIGH = 1.25, 2.50
BOOTSTRAPS = 10_000
FAMILIES = {
    "small_drift": tuple(range(50_000, 50_006)),
    "moderate_rotation": tuple(range(60_000, 60_006)),
    "mean_reversion": tuple(range(70_000, 70_006)),
    "correlation_break": tuple(range(80_000, 80_006)),
}
METHODS = ("evolution", "random", "hybrid", "gate")


def simulate_family(seed: int, family: str) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pre = dict(mu=np.array([0.00025, 0.00012, 0.00008]),
               phi=np.array([0.12, 0.04, -0.03]), vol=np.array([0.010, 0.006, 0.009]),
               corr=np.array([[1, -0.20, 0.10], [-0.20, 1, 0.05], [0.10, 0.05, 1]]))
    posts = {
        "small_drift": dict(mu=np.array([0.00022, 0.00014, 0.00010]),
                            phi=np.array([0.09, 0.06, -0.01]), vol=np.array([0.0105, 0.0063, 0.0092]),
                            corr=np.array([[1, -0.15, 0.12], [-0.15, 1, 0.06], [0.12, 0.06, 1]])),
        "moderate_rotation": dict(mu=np.array([-0.00002, 0.00016, 0.00027]),
                                  phi=np.array([-0.06, 0.08, 0.16]), vol=np.array([0.012, 0.007, 0.010]),
                                  corr=np.array([[1, -0.08, 0.16], [-0.08, 1, 0.10], [0.16, 0.10, 1]])),
        "mean_reversion": dict(mu=np.array([-0.00008, 0.00005, 0.00011]),
                               phi=np.array([-0.25, -0.18, -0.12]), vol=np.array([0.013, 0.008, 0.011]),
                               corr=np.array([[1, 0.12, -0.04], [0.12, 1, 0.11], [-0.04, 0.11, 1]])),
        "correlation_break": dict(mu=np.array([0.00001, -0.00010, 0.00023]),
                                  phi=np.array([-0.18, -0.08, 0.15]), vol=np.array([0.016, 0.012, 0.008]),
                                  corr=np.array([[1, 0.65, 0.30], [0.65, 1, 0.25], [0.30, 0.25, 1]])),
    }
    if family not in posts:
        raise ValueError(family)
    returns = np.zeros((B.END, 3))
    for t in range(B.END):
        p = pre if t < START else posts[family]
        cov = np.outer(p["vol"], p["vol"]) * p["corr"]
        prior = returns[t - 1] if t else p["mu"]
        returns[t] = p["mu"] + p["phi"] * (prior - p["mu"]) + rng.multivariate_normal(np.zeros(3), cov)
    return returns


def ar1(x: np.ndarray) -> np.ndarray:
    prior, current = x[:-1], x[1:]
    prior = prior - prior.mean(axis=0)
    current = current - current.mean(axis=0)
    denominator = np.sum(prior ** 2, axis=0)
    return np.divide(np.sum(prior * current, axis=0), denominator,
                     out=np.zeros(3), where=denominator > 1e-16)


def safe_corr(x: np.ndarray) -> np.ndarray:
    if np.any(x.std(axis=0, ddof=1) < 1e-16):
        return np.eye(x.shape[1])
    return np.corrcoef(x, rowvar=False)


def environmental_distance(returns: np.ndarray, end: int) -> float:
    ref = returns[REFERENCE]
    recent = returns[end - RECENT:end]
    n0, n1 = len(ref), len(recent)
    ref_vol = ref.std(axis=0, ddof=1)
    recent_vol = recent.std(axis=0, ddof=1)
    mean_se = ref_vol * np.sqrt(1 / n0 + 1 / n1)
    mean_z = np.divide(recent.mean(axis=0) - ref.mean(axis=0), mean_se,
                       out=np.zeros(3), where=mean_se > 1e-16)
    logvol_se = np.sqrt(1 / (2 * (n0 - 1)) + 1 / (2 * (n1 - 1)))
    vol_z = np.log(np.maximum(recent_vol, 1e-16) / np.maximum(ref_vol, 1e-16)) / logvol_se
    corr0, corr1 = safe_corr(ref), safe_corr(recent)
    pairs = ((0, 1), (0, 2), (1, 2))
    corr_se = np.sqrt(1 / (n0 - 3) + 1 / (n1 - 3))
    corr_z = np.array([(np.arctanh(np.clip(corr1[i, j], -0.999, 0.999)) -
                             np.arctanh(np.clip(corr0[i, j], -0.999, 0.999))) / corr_se
                       for i, j in pairs])
    phi0, phi1 = ar1(ref), ar1(recent)
    phi_se = np.sqrt((1 - np.clip(phi0, -0.999, 0.999) ** 2) * (1 / n0 + 1 / n1))
    phi_z = np.divide(phi1 - phi0, phi_se, out=np.zeros(3), where=phi_se > 1e-16)
    components = np.r_[mean_z, vol_z, corr_z, phi_z]
    components = components[np.isfinite(components)]
    return float(np.sqrt(np.mean(components ** 2))) if len(components) else 0.0


def route(distance: float) -> str:
    if distance < LOW:
        return "evolution"
    if distance < HIGH:
        return "hybrid_quality"
    return "random"


def generate(method: str, population: list[B.Genome], rng: np.random.Generator,
             returns: np.ndarray, end: int) -> tuple[list[B.Genome], str, float]:
    if method == "gate":
        distance = environmental_distance(returns, end)
        chosen = route(distance)
    else:
        distance = np.nan
        chosen = "hybrid_quality" if method == "hybrid" else method
    candidates, _ = E.generate_candidates(chosen, population, rng)
    return candidates, chosen, distance


def method_path(method: str, returns: np.ndarray, initial: list[B.Genome], seed: int):
    population = list(initial)
    net = np.zeros(B.END)
    gross = np.zeros(B.END)
    routes = {"evolution": 0, "hybrid_quality": 0, "random": 0}
    distances = []
    evaluated = 0
    rng = np.random.default_rng(seed)
    for start in range(START, END, B.STEP):
        candidates, chosen, distance = generate(method, population, rng, returns, start)
        routes[chosen] += 1
        if np.isfinite(distance):
            distances.append(distance)
        evaluated += len(candidates)
        population = E.select_quality(population + candidates, returns, start)
        block_end = min(start + B.STEP, END)
        net[start:block_end], gross[start:block_end] = B.ensemble_block(population, returns, start, block_end)
    total_routes = sum(routes.values())
    return net, gross, evaluated, {k: v / total_routes for k, v in routes.items()}, float(np.mean(distances)) if distances else np.nan


def metrics(net: np.ndarray, gross: np.ndarray) -> dict[str, float]:
    full, early = net[START:END], net[START:MID]
    q = np.quantile(full, 0.05)
    return {
        "full_return": float(full.sum()), "early_return": float(early.sum()),
        "annual_volatility": float(full.std(ddof=1) * np.sqrt(B.TRADING_DAYS)),
        "annual_es_5": -float(full[full <= q].mean()) * B.TRADING_DAYS,
        "annual_turnover": float((gross[START:END].mean() - full.mean()) * B.TRADING_DAYS / B.COST),
    }


def run_seed(seed: int, family: str):
    returns = simulate_family(seed, family)
    init_rng = np.random.default_rng(seed + 1_000_000)
    initial = [B.draw_genome(init_rng) for _ in range(B.POPULATION)]
    rows = []
    for offset, method in enumerate(METHODS):
        net, gross, evaluated, routes, mean_distance = method_path(
            method, returns, initial, seed + 2_000_000 + offset)
        rows.append({"seed": seed, "family": family, "method": method, **metrics(net, gross),
                     "evaluated_candidates": evaluated, "mean_distance": mean_distance,
                     "local_share": routes["evolution"], "hybrid_share": routes["hybrid_quality"],
                     "global_share": routes["random"]})
    return rows


def run_seed_args(args):
    return run_seed(*args)


def stratified_bootstrap(frame: pd.DataFrame, baseline: str, seed: int):
    pivot = frame.pivot(index=["family", "seed"], columns="method", values="full_return")
    differences = pivot["gate"] - pivot[baseline]
    groups = [x.to_numpy() for _, x in differences.groupby(level="family")]
    estimate = float(np.mean([x.mean() for x in groups]))
    rng = np.random.default_rng(seed)
    draws = np.empty(BOOTSTRAPS)
    for i in range(BOOTSTRAPS):
        draws[i] = np.mean([rng.choice(x, len(x), replace=True).mean() for x in groups])
    return estimate, float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))


def summarize(frame: pd.DataFrame):
    comparisons = {m: stratified_bootstrap(frame, m, 2026080300 + i)
                   for i, m in enumerate(("evolution", "random", "hybrid"), 1)}
    gate = frame[frame.method == "gate"]
    route_means = gate.groupby("family").global_share.mean()
    order = ["small_drift", "moderate_rotation", "mean_reversion", "correlation_break"]
    monotonic = all(route_means[order[i]] < route_means[order[i + 1]] for i in range(3))
    es = frame.groupby("method").annual_es_5.mean()
    es_gap = float(es["gate"] - min(es[m] for m in ("evolution", "random", "hybrid")))
    rows = [{"endpoint": f"gate_minus_{m}_full", "estimate": v[0], "ci_low": v[1], "ci_high": v[2]}
            for m, v in comparisons.items()]
    rows += [{"endpoint": f"global_share_{family}", "estimate": route_means[family],
              "ci_low": np.nan, "ci_high": np.nan} for family in order]
    rows.append({"endpoint": "gate_es_minus_best_fixed", "estimate": es_gap,
                 "ci_low": np.nan, "ci_high": np.nan})
    tests = {"P1": comparisons["evolution"][1] > 0,
             "P2": comparisons["random"][1] > 0,
             "P3": comparisons["hybrid"][1] > 0,
             "P4": monotonic, "P5": es_gap <= 0.05}
    tests["joint"] = all(tests.values())
    return pd.DataFrame(rows), {k: bool(v) for k, v in tests.items()}


def main() -> None:
    jobs = [(seed, family) for family, seeds in FAMILIES.items() for seed in seeds]
    rows = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        for result in executor.map(run_seed_args, jobs):
            rows.extend(result)
    frame = pd.DataFrame(rows)
    assert (frame.evaluated_candidates == 576).all()
    summary, tests = summarize(frame)
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "seed_metrics.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.json").write_text(json.dumps({"families": {k: len(v) for k, v in FAMILIES.items()},
                                                   "thresholds": [LOW, HIGH], "tests": tests}, indent=2), encoding="utf-8")
    digest = hashlib.sha256((OUT / "seed_metrics.csv").read_bytes()).hexdigest()
    (OUT / "sha256.txt").write_text(digest + "\n", encoding="ascii")
    print(summary.to_string(index=False))
    print(json.dumps(tests, indent=2))
    print(f"seed_metrics_sha256={digest}")


if __name__ == "__main__":
    main()
