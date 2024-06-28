import pickle
import pandas as pd
import numpy as np

with open("stocks.pkl","rb") as f:
    stocks = pickle.load(f)
print(stocks[0])

    