import pickle
import pandas as pd
import numpy as np

with open("stocks.pkl","rb") as f:
    stocks = pickle.load(f)
avg_size_dict= {}
for s in stocks:
    #计算平均市值
    avg_size = np.mean(s['size'])
    avg_size_dict[avg_size] = s
avg_size_dict_item = avg_size_dict.items()
avg_size_dict_item = sorted(avg_size_dict_item,key=lambda x:x[0],reverse=True)

def get_all():
    return stocks
def get_big():
    stocks = []
    for i in range(int(len(avg_size_dict_item)*0.3)):
        stocks.append(avg_size_dict_item[i][1])
    return stocks

def get_small():
    stocks = []
    for i in range(int(len(avg_size_dict_item)*0.7),int(len(avg_size_dict_item))):
        stocks.append(avg_size_dict_item[i][1])
    return stocks

def get_mid():
    stocks = []
    for i in range(int(len(avg_size_dict_item)*0.3),int(len(avg_size_dict_item)*0.7)):
        stocks.append(avg_size_dict_item[i][1])
    return stocks

