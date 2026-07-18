"""EXP-014: C&Z publication decay under JKP-like history floors."""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "datasets/raw"
OUT = Path(__file__).parent / "results"

def load_panel():
    doc = pd.read_csv(RAW / "SignalDoc.csv")
    doc = doc[(doc["Cat.Signal"] == "Predictor") & doc["Predictability in OP"].isin(["1_clear", "2_likely"]) & doc[["SampleStartYear", "SampleEndYear", "Year"]].notna().all(axis=1)]
    port = pd.read_parquet(RAW / "PredictorPortsFull.parquet")
    d = port[port.port == "LS"].merge(doc[["Acronym", "Predictability in OP", "SampleStartYear", "SampleEndYear", "Year"]], left_on="signalname", right_on="Acronym")
    d["date"] = pd.to_datetime(d.date); d = d[d.date <= "2024-12-31"].copy(); y = d.date.dt.year
    d["window"] = np.select([y < d.SampleStartYear, y <= d.SampleEndYear, y <= d.Year], ["pre", "in_sample", "post_sample"], default="post_pub")
    return d[d.window != "pre"].copy()

def eligible(d):
    c = d.groupby(["signalname", "window"]).size().unstack(fill_value=0)
    for col in ["in_sample", "post_pub"]:
        if col not in c: c[col] = 0
    keep = c[(c.in_sample >= 12) & (c.post_pub >= 12)].index
    return d[d.signalname.isin(keep)].copy()

def estimate(d, spec):
    d = eligible(d); d["ps"] = (d.window == "post_sample").astype(float); d["pp"] = (d.window == "post_pub").astype(float)
    y = d.ret - d.groupby("signalname").ret.transform("mean")
    x = d[["ps", "pp"]] - d.groupby("signalname")[["ps", "pp"]].transform("mean")
    fit = sm.OLS(y, x).fit(cov_type="cluster", cov_kwds={"groups": d.date})
    contrast = np.array([-1., 1.]); diff = float(contrast @ fit.params); se = float(np.sqrt(contrast @ fit.cov_params() @ contrast))
    return {"spec": spec, "factors": d.signalname.nunique(), "observations": len(d), "post_sample": fit.params.ps, "post_sample_t": fit.tvalues.ps, "post_pub": fit.params.pp, "post_pub_t": fit.tvalues.pp, "postpub_minus_postsample": diff, "contrast_t": diff/se}

def main():
    d = load_panel()
    rows = [estimate(d, "full"), estimate(d[d.date >= "1986-01-01"], "floor_1986"), estimate(d[d.date >= "1990-01-01"], "floor_1990"), estimate(d[(d.date >= "1986-01-01") & (d["Predictability in OP"] == "1_clear")], "floor_1986_clear")]
    out = pd.DataFrame(rows); full = out.set_index("spec").loc["full"]; p = out.set_index("spec").loc["floor_1986"]
    attenuation = 1 - abs(p.post_pub / full.post_pub)
    verdicts = {"P1": bool(p.post_pub < 0 and abs(p.post_pub_t) >= 2 and attenuation >= .25), "P2": bool(p.post_pub >= -.10), "P3": bool(p.postpub_minus_postsample < 0), "P4": bool(abs(out.set_index('spec').loc['floor_1990'].post_pub) < abs(full.post_pub) and abs(out.set_index('spec').loc['floor_1986_clear'].post_pub) < abs(full.post_pub))}
    falsifier = bool(p.post_pub >= 0 or abs(p.post_pub) >= abs(full.post_pub))
    OUT.mkdir(exist_ok=True); out.to_csv(OUT / "estimates.csv", index=False); pd.DataFrame([{**verdicts, "attenuation": attenuation, "falsifier": falsifier}]).to_csv(OUT / "summary.csv", index=False)
    log = "\n".join([*(f"{k}={v}" for k,v in verdicts.items()), f"falsifier={falsifier}"]); (OUT / "run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(out.to_string(index=False)); print(f"attenuation={attenuation:.6f}\n{log}")

if __name__ == "__main__": main()
