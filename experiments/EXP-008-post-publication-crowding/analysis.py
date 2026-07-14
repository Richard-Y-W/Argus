from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm
ROOT=Path(__file__).resolve().parents[2]; RAW=ROOT/'datasets'/'raw'; OUT=Path(__file__).parent/'results'; OUT.mkdir(exist_ok=True)

def load():
 d=pd.read_csv(RAW/'SignalDoc.csv'); d=d.dropna(subset=['Year']); pdx=d[(d['Cat.Signal']=='Predictor')&d['Predictability in OP'].isin(['1_clear','2_likely'])].set_index('Acronym'); plx=d[d['Cat.Signal']=='Placebo'].set_index('Acronym')
 def ports(file,names):
  x=pd.read_parquet(RAW/file); x=x[x.port=='LS'].copy(); x['date']=pd.to_datetime(x.date).dt.to_period('M').dt.to_timestamp(); x=x[x.date<='2024-12-01']; return x[x.signalname.isin(names)].pivot(index='date',columns='signalname',values='ret')
 return pdx,plx,ports('PredictorPortsFull.parquet',pdx.index),ports('PlaceboPortsFull.parquet',plx.index)

def changes(targets,meta,pred,pm,months=60,need=36):
 rows=[]
 for name in targets.columns:
  pub=int(meta.loc[name,'Year']); prior=meta.index[meta.Year<pub]; x=pred.reindex(columns=prior)
  comp=x.where(x.notna().sum(axis=1)>=5).mean(axis=1); s=targets[name]
  cut=pd.Timestamp(pub,12,1); pre=pd.concat([s,comp],axis=1).loc[cut-pd.DateOffset(months=months):cut-pd.DateOffset(months=1)].dropna(); post=pd.concat([s,comp],axis=1).loc[cut+pd.DateOffset(months=1):cut+pd.DateOffset(months=months)].dropna()
  if len(pre)>=need and len(post)>=need: rows.append({'signalname':name,'pre_corr':pre.iloc[:,0].corr(pre.iloc[:,1]),'post_corr':post.iloc[:,0].corr(post.iloc[:,1]),'pre_n':len(pre),'post_n':len(post)})
 q=pd.DataFrame(rows,columns=['signalname','pre_corr','post_corr','pre_n','post_n']); q['change']=q.post_corr-q.pre_corr; return q

def summarize(q,label):
 if q.empty:return {'group':label,'n':0,'mean_change':np.nan,'se':np.nan,'t':np.nan,'positive_share':np.nan}
 r=sm.OLS(q.change,np.ones((len(q),1))).fit(cov_type='HC3'); return {'group':label,'n':len(q),'mean_change':r.params.iloc[0],'se':r.bse.iloc[0],'t':r.tvalues.iloc[0],'positive_share':(q.change>0).mean()}
def main():
 pdx,plx,pred,plac=load(); tables=[]
 for m,n in [(60,36),(120,60)]:
  a=changes(pred,pdx,pred,pdx,m,n); b=changes(plac,plx,pred,pdx,m,n); a.to_csv(OUT/f'predictors_{m}m.csv',index=False); b.to_csv(OUT/f'placebos_{m}m.csv',index=False)
  sa=summarize(a,f'predictors_{m}m'); sb=summarize(b,f'placebos_{m}m'); diff=sa['mean_change']-sb['mean_change']; se=np.sqrt(sa['se']**2+sb['se']**2); tables += [sa,sb,{'group':f'difference_{m}m','n':min(len(a),len(b)),'mean_change':diff,'se':se,'t':diff/se,'positive_share':np.nan}]
 out=pd.DataFrame(tables); out.to_csv(OUT/'summary.csv',index=False); print(out.round(3).to_string(index=False))
if __name__=='__main__': main()
