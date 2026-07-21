"""EXP-018: publication-year donut robustness."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import fit_row, load_eligible_us, window_fit

OUT = Path(__file__).parent / "results"
FROZEN = -0.164


def main() -> None:
    panel = load_eligible_us(ROOT)
    year = panel.date.dt.year
    samples = {
        "exclude_publication_year": panel[year != panel.publication_year],
        "exclude_publication_plus_minus_one": panel[(year - panel.publication_year).abs() > 1],
    }
    estimates = pd.DataFrame([
        fit_row(window_fit(data), spec, len(data), data.name.nunique()) for spec, data in samples.items()
    ])
    a, b = estimates.iloc[0], estimates.iloc[1]
    p1 = bool(a.post_pub_pct <= -0.10 and abs(a.post_pub_t) >= 2.0)
    p2 = bool(b.post_pub_pct < 0 and abs(b.post_pub_t) >= 1.65)
    p3 = bool(abs(b.post_pub_pct - FROZEN) <= 0.08)
    falsifier = bool(a.post_pub_pct >= 0 or b.post_pub_pct >= 0)
    summary = pd.DataFrame([{"P1": p1, "P2": p2, "P3": p3, "falsifier": falsifier, "survives": p1 and p2 and p3, "strict_change_from_frozen_pct": b.post_pub_pct - FROZEN}])
    OUT.mkdir(exist_ok=True)
    estimates.to_csv(OUT / "estimates.csv", index=False); summary.to_csv(OUT / "summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(estimates.round(4).to_string(index=False)); print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
