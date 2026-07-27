"""EXP-022: pre-publication dependence and effective factor breadth."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.factor_dependence import (
    cluster_factors, effective_rank, prepublication_correlation, within_between_summary,
)
from engineering.argus_lab.jkp_decay import load_eligible_us

OUT = Path(__file__).parent / "results"


def main() -> None:
    panel = load_eligible_us(ROOT)
    correlation, overlap, coverage = prepublication_correlation(panel)
    assignments = cluster_factors(correlation)
    rank = effective_rank(correlation)
    dependence = within_between_summary(correlation, assignments)
    sizes = assignments.groupby("cluster").size().rename("factors").reset_index()
    nominal = len(correlation)
    summary = pd.DataFrame([{
        "nominal_factors": nominal, "effective_rank": rank,
        "effective_share": rank / nominal, "eligible_pair_coverage": coverage,
        **dependence,
        "P1": rank <= 70, "P2": rank <= nominal / 2,
        "P3": dependence["median_gap"] >= .10, "falsifier": rank > 100,
    }])
    summary["survives"] = summary.P1 & summary.P2 & summary.P3
    OUT.mkdir(exist_ok=True)
    summary.to_csv(OUT / "summary.csv", index=False)
    assignments.merge(sizes, on="cluster", suffixes=("", "_cluster")).to_csv(OUT / "assignments.csv", index=False)
    sizes.to_csv(OUT / "cluster_sizes.csv", index=False)
    correlation.to_csv(OUT / "prepublication_correlation.csv")
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
