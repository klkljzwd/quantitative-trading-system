import pandas as pd
import numpy as np
from ReadData import * 
from Model import *
import pickle

f = []
for i in range(1,6):
    f.append("data/RESSET_MRESSTK_"+str(i)+".xls")
readData = ReadData(f)
data = readData.read_data()
stock_list = readData.data_clean(data)