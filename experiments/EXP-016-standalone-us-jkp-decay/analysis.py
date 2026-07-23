"""EXP-016: standalone JKP US publication-decay test."""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import (
    assign_jkp_windows,
    eligible_factor_locations,
    fit_row,
    load_jkp_metadata,
    window_fit,
)

USA = ROOT / "datasets/raw/jkp_usa/[usa]_[all_factors]_[monthly]_[vw].csv"
GLOBAL = ROOT / "datasets/raw/jkp_global/[all_regions]_[all_factors]_[monthly]_[vw].csv"
OUT = Path(__file__).parent / "results"


def load_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata, flow = load_jkp_metadata(ROOT)
    usa = pd.read_csv(USA, usecols=["location", "name", "date", "ret", "n_stocks"])
    usa["n_securities"] = usa.pop("n_stocks")
    exus = pd.read_csv(GLOBAL, usecols=["location", "name", "date", "ret", "n_countries"])
    exus = exus[exus.location == "world_ex_us"].copy()
    exus["n_securities"] = np.nan
    panel = pd.concat([usa, exus.drop(columns="n_countries")], ignore_index=True)
    panel = panel.merge(metadata, on="name", how="inner", validate="many_to_one")
    panel = assign_jkp_windows(panel)
    valid = eligible_factor_locations(panel)
    return panel.merge(valid, on=["location", "name"], validate="many_to_many"), flow


def estimate(data: pd.DataFrame, spec: str) -> dict:
    return fit_row(window_fit(data), spec, len(data), data.name.nunique())


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
