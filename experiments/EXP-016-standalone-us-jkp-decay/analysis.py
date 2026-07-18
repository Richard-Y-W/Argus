"""EXP-016: standalone JKP US publication-decay test."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
USA = ROOT / "datasets/raw/jkp_usa/[usa]_[all_factors]_[monthly]_[vw].csv"
GLOBAL = ROOT / "datasets/raw/jkp_global/[all_regions]_[all_factors]_[monthly]_[vw].csv"
METADATA = ROOT / "datasets/raw/jkp_factor_details.xlsx"
OUT = Path(__file__).parent / "results"


def parse_metadata() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(METADATA, sheet_name="details")
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
    flow.loc[(flow.reason == "eligible") & (flow.publication_year < flow.sample_end), "reason"] = "publication_before_sample_end"
    duplicates = flow.name.notna() & flow.name.duplicated(keep=False)
    flow.loc[(flow.reason == "eligible") & duplicates, "reason"] = "duplicate_name"
    eligible = flow[flow.reason == "eligible"].copy()
    eligible[["sample_start", "sample_end", "publication_year"]] = eligible[["sample_start", "sample_end", "publication_year"]].astype(int)
    return eligible.drop(columns="reason"), flow


def load_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata, flow = parse_metadata()
    usa = pd.read_csv(USA, usecols=["location", "name", "date", "ret", "n_stocks"])
    usa["n_securities"] = usa.pop("n_stocks")
    exus = pd.read_csv(GLOBAL, usecols=["location", "name", "date", "ret", "n_countries"])
    exus = exus[exus.location == "world_ex_us"].copy()
    exus["n_securities"] = np.nan
    panel = pd.concat([usa, exus.drop(columns="n_countries")], ignore_index=True)
    panel = panel.merge(metadata, on="name", how="inner", validate="many_to_one")
    panel["date"] = pd.to_datetime(panel.date)
    panel = panel[panel.date.dt.year >= panel.sample_start].copy()
    year = panel.date.dt.year
    panel["window"] = np.select(
        [year <= panel.sample_end, year <= panel.publication_year],
        ["in_sample", "post_sample"], default="post_pub",
    )
    counts = panel.groupby(["location", "name", "window"]).size().unstack(fill_value=0)
    for column in ("in_sample", "post_pub"):
        if column not in counts:
            counts[column] = 0
    valid = counts[(counts.in_sample >= 12) & (counts.post_pub >= 12)].reset_index()[["location", "name"]]
    return panel.merge(valid, on=["location", "name"], validate="many_to_many"), flow


def estimate(data: pd.DataFrame, spec: str) -> dict:
    data = data.copy()
    data["post_sample"] = (data.window == "post_sample").astype(float)
    data["post_pub"] = (data.window == "post_pub").astype(float)
    y = data.ret - data.groupby("name").ret.transform("mean")
    x = data[["post_sample", "post_pub"]] - data.groupby("name")[["post_sample", "post_pub"]].transform("mean")
    fit = sm.OLS(y, x).fit(cov_type="cluster", cov_kwds={"groups": data.date})
    contrast = np.array([-1.0, 1.0])
    difference = float(contrast @ fit.params.to_numpy())
    difference_se = float(np.sqrt(contrast @ fit.cov_params().to_numpy() @ contrast))
    return {
        "spec": spec, "observations": len(data), "factors": data.name.nunique(),
        "post_sample_pct": fit.params.post_sample * 100,
        "post_sample_t": fit.tvalues.post_sample,
        "post_pub_pct": fit.params.post_pub * 100,
        "post_pub_t": fit.tvalues.post_pub,
        "postpub_minus_postsample_pct": difference * 100,
        "contrast_t": difference / difference_se,
    }


def main() -> None:
    panel, metadata_flow = load_panel()
    usa = panel[panel.location == "usa"].copy()
    exus = panel[panel.location == "world_ex_us"].copy()
    common = sorted(set(usa.name) & set(exus.name))
    direct = usa[usa.name.isin(common)].merge(
        exus[exus.name.isin(common)][["name", "date", "ret"]],
        on=["name", "date"], suffixes=("_usa", "_exus"), validate="one_to_one",
    )
    direct["ret"] = direct.ret_usa - direct.ret_exus

    estimates = pd.DataFrame([
        estimate(usa, "usa"), estimate(exus, "world_ex_us"),
        estimate(direct, "usa_minus_world_ex_us"),
        estimate(usa[usa.significance == 1], "usa_significant"),
    ])
    windows = panel.groupby(["location", "name", "window"], as_index=False).agg(
        mean_return=("ret", "mean"), months=("ret", "size"), median_securities=("n_securities", "median")
    ).pivot(index=["location", "name"], columns="window", values="mean_return").reset_index()
    windows["postpub_minus_insample"] = windows.post_pub - windows.in_sample
    common_windows = windows[windows.name.isin(common)].pivot(index="name", columns="location", values="postpub_minus_insample").dropna()
    equal_factor_gap = float((common_windows.usa - common_windows.world_ex_us).mean())
    usa_windows = windows[windows.location == "usa"]
    breadth = float((usa_windows.postpub_minus_insample < 0).mean())

    indexed = estimates.set_index("spec")
    primary = indexed.loc["usa"]
    paired = indexed.loc["usa_minus_world_ex_us"]
    significant = indexed.loc["usa_significant"]
    verdicts = {
        "P1": bool(primary.post_pub_pct <= -0.15 and abs(primary.post_pub_t) >= 2.0),
        "P2": bool(primary.postpub_minus_postsample_pct <= -0.10 and abs(primary.contrast_t) >= 1.65),
        "P3": bool(paired.post_pub_pct <= -0.10 and abs(paired.post_pub_t) >= 1.65),
        "P4": bool(breadth > 0.60 and significant.post_pub_pct < 0 and equal_factor_gap < 0),
    }
    falsifier = bool(not verdicts["P1"] or paired.post_pub_pct >= 0 or equal_factor_gap >= 0)
    summary = {**verdicts, "falsifier": falsifier, "survives": all(verdicts.values()),
               "usa_negative_breadth": breadth, "equal_factor_gap_pct": equal_factor_gap * 100,
               "common_factors": len(common), "paired_factor_months": len(direct)}

    OUT.mkdir(exist_ok=True)
    estimates.to_csv(OUT / "estimates.csv", index=False)
    windows.to_csv(OUT / "factor_windows.csv", index=False)
    metadata_flow.to_csv(OUT / "metadata_flow.csv", index=False)
    pd.DataFrame([summary]).to_csv(OUT / "summary.csv", index=False)
    log = "\n".join([*(f"{key}={value}" for key, value in verdicts.items()),
                      f"falsifier={falsifier}", f"survives={all(verdicts.values())}"])
    (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(estimates.round(4).to_string(index=False))
    print(pd.DataFrame([summary]).round(4).to_string(index=False))
    print(log)


if __name__ == "__main__":
    main()
