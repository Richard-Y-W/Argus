from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
BASE_PATH = HERE.parent / "EXP-025-financial-genome-adaptation" / "analysis.py"
SPEC = importlib.util.spec_from_file_location("exp025_base", BASE_PATH)
B = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = B
SPEC.loader.exec_module(B)

OUT = HERE / "results"
FAMILIES = {
    "rotation": tuple(range(20_000, 20_012)),
    "correlation_flip": tuple(range(30_000, 30_012)),
    "mean_reversion": tuple(range(40_000, 40_012)),
}
METHODS = ("evolution", "random", "hybrid_quality", "hybrid_diverse")
START, MID, END = 252, 378, 504
BOOTSTRAPS = 10_000


def simulate_family(seed: int, family: str) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pre = dict(mu=np.array([0.00025, 0.00012, 0.00008]),
               phi=np.array([0.12, 0.04, -0.03]), vol=np.array([0.010, 0.006, 0.009]),
               corr=np.array([[1, -0.20, 0.10], [-0.20, 1, 0.05], [0.10, 0.05, 1]]))
    posts = {
        "rotation": dict(mu=np.array([-0.00005, 0.00015, 0.00030]),
                         phi=np.array([-0.10, 0.06, 0.18]), vol=np.array([0.012, 0.007, 0.010]),
                         corr=np.array([[1, -0.10, 0.15], [-0.10, 1, 0.10], [0.15, 0.10, 1]])),
        "correlation_flip": dict(mu=np.array([0.00002, -0.00008, 0.00024]),
                                 phi=np.array([-0.16, -0.05, 0.14]), vol=np.array([0.015, 0.011, 0.008]),
                                 corr=np.array([[1, 0.55, 0.25], [0.55, 1, 0.20], [0.25, 0.20, 1]])),
        "mean_reversion": dict(mu=np.array([-0.00010, 0.00004, 0.00010]),
                               phi=np.array([-0.28, -0.20, -0.14]), vol=np.array([0.013, 0.008, 0.011]),
                               corr=np.array([[1, 0.15, -0.05], [0.15, 1, 0.10], [-0.05, 0.10, 1]])),
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


def phenotype_signature(genome: B.Genome, returns: np.ndarray, end: int) -> np.ndarray:
    weights = np.array([B.weight(genome, returns, t) for t in range(end - 21, end)])
    return np.r_[weights.mean(axis=0), weights.std(axis=0, ddof=1)]


def standardized_signatures(genomes: list[B.Genome], returns: np.ndarray, end: int) -> np.ndarray:
    x = np.array([phenotype_signature(g, returns, end) for g in genomes])
    scale = x.std(axis=0, ddof=1)
    scale = np.where(scale < 1e-8, np.inf, scale)
    return (x - x.mean(axis=0)) / scale


def pairwise_diversity(x: np.ndarray) -> float:
    distances = [np.linalg.norm(x[i] - x[j]) for i in range(len(x)) for j in range(i)]
    return float(np.mean(distances)) if distances else 0.0


def generate_candidates(method: str, population: list[B.Genome], rng: np.random.Generator) -> tuple[list[B.Genome], list[str]]:
    if method == "evolution":
        return ([B.mutate(parent, rng)[0] for parent in population for _ in range(4)], ["child"] * 48)
    if method == "random":
        return ([B.draw_genome(rng) for _ in range(48)], ["immigrant"] * 48)
    if method in ("hybrid_quality", "hybrid_diverse"):
        children = [B.mutate(parent, rng)[0] for parent in population for _ in range(3)]
        immigrants = [B.draw_genome(rng) for _ in range(12)]
        return children + immigrants, ["child"] * 36 + ["immigrant"] * 12
    raise ValueError(method)


def select_quality(pool: list[B.Genome], returns: np.ndarray, end: int) -> list[B.Genome]:
    scored = [(B.fitness(g, returns, end), i, g) for i, g in enumerate(pool)]
    return [x[2] for x in sorted(scored, key=lambda z: (-z[0], z[1]))[:12]]


def select_diverse(pool: list[B.Genome], returns: np.ndarray, end: int) -> tuple[list[B.Genome], float]:
    fitness = np.array([B.fitness(g, returns, end) for g in pool])
    order = np.argsort(-fitness, kind="stable")
    selected = list(order[:8])
    floor = float(np.median(fitness))
    eligible = [int(i) for i in order[8:] if fitness[i] >= floor]
    signatures = standardized_signatures(pool, returns, end)
    while len(selected) < 12 and eligible:
        scores = []
        for i in eligible:
            minimum = min(np.linalg.norm(signatures[i] - signatures[j]) for j in selected)
            scores.append((minimum, -i, i))
        chosen = max(scores)[2]
        selected.append(chosen)
        eligible.remove(chosen)
    if len(selected) < 12:
        selected.extend([int(i) for i in order if i not in selected][:12 - len(selected)])
    return [pool[i] for i in selected], min(float(fitness[i]) for i in selected[8:]) - floor


def method_path(method: str, returns: np.ndarray, initial: list[B.Genome], seed: int) -> tuple[np.ndarray, np.ndarray, list[B.Genome], int, float]:
    population = list(initial)
    net_path = np.zeros(B.END)
    gross_path = np.zeros(B.END)
    evaluated = 0
    reserve_margin = np.nan
    rng = np.random.default_rng(seed)
    for start in range(START, END, B.STEP):
        candidates, _ = generate_candidates(method, population, rng)
        evaluated += len(candidates)
        pool = population + candidates
        if method == "hybrid_diverse":
            population, reserve_margin = select_diverse(pool, returns, start)
        else:
            population = select_quality(pool, returns, start)
        block_end = min(start + B.STEP, END)
        net_path[start:block_end], gross_path[start:block_end] = B.ensemble_block(population, returns, start, block_end)
    return net_path, gross_path, population, evaluated, reserve_margin


def metrics(net: np.ndarray, gross: np.ndarray, population: list[B.Genome], returns: np.ndarray) -> dict[str, float]:
    full = net[START:END]
    early = net[START:MID]
    q = np.quantile(full, 0.05)
    es = -float(full[full <= q].mean()) * B.TRADING_DAYS
    return {
        "full_return": float(full.sum()), "early_return": float(early.sum()),
        "annual_volatility": float(full.std(ddof=1) * np.sqrt(B.TRADING_DAYS)),
        "annual_es_5": es,
        "annual_turnover": float((gross[START:END].mean() - full.mean()) * B.TRADING_DAYS / B.COST),
        "genome_diversity": B.normalized_distance(population),
        "phenotype_diversity": pairwise_diversity(
            np.array([phenotype_signature(g, returns, END) for g in population])),
    }


def run_seed(seed: int, family: str) -> list[dict[str, float | int | str]]:
    returns = simulate_family(seed, family)
    init_rng = np.random.default_rng(seed + 1_000_000)
    initial = [B.draw_genome(init_rng) for _ in range(B.POPULATION)]
    rows = []
    for offset, method in enumerate(METHODS):
        net, gross, population, evaluated, margin = method_path(method, returns, initial, seed + 2_000_000 + offset)
        rows.append({"seed": seed, "family": family, "method": method,
                     **metrics(net, gross, population, returns),
                     "evaluated_candidates": evaluated, "reserve_floor_margin": margin})
    return rows


def run_seed_args(args: tuple[int, str]) -> list[dict[str, float | int | str]]:
    return run_seed(*args)


def stratified_bootstrap(frame: pd.DataFrame, endpoint: str, left: str, right: str, seed: int) -> tuple[float, float, float]:
    pivot = frame.pivot(index=["family", "seed"], columns="method", values=endpoint)
    differences = pivot[left] - pivot[right]
    by_family = {family: group.to_numpy() for family, group in differences.groupby(level="family")}
    estimate = float(np.mean([x.mean() for x in by_family.values()]))
    rng = np.random.default_rng(seed)
    draws = np.empty(BOOTSTRAPS)
    for b in range(BOOTSTRAPS):
        draws[b] = np.mean([rng.choice(x, len(x), replace=True).mean() for x in by_family.values()])
    return estimate, float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))


def summarize(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, bool]]:
    full_e = stratified_bootstrap(frame, "full_return", "hybrid_diverse", "evolution", 2026080261)
    full_r = stratified_bootstrap(frame, "full_return", "hybrid_diverse", "random", 2026080262)
    early_e = stratified_bootstrap(frame, "early_return", "hybrid_diverse", "evolution", 2026080263)
    early_r = stratified_bootstrap(frame, "early_return", "hybrid_diverse", "random", 2026080264)
    means = frame.groupby(["family", "method"]).mean(numeric_only=True)
    diversity_ratios = [means.loc[(f, "hybrid_diverse"), "phenotype_diversity"] /
                        means.loc[(f, "evolution"), "phenotype_diversity"] for f in FAMILIES]
    es = frame.groupby("method").annual_es_5.mean()
    es_gap = float(es["hybrid_diverse"] - min(es["evolution"], es["random"]))
    summary = pd.DataFrame([
        {"endpoint": "hybrid_minus_evolution_full", "estimate": full_e[0], "ci_low": full_e[1], "ci_high": full_e[2]},
        {"endpoint": "hybrid_minus_random_full", "estimate": full_r[0], "ci_low": full_r[1], "ci_high": full_r[2]},
        {"endpoint": "hybrid_minus_evolution_early", "estimate": early_e[0], "ci_low": early_e[1], "ci_high": early_e[2]},
        {"endpoint": "hybrid_minus_random_early", "estimate": early_r[0], "ci_low": early_r[1], "ci_high": early_r[2]},
        {"endpoint": "minimum_family_phenotype_diversity_ratio", "estimate": min(diversity_ratios), "ci_low": np.nan, "ci_high": np.nan},
        {"endpoint": "hybrid_es_minus_better_baseline", "estimate": es_gap, "ci_low": np.nan, "ci_high": np.nan},
    ])
    tests = {"P1": full_e[1] > 0, "P2": full_r[1] > 0,
             "P3": early_e[1] > -0.005 and early_r[1] > -0.005,
             "P4": min(diversity_ratios) >= 1.25, "P5": es_gap <= 0.05}
    tests["joint"] = all(tests.values())
    return summary, tests


def main() -> None:
    if "--finalize-existing" in sys.argv:
        frame = pd.read_csv(OUT / "seed_metrics.csv")
        write_outputs(frame)
        return
    jobs = [(seed, family) for family, seeds in FAMILIES.items() for seed in seeds]
    rows = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        for result in executor.map(run_seed_args, jobs):
            rows.extend(result)
    frame = pd.DataFrame(rows)
    counts = frame.groupby(["family", "seed"]).evaluated_candidates.nunique()
    assert (counts == 1).all() and (frame.evaluated_candidates == 576).all()
    assert frame.loc[frame.method == "hybrid_diverse", "reserve_floor_margin"].min() >= -1e-12
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "seed_metrics.csv", index=False)
    write_outputs(frame)


def write_outputs(frame: pd.DataFrame) -> None:
    summary, tests = summarize(frame)
    summary.to_csv(OUT / "summary.csv", index=False)
    tests = {key: bool(value) for key, value in tests.items()}
    (OUT / "run_log.json").write_text(json.dumps({"families": {k: len(v) for k, v in FAMILIES.items()},
                                                   "tests": tests}, indent=2), encoding="utf-8")
    digest = hashlib.sha256((OUT / "seed_metrics.csv").read_bytes()).hexdigest()
    (OUT / "sha256.txt").write_text(digest + "\n", encoding="ascii")
    print(summary.to_string(index=False))
    print(json.dumps(tests, indent=2))
    print(f"seed_metrics_sha256={digest}")


if __name__ == "__main__":
    main()
