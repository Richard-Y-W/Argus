from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm
ROOT=Path(__file__).resolve().parents[2]; RAW=ROOT/'datasets'/'raw'; OUT=Path(__file__).parent/'results'; OUT.mkdir(exist_ok=True)
def load():
 d=pd.read_csv(RAW/'SignalDoc.csv'); d=d[(d['Cat.Signal']=='Predictor')&d['Predictability in OP'].isin(['1_clear','2_likely'])&d[['SampleStartYear','SampleEndYear','Year']].notna().all(axis=1)]
 p=pd.read_parquet(RAW/'PredictorPortsFull.parquet'); p=p[p.port=='LS'].copy(); p['date']=pd.to_datetime(p.date); p=p[p.date<='2024-12-31']; q=p.merge(d[['Acronym','Predictability in OP','SampleStartYear','SampleEndYear','Year','Stock Weight']],left_on='signalname',right_on='Acronym'); y=q.date.dt.year; q['window']=np.select([y<q.SampleStartYear,y<=q.SampleEndYear,y<=q.Year],['pre','in_sample','post_sample'],default='post_pub'); q=q[q.window!='pre']; c=q.pivot_table(index='signalname',columns='window',values='ret',aggfunc='count').fillna(0); keep=c.index[(c.get('in_sample',0)>=12)&(c.get('post_pub',0)>=12)]; q=q[q.signalname.isin(keep)]
 w=q.pivot_table(index='signalname',columns='window',values='ret',aggfunc=['mean','count']); z=pd.DataFrame(index=w.index); z['is_mean']=w[('mean','in_sample')];z['pp_mean']=w[('mean','post_pub')];z['pp_n']=w[('count','post_pub')]; z=z.join(q.groupby('signalname')[['Year','Stock Weight','Predictability in OP']].first()); z=z[(z.is_mean>.10)&z['Stock Weight'].isin(['EW','VW'])].dropna();z['decay']=(z.is_mean-z.pp_mean)/z.is_mean;z['vw']=(z['Stock Weight']=='VW').astype(float); return z
def reg(z,outcome,label,winsor=False,clear=False):
 q=z.copy();
 if winsor:q[outcome]=q[outcome].clip(q[outcome].quantile(.05),q[outcome].quantile(.95))
 if clear:q=q[q['Predictability in OP']=='1_clear']
 for v in ['is_mean','Year']:q[v+'_z']=(q[v]-q[v].mean())/q[v].std()
 x=sm.add_constant(pd.DataFrame({'vw':q.vw,'is_mean_z':q.is_mean_z,'year_z':q.Year_z,'log_pp_n':np.log(q.pp_n)}));r=sm.OLS(q[outcome],x).fit(cov_type='HC3');return pd.DataFrame({'spec':label,'term':r.params.index,'coef':r.params.values,'se':r.bse.values,'t':r.tvalues.values,'n':len(q)})
def main():
 z=load(); tabs=[reg(z,'decay','primary'),reg(z,'pp_mean','secondary_pp_mean'),reg(z,'decay','R1_winsor',True),reg(z,'decay','R2_clear',False,True)];pd.concat(tabs).to_csv(OUT/'regressions.csv',index=False);g=z.groupby('Stock Weight').agg(n=('decay','size'),is_mean=('is_mean','mean'),pp_mean=('pp_mean','mean'),decay=('decay','mean'));g.to_csv(OUT/'groups.csv');z.to_csv(OUT/'predictors.csv');print(pd.concat(tabs).round(3).to_string(index=False));print(g.round(3))
if __name__=='__main__':main()
