"""EXP-024: leave-one-family-out influence audit."""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.factor_dependence import factor_contrasts
from engineering.argus_lab.jkp_decay import load_eligible_us

OUT = Path(__file__).parent / "results"
ASSIGNMENTS = ROOT / "experiments/EXP-022-effective-factor-breadth/results/assignments.csv"


def main() -> None:
    contrasts = factor_contrasts(load_eligible_us(ROOT))
    assignments = pd.read_csv(ASSIGNMENTS, usecols=["name", "cluster"])
    joined = contrasts.merge(assignments, on="name", validate="one_to_one")
    full = float(joined.contrast_pct.mean())
    rows = []
    for cluster, omitted in joined.groupby("cluster"):
        retained = joined[joined.cluster != cluster]
        estimate = float(retained.contrast_pct.mean())
        rows.append({
            "omitted_cluster": cluster, "omitted_factors": len(omitted),
            "estimate_pct": estimate, "shift_pct": estimate - full,
            "members": ";".join(sorted(omitted.name)),
        })
    influence = pd.DataFrame(rows)
    max_abs_shift = float(influence.shift_pct.abs().max())
    least_negative = float(influence.estimate_pct.max())
    summary = pd.DataFrame([{
        "full_mean_pct": full, "deletions": len(influence),
        "minimum_estimate_pct": influence.estimate_pct.min(),
        "maximum_estimate_pct": least_negative, "max_abs_shift_pct": max_abs_shift,
        "most_influential_cluster": int(influence.loc[influence.shift_pct.abs().idxmax(), "omitted_cluster"]),
        "P1": bool((influence.estimate_pct < 0).all()), "P2": least_negative <= -.10,
        "P3": max_abs_shift <= .03, "falsifier": bool((influence.estimate_pct >= 0).any()),
    }])
    summary["survives"] = summary.P1 & summary.P2 & summary.P3
    OUT.mkdir(exist_ok=True)
    influence.to_csv(OUT / "leave_one_family_out.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
