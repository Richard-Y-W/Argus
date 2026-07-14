from pathlib import Path
import numpy as np, pandas as pd

OUT=Path(__file__).parent/'output.csv'; rng=np.random.default_rng(20260714); rows=[]
for run in range(1000):
    ret=rng.normal(0,1,1000); train,test=ret[:500],ret[500:]
    train_masks=rng.random((50,500))<.5; test_masks=rng.random((50,500))<.5
    train_means=np.array([train[m].mean() for m in train_masks]); chosen=train_means.argmax()
    rows.append({'run':run,'selected_train_mean':train_means[chosen],'selected_test_mean':test[test_masks[chosen]].mean(),'chosen_filter':chosen})
q=pd.DataFrame(rows);q.to_csv(OUT,index=False)
print(q[['selected_train_mean','selected_test_mean']].agg(['mean','std']).round(4).to_string())
print('positive train share',round((q.selected_train_mean>0).mean(),3),'positive test share',round((q.selected_test_mean>0).mean(),3))
