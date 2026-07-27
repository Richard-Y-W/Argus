"""EXP-023: exact family-level publication-decay inference."""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.factor_dependence import exact_sign_pvalue, factor_contrasts
from engineering.argus_lab.jkp_decay import load_eligible_us

OUT = Path(__file__).parent / "results"
ASSIGNMENTS = ROOT / "experiments/EXP-022-effective-factor-breadth/results/assignments.csv"


def main() -> None:
    panel = load_eligible_us(ROOT)
    contrasts = factor_contrasts(panel)
    assignments = pd.read_csv(ASSIGNMENTS, usecols=["name", "cluster"])
    joined = contrasts.merge(assignments, on="name", validate="one_to_one")
    families = joined.groupby("cluster").contrast_pct.agg(
        factors="size", mean_pct="mean", median_pct="median"
    ).reset_index()
    negative_share = joined.assign(negative=joined.contrast_pct < 0).groupby("cluster").negative.mean()
    families["negative_factor_share"] = families.cluster.map(negative_share)
    mean = float(families.mean_pct.mean())
    pvalue = exact_sign_pvalue(families.mean_pct)
    negative = int((families.mean_pct < 0).sum())
    summary = pd.DataFrame([{
        "clusters": len(families), "equal_cluster_mean_pct": mean,
        "negative_clusters": negative, "exact_two_sided_p": pvalue,
        "P1": mean <= -.10, "P2": negative >= 9, "P3": pvalue <= .05,
        "falsifier": mean >= 0,
    }])
    summary["survives"] = summary.P1 & summary.P2 & summary.P3
    OUT.mkdir(exist_ok=True)
    families.to_csv(OUT / "family_contrasts.csv", index=False)
    joined.to_csv(OUT / "factor_contrasts_with_family.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
