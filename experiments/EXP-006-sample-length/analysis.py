"""EXP-006 registered sample-length test. Deterministic."""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)

def load():
    raw = ROOT / "datasets" / "raw"
    doc = pd.read_csv(raw / "SignalDoc.csv")
    doc = doc[(doc["Cat.Signal"] == "Predictor") & doc["Predictability in OP"].isin(["1_clear", "2_likely"]) & doc[["SampleStartYear","SampleEndYear","Year"]].notna().all(axis=1)]
    p = pd.read_parquet(raw / "PredictorPortsFull.parquet")
    p = p[(p.port == "LS")].copy(); p["date"] = pd.to_datetime(p.date); p = p[p.date <= "2024-12-31"]
    d = p.merge(doc[["Acronym","Predictability in OP","SampleStartYear","SampleEndYear","Year"]], left_on="signalname", right_on="Acronym")
    y = d.date.dt.year
    d["window"] = np.select([y < d.SampleStartYear, y <= d.SampleEndYear, y <= d.Year], ["pre","in_sample","post_sample"], default="post_pub")
    d = d[d.window != "pre"].copy()
    c = d.pivot_table(index="signalname",columns="window",values="ret",aggfunc="count").fillna(0)
    keep = c.index[(c.get("in_sample",0)>=12)&(c.get("post_pub",0)>=12)]
    return d[d.signalname.isin(keep)].copy()

def hc3(y, x, names):
    r=sm.OLS(y,sm.add_constant(x)).fit(cov_type="HC3")
    return pd.DataFrame({"term":["const"]+names,"coef":r.params,"se":r.bse,"t":r.tvalues})

def cross(d, floor=.10, clear=False, winsor=False):
    if clear: d=d[d["Predictability in OP"]=="1_clear"]
    w=d.pivot_table(index="signalname",columns="window",values="ret",aggfunc=["mean","count"])
    meta=d.groupby("signalname").Year.first()
    z=pd.DataFrame(index=w.index); z["is_mean"]=w[("mean","in_sample")]; z["pp_mean"]=w[("mean","post_pub")]; z["is_n"]=w[("count","in_sample")]; z["pub_year"]=meta
    z=z[z.is_mean>floor].dropna(); z["retention"]=z.pp_mean/z.is_mean
    if winsor: z.retention=z.retention.clip(z.retention.quantile(.05),z.retention.quantile(.95))
    for v in ["is_mean","pub_year"]: z[v+"_z"]=(z[v]-z[v].mean())/z[v].std()
    z["log_n_z"]=(np.log(z.is_n)-np.log(z.is_n).mean())/np.log(z.is_n).std()
    return z,hc3(z.retention,z[["log_n_z","is_mean_z","pub_year_z"]],["log_n_z","is_mean_z","pub_year_z"])

def panel_reg(d,z):
    q=d.merge(z[["is_mean","log_n_z"]],left_on="signalname",right_index=True)
    q["ps"]=(q.window=="post_sample").astype(float); q["pp"]=(q.window=="post_pub").astype(float)
    q["pp_is"]=q.pp*q.is_mean; q["pp_n"]=q.pp*q.log_n_z; q["pp_is_n"]=q.pp*q.is_mean*q.log_n_z
    names=["ps","pp","pp_is","pp_n","pp_is_n"]
    for v in ["ret"]+names: q[v+"_w"]=q[v]-q.groupby("signalname")[v].transform("mean")
    r=sm.OLS(q.ret_w,q[[v+"_w" for v in names]]).fit(cov_type="cluster",cov_kwds={"groups":q.date})
    return pd.DataFrame({"term":names,"coef":r.params.values,"se":r.bse.values,"t":r.tvalues.values})

def main():
    d=load(); rows=[]
    z,tab=cross(d); tab.insert(0,"spec","primary"); rows.append(tab)
    for name,kw in [("R1_winsor",{"winsor":True}),("R2_floor20",{"floor":.20}),("R3_clear",{"clear":True})]:
        _,t=cross(d,**kw); t.insert(0,"spec",name); rows.append(t)
    regs=pd.concat(rows); regs.to_csv(OUT/"cross_regressions.csv",index=False)
    terc=pd.qcut(z.is_n,3,labels=["short","middle","long"]); tt=z.assign(tercile=terc).groupby("tercile",observed=True).agg(n=("retention","size"),is_months=("is_n","mean"),retention=("retention","mean"),is_mean=("is_mean","mean"),pp_mean=("pp_mean","mean")); tt.to_csv(OUT/"terciles.csv")
    pr=panel_reg(d,z); pr.to_csv(OUT/"panel_regression.csv",index=False); z.to_csv(OUT/"predictors.csv")
    print(regs.round(3).to_string(index=False)); print("\nTerciles\n",tt.round(3)); print("\nPanel\n",pr.round(3).to_string(index=False))

if __name__=="__main__": main()
