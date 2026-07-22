"""EXP-021: leave-one-factor-out audit of pooled US decay."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import load_eligible_us, window_fit

OUT = Path(__file__).parent / "results"


def coefficient(panel: pd.DataFrame) -> tuple[float, float]:
    fit = window_fit(panel, cluster="month")
    return float(fit.params.post_pub * 100), float(fit.tvalues.post_pub)


def main() -> None:
    panel = load_eligible_us(ROOT)
    full_coef, full_t = coefficient(panel)
    rows = []
    for name in sorted(panel.name.unique()):
        coef, t_value = coefficient(panel[panel.name != name])
        rows.append({"deleted_factor": name, "post_pub_pct": coef, "post_pub_t": t_value, "shift_pct": coef - full_coef})
    deletions = pd.DataFrame(rows)
    max_shift = deletions.shift_pct.abs().max()
    coef_range = deletions.post_pub_pct.max() - deletions.post_pub_pct.min()
    summary = pd.DataFrame([{
        "factors": panel.name.nunique(), "full_post_pub_pct": full_coef, "full_t": full_t,
        "minimum_loo_pct": deletions.post_pub_pct.min(), "maximum_loo_pct": deletions.post_pub_pct.max(),
        "max_abs_shift_pct": max_shift, "loo_range_pct": coef_range,
        "most_influential_factor": deletions.loc[deletions.shift_pct.abs().idxmax(), "deleted_factor"],
        "P1": bool(deletions.post_pub_pct.max() <= -.10), "P2": bool(max_shift <= .03),
        "P3": bool(coef_range <= .05), "falsifier": bool((deletions.post_pub_pct >= 0).any()),
    }])
    summary["survives"] = summary.P1 & summary.P2 & summary.P3
    OUT.mkdir(exist_ok=True)
    deletions.to_csv(OUT / "leave_one_factor_out.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
