"""EXP-002: Placebo test of publication-timed decay.

Registered design: experiments/EXP-002-placebo-decay/design.md (written before this file).
Data: Chen & Zimmermann Oct 2025 release (datasets/chen_zimmermann_oct2025.md).

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
MIN_MONTHS = 12  # design step 3


def load_panel(kind: str) -> pd.DataFrame:
    """kind: 'Placebo' or 'Predictor'. Window logic identical to EXP-001."""
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    doc = doc[
        (doc["Cat.Signal"] == kind)
        & doc[["SampleStartYear", "SampleEndYear", "Year"]].notna().all(axis=1)
    ]
    if kind == "Predictor":  # EXP-001 primary sample filter
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
    df = df[df["window"] != "pre_sample"]
    df["group"] = kind
    return df[["signalname", "date", "ret", "window", "group", "Predictability in OP"]]


def apply_min_months(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.pivot_table(
        index="signalname", columns="window", values="ret", aggfunc="count"
    ).fillna(0)
    keep = counts.index[
        (counts.get("in_sample", 0) >= MIN_MONTHS)
        & (counts.get("post_pub", 0) >= MIN_MONTHS)
    ]
    return df[df["signalname"].isin(keep)].copy()


def within_demean(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        d[f"{col}_w"] = d[col] - d.groupby("signalname")[col].transform("mean")
    return d


def fe_panel(df: pd.DataFrame) -> dict:
    """E1: signal FE via within-transformation, month-clustered SEs."""
    d = df.copy()
    d["ps"] = (d["window"] == "post_sample").astype(float)
    d["pp"] = (d["window"] == "post_pub").astype(float)
    d = within_demean(d, ["ret", "ps", "pp"])
    res = sm.OLS(d["ret_w"].to_numpy(), d[["ps_w", "pp_w"]].to_numpy()).fit(
        cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
    )
    mean_is = df.loc[df["window"] == "in_sample", "ret"].mean()
    return {
        "n_signals": df["signalname"].nunique(),
        "n_rows": len(df),
        "mean_in_sample": mean_is,
        "beta_post_sample": res.params[0],
        "t_post_sample": res.tvalues[0],
        "beta_post_pub": res.params[1],
        "t_post_pub": res.tvalues[1],
    }


def pooled_did(placebo: pd.DataFrame, predictor: pd.DataFrame) -> dict:
    """E2: pooled DiD. Signal FE absorb the group main effect."""
    d = pd.concat([placebo, predictor], ignore_index=True)
    d["pred"] = (d["group"] == "Predictor").astype(float)
    d["ps"] = (d["window"] == "post_sample").astype(float)
    d["pp"] = (d["window"] == "post_pub").astype(float)
    d["ps_x"] = d["ps"] * d["pred"]
    d["pp_x"] = d["pp"] * d["pred"]
    d = within_demean(d, ["ret", "ps", "pp", "ps_x", "pp_x"])
    X = d[["ps_w", "pp_w", "ps_x_w", "pp_x_w"]].to_numpy()
    res = sm.OLS(d["ret_w"].to_numpy(), X).fit(
        cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
    )
    names = ["beta_ps_placebo", "beta_pp_placebo", "gamma_ps_extra_pred", "gamma_pp_extra_pred"]
    out = {"n_signals": d["signalname"].nunique(), "n_rows": len(d)}
    for i, nm in enumerate(names):
        out[nm] = res.params[i]
        out[f"t_{nm}"] = res.tvalues[i]
    return out


def per_signal_means(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(
        index="signalname", columns="window", values="ret", aggfunc="mean"
    ).reindex(columns=["in_sample", "post_sample", "post_pub"])


def run_spec(df: pd.DataFrame, label: str) -> dict:
    out = {"spec": label}
    out.update(fe_panel(df))
    return out


def main() -> None:
    placebo = apply_min_months(load_panel("Placebo"))
    predictor = apply_min_months(load_panel("Predictor"))

    per_sig = per_signal_means(placebo)
    per_sig.to_csv(OUT / "window_means_by_placebo.csv")

    # E1 primary + robustness (placebo-only panel)
    specs = [run_spec(placebo, "primary_placebo")]
    specs.append(run_spec(placebo[placebo["Predictability in OP"] == "indirect"], "R1a_indirect"))
    specs.append(run_spec(placebo[placebo["Predictability in OP"] == "4_not"], "R1b_4not_descriptive"))

    w = placebo.copy()
    lo = w.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.01))
    hi = w.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.99))
    w["ret"] = w["ret"].clip(lo, hi)
    specs.append(run_spec(w, "R2_winsorized_1_99"))

    specs.append(run_spec(placebo[placebo["date"] <= "2019-12-31"], "R3_end_2019"))

    # R4: selection-bias demonstration — condition on positive in-sample mean
    pos = per_sig.index[per_sig["in_sample"] > 0]
    specs.append(run_spec(placebo[placebo["signalname"].isin(pos)], "R4_selected_positive_IS"))

    counts = placebo.pivot_table(
        index="signalname", columns="window", values="ret", aggfunc="count"
    ).fillna(0)
    bal = counts.index[(counts >= 36).all(axis=1)]
    specs.append(run_spec(placebo[placebo["signalname"].isin(bal)], "R5_balanced_36m"))

    # Predictor benchmark on the identical pipeline (sanity tie-back to EXP-001)
    specs.append(run_spec(predictor, "benchmark_predictors"))

    summary = pd.DataFrame(specs)
    summary.to_csv(OUT / "summary_placebo_panel.csv", index=False)
    with pd.option_context("display.width", 220, "display.max_columns", 30):
        print(summary.round(3).to_string(index=False))

    # E2 pooled DiD (primary test for P2), plus winsorized variant
    did = {"spec": "did_primary"}
    did.update(pooled_did(placebo, predictor))
    wp = predictor.copy()
    lo = wp.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.01))
    hi = wp.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.99))
    wp["ret"] = wp["ret"].clip(lo, hi)
    did_w = {"spec": "did_winsorized"}
    did_w.update(pooled_did(w, wp))
    did_df = pd.DataFrame([did, did_w])
    did_df.to_csv(OUT / "summary_did.csv", index=False)
    print()
    with pd.option_context("display.width", 220, "display.max_columns", 30):
        print(did_df.round(3).to_string(index=False))

    # E3: window-level pooled means with month-clustered CIs, by group & placebo subtype
    rows = []
    frames = {
        "placebo_all": placebo,
        "placebo_indirect": placebo[placebo["Predictability in OP"] == "indirect"],
        "placebo_4not": placebo[placebo["Predictability in OP"] == "4_not"],
        "predictor": predictor,
    }
    for gname, g in frames.items():
        for win in ["in_sample", "post_sample", "post_pub"]:
            d = g[g["window"] == win]
            res = sm.OLS(d["ret"].to_numpy(), np.ones((len(d), 1))).fit(
                cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
            )
            rows.append({"group": gname, "window": win, "mean": res.params[0],
                         "se": res.bse[0], "n_rows": len(d)})
    pd.DataFrame(rows).to_csv(OUT / "window_level_by_group.csv", index=False)

    desc = per_sig.describe().T[["count", "mean", "50%", "25%", "75%"]]
    desc.to_csv(OUT / "cross_placebo_descriptives.csv")
    print()
    print(desc.round(3).to_string())


if __name__ == "__main__":
    main()
