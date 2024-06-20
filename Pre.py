import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
with open("pre_result.pkl","rb") as f:
    pre_result = pickle.load(f)

date_list = pre_result[0]['date'].values
r_list = []
r_list2 = []
r_list3 = []
r_list4 = []
r_list5 = []
sum_r1 = 1
sum_list1 =[1]
sum_r2 = 1
sum_list2 =[1]
sum_r3 = 1
sum_list3 =[1]
sum_r4 = 1
sum_list4 =[1]
sum_r5 = 1
sum_list5 =[1]
sum_r_whole = 1
sum_r_whole_list = [1]
def get_r(current_pd):
    l1 = int((len(current_pd)*0.2))
    l2 = int((len(current_pd)*0.4))
    l3 = int((len(current_pd)*0.6))
    l4 = int((len(current_pd)*0.8))
    l5 = int((len(current_pd)*1))
    r1 = np.sum(current_pd.iloc[0:l1,1])/len(current_pd.iloc[0:l1])
    r2 = np.sum(current_pd.iloc[l1:l2,1])/len(current_pd.iloc[l1:l2])
    r3 = np.sum(current_pd.iloc[l2:l3,1])/len(current_pd.iloc[l2:l3])
    r4 = np.sum(current_pd.iloc[l3:l4,1])/len(current_pd.iloc[l3:l4])
    r5 = np.sum(current_pd.iloc[l4:l5,1])/len(current_pd.iloc[l4:l5])
    return r1,r2,r3,r4,r5
    


for i in range(len(date_list)):
    date = date_list[i]
    current_s = []
    for stock in pre_result:
        if date not in list(stock['date']):
            continue
        current_s.append(stock[stock['date']==date])
    current_pd = pd.DataFrame()
    code_list = []
    real_list = []
    pre_list =[]
    for c in current_s:
        code_list.append(c['code'].item())
        real_list.append(c['realexr1'].item())
        pre_list.append(c['preexr1'].item())
    current_pd['code'] = pd.Series(code_list)
    current_pd['real'] = pd.Series(real_list)
    current_pd['pre'] = pd.Series(pre_list)
    #按照pre排序
    current_pd.sort_values(by='pre',inplace=True,ascending=False)
    
    
    r1,r2,r3,r4,r5 = get_r(current_pd)         
    r_whole = np.sum(current_pd.loc[:,'real'])/len(current_pd)
    sum_r_whole*=(1+r_whole)
    sum_r1*=(1+r1)
    sum_list1.append(sum_r1)
    sum_r2*=(1+r2)
    sum_list2.append(sum_r2)
    sum_r3*=(1+r3)
    sum_list3.append(sum_r3)
    sum_r4*=(1+r4)
    sum_list4.append(sum_r4)
    sum_r5*=(1+r5)
    sum_list5.append(sum_r5)
    sum_r_whole_list.append(sum_r_whole)
    r_list.append(r1)
    r_list2.append(r2)
    r_list3.append(r3)
    r_list4.append(r4)
    r_list5.append(r5)

print(np.mean(r_list)/np.std(r_list)*np.sqrt(12))
print(np.mean(r_list2)/np.std(r_list2)*np.sqrt(12))
print(np.mean(r_list3)/np.std(r_list3)*np.sqrt(12))
print(np.mean(r_list4)/np.std(r_list4)*np.sqrt(12))
print(np.mean(r_list5)/np.std(r_list5)*np.sqrt(12))

plt.plot(date_list,sum_list1[:-1],label="1")
plt.plot(date_list,sum_list2[:-1],label="2")
plt.plot(date_list,sum_list3[:-1],label="3")
plt.plot(date_list,sum_list4[:-1],label="4")
plt.plot(date_list,sum_list5[:-1],label="5")
plt.plot(date_list,sum_r_whole_list[:-1],label="whole")
plt.xticks(date_list[::10])
plt.legend()
plt.show()

