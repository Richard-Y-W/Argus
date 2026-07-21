"""EXP-017: two-way clustered inference for standalone US decay."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import fit_row, load_eligible_us, window_fit

OUT = Path(__file__).parent / "results"


def main() -> None:
    panel = load_eligible_us(ROOT)
    estimates = pd.DataFrame([
        fit_row(window_fit(panel, "month"), "month_cluster_frozen", len(panel), panel.name.nunique()),
        fit_row(window_fit(panel, "two_way"), "factor_and_month_clusters", len(panel), panel.name.nunique()),
    ])
    primary = estimates.iloc[1]
    p1 = bool(primary.post_pub_pct <= -0.10 and abs(primary.post_pub_t) >= 2.0)
    p2 = bool(primary.postpub_minus_postsample_pct <= -0.10 and abs(primary.contrast_t) >= 2.0)
    falsifier = bool(primary.post_pub_pct >= 0 or abs(primary.post_pub_t) < 1.65 or primary.postpub_minus_postsample_pct >= 0 or abs(primary.contrast_t) < 1.65)
    summary = pd.DataFrame([{"P1": p1, "P2": p2, "falsifier": falsifier, "survives": p1 and p2}])
    OUT.mkdir(exist_ok=True)
    estimates.to_csv(OUT / "estimates.csv", index=False)
    summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(estimates.round(4).to_string(index=False)); print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
