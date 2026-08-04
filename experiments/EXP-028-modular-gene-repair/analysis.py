"""EXP-028 walk-forward modular repair experiment."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "datasets" / "raw" / "french_5_industry"
OUT = Path(__file__).resolve().parent / "outputs"
N_CANDIDATES = 64
BASE_SEED = 28032026
COST = 0.001
RISK_AVERSION = 1.5
METHODS = ("localized", "all_gene", "random", "min_variance", "equal_weight")


def load_french_zip(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != 1:
            raise ValueError(f"Expected one CSV in {path}, found {names}")
        text = archive.read(names[0]).decode("utf-8", errors="replace")
    lines = text.splitlines()
    expected = ["", "Cnsmr", "Manuf", "HiTec", "Hlth", "Other"]
    header_idx = next(i for i, line in enumerate(lines)
                      if [part.strip() for part in line.split(",")] == expected)
    rows = [lines[header_idx].lstrip()]
    for line in lines[header_idx + 1:]:
        first = line.split(",", 1)[0].strip()
        if len(first) != 8 or not first.isdigit():
            break
        rows.append(line)
    frame = pd.read_csv(io.StringIO("\n".join(rows)), index_col=0)
    frame.columns = frame.columns.str.strip()
    frame.index = pd.to_datetime(frame.index.astype(str), format="%Y%m%d")
    frame = frame.apply(pd.to_numeric, errors="raise") / 100.0
    if frame.isna().any().any() or (frame <= -0.999).any().any():
        raise ValueError("Missing or sentinel return in value-weighted daily block")
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError("Dates must be unique and increasing")
    return frame


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def fitness(weights: np.ndarray, train: np.ndarray, incumbent: np.ndarray) -> np.ndarray:
    portfolio = train @ weights.T
    ce = 252.0 * portfolio.mean(axis=0) - RISK_AVERSION * 252.0 * portfolio.var(axis=0, ddof=1)
    turnover = 0.5 * np.abs(weights - incumbent).sum(axis=1)
    return ce - COST * turnover


def damage_scores(train: np.ndarray) -> np.ndarray:
    old, recent = train[-252:-63], train[-63:]
    pooled_se = np.sqrt(old.var(axis=0, ddof=1) / len(old) + recent.var(axis=0, ddof=1) / len(recent))
    mean_shift = np.abs(recent.mean(axis=0) - old.mean(axis=0)) / np.maximum(pooled_se, 1e-12)
    vol_shift = np.abs(np.log(np.maximum(recent.std(axis=0, ddof=1), 1e-12) /
                              np.maximum(old.std(axis=0, ddof=1), 1e-12)))
    return mean_shift + vol_shift


def stochastic_weights(method: str, train: np.ndarray, incumbent: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = np.log(np.maximum(incumbent, 1e-10))
    if method == "random":
        candidates = rng.dirichlet(np.ones(5), N_CANDIDATES - 1)
    elif method == "localized":
        allowed = np.argsort(damage_scores(train))[-2:]
        first, second = int(allowed[0]), int(allowed[1])
        delta = rng.uniform(-incumbent[first], incumbent[second], size=N_CANDIDATES - 1)
        candidates = np.repeat(incumbent[None, :], N_CANDIDATES - 1, axis=0)
        candidates[:, first] += delta
        candidates[:, second] -= delta
    else:
        noise = rng.normal(0.0, 0.35, size=(N_CANDIDATES - 1, 5))
        if method != "all_gene":
            raise ValueError(method)
        candidates = softmax(base + noise)
    return np.vstack([incumbent, candidates])


def min_variance_weights(train: np.ndarray) -> np.ndarray:
    covariance = np.cov(train, rowvar=False)
    objective = lambda w: float(w @ covariance @ w)
    result = minimize(objective, np.full(5, 0.2), method="SLSQP",
                      bounds=[(0.0, 1.0)] * 5,
                      constraints={"type": "eq", "fun": lambda w: w.sum() - 1.0},
                      options={"ftol": 1e-12, "maxiter": 500})
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def month_starts(index: pd.DatetimeIndex, start: str, end: str) -> list[pd.Timestamp]:
    eligible = index[(index >= start) & (index <= end)]
    return list(pd.Series(eligible, index=eligible).groupby(eligible.to_period("M")).first())


def run_period(data: pd.DataFrame, start: str, end: str, label: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    incumbents = {method: np.full(5, 0.2) for method in METHODS}
    daily_rows, rebalance_rows = [], []
    starts = month_starts(data.index, start, end)
    for rebalance_no, date in enumerate(starts):
        position = data.index.get_loc(date)
        if position < 252:
            raise ValueError("Insufficient training history")
        train = data.iloc[position - 252:position].to_numpy()
        month = data.loc[(data.index >= date) & (data.index.to_period("M") == date.to_period("M"))]
        for method_no, method in enumerate(METHODS):
            old = incumbents[method]
            if method in ("localized", "all_gene", "random"):
                seed = BASE_SEED + 100_000 * method_no + rebalance_no
                candidates = stochastic_weights(method, train, old, seed)
                new = candidates[np.argmax(fitness(candidates, train, old))]
                count = len(candidates)
            elif method == "min_variance":
                new, count = min_variance_weights(train), 1
            else:
                new, count = np.full(5, 0.2), 1
            turnover = 0.5 * np.abs(new - old).sum()
            realized = month.to_numpy() @ new
            realized[0] -= COST * turnover
            for day, value in zip(month.index, realized):
                daily_rows.append({"period": label, "date": day, "method": method, "net_return": value})
            rebalance_rows.append({"period": label, "date": date, "method": method,
                                   "turnover": turnover, "candidate_count": count,
                                   **{f"w_{c}": v for c, v in zip(data.columns, new)}})
            incumbents[method] = new
    return pd.DataFrame(daily_rows), pd.DataFrame(rebalance_rows)


def monthly_metrics(daily: pd.DataFrame) -> pd.DataFrame:
    work = daily.copy()
    work["month"] = pd.to_datetime(work["date"]).dt.to_period("M").astype(str)
    grouped = work.groupby(["period", "method", "month"])["net_return"]
    result = grouped.agg(month_return=lambda x: np.prod(1.0 + x) - 1.0,
                         month_variance=lambda x: x.var(ddof=1)).reset_index()
    result["certainty_equivalent"] = result["month_return"] - RISK_AVERSION * result["month_variance"]
    return result


def circular_block_interval(values: np.ndarray, seed: int, reps: int = 10_000, block: int = 12) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = len(values)
    samples = np.empty(reps)
    blocks_needed = int(np.ceil(n / block))
    offsets = np.arange(block)
    for i in range(reps):
        starts = rng.integers(0, n, size=blocks_needed)
        indexes = ((starts[:, None] + offsets) % n).ravel()[:n]
        samples[i] = values[indexes].mean()
    return tuple(np.quantile(samples, [0.025, 0.975]))


def summarize(daily: pd.DataFrame, rebalances: pd.DataFrame, monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for (period, method), group in daily.groupby(["period", "method"]):
        values = group["net_return"].to_numpy()
        wealth = np.cumprod(1.0 + values)
        drawdown = wealth / np.maximum.accumulate(wealth) - 1.0
        tail = values[values <= np.quantile(values, 0.05)]
        turnover = rebalances.query("period == @period and method == @method")["turnover"].sum()
        rows.append({"period": period, "method": method,
                     "cumulative_net_log_return": np.log1p(values).sum(),
                     "annualized_volatility": values.std(ddof=1) * np.sqrt(252),
                     "annualized_expected_shortfall_5pct": -tail.mean() * np.sqrt(252),
                     "maximum_drawdown": drawdown.min(), "turnover": turnover,
                     "months": monthly.query("period == @period and method == @method").shape[0]})
    comparisons = []
    primary = monthly.query("period == 'confirmation'").pivot(index="month", columns="method", values="certainty_equivalent")
    for number, comparator in enumerate(("all_gene", "random", "min_variance", "equal_weight")):
        diff = (primary["localized"] - primary[comparator]).to_numpy()
        low, high = circular_block_interval(diff, BASE_SEED + 9000 + number)
        comparisons.append({"comparator": comparator, "mean_monthly_ce_difference": diff.mean(),
                            "ci_low": low, "ci_high": high,
                            "localized_win_fraction": float((diff > 0).mean())})
    return pd.DataFrame(rows), pd.DataFrame(comparisons)


def main() -> None:
    archive = load_french_zip(RAW / "archive_202412.zip")
    current = load_french_zip(RAW / "current.zip")
    confirmation_daily, confirmation_rebalances = run_period(archive, "2015-01-01", "2024-12-31", "confirmation")
    later_daily, later_rebalances = run_period(current, "2025-01-01", str(current.index.max().date()), "later_vintage")
    daily = pd.concat([confirmation_daily, later_daily], ignore_index=True)
    rebalances = pd.concat([confirmation_rebalances, later_rebalances], ignore_index=True)
    monthly = monthly_metrics(daily)
    summary, comparisons = summarize(daily, rebalances, monthly)
    OUT.mkdir(exist_ok=True)
    daily.to_csv(OUT / "daily_returns.csv", index=False)
    rebalances.to_csv(OUT / "rebalances.csv", index=False)
    monthly.to_csv(OUT / "monthly_metrics.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    comparisons.to_csv(OUT / "comparisons.csv", index=False)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (RAW / "archive_202412.zip", RAW / "current.zip")}
    (OUT / "run_metadata.json").write_text(json.dumps({"input_sha256": hashes,
        "base_seed": BASE_SEED, "candidate_count": N_CANDIDATES, "cost": COST,
        "risk_aversion": RISK_AVERSION}, indent=2) + "\n", encoding="utf-8")
    print(summary.to_string(index=False))
    print(comparisons.to_string(index=False))


if __name__ == "__main__":
    main()
