"""EXP-003: Calendar-time vs event-time decomposition of predictor decay.

Registered design: experiments/EXP-003-calendar-vs-event-time/design.md
(written before this file). Data: Chen & Zimmermann Oct 2025 release.

Deterministic; no resampling. Outputs to results/ as CSV.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "datasets" / "raw"
OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)

PANEL_END = pd.Timestamp("2024-12-31")
MIN_MONTHS = 12

# Era bins fixed in design.md: base 1926-1992
ERA_EDGES = [1993, 2001, 2011, 2020]
ERA_NAMES = ["era_1993_2000", "era_2001_2010", "era_2011_2019", "era_2020_2024"]
# R1 alternative: 5-year bins from 1990, base 1926-1989
ALT_EDGES = list(range(1990, 2025, 5))
ALT_NAMES = [f"era_{y}_{min(y + 4, 2024)}" for y in ALT_EDGES]


def load_panel(kind: str) -> pd.DataFrame:
    """Same construction as EXP-002 analysis.py, plus publication year kept."""
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    doc = doc[
        (doc["Cat.Signal"] == kind)
        & doc[["SampleStartYear", "SampleEndYear", "Year"]].notna().all(axis=1)
    ]
    if kind == "Predictor":
        doc = doc[doc["Predictability in OP"].isin(["1_clear", "2_likely"])]
    doc = doc[["Acronym", "Predictability in OP", "SampleStartYear", "SampleEndYear", "Year"]]

    fname = "PlaceboPortsFull.parquet" if kind == "Placebo" else "PredictorPortsFull.parquet"
    port = pd.read_parquet(RAW / fname)
    ls = port[port["port"] == "LS"].copy()
    ls["date"] = pd.to_datetime(ls["date"])
    ls = ls[ls["date"] <= PANEL_END]

    df = ls.merge(doc, left_on="signalname", right_on="Acronym", how="inner")
    y = df["date"].dt.year
    df["window"] = np.select(
        [y < df["SampleStartYear"], y <= df["SampleEndYear"], y <= df["Year"]],
        ["pre_sample", "in_sample", "post_sample"],
        default="post_pub",
    )
    df = df[df["window"] != "pre_sample"].copy()
    df["cal_year"] = df["date"].dt.year
    df["event_years"] = df["cal_year"] - df["Year"]  # years since publication year
    counts = df.pivot_table(index="signalname", columns="window", values="ret", aggfunc="count").fillna(0)
    keep = counts.index[
        (counts.get("in_sample", 0) >= MIN_MONTHS) & (counts.get("post_pub", 0) >= MIN_MONTHS)
    ]
    return df[df["signalname"].isin(keep)][
        ["signalname", "date", "ret", "window", "cal_year", "event_years", "Predictability in OP"]
    ].copy()


def add_eras(d: pd.DataFrame, edges: list[int], names: list[str]) -> tuple[pd.DataFrame, list[str]]:
    for i, start in enumerate(edges):
        end = edges[i + 1] - 1 if i + 1 < len(edges) else 3000
        d[names[i]] = ((d["cal_year"] >= start) & (d["cal_year"] <= end)).astype(float)
    return d, names


def fe_reg(d: pd.DataFrame, xcols: list[str], contrast: tuple[str, str] | None = None):
    """Within-FE OLS, month-clustered. Optional contrast returns (diff, se, t)
    for coef[a] - coef[b] via the cluster-robust covariance."""
    dd = d.copy()
    for col in ["ret"] + xcols:
        dd[f"{col}_w"] = dd[col] - dd.groupby("signalname")[col].transform("mean")
    X = dd[[f"{c}_w" for c in xcols]].to_numpy()
    res = sm.OLS(dd["ret_w"].to_numpy(), X).fit(
        cov_type="cluster", cov_kwds={"groups": dd["date"].to_numpy()}
    )
    tab = pd.DataFrame({"term": xcols, "coef": res.params, "se": res.bse, "t": res.tvalues})
    if contrast is None:
        return tab
    ia, ib = xcols.index(contrast[0]), xcols.index(contrast[1])
    diff = res.params[ia] - res.params[ib]
    var = res.cov_params()[ia, ia] + res.cov_params()[ib, ib] - 2 * res.cov_params()[ia, ib]
    return tab, (diff, np.sqrt(var), diff / np.sqrt(var))


def window_dummies(d: pd.DataFrame) -> pd.DataFrame:
    d["ps"] = (d["window"] == "post_sample").astype(float)
    d["pp"] = (d["window"] == "post_pub").astype(float)
    return d


def event_bins(d: pd.DataFrame) -> pd.DataFrame:
    pp = d["window"] == "post_pub"
    d["pp1"] = (pp & (d["event_years"] <= 5)).astype(float)
    d["pp2"] = (pp & (d["event_years"] > 5) & (d["event_years"] <= 10)).astype(float)
    d["pp3"] = (pp & (d["event_years"] > 10)).astype(float)
    return d


def run_all(pred: pd.DataFrame, plc: pd.DataFrame) -> None:
    results = {}

    # E1 primary: windows + registered eras, predictors.
    # P3's registered comparison (era_2020_2024 vs era_2011_2019) reported as a
    # cluster-robust linear-combination test.
    d, eras = add_eras(window_dummies(pred.copy()), ERA_EDGES, ERA_NAMES)
    results["E1_pred_eras"], p3 = fe_reg(
        d, ["ps", "pp"] + eras, contrast=("era_2020_2024", "era_2011_2019")
    )
    pd.DataFrame([{"contrast": "era_2020_2024 - era_2011_2019",
                   "diff": p3[0], "se": p3[1], "t": p3[2]}]).to_csv(
        OUT / "p3_contrast.csv", index=False)
    print(f"P3 contrast era_2020_2024 - era_2011_2019: "
          f"{p3[0]:.3f} (se {p3[1]:.3f}, t {p3[2]:.2f})")

    # Benchmark without eras (ties back to EXP-002 benchmark run)
    results["E0_pred_no_eras"] = fe_reg(window_dummies(pred.copy()), ["ps", "pp"])

    # E2 event-time profile with eras
    d2, _ = add_eras(event_bins(window_dummies(pred.copy())), ERA_EDGES, ERA_NAMES)
    results["E2_pred_eventtime"] = fe_reg(d2, ["ps", "pp1", "pp2", "pp3"] + eras)

    # E3 placebo cross-check
    d3, _ = add_eras(window_dummies(plc.copy()), ERA_EDGES, ERA_NAMES)
    results["E3_placebo_eras"] = fe_reg(d3, ["ps", "pp"] + eras)
    results["E3b_placebo_no_eras"] = fe_reg(window_dummies(plc.copy()), ["ps", "pp"])

    # R1 alternative binning
    d4, alt = add_eras(window_dummies(pred.copy()), ALT_EDGES, ALT_NAMES)
    results["R1_pred_5y_bins"] = fe_reg(d4, ["ps", "pp"] + alt)

    # R2 linear trend
    d5 = window_dummies(pred.copy())
    d5["trend"] = (d5["cal_year"] - 1990) / 10.0
    results["R2_pred_linear_trend"] = fe_reg(d5, ["ps", "pp", "trend"])

    # R3 winsorized
    d6 = pred.copy()
    lo = d6.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.01))
    hi = d6.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.99))
    d6["ret"] = d6["ret"].clip(lo, hi)
    d6, _ = add_eras(window_dummies(d6), ERA_EDGES, ERA_NAMES)
    results["R3_pred_winsorized"] = fe_reg(d6, ["ps", "pp"] + eras)

    # R4 clear-reproduction only
    d7 = pred[pred["Predictability in OP"] == "1_clear"].copy()
    d7, _ = add_eras(window_dummies(d7), ERA_EDGES, ERA_NAMES)
    results["R4_pred_clear_only"] = fe_reg(d7, ["ps", "pp"] + eras)

    rows = []
    for spec, tab in results.items():
        t = tab.copy()
        t.insert(0, "spec", spec)
        rows.append(t)
    all_res = pd.concat(rows, ignore_index=True)
    all_res.to_csv(OUT / "regressions.csv", index=False)
    with pd.option_context("display.width", 160):
        for spec, tab in results.items():
            print(f"\n== {spec} ==")
            print(tab.round(3).to_string(index=False))

    # Composition table: predictor-months per era x window
    d, _ = add_eras(pred.copy(), ERA_EDGES, ERA_NAMES)
    d["era"] = "era_1926_1992"
    for nm in ERA_NAMES:
        d.loc[d[nm] == 1, "era"] = nm
    comp = d.pivot_table(index="era", columns="window", values="ret", aggfunc="count").fillna(0).astype(int)
    comp.to_csv(OUT / "composition_era_window.csv")
    print("\n== composition (predictor-months) ==")
    print(comp.to_string())


if __name__ == "__main__":
    predictors = load_panel("Predictor")
    placebos = load_panel("Placebo")
    print(f"predictors: {predictors['signalname'].nunique()} signals, {len(predictors)} rows")
    print(f"placebos:   {placebos['signalname'].nunique()} signals, {len(placebos)} rows")
    run_all(predictors, placebos)
