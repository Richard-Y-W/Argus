"""EXP-020: equal-factor publication-decay contrasts."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import load_eligible_us

OUT = Path(__file__).parent / "results"


def t_stat(values: pd.Series) -> float:
    return float(values.mean() / (values.std(ddof=1) / np.sqrt(len(values))))


def main() -> None:
    panel = load_eligible_us(ROOT)
    means = panel.groupby(["name", "window"], observed=True).ret.mean().unstack()
    means = means.dropna(subset=["in_sample", "post_sample", "post_pub"])
    contrasts = means.assign(
        postpub_minus_insample=(means.post_pub - means.in_sample) * 100,
        postpub_minus_postsample=(means.post_pub - means.post_sample) * 100,
    ).reset_index()
    primary = contrasts.postpub_minus_insample
    diagnostic = contrasts.postpub_minus_postsample
    summary = pd.DataFrame([{
        "factors": len(primary), "mean_pct": primary.mean(), "median_pct": primary.median(),
        "t_stat": t_stat(primary), "negative_share": (primary < 0).mean(),
        "q25_pct": primary.quantile(.25), "q75_pct": primary.quantile(.75),
        "diagnostic_mean_pct": diagnostic.mean(), "diagnostic_t": t_stat(diagnostic),
        "P1": bool(primary.mean() <= -.10), "P2": bool(t_stat(primary) <= -2.0),
        "P3": bool((primary < 0).mean() >= .55), "falsifier": bool(primary.mean() >= 0),
    }])
    summary["survives"] = summary.P1 & summary.P2 & summary.P3
    OUT.mkdir(exist_ok=True)
    contrasts.to_csv(OUT / "factor_contrasts.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
