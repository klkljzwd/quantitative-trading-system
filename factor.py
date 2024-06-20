import pandas as pd
import numpy as np
from scipy.stats import norm
import pickle

with open("stocks.pkl","rb") as f:
    s = pickle.load(f)

data = pd.DataFrame()
for i in s:
    data=pd.concat((data,i))
dates=np.unique(data['date'])

factors=['EP', 'BM', 'exrtn', 'size', 'MA112', 'roe', 'turn', 'MBI']

for factor in factors:
    Q=np.zeros((1,5))
    for i in range(1,len(dates)):
        tmp1=data[data['date']==dates[i-1]]
        tmp1=tmp1.sort_values(by=factor,ignore_index=True)
        tmp2=data[data['date']==dates[i]]
        indices=np.linspace(0,len(tmp1),6,dtype=int)
        Q_tmp=np.zeros((1,5))
        for i in range(5):
            group=tmp1.loc[indices[i]:indices[i+1]]['code']
            ans=pd.merge(left=group,right=tmp2,on='code',how='inner')
            Q_tmp[0][i]=ans['exrtn'].mean()
        Q=np.concatenate((Q,Q_tmp),axis=0)
    Q=Q[1:,:]
    Q_ans=Q.mean(axis=0)*100
    print(factor)
    for i in range(5):
        print("Q{}: {:.4f}%".format(i+1,Q_ans[i]),end=' ')
    print()
    print("Q5-Q1: {:.4f}%".format(Q_ans[4]-Q_ans[0]))
    print("Q5>Q1: {:.4f}%".format(np.mean(Q[:,4]>Q[:,0])*100))
    RH=Q[:,4]
    RL=Q[:,0]
    T=Q.shape[0]
    sH=RH.std(ddof=1)
    sL=RL.std(ddof=1)
    sH_L=np.sqrt(sH**2/T+sL**2/T)
    t=(RH.mean()-RL.mean())/sH_L
    p=2-2*norm.cdf(np.abs(t))
    print("t: {:.4f} p-value: {:.4f}".format(t,p))
