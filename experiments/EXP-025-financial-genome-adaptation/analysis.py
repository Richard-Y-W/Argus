from __future__ import annotations

import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "results"
TRADING_DAYS = 252
COST = 0.0005
POPULATION = 12
CHILDREN = 4
CANDIDATES = POPULATION * CHILDREN
ADAPT_START = 252
SCORE_START = 504
END = 756
STEP = 21
FIT_WINDOW = 126
DEV_SEEDS = tuple(range(10))
CONFIRM_SEEDS = tuple(range(10_000, 10_030))
BOOTSTRAPS = 10_000


@dataclass(frozen=True)
class Genome:
    signal_horizon: int
    vol_horizon: int
    risk_target: float
    asset_cap: float
    drawdown_threshold: float


BOUNDS = {
    "signal_horizon": (5, 160),
    "vol_horizon": (10, 80),
    "risk_target": (0.05, 0.15),
    "asset_cap": (0.35, 0.85),
    "drawdown_threshold": (0.04, 0.20),
}
GENES = tuple(BOUNDS)


def draw_genome(rng: np.random.Generator) -> Genome:
    return Genome(
        int(rng.integers(5, 161)), int(rng.integers(10, 81)),
        float(rng.uniform(0.05, 0.15)), float(rng.uniform(0.35, 0.85)),
        float(rng.uniform(0.04, 0.20)),
    )


def mutate(parent: Genome, rng: np.random.Generator) -> tuple[Genome, str]:
    gene = str(rng.choice(GENES))
    values = asdict(parent)
    sds = {"signal_horizon": 15, "vol_horizon": 8, "risk_target": 0.015,
           "asset_cap": 0.08, "drawdown_threshold": 0.025}
    lo, hi = BOUNDS[gene]
    value = float(np.clip(float(values[gene]) + rng.normal(0, sds[gene]), lo, hi))
    values[gene] = int(round(value)) if gene in ("signal_horizon", "vol_horizon") else value
    return Genome(**values), gene


def simulate_market(seed: int, family: str) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pre = dict(mu=np.array([0.00025, 0.00012, 0.00008]),
               phi=np.array([0.12, 0.04, -0.03]),
               vol=np.array([0.010, 0.006, 0.009]),
               corr=np.array([[1, -0.20, 0.10], [-0.20, 1, 0.05], [0.10, 0.05, 1]]))
    if family == "development":
        post = dict(mu=np.array([-0.00005, 0.00015, 0.00030]),
                    phi=np.array([-0.10, 0.06, 0.18]),
                    vol=np.array([0.012, 0.007, 0.010]),
                    corr=np.array([[1, -0.10, 0.15], [-0.10, 1, 0.10], [0.15, 0.10, 1]]))
    elif family == "confirmation":
        post = dict(mu=np.array([0.00002, -0.00008, 0.00024]),
                    phi=np.array([-0.16, -0.05, 0.14]),
                    vol=np.array([0.015, 0.011, 0.008]),
                    corr=np.array([[1, 0.55, 0.25], [0.55, 1, 0.20], [0.25, 0.20, 1]]))
    else:
        raise ValueError(f"unknown family {family}")
    returns = np.zeros((END, 3))
    for t in range(END):
        p = pre if t < ADAPT_START else post
        cov = np.outer(p["vol"], p["vol"]) * p["corr"]
        innovation = rng.multivariate_normal(np.zeros(3), cov)
        prior = returns[t - 1] if t else p["mu"]
        returns[t] = p["mu"] + p["phi"] * (prior - p["mu"]) + innovation
    return returns


def benchmark_drawdown(returns: np.ndarray, t: int) -> float:
    start = max(0, t - 63)
    wealth = np.exp(np.cumsum(returns[start:t].mean(axis=1)))
    if not len(wealth):
        return 0.0
    return float(1 - wealth[-1] / np.maximum.accumulate(wealth).max())


def weight(genome: Genome, returns: np.ndarray, t: int) -> np.ndarray:
    hs = min(genome.signal_horizon, t)
    hv = min(genome.vol_horizon, t)
    if hs < 2 or hv < 2:
        return np.zeros(3)
    signal = returns[t - hs:t].mean(axis=0) > 0
    vol = returns[t - hv:t].std(axis=0, ddof=1) * np.sqrt(TRADING_DAYS)
    raw = np.where(signal, 1 / np.maximum(vol, 1e-6), 0.0)
    if raw.sum() == 0:
        return np.zeros(3)
    raw /= raw.sum()
    raw = np.minimum(raw, genome.asset_cap)
    forecast = float(np.sqrt(np.sum((raw * vol) ** 2)))
    scale = min(1.0, genome.risk_target / max(forecast, 1e-8))
    if benchmark_drawdown(returns, t) > genome.drawdown_threshold:
        scale *= 0.5
    return raw * scale


def phenotype(genome: Genome, returns: np.ndarray, start: int, end: int) -> tuple[np.ndarray, np.ndarray]:
    net = np.zeros(end - start)
    gross = np.zeros(end - start)
    prior_w = weight(genome, returns, start - 1) if start else np.zeros(3)
    for j, t in enumerate(range(start, end)):
        w = weight(genome, returns, t)
        turnover = float(np.abs(w - prior_w).sum())
        gross[j] = float(w @ returns[t])
        net[j] = gross[j] - COST * turnover
        prior_w = w
    return net, gross


def fitness(genome: Genome, returns: np.ndarray, end: int) -> float:
    net, gross = phenotype(genome, returns, end - FIT_WINDOW, end)
    downside = np.sqrt(np.mean(np.minimum(net, 0) ** 2)) * np.sqrt(TRADING_DAYS)
    turnover_cost = max(0.0, (net.mean() - gross.mean()) * -TRADING_DAYS)
    return float(net.mean() * TRADING_DAYS - 2 * downside - 0.25 * turnover_cost)


def select_top(genomes: list[Genome], returns: np.ndarray, end: int) -> list[Genome]:
    ranked = sorted(((fitness(g, returns, end), i, g) for i, g in enumerate(genomes)),
                    key=lambda x: (-x[0], x[1]))
    return [row[2] for row in ranked[:POPULATION]]


def ensemble_block(population: list[Genome], returns: np.ndarray, start: int, end: int) -> tuple[np.ndarray, np.ndarray]:
    paths = [phenotype(g, returns, start, end) for g in population]
    return np.mean([p[0] for p in paths], axis=0), np.mean([p[1] for p in paths], axis=0)


def normalized_distance(population: list[Genome]) -> float:
    x = np.array([[asdict(g)[k] for k in GENES] for g in population], dtype=float)
    ranges = np.array([BOUNDS[k][1] - BOUNDS[k][0] for k in GENES])
    x /= ranges
    distances = [np.linalg.norm(x[i] - x[j]) for i in range(len(x)) for j in range(i)]
    return float(np.mean(distances)) if distances else 0.0


def method_path(method: str, returns: np.ndarray, initial: list[Genome], seed: int) -> tuple[np.ndarray, np.ndarray, list[Genome], int]:
    population = list(initial)
    path = np.zeros(END)
    gross_path = np.zeros(END)
    evaluated = 0
    rng = np.random.default_rng(seed)
    for start in range(ADAPT_START, END, STEP):
        end = min(start + STEP, END)
        if start <= SCORE_START - 1 and method != "static":
            if method == "evolution":
                children = [mutate(parent, rng)[0] for parent in population for _ in range(CHILDREN)]
            elif method == "random":
                children = [draw_genome(rng) for _ in range(CANDIDATES)]
            else:
                raise ValueError(method)
            evaluated += len(children)
            population = select_top(population + children, returns, start)
        path[start:end], gross_path[start:end] = ensemble_block(population, returns, start, end)
    return path, gross_path, population, evaluated


def oracle_path(returns: np.ndarray, pool: list[Genome]) -> np.ndarray:
    path = np.zeros(END)
    for start in range(ADAPT_START, END, STEP):
        end = min(start + STEP, END)
        scored = [(phenotype(g, returns, start, end)[0].sum(), i, g) for i, g in enumerate(pool)]
        best = max(scored, key=lambda x: (x[0], -x[1]))[2]
        path[start:end] = phenotype(best, returns, start, end)[0]
    return path


def metrics(path: np.ndarray, gross_path: np.ndarray, oracle: np.ndarray) -> dict[str, float]:
    x = path[SCORE_START:END]
    gross = gross_path[SCORE_START:END]
    o = oracle[SCORE_START:END]
    wealth = np.exp(np.cumsum(x))
    recovery = next((i + 1 for i, value in enumerate(wealth) if value >= 1), len(x))
    q = np.quantile(x, 0.05)
    es = -float(x[x <= q].mean()) * TRADING_DAYS
    return {
        "regret": float(o.sum() - x.sum()),
        "recovery_days": float(recovery),
        "annual_return": float(x.mean() * TRADING_DAYS),
        "annual_volatility": float(x.std(ddof=1) * np.sqrt(TRADING_DAYS)),
        "annual_es_5": es,
        "annual_turnover": float((gross.mean() - x.mean()) * TRADING_DAYS / COST),
    }


def run_seed(seed: int, family: str) -> list[dict[str, float | int | str]]:
    returns = simulate_market(seed, family)
    init_rng = np.random.default_rng(seed + 1_000_000)
    initial = [draw_genome(init_rng) for _ in range(POPULATION)]
    oracle_rng = np.random.default_rng(seed + 2_000_000)
    oracle = oracle_path(returns, [draw_genome(oracle_rng) for _ in range(100)])
    rows = []
    for offset, method in enumerate(("static", "random", "evolution")):
        path, gross_path, final, evaluated = method_path(method, returns, initial, seed + 3_000_000 + offset)
        row = {"seed": seed, "family": family, "method": method, **metrics(path, gross_path, oracle),
               "genome_diversity": normalized_distance(final), "evaluated_candidates": evaluated}
        rows.append(row)
    return rows


def paired_bootstrap(values: np.ndarray, seed: int) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    means = np.empty(BOOTSTRAPS)
    for i in range(BOOTSTRAPS):
        means[i] = rng.choice(values, size=len(values), replace=True).mean()
    return float(values.mean()), float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def run_seed_args(args: tuple[int, str]) -> list[dict[str, float | int | str]]:
    return run_seed(*args)


def summarize(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, bool]]:
    confirm = frame[frame.family == "confirmation"]
    wide = confirm.pivot(index="seed", columns="method")
    d_regret = wide["regret"]["random"] - wide["regret"]["evolution"]
    d_recovery = wide["recovery_days"]["random"] - wide["recovery_days"]["evolution"]
    r1 = paired_bootstrap(d_regret.to_numpy(), 2026080201)
    r2 = paired_bootstrap(d_recovery.to_numpy(), 2026080202)
    vols = confirm.groupby("method").annual_volatility.mean()
    es = confirm.groupby("method").annual_es_5.mean()
    ratio = float(vols["evolution"] / vols["random"])
    rows = pd.DataFrame([
        {"endpoint": "random_minus_evolution_regret", "estimate": r1[0], "ci_low": r1[1], "ci_high": r1[2]},
        {"endpoint": "random_minus_evolution_recovery_days", "estimate": r2[0], "ci_low": r2[1], "ci_high": r2[2]},
        {"endpoint": "evolution_to_random_volatility", "estimate": ratio, "ci_low": np.nan, "ci_high": np.nan},
        {"endpoint": "evolution_minus_random_annual_es_5", "estimate": float(es["evolution"] - es["random"]), "ci_low": np.nan, "ci_high": np.nan},
    ])
    tests = {"P1": r1[1] > 0, "P2": r2[1] > 0, "P3": 0.90 <= ratio <= 1.10,
             "P4": float(es["evolution"] - es["random"]) <= 0.0005}
    tests["joint"] = all(tests.values())
    return rows, tests


def main() -> None:
    jobs = [(seed, "development") for seed in DEV_SEEDS]
    jobs += [(seed, "confirmation") for seed in CONFIRM_SEEDS]
    rows = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        for result in executor.map(run_seed_args, jobs):
            rows.extend(result)
    frame = pd.DataFrame(rows)
    assert frame.groupby(["family", "seed"]).evaluated_candidates.apply(
        lambda x: x.loc[frame.loc[x.index, "method"] == "random"].iloc[0] ==
                  x.loc[frame.loc[x.index, "method"] == "evolution"].iloc[0]).all()
    summary, tests = summarize(frame)
    OUT.mkdir(exist_ok=True)
    frame.to_csv(OUT / "seed_metrics.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    payload = {"constants": {"cost": COST, "population": POPULATION, "candidates_per_adaptation": CANDIDATES,
                              "dev_seeds": len(DEV_SEEDS), "confirmation_seeds": len(CONFIRM_SEEDS),
                              "bootstraps": BOOTSTRAPS}, "tests": tests}
    (OUT / "run_log.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    digest = hashlib.sha256((OUT / "seed_metrics.csv").read_bytes()).hexdigest()
    (OUT / "sha256.txt").write_text(digest + "\n", encoding="ascii")
    print(summary.to_string(index=False))
    print(json.dumps(tests, indent=2))
    print(f"seed_metrics_sha256={digest}")


if __name__ == "__main__":
    main()
