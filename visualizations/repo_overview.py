"""Generate README figures entirely from committed experiment outputs."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).parent/"generated";OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"figure.dpi":160})

# Figure 1: core three-window replication with placebo comparison
p=pd.read_csv(ROOT/'experiments/EXP-002-placebo-decay/results/window_level_by_group.csv');p=p[p.group.isin(['predictor','placebo_all'])]
order=['in_sample','post_sample','post_pub'];labels=['In sample','Post-sample','Post-publication'];colors={'predictor':'#2563eb','placebo_all':'#94a3b8'}
fig,ax=plt.subplots(figsize=(7.2,4.2));x=np.arange(3);width=.34
for i,g in enumerate(['predictor','placebo_all']):
 q=p[p.group==g].set_index('window').reindex(order);ax.bar(x+(i-.5)*width,q['mean'],width,yerr=q['se'],capsize=3,label='Published predictors' if g=='predictor' else 'Published placebos',color=colors[g])
ax.axhline(0,color='black',lw=.7);ax.set_xticks(x,labels);ax.set_ylabel('Mean long–short return (% per month)');ax.set_title('Publication decay is concentrated in claimed predictors');ax.legend(frameon=False);fig.tight_layout();fig.savefig(OUT/'publication_decay.png',bbox_inches='tight');plt.close(fig)

# Figure 2: experiment verdict history. Keep every ID explicit so omissions are visible in review.
verdicts={1:'Supported',2:'Supported',3:'Partial',4:'Rejected',5:'Rejected',6:'Rejected',7:'Inconclusive',8:'Rejected',9:'Rejected',10:'Rejected',11:'Supported',12:'Supported',13:'Rejected',14:'Rejected',15:'Supported',16:'Rejected'}
palette={'Supported':'#15803d','Partial':'#ca8a04','Rejected':'#b91c1c','Inconclusive':'#64748b'}
fig,ax=plt.subplots(figsize=(9.8,2.6));ids=np.array(list(verdicts));labels=list(verdicts.values())
ax.scatter(ids,[1]*len(ids),s=260,c=[palette[v] for v in labels],edgecolor='white',linewidth=1.5)
for i,v in verdicts.items():ax.text(i,1.0,str(i),ha='center',va='center',color='white',weight='bold',fontsize=8);ax.text(i,.91,v,ha='center',va='top',rotation=35,fontsize=8)
counts=pd.Series(labels).value_counts();summary=' · '.join(f'{k}: {counts.get(k,0)}' for k in ['Supported','Partial','Inconclusive','Rejected'])
ax.set_xlim(.4,16.6);ax.set_ylim(.76,1.17);ax.set_yticks([]);ax.set_xticks([]);ax.spines['left'].set_visible(False);ax.spines['bottom'].set_visible(False);ax.set_title(f'Sixteen preregistered experiments — {summary}');fig.tight_layout();fig.savefig(OUT/'experiment_verdicts.png',bbox_inches='tight');plt.close(fig)

# Figure 3: raw versus adjusted VW association
groups=pd.read_csv(ROOT/'experiments/EXP-009-weighting-and-decay/results/groups.csv').set_index('Stock Weight');regs=pd.read_csv(ROOT/'experiments/EXP-009-weighting-and-decay/results/regressions.csv');adj=regs[(regs.spec=='primary')&(regs.term=='vw')].iloc[0]
fig,ax=plt.subplots(figsize=(6.6,4));raw=(groups.loc['VW','decay']-groups.loc['EW','decay'])*100;vals=[raw,adj.coef*100];errs=[0,adj.se*100]
ax.bar(['Raw VW−EW gap','Adjusted VW coefficient'],vals,yerr=errs,capsize=4,color=['#f59e0b','#475569']);ax.axhline(0,color='black',lw=.7);ax.set_ylabel('Difference in proportional decay (percentage points)');ax.set_title('The striking weighting gap does not survive controls');ax.text(1,vals[1]+errs[1]+3,f't = {adj.t:.2f}',ha='center');fig.tight_layout();fig.savefig(OUT/'weighting_gap.png',bbox_inches='tight');plt.close(fig)
