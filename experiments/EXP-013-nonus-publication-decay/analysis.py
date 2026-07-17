"""EXP-013: registered non-US publication-decay replication."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
RETURNS = ROOT / "datasets/raw/jkp_global/[all_regions]_[all_factors]_[monthly]_[vw].csv"
METADATA = ROOT / "datasets/raw/jkp_factor_details.xlsx"
OUT = Path(__file__).parent / "results"
LOCATIONS = ("world_ex_us", "developed", "emerging")


def parse_metadata() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(METADATA, sheet_name="details")
    rows = []
    for idx, row in raw.iterrows():
        period_years = [int(x) for x in re.findall(r"(?<!\d)(?:18|19|20)\d{2}(?!\d)", str(row.get("in-sample period", "")))]
        pub_years = re.findall(r"\(((?:18|19|20)\d{2})\)", str(row.get("cite", "")))
        rows.append({
            "source_row": idx, "name": row.get("abr_jkp") if pd.notna(row.get("abr_jkp")) else None,
            "sample_start": period_years[0] if period_years else np.nan,
            "sample_end": period_years[-1] if period_years else np.nan,
            "publication_year": int(pub_years[-1]) if pub_years else np.nan,
            "significance": pd.to_numeric(row.get("significance"), errors="coerce"),
            "cite": str(row.get("cite", "")),
        })
    parsed = pd.DataFrame(rows)
    parsed["reason"] = "eligible"
    parsed.loc[parsed.name.isna(), "reason"] = "missing_name"
    missing_year = parsed[["sample_start", "sample_end", "publication_year"]].isna().any(axis=1)
    parsed.loc[missing_year, "reason"] = "missing_or_ambiguous_year"
    parsed.loc[(parsed.reason == "eligible") & (parsed.publication_year < parsed.sample_end), "reason"] = "publication_before_sample_end"
    duplicated = parsed.name.notna() & parsed.name.duplicated(keep=False)
    parsed.loc[(parsed.reason == "eligible") & duplicated, "reason"] = "duplicate_name"
    eligible = parsed[parsed.reason == "eligible"].copy()
    years = ["sample_start", "sample_end", "publication_year"]
    eligible[years] = eligible[years].astype(int)
    return eligible, parsed


def build_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    meta, flow = parse_metadata()
    use = pd.read_csv(RETURNS, usecols=["location", "name", "date", "ret"])
    use = use[use.location.isin(LOCATIONS)].merge(meta, on="name", how="inner", validate="many_to_one")
    use["date"] = pd.to_datetime(use.date)
    use["year"] = use.date.dt.year
    use = use[use.year >= use.sample_start].copy()
    use["window"] = np.select(
        [use.year <= use.sample_end, use.year <= use.publication_year],
        ["in_sample", "post_sample"], default="post_pub"
    )
    counts = use.groupby(["location", "name", "window"]).size().unstack(fill_value=0)
    for col in ("in_sample", "post_pub"):
        if col not in counts:
            counts[col] = 0
    eligible_pairs = counts[(counts.in_sample >= 12) & (counts.post_pub >= 12)].reset_index()[["location", "name"]]
    return use.merge(eligible_pairs, on=["location", "name"], how="inner"), flow


def panel_estimate(panel: pd.DataFrame, label: str) -> dict:
    d = panel.copy()
    d["post_sample"] = (d.window == "post_sample").astype(float)
    d["post_pub"] = (d.window == "post_pub").astype(float)
    y = d.ret - d.groupby("name").ret.transform("mean")
    x = d[["post_sample", "post_pub"]] - d.groupby("name")[["post_sample", "post_pub"]].transform("mean")
    fit = sm.OLS(y, x).fit(cov_type="cluster", cov_kwds={"groups": d.date})
    contrast = np.array([-1.0, 1.0])
    diff = float(contrast @ fit.params.to_numpy())
    diff_se = float(np.sqrt(contrast @ fit.cov_params().to_numpy() @ contrast))
    return {
        "spec": label, "observations": len(d), "factors": d.name.nunique(),
        "post_sample_coef_pct": fit.params["post_sample"] * 100,
        "post_sample_se_pct": fit.bse["post_sample"] * 100,
        "post_sample_t": fit.tvalues["post_sample"],
        "post_pub_coef_pct": fit.params["post_pub"] * 100,
        "post_pub_se_pct": fit.bse["post_pub"] * 100,
        "post_pub_t": fit.tvalues["post_pub"],
        "postpub_minus_postsample_pct": diff * 100,
        "contrast_se_pct": diff_se * 100,
        "contrast_t": diff / diff_se,
    }


def scalar(value) -> float:
    return float(value.iloc[0] if hasattr(value, "iloc") else value[0])


def main() -> None:
    panel, metadata_flow = build_panel()
    estimates = [panel_estimate(panel[panel.location == location], location) for location in LOCATIONS]
    primary = panel[panel.location == "world_ex_us"].copy()
    estimates.append(panel_estimate(primary[primary.significance == 1], "world_ex_us_significant"))

    windows = primary.groupby(["name", "window"], as_index=False).ret.mean().pivot(index="name", columns="window", values="ret").reset_index()
    windows = windows.merge(primary[["name", "significance"]].drop_duplicates(), on="name", validate="one_to_one")
    windows["postpub_minus_insample"] = windows.post_pub - windows.in_sample
    breadth = float((windows.postpub_minus_insample < 0).mean())
    factor_fit = sm.OLS(windows.postpub_minus_insample, np.ones((len(windows), 1))).fit(cov_type="HC3")
    factor_change, factor_se = scalar(factor_fit.params), scalar(factor_fit.bse)

    estimates_df = pd.DataFrame(estimates)
    p = estimates_df[estimates_df.spec == "world_ex_us"].iloc[0]
    regional = estimates_df[estimates_df.spec.isin(["developed", "emerging"])]
    sig = estimates_df[estimates_df.spec == "world_ex_us_significant"].iloc[0]
    verdicts = {
        "P1": bool(p.post_pub_coef_pct <= -0.10 and abs(p.post_pub_t) >= 2.0),
        "P2": bool(p.post_sample_coef_pct < 0 and p.postpub_minus_postsample_pct <= -0.05 and abs(p.contrast_t) >= 1.65),
        "P3": bool((regional.post_pub_coef_pct < 0).all() and (regional.post_pub_t.abs() >= 2.0).any()),
        "P4": bool(breadth > 0.55),
        "P5": bool(sig.post_pub_coef_pct < 0 and factor_change < 0),
    }
    falsifier = not verdicts["P1"] or sig.post_pub_coef_pct >= 0 or factor_change >= 0
    summary = {"eligible_world_ex_us_factors": primary.name.nunique(), "breadth_negative_share": breadth,
               "factor_equal_weight_change_pct": factor_change * 100, "factor_equal_weight_se_pct": factor_se * 100,
               "factor_equal_weight_t": factor_change / factor_se, **verdicts, "falsifier": falsifier}

    OUT.mkdir(exist_ok=True)
    estimates_df.to_csv(OUT / "panel_estimates.csv", index=False)
    windows.to_csv(OUT / "factor_windows.csv", index=False)
    metadata_flow.to_csv(OUT / "metadata_flow.csv", index=False)
    pd.DataFrame([summary]).to_csv(OUT / "summary.csv", index=False)
    log = "\n".join([f"{k}={v}" for k, v in verdicts.items()] + [f"falsifier={falsifier}"])
    (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(estimates_df.round(4).to_string(index=False))
    print(pd.DataFrame([summary]).round(4).to_string(index=False))
    print(log)


if __name__ == "__main__":
    main()
