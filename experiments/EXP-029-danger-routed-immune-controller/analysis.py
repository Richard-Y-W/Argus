"""EXP-029 danger-routed portfolio controller."""

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
RAW = ROOT / "datasets" / "raw" / "french_10_industry"
OUT = Path(__file__).resolve().parent / "outputs"
METHODS = ("controller", "localized", "all_gene", "random", "min_variance", "equal_weight")
N_CANDIDATES, BASE_SEED, COST, RISK_AVERSION = 64, 29042026, 0.001, 1.5


def load_french_zip(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != 1:
            raise ValueError(f"Expected one CSV, found {names}")
        lines = archive.read(names[0]).decode("utf-8", errors="replace").splitlines()
    header_idx = next(i for i, line in enumerate(lines[:-1])
                      if len(line.split(",")) == 11
                      and line.split(",")[0].strip() == ""
                      and len(lines[i + 1].split(",", 1)[0].strip()) == 8
                      and lines[i + 1].split(",", 1)[0].strip().isdigit())
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
    if frame.shape[1] != 10 or frame.isna().any().any() or (frame <= -0.999).any().any():
        raise ValueError("Invalid value-weighted daily block")
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError("Invalid dates")
    return frame


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def damage_scores(train: np.ndarray) -> np.ndarray:
    old, recent = train[-252:-63], train[-63:]
    se = np.sqrt(old.var(0, ddof=1) / len(old) + recent.var(0, ddof=1) / len(recent))
    mean = np.abs(recent.mean(0) - old.mean(0)) / np.maximum(se, 1e-12)
    vol = np.abs(np.log(np.maximum(recent.std(0, ddof=1), 1e-12) /
                        np.maximum(old.std(0, ddof=1), 1e-12)))
    return mean + vol


def signals(train: np.ndarray) -> tuple[float, float]:
    damage = damage_scores(train)
    danger = float(np.sqrt(np.mean(damage ** 2)))
    localization = float(np.sort(damage)[-2:].sum() / max(damage.sum(), 1e-12))
    return danger, localization


def candidates(response: str, train: np.ndarray, incumbent: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(incumbent)
    if response == "random":
        new = rng.dirichlet(np.ones(n), N_CANDIDATES - 1)
    elif response == "localized":
        first, second = map(int, np.argsort(damage_scores(train))[-2:])
        delta = rng.uniform(-incumbent[first], incumbent[second], N_CANDIDATES - 1)
        new = np.repeat(incumbent[None, :], N_CANDIDATES - 1, axis=0)
        new[:, first] += delta
        new[:, second] -= delta
    elif response == "all_gene":
        noise = rng.normal(0.0, 0.35, size=(N_CANDIDATES - 1, n))
        new = softmax(np.log(np.maximum(incumbent, 1e-10)) + noise)
    else:
        raise ValueError(response)
    return np.vstack([incumbent, new])


def candidate_fitness(weights: np.ndarray, train: np.ndarray, incumbent: np.ndarray) -> np.ndarray:
    returns = train @ weights.T
    ce = 252 * returns.mean(0) - RISK_AVERSION * 252 * returns.var(0, ddof=1)
    turnover = 0.5 * np.abs(weights - incumbent).sum(1)
    return ce - COST * turnover


def min_variance(train: np.ndarray) -> np.ndarray:
    covariance, n = np.cov(train, rowvar=False), train.shape[1]
    result = minimize(lambda w: float(w @ covariance @ w), np.full(n, 1 / n),
                      method="SLSQP", bounds=[(0, 1)] * n,
                      constraints={"type": "eq", "fun": lambda w: w.sum() - 1},
                      options={"ftol": 1e-12, "maxiter": 500})
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def starts(index: pd.DatetimeIndex, start: str, end: str) -> list[pd.Timestamp]:
    eligible = index[(index >= start) & (index <= end)]
    return list(pd.Series(eligible, index=eligible).groupby(eligible.to_period("M")).first())


def calibrate(data: pd.DataFrame) -> dict[str, float]:
    values = []
    for date in starts(data.index, "1995-01-01", "2004-12-31"):
        position = data.index.get_loc(date)
        values.append(signals(data.iloc[position - 252:position].to_numpy()))
    array = np.asarray(values)
    return {"danger_q75": float(np.quantile(array[:, 0], 0.75)),
            "localization_q70": float(np.quantile(array[:, 1], 0.70)),
            "calibration_months": len(array)}


def controller_route(danger: float, localization: float, thresholds: dict[str, float]) -> str:
    if danger < thresholds["danger_q75"]:
        return "tolerate"
    if localization >= thresholds["localization_q70"]:
        return "localized"
    return "systemic"


def run_period(data: pd.DataFrame, start: str, end: str, label: str,
               thresholds: dict[str, float]) -> tuple[pd.DataFrame, pd.DataFrame]:
    n = data.shape[1]
    memory = {method: np.full(n, 1 / n) for method in METHODS}
    daily_rows, decision_rows = [], []
    for rebalance_no, date in enumerate(starts(data.index, start, end)):
        position = data.index.get_loc(date)
        train = data.iloc[position - 252:position].to_numpy()
        danger, localization = signals(train)
        month = data.loc[(data.index >= date) & (data.index.to_period("M") == date.to_period("M"))]
        for method_no, method in enumerate(METHODS):
            old, route, count = memory[method], method, 1
            if method == "controller":
                route = controller_route(danger, localization, thresholds)
                response = "random" if route == "systemic" else route
                if route == "tolerate":
                    new, count = old.copy(), 0
                else:
                    pool = candidates(response, train, old, BASE_SEED + method_no * 1_000_000 + rebalance_no)
                    new, count = pool[np.argmax(candidate_fitness(pool, train, old))], len(pool)
            elif method in ("localized", "all_gene", "random"):
                pool = candidates(method, train, old, BASE_SEED + method_no * 1_000_000 + rebalance_no)
                new, count = pool[np.argmax(candidate_fitness(pool, train, old))], len(pool)
            elif method == "min_variance":
                new = min_variance(train)
            else:
                new = np.full(n, 1 / n)
            turnover = 0.5 * np.abs(new - old).sum()
            realized = month.to_numpy() @ new
            realized[0] -= COST * turnover
            for day, value in zip(month.index, realized):
                daily_rows.append({"period": label, "date": day, "method": method, "net_return": value})
            decision_rows.append({"period": label, "date": date, "method": method, "route": route,
                                  "danger": danger, "localization": localization,
                                  "turnover": turnover, "candidate_count": count})
            memory[method] = new
    return pd.DataFrame(daily_rows), pd.DataFrame(decision_rows)


def monthly_metrics(daily: pd.DataFrame) -> pd.DataFrame:
    work = daily.copy()
    work["month"] = pd.to_datetime(work.date).dt.to_period("M").astype(str)
    result = work.groupby(["period", "method", "month"]).net_return.agg(
        month_return=lambda x: np.prod(1 + x) - 1,
        month_variance=lambda x: x.var(ddof=1)).reset_index()
    result["certainty_equivalent"] = result.month_return - RISK_AVERSION * result.month_variance
    return result


def block_interval(values: np.ndarray, seed: int, reps: int = 10_000, block: int = 12) -> tuple[float, float]:
    rng, n = np.random.default_rng(seed), len(values)
    result = np.empty(reps)
    width = int(np.ceil(n / block))
    offsets = np.arange(block)
    for i in range(reps):
        first = rng.integers(0, n, width)
        indexes = ((first[:, None] + offsets) % n).ravel()[:n]
        result[i] = values[indexes].mean()
    return tuple(np.quantile(result, [0.025, 0.975]))


def summarize(daily: pd.DataFrame, decisions: pd.DataFrame, monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for (period, method), group in daily.groupby(["period", "method"]):
        values = group.net_return.to_numpy()
        wealth = np.cumprod(1 + values)
        tail = values[values <= np.quantile(values, 0.05)]
        d = decisions.query("period == @period and method == @method")
        rows.append({"period": period, "method": method,
                     "cumulative_net_log_return": np.log1p(values).sum(),
                     "annualized_volatility": values.std(ddof=1) * np.sqrt(252),
                     "annualized_expected_shortfall_5pct": -tail.mean() * np.sqrt(252),
                     "maximum_drawdown": (wealth / np.maximum.accumulate(wealth) - 1).min(),
                     "turnover": d.turnover.sum(), "candidate_count": int(d.candidate_count.sum())})
    pivot = monthly.query("period == 'confirmation'").pivot(index="month", columns="method", values="certainty_equivalent")
    comparisons = []
    for number, comparator in enumerate(("localized", "random", "all_gene", "min_variance", "equal_weight")):
        diff = (pivot.controller - pivot[comparator]).to_numpy()
        low, high = block_interval(diff, BASE_SEED + 9000 + number)
        comparisons.append({"comparator": comparator, "mean_monthly_ce_difference": diff.mean(),
                            "ci_low": low, "ci_high": high, "controller_win_fraction": (diff > 0).mean()})
    return pd.DataFrame(rows), pd.DataFrame(comparisons)


def main() -> None:
    archive = load_french_zip(RAW / "archive_202412.zip")
    current = load_french_zip(RAW / "current.zip")
    thresholds = calibrate(archive)
    first = run_period(archive, "2005-01-01", "2024-12-31", "confirmation", thresholds)
    second = run_period(current, "2025-01-01", str(current.index.max().date()), "later_vintage", thresholds)
    daily = pd.concat([first[0], second[0]], ignore_index=True)
    decisions = pd.concat([first[1], second[1]], ignore_index=True)
    monthly = monthly_metrics(daily)
    summary, comparisons = summarize(daily, decisions, monthly)
    OUT.mkdir(exist_ok=True)
    for name, frame in (("daily_returns", daily), ("decisions", decisions),
                        ("monthly_metrics", monthly), ("summary", summary), ("comparisons", comparisons)):
        frame.to_csv(OUT / f"{name}.csv", index=False)
    routes = decisions.query("period == 'confirmation' and method == 'controller'").route.value_counts(normalize=True)
    metadata = {"thresholds": thresholds, "route_shares": routes.to_dict(), "base_seed": BASE_SEED,
                "candidate_count": N_CANDIDATES, "cost": COST, "risk_aversion": RISK_AVERSION,
                "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (RAW / "archive_202412.zip", RAW / "current.zip")}}
    (OUT / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    print(summary.to_string(index=False))
    print(comparisons.to_string(index=False))


if __name__ == "__main__":
    main()

