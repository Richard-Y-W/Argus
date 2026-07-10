"""EXP-001: Three-window replication of McLean & Pontiff (2016).

Registered design: experiments/EXP-001-anomaly-decay/design.md (written before this file).
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
MIN_MONTHS = 12  # per design step 5


def load_panel() -> pd.DataFrame:
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    doc = doc[
        (doc["Cat.Signal"] == "Predictor")
        & doc["Predictability in OP"].isin(["1_clear", "2_likely"])
        & doc[["SampleStartYear", "SampleEndYear", "Year"]].notna().all(axis=1)
    ][["Acronym", "Predictability in OP", "SampleStartYear", "SampleEndYear", "Year"]]

    port = pd.read_parquet(RAW / "PredictorPortsFull.parquet")
    ls = port[port["port"] == "LS"].copy()
    ls["date"] = pd.to_datetime(ls["date"])
    ls = ls[ls["date"] <= PANEL_END]

    df = ls.merge(doc, left_on="signalname", right_on="Acronym", how="inner")
    y = df["date"].dt.year
    df["window"] = np.select(
        [
            y < df["SampleStartYear"],
            y <= df["SampleEndYear"],
            y <= df["Year"],
        ],
        ["pre_sample", "in_sample", "post_sample"],
        default="post_pub",
    )
    # M&P's design has no pre-sample category; C&Z extends returns backward.
    df = df[df["window"] != "pre_sample"]
    return df[["signalname", "date", "ret", "window", "Predictability in OP"]]


def apply_min_months(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.pivot_table(
        index="signalname", columns="window", values="ret", aggfunc="count"
    ).fillna(0)
    keep = counts.index[
        (counts.get("in_sample", 0) >= MIN_MONTHS)
        & (counts.get("post_pub", 0) >= MIN_MONTHS)
    ]
    return df[df["signalname"].isin(keep)].copy()


def fe_panel_estimates(df: pd.DataFrame) -> dict:
    """E1: ret_it = a_i + b1*PostSample + b2*PostPub, month-clustered SEs.

    Estimated by within-transformation (demeaning by predictor), which is
    numerically identical to including predictor fixed effects.
    """
    d = df.copy()
    d["ps"] = (d["window"] == "post_sample").astype(float)
    d["pp"] = (d["window"] == "post_pub").astype(float)
    for col in ["ret", "ps", "pp"]:
        d[f"{col}_w"] = d[col] - d.groupby("signalname")[col].transform("mean")
    X = d[["ps_w", "pp_w"]].to_numpy()
    res = sm.OLS(d["ret_w"].to_numpy(), X).fit(
        cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
    )
    mean_is = df.loc[df["window"] == "in_sample", "ret"].mean()
    b1, b2 = res.params
    return {
        "n_predictors": df["signalname"].nunique(),
        "n_months_rows": len(df),
        "mean_in_sample": mean_is,
        "beta_post_sample": b1,
        "se_post_sample": res.bse[0],
        "t_post_sample": res.tvalues[0],
        "beta_post_pub": b2,
        "se_post_pub": res.bse[1],
        "t_post_pub": res.tvalues[1],
        "decline_post_sample_pct": -b1 / mean_is * 100,
        "decline_post_pub_pct": -b2 / mean_is * 100,
    }


def postpub_mean_test(df: pd.DataFrame) -> dict:
    """E3: is the post-publication mean return > 0? Month-clustered SE."""
    d = df[df["window"] == "post_pub"]
    res = sm.OLS(d["ret"].to_numpy(), np.ones((len(d), 1))).fit(
        cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
    )
    return {
        "postpub_mean": res.params[0],
        "postpub_se": res.bse[0],
        "postpub_t": res.tvalues[0],
    }


def per_predictor_means(df: pd.DataFrame) -> pd.DataFrame:
    """E2: window means per predictor."""
    return (
        df.pivot_table(index="signalname", columns="window", values="ret", aggfunc="mean")
        .reindex(columns=["in_sample", "post_sample", "post_pub"])
    )


def run_spec(df: pd.DataFrame, label: str) -> dict:
    out = {"spec": label}
    out.update(fe_panel_estimates(df))
    out.update(postpub_mean_test(df))
    return out


def main() -> None:
    base = apply_min_months(load_panel())

    per_pred = per_predictor_means(base)
    per_pred.to_csv(OUT / "window_means_by_predictor.csv")

    specs = [run_spec(base, "primary")]

    # R1: clearly-reproduced predictors only
    specs.append(run_spec(base[base["Predictability in OP"] == "1_clear"], "R1_clear_only"))

    # R2: drop predictors whose in-sample mean LS <= 0 in our data
    is_mean = per_pred["in_sample"]
    good = is_mean.index[is_mean > 0]
    specs.append(run_spec(base[base["signalname"].isin(good)], "R2_positive_IS_only"))

    # R3: winsorize monthly returns at 1/99 pct within predictor
    w = base.copy()
    lo = w.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.01))
    hi = w.groupby("signalname")["ret"].transform(lambda s: s.quantile(0.99))
    w["ret"] = w["ret"].clip(lo, hi)
    specs.append(run_spec(w, "R3_winsorized_1_99"))

    # R4: end panel 2019-12 (pre-COVID regime check)
    specs.append(run_spec(base[base["date"] <= "2019-12-31"], "R4_end_2019"))

    # R5: balanced windows, >=36 months in each of the three windows
    counts = base.pivot_table(
        index="signalname", columns="window", values="ret", aggfunc="count"
    ).fillna(0)
    bal = counts.index[(counts >= 36).all(axis=1)]
    specs.append(run_spec(base[base["signalname"].isin(bal)], "R5_balanced_36m"))

    summary = pd.DataFrame(specs)
    summary.to_csv(OUT / "summary.csv", index=False)

    with pd.option_context("display.width", 200, "display.max_columns", 30):
        print(summary.round(3).to_string(index=False))

    # Window-level pooled means with month-clustered 95% CIs (for fig 1)
    rows = []
    for win in ["in_sample", "post_sample", "post_pub"]:
        d = base[base["window"] == win]
        res = sm.OLS(d["ret"].to_numpy(), np.ones((len(d), 1))).fit(
            cov_type="cluster", cov_kwds={"groups": d["date"].to_numpy()}
        )
        rows.append(
            {"window": win, "mean": res.params[0], "se": res.bse[0], "n_months_rows": len(d)}
        )
    pd.DataFrame(rows).to_csv(OUT / "window_level_estimates.csv", index=False)

    # Cross-predictor descriptives for the write-up
    desc = per_pred.describe().T[["count", "mean", "50%", "25%", "75%"]]
    desc.to_csv(OUT / "cross_predictor_descriptives.csv")
    print()
    print(desc.round(3).to_string())


if __name__ == "__main__":
    main()
