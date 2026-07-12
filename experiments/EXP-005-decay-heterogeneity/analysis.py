"""EXP-005: Cross-predictor heterogeneity in post-publication decay.

Registered design: experiments/EXP-005-decay-heterogeneity/design.md
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

# Era bins registered in EXP-003 design (base 1926-1992), reused for R1
ERA_EDGES = [1993, 2001, 2011, 2020]
ERA_NAMES = ["era_1993_2000", "era_2001_2010", "era_2011_2019", "era_2020_2024"]


def load_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Panel as in EXP-001/003, plus SignalDoc characteristics per predictor.

    Returns (panel, excluded_summary): predictors dropped for missing OP
    T-Stat are summarized so the selection is visible (design: Data section).
    """
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    doc = doc[
        (doc["Cat.Signal"] == "Predictor")
        & doc["Predictability in OP"].isin(["1_clear", "2_likely"])
        & doc[["SampleStartYear", "SampleEndYear", "Year"]].notna().all(axis=1)
    ][
        [
            "Acronym", "Predictability in OP", "SampleStartYear", "SampleEndYear",
            "Year", "T-Stat", "GScholarCites202509", "Cat.Data", "Stock Weight",
        ]
    ].rename(columns={"T-Stat": "op_t_raw", "GScholarCites202509": "cites_raw"})

    port = pd.read_parquet(RAW / "PredictorPortsFull.parquet")
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

    counts = df.pivot_table(index="signalname", columns="window", values="ret", aggfunc="count").fillna(0)
    keep = counts.index[
        (counts.get("in_sample", 0) >= MIN_MONTHS) & (counts.get("post_pub", 0) >= MIN_MONTHS)
    ]
    df = df[df["signalname"].isin(keep)].copy()

    # Additional EXP-005 filter: non-missing OP T-Stat; report the excluded.
    has_t = df["op_t_raw"].notna()
    excl = df[~has_t]
    excl_summary = (
        excl.pivot_table(index="signalname", columns="window", values="ret", aggfunc="mean")
        .reindex(columns=["in_sample", "post_sample", "post_pub"])
    )
    df = df[has_t].copy()
    return df, excl_summary


def characteristics(df: pd.DataFrame) -> pd.DataFrame:
    """Per-predictor characteristics, z-scored across the estimation sample."""
    is_ret = df[df["window"] == "in_sample"].groupby("signalname")["ret"]
    ch = pd.DataFrame(
        {
            "op_t_raw": df.groupby("signalname")["op_t_raw"].first(),
            "cites_raw": df.groupby("signalname")["cites_raw"].first(),
            "pub_year": df.groupby("signalname")["Year"].first(),
            "is_mean": is_ret.mean(),
            "is_vol_raw": is_ret.std(),
            "is_n": is_ret.count(),
            "cat_data": df.groupby("signalname")["Cat.Data"].first(),
            "stock_weight": df.groupby("signalname")["Stock Weight"].first(),
        }
    )
    ch["rt_raw"] = ch["is_mean"] / (ch["is_vol_raw"] / np.sqrt(ch["is_n"]))

    def z(s: pd.Series) -> pd.Series:
        return (s - s.mean()) / s.std()

    ch["op_t"] = z(ch["op_t_raw"])
    ch["vol"] = z(np.log(ch["is_vol_raw"]))
    ch["cites"] = z(np.log(ch["cites_raw"]))
    ch["rt"] = z(ch["rt_raw"])
    ch["pubyear_z"] = z(ch["pub_year"])
    return ch


def fe_reg(d: pd.DataFrame, xcols: list[str]) -> pd.DataFrame:
    """Within-FE OLS (demeaned by predictor), month-clustered SEs."""
    dd = d.copy()
    for col in ["ret"] + xcols:
        dd[f"{col}_w"] = dd[col] - dd.groupby("signalname")[col].transform("mean")
    X = dd[[f"{c}_w" for c in xcols]].to_numpy()
    res = sm.OLS(dd["ret_w"].to_numpy(), X).fit(
        cov_type="cluster", cov_kwds={"groups": dd["date"].to_numpy()}
    )
    return pd.DataFrame({"term": xcols, "coef": res.params, "se": res.bse, "t": res.tvalues})


def with_interactions(df: pd.DataFrame, ch: pd.DataFrame, chars: list[str]) -> tuple[pd.DataFrame, list[str]]:
    d = df.merge(ch[chars + ["pubyear_z"]], left_on="signalname", right_index=True)
    d["ps"] = (d["window"] == "post_sample").astype(float)
    d["pp"] = (d["window"] == "post_pub").astype(float)
    xcols = ["ps", "pp"]
    for c in chars:
        d[f"ps_x_{c}"] = d["ps"] * d[c]
        d[f"pp_x_{c}"] = d["pp"] * d[c]
        xcols += [f"ps_x_{c}", f"pp_x_{c}"]
    return d, xcols


def add_eras(d: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    for i, start in enumerate(ERA_EDGES):
        end = ERA_EDGES[i + 1] - 1 if i + 1 < len(ERA_EDGES) else 3000
        d[ERA_NAMES[i]] = ((d["cal_year"] >= start) & (d["cal_year"] <= end)).astype(float)
    return d, ERA_NAMES


def tercile_table(df: pd.DataFrame, ch: pd.DataFrame, char: str) -> pd.DataFrame:
    """E2: window means per tercile of `char`, month-clustered SEs."""
    terc = pd.qcut(ch[char], 3, labels=["T1_low", "T2_mid", "T3_high"])
    d = df.merge(terc.rename("terc"), left_on="signalname", right_index=True)
    rows = []
    for (t, win), g in d.groupby(["terc", "window"], observed=True):
        res = sm.OLS(g["ret"].to_numpy(), np.ones((len(g), 1))).fit(
            cov_type="cluster", cov_kwds={"groups": g["date"].to_numpy()}
        )
        rows.append(
            {"char": char, "tercile": t, "window": win, "mean": res.params[0],
             "se": res.bse[0], "n_predictors": g["signalname"].nunique()}
        )
    tab = pd.DataFrame(rows)
    order = {"in_sample": 0, "post_sample": 1, "post_pub": 2}
    return tab.sort_values(["tercile", "window"], key=lambda s: s.map(order) if s.name == "window" else s)


def main() -> None:
    df, excl = load_panel()
    ch = characteristics(df)
    n_pred = df["signalname"].nunique()
    print(f"estimation sample: {n_pred} predictors, {len(df)} predictor-months")
    print(f"excluded for missing OP T-Stat: {len(excl)} predictors")
    excl.to_csv(OUT / "excluded_missing_op_t.csv")

    print("\ncharacteristic correlations (raw-space pairs z-scored):")
    corr = ch[["op_t", "vol", "cites", "rt", "pubyear_z"]].corr()
    print(corr.round(2).to_string())
    corr.to_csv(OUT / "characteristic_correlations.csv")

    results: dict[str, pd.DataFrame] = {}

    # E1 primary: op_t and vol jointly
    d1, x1 = with_interactions(df, ch, ["op_t", "vol"])
    results["E1_primary_op_t_vol"] = fe_reg(d1, x1)

    # E3 exploratory: + cites
    d3, x3 = with_interactions(df, ch, ["op_t", "vol", "cites"])
    results["E3_plus_cites"] = fe_reg(d3, x3)

    # E4 one-at-a-time
    for c in ["op_t", "vol", "cites"]:
        d4, x4 = with_interactions(df, ch, [c])
        results[f"E4_solo_{c}"] = fe_reg(d4, x4)

    # R1: era controls
    d5, x5 = with_interactions(df, ch, ["op_t", "vol"])
    d5, eras = add_eras(d5)
    results["R1_era_controls"] = fe_reg(d5, x5 + eras)

    # R2: cohort trend control (pp x publication year)
    d6, x6 = with_interactions(df, ch, ["op_t", "vol"])
    d6["pp_x_pubyear"] = d6["pp"] * d6["pubyear_z"]
    results["R2_pubyear_control"] = fe_reg(d6, x6 + ["pp_x_pubyear"])

    # R3: realized in-sample t instead of OP t
    d7, x7 = with_interactions(df, ch, ["rt", "vol"])
    results["R3_realized_t"] = fe_reg(d7, x7)

    # R4: winsorized returns
    d8 = df.copy()
    lo = d8.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.01))
    hi = d8.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.99))
    d8["ret"] = d8["ret"].clip(lo, hi)
    d8, x8 = with_interactions(d8, ch, ["op_t", "vol"])
    results["R4_winsorized"] = fe_reg(d8, x8)

    # R5: 1_clear only
    d9 = df[df["Predictability in OP"] == "1_clear"].copy()
    ch9 = characteristics(d9)  # re-z-scored within subsample
    d9, x9 = with_interactions(d9, ch9, ["op_t", "vol"])
    results["R5_clear_only"] = fe_reg(d9, x9)

    rows = []
    for spec, tab in results.items():
        t = tab.copy()
        t.insert(0, "spec", spec)
        rows.append(t)
    pd.concat(rows, ignore_index=True).to_csv(OUT / "regressions.csv", index=False)
    for spec, tab in results.items():
        print(f"\n== {spec} ==")
        print(tab.round(3).to_string(index=False))

    # E2 tercile sorts
    tercs = pd.concat([tercile_table(df, ch, c) for c in ["op_t", "vol", "cites"]])
    tercs.to_csv(OUT / "terciles.csv", index=False)
    print("\n== terciles ==")
    print(tercs.round(3).to_string(index=False))

    # Per-predictor characteristics + window means (for the scatter / write-up)
    wm = df.pivot_table(index="signalname", columns="window", values="ret", aggfunc="mean")
    out = ch.join(wm.reindex(columns=["in_sample", "post_sample", "post_pub"]))
    out["decline_pp"] = out["in_sample"] - out["post_pub"]
    out.to_csv(OUT / "characteristics.csv")

    # Descriptive check registered in HYP-005: EW vs VW decay (not a spec)
    ew_vw = out.groupby("stock_weight")[["in_sample", "post_pub", "decline_pp"]].mean()
    print("\n== EW vs VW (descriptive only) ==")
    print(ew_vw.round(3).to_string())


if __name__ == "__main__":
    main()
