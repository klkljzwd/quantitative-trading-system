import pandas as pd
import numpy as np
from ReadData import * 
from Model import *
import pickle

with open("stocks.pkl","rb") as f:
    stock_list = pickle.load(f)
print(len(stock_list))
print(stock_list[0])
model = Model()
sum = 0
pre_result = []
for i in range(len(stock_list)):
    try:
        pre,real_data = model.gradientBoosting(stock_list[i],'202101')
        pre_data = pd.DataFrame()
        pre_data['code'] = real_data['code']
        pre_data['date'] = real_data['date']
        pre_data['realexr1'] = real_data['exrtn1']
        pre_data['preexr1'] = pre
        pre_result.append(pre_data)
        print(i)
    except:
        print("训练数据不足")
with open("pre_result.pkl","wb") as f:
    pickle.dump(pre_result,f)



