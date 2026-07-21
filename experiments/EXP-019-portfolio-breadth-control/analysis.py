"""EXP-019: control US decay for time-varying portfolio breadth."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engineering.argus_lab.jkp_decay import load_eligible_us

OUT = Path(__file__).parent / "results"
FROZEN = -0.164


def estimate(data: pd.DataFrame, spec: str, interactions: bool) -> dict:
    d = data.copy()
    d["post_sample"] = (d.window == "post_sample").astype(float)
    d["post_pub"] = (d.window == "post_pub").astype(float)
    d["log_breadth"] = np.log(d.n_stocks)
    d["log_breadth_dm"] = d.log_breadth - d.groupby("name").log_breadth.transform("mean")
    columns = ["post_sample", "post_pub", "log_breadth_dm"]
    if interactions:
        d["post_sample_x_breadth"] = d.post_sample * d.log_breadth_dm
        d["post_pub_x_breadth"] = d.post_pub * d.log_breadth_dm
        columns += ["post_sample_x_breadth", "post_pub_x_breadth"]
    y = d.ret - d.groupby("name").ret.transform("mean")
    x = d[columns] - d.groupby("name")[columns].transform("mean")
    fit = sm.OLS(y, x).fit(cov_type="cluster", cov_kwds={"groups": d.date})
    return {"spec": spec, "observations": len(d), "factors": d.name.nunique(), "post_pub_pct": fit.params.post_pub * 100, "post_pub_t": fit.tvalues.post_pub, "breadth_coef_pct": fit.params.log_breadth_dm * 100, "breadth_t": fit.tvalues.log_breadth_dm}


def main() -> None:
    panel = load_eligible_us(ROOT)
    usable = panel[(panel.n_stocks > 0) & panel.n_stocks.notna()].copy()
    estimates = pd.DataFrame([estimate(usable, "breadth_control", False), estimate(usable, "breadth_interactions", True)])
    controlled, interacted = estimates.iloc[0], estimates.iloc[1]
    attenuation = 1 - abs(controlled.post_pub_pct) / abs(FROZEN)
    p1 = bool(controlled.post_pub_pct <= -0.10 and abs(controlled.post_pub_t) >= 2.0)
    p2 = bool(attenuation < 0.25)
    p3 = bool(interacted.post_pub_pct < 0 and abs(interacted.post_pub_t) >= 1.65)
    falsifier = bool(controlled.post_pub_pct >= 0)
    summary = pd.DataFrame([{"P1": p1, "P2": p2, "P3": p3, "falsifier": falsifier, "survives": p1 and p2 and p3, "attenuation": attenuation, "observations_lost": len(panel) - len(usable)}])
    breadth = usable.groupby("window").n_stocks.agg(["count", "median", "mean", "min", "max"]).reset_index()
    OUT.mkdir(exist_ok=True)
    estimates.to_csv(OUT / "estimates.csv", index=False); summary.to_csv(OUT / "summary.csv", index=False); breadth.to_csv(OUT / "breadth_summary.csv", index=False)
    (OUT / "run_log.txt").write_text(summary.to_string(index=False) + "\n", encoding="utf-8")
    print(estimates.round(4).to_string(index=False)); print(summary.round(4).to_string(index=False)); print(breadth.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
