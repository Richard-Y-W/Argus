"""EXP-007 registered cohort-stability test. Deterministic."""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent/"results"; OUT.mkdir(exist_ok=True)

def load(first60=False):
    raw=ROOT/"datasets"/"raw"; doc=pd.read_csv(raw/"SignalDoc.csv")
    doc=doc[(doc["Cat.Signal"]=="Predictor")&doc["Predictability in OP"].isin(["1_clear","2_likely"])&doc[["SampleStartYear","SampleEndYear","Year"]].notna().all(axis=1)]
    p=pd.read_parquet(raw/"PredictorPortsFull.parquet"); p=p[p.port=="LS"].copy(); p["date"]=pd.to_datetime(p.date); p=p[p.date<="2024-12-31"]
    d=p.merge(doc[["Acronym","Predictability in OP","SampleStartYear","SampleEndYear","Year"]],left_on="signalname",right_on="Acronym"); y=d.date.dt.year
    d["window"]=np.select([y<d.SampleStartYear,y<=d.SampleEndYear,y<=d.Year],["pre","in_sample","post_sample"],default="post_pub"); d=d[d.window!="pre"].copy()
    c=d.pivot_table(index="signalname",columns="window",values="ret",aggfunc="count").fillna(0); need=60 if first60 else 12; keep=c.index[(c.get("in_sample",0)>=12)&(c.get("post_pub",0)>=need)]; d=d[d.signalname.isin(keep)]
    if first60: d=d[(d.window!="post_pub")|(d.groupby("signalname").cumcount()<0)].copy() if False else pd.concat([d[d.window!="post_pub"],d[d.window=="post_pub"].sort_values(["signalname","date"]).groupby("signalname").head(60)])
    w=d.pivot_table(index="signalname",columns="window",values="ret",aggfunc=["mean","count"]); z=pd.DataFrame(index=w.index); z["is_mean"]=w[("mean","in_sample")]; z["pp_mean"]=w[("mean","post_pub")]; z["pp_n"]=w[("count","post_pub")]
    z=z.join(d.groupby("signalname")[["Year"]].first()).join(d.groupby("signalname")["Predictability in OP"].first()); z["decay"]=(z.is_mean-z.pp_mean)/z.is_mean
    return z

def reg(z,floor=.10,clear=False,winsor=False,equal_horizon=False):
    q=z[z.is_mean>floor].dropna().copy()
    if clear:q=q[q["Predictability in OP"]=="1_clear"]
    if winsor:q.decay=q.decay.clip(q.decay.quantile(.05),q.decay.quantile(.95))
    q["year_z"]=(q.Year-q.Year.mean())/q.Year.std(); q["is_z"]=(q.is_mean-q.is_mean.mean())/q.is_mean.std()
    cols={"year_z":q.year_z,"is_mean_z":q.is_z}
    if not equal_horizon: cols["log_pp_n"]=np.log(q.pp_n)
    x=sm.add_constant(pd.DataFrame(cols)); r=sm.OLS(q.decay,x).fit(cov_type="HC3")
    return q,pd.DataFrame({"term":x.columns,"coef":r.params,"se":r.bse,"t":r.tvalues})

def main():
    z=load(); outs=[]
    specs=[("primary",{}),("R1_winsor",{"winsor":True}),("R2_clear",{"clear":True}),("R3_floor20",{"floor":.20})]
    for name,kw in specs:
        q,t=reg(z,**kw); t.insert(0,"spec",name); outs.append(t)
    q60,t60=reg(load(True),equal_horizon=True); t60.insert(0,"spec","R4_first60"); outs.append(t60)
    regs=pd.concat(outs); regs.to_csv(OUT/"regressions.csv",index=False)
    q,_=reg(z); q["cohort"]=pd.cut(q.Year,[-np.inf,1989,2000,np.inf],labels=["through_1989","1990_2000","2001_plus"])
    ct=q.groupby("cohort",observed=True).agg(n=("decay","size"),is_mean=("is_mean","mean"),pp_mean=("pp_mean","mean"),decay=("decay","mean"),pp_months=("pp_n","mean"),decay_sd=("decay","std")); ct.to_csv(OUT/"cohorts.csv")
    a=q[q.cohort=="through_1989"].decay; b=q[q.cohort=="2001_plus"].decay; diff=b.mean()-a.mean(); se=np.sqrt(a.var()/len(a)+b.var()/len(b)); pd.DataFrame([{"newest_minus_oldest":diff,"se":se,"t":diff/se}]).to_csv(OUT/"cohort_contrast.csv",index=False)
    q.to_csv(OUT/"predictors.csv"); print(regs.round(3).to_string(index=False)); print("\nCohorts\n",ct.round(3)); print("\nContrast",round(diff,3),round(se,3),round(diff/se,3))

if __name__=="__main__":main()
