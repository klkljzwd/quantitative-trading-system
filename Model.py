import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingRegressor,HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression,RidgeCV,Lasso,Ridge
from xgboost import XGBRegressor,XGBClassifier
from lightgbm import LGBMRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
class Model:
    def __init__(self) -> None:
        pass
    def gradientBoosting(self,stock,date):
        #训练集
        train_data = stock[stock['date']<date].iloc[:,3:-1].values
        train_label = stock[stock['date']<date]['exrtn1'].values
        test_data = stock[stock['date']>=date].iloc[:,3:-1].values
        real_data = stock[stock['date']>=date][['code','date','exrtn1']]
        model = Ridge()
        fitted_model = model.fit(train_data,train_label)
        pre = fitted_model.predict(test_data)
        return pre,real_data
        # plt.plot(pre,label='pre')
        # plt.plot(real_data,label='real')
        # plt.legend()
        # plt.show()






