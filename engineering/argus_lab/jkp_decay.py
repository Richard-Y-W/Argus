"""Shared, deterministic loaders and estimators for JKP publication-decay tests."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


def parse_jkp_metadata(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse JKP dates and retain an auditable reason for every source row."""
    rows = []
    for idx, row in raw.iterrows():
        years = [int(x) for x in re.findall(r"(?<!\d)(?:18|19|20)\d{2}(?!\d)", str(row.get("in-sample period", "")))]
        publications = re.findall(r"\(((?:18|19|20)\d{2})\)", str(row.get("cite", "")))
        rows.append({
            "source_row": idx,
            "name": row.get("abr_jkp") if pd.notna(row.get("abr_jkp")) else None,
            "sample_start": years[0] if years else np.nan,
            "sample_end": years[-1] if years else np.nan,
            "publication_year": int(publications[-1]) if publications else np.nan,
            "significance": pd.to_numeric(row.get("significance"), errors="coerce"),
        })
    flow = pd.DataFrame(rows)
    flow["reason"] = "eligible"
    flow.loc[flow.name.isna(), "reason"] = "missing_name"
    missing = flow[["sample_start", "sample_end", "publication_year"]].isna().any(axis=1)
    flow.loc[missing, "reason"] = "missing_or_ambiguous_year"
    invalid_order = (flow.reason == "eligible") & (flow.publication_year < flow.sample_end)
    flow.loc[invalid_order, "reason"] = "publication_before_sample_end"
    duplicates = flow.name.notna() & flow.name.duplicated(keep=False)
    flow.loc[(flow.reason == "eligible") & duplicates, "reason"] = "duplicate_name"
    eligible = flow[flow.reason == "eligible"].copy()
    eligible[["sample_start", "sample_end", "publication_year"]] = eligible[
        ["sample_start", "sample_end", "publication_year"]
    ].astype(int)
    return eligible.drop(columns="reason"), flow


def assign_jkp_windows(panel: pd.DataFrame) -> pd.DataFrame:
    """Apply the registered annual JKP publication clock."""
    panel = panel.copy()
    panel["date"] = pd.to_datetime(panel.date)
    panel = panel[panel.date.dt.year >= panel.sample_start].copy()
    year = panel.date.dt.year
    panel["window"] = np.select(
        [year <= panel.sample_end, year <= panel.publication_year],
        ["in_sample", "post_sample"], default="post_pub",
    )
    return panel


def eligible_factor_locations(panel: pd.DataFrame) -> pd.DataFrame:
    """Return location/name pairs with at least 12 in-sample and post-pub months."""
    keys = ["name"] if "location" not in panel else ["location", "name"]
    counts = panel.groupby(keys + ["window"]).size().unstack(fill_value=0)
    for column in ("in_sample", "post_pub"):
        if column not in counts:
            counts[column] = 0
    return counts[(counts.in_sample >= 12) & (counts.post_pub >= 12)].reset_index()[keys]


def load_jkp_metadata(root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(root / "datasets/raw/jkp_factor_details.xlsx", sheet_name="details")
    return parse_jkp_metadata(raw)


def load_eligible_us(root: Path) -> pd.DataFrame:
    metadata, _ = load_jkp_metadata(root)
    returns_path = root / "datasets/raw/jkp_usa/[usa]_[all_factors]_[monthly]_[vw].csv"
    panel = pd.read_csv(returns_path, usecols=["name", "date", "ret", "n_stocks"])
    panel = panel.merge(metadata, on="name", how="inner", validate="many_to_one")
    panel = assign_jkp_windows(panel)
    valid = eligible_factor_locations(panel)
    return panel.merge(valid, on="name", validate="many_to_many")


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
