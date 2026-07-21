"""Shared, deterministic loaders and estimators for JKP publication-decay tests."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


def load_eligible_us(root: Path) -> pd.DataFrame:
    metadata_path = root / "datasets/raw/jkp_factor_details.xlsx"
    returns_path = root / "datasets/raw/jkp_usa/[usa]_[all_factors]_[monthly]_[vw].csv"
    raw = pd.read_excel(metadata_path, sheet_name="details")
    rows = []
    for _, row in raw.iterrows():
        years = [int(x) for x in re.findall(r"(?<!\d)(?:18|19|20)\d{2}(?!\d)", str(row.get("in-sample period", "")))]
        publications = re.findall(r"\(((?:18|19|20)\d{2})\)", str(row.get("cite", "")))
        rows.append({
            "name": row.get("abr_jkp") if pd.notna(row.get("abr_jkp")) else None,
            "sample_start": years[0] if years else np.nan,
            "sample_end": years[-1] if years else np.nan,
            "publication_year": int(publications[-1]) if publications else np.nan,
        })
    metadata = pd.DataFrame(rows).dropna()
    metadata = metadata[metadata.publication_year >= metadata.sample_end]
    metadata = metadata[~metadata.name.duplicated(keep=False)].copy()
    metadata[["sample_start", "sample_end", "publication_year"]] = metadata[
        ["sample_start", "sample_end", "publication_year"]
    ].astype(int)
    panel = pd.read_csv(returns_path, usecols=["name", "date", "ret", "n_stocks"])
    panel = panel.merge(metadata, on="name", how="inner", validate="many_to_one")
    panel["date"] = pd.to_datetime(panel.date)
    panel = panel[panel.date.dt.year >= panel.sample_start].copy()
    year = panel.date.dt.year
    panel["window"] = np.select(
        [year <= panel.sample_end, year <= panel.publication_year],
        ["in_sample", "post_sample"], default="post_pub",
    )
    counts = panel.groupby(["name", "window"]).size().unstack(fill_value=0)
    for column in ("in_sample", "post_pub"):
        if column not in counts:
            counts[column] = 0
    valid = counts[(counts.in_sample >= 12) & (counts.post_pub >= 12)].index
    return panel[panel.name.isin(valid)].copy()


def window_fit(panel: pd.DataFrame, cluster: str = "month"):
    data = panel.copy()
    data["post_sample"] = (data.window == "post_sample").astype(float)
    data["post_pub"] = (data.window == "post_pub").astype(float)
    columns = ["post_sample", "post_pub"]
    y = data.ret - data.groupby("name").ret.transform("mean")
    x = data[columns] - data.groupby("name")[columns].transform("mean")
    groups = data.date if cluster == "month" else pd.DataFrame({"factor": pd.Categorical(data.name).codes, "month": pd.Categorical(data.date).codes})
    return sm.OLS(y, x).fit(cov_type="cluster", cov_kwds={"groups": groups})


def fit_row(fit, spec: str, observations: int, factors: int) -> dict:
    contrast = np.array([-1.0, 1.0])
    difference = float(contrast @ fit.params.to_numpy())
    difference_se = float(np.sqrt(contrast @ fit.cov_params().to_numpy() @ contrast))
    return {
        "spec": spec, "observations": observations, "factors": factors,
        "post_sample_pct": fit.params.post_sample * 100,
        "post_sample_t": fit.tvalues.post_sample,
        "post_pub_pct": fit.params.post_pub * 100,
        "post_pub_t": fit.tvalues.post_pub,
        "postpub_minus_postsample_pct": difference * 100,
        "contrast_t": difference / difference_se,
    }
