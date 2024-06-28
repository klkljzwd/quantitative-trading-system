import numpy as np
import pandas as pd
import pickle
class ReadData:
    def __init__(self,data_list) -> None:
        self.data_list = data_list
        self.cpi = pd.read_excel("data\RESSET_MACHINACPI_1.xls")
        self.ppi = pd.read_excel("data\RESSET_MAINDUPPI_1.xls")
    def read_data(self):
        data = pd.read_excel(self.data_list[0])
        for i in range(1,len(self.data_list)):
            d = pd.read_excel(self.data_list[i])
            data = pd.concat((data,d),axis=0)
        data.columns = ['code','name','date','price','trade','turn','amount','rtn','rf','pe','pb','eps','roe','naps']
        self.cpi.columns = ['date','cpi']
        self.ppi.columns = ['date','ppi']
        self.cpi['date'] = self.cpi['date'].dt.strftime("%Y%m")
        self.ppi['date'] = self.ppi['date'].dt.strftime("%Y%m")
        return data
    def data_clean(self,data):
        codes = np.unique(data['code'])
        stock_list = []
        for code in codes:
            stock = data[data['code']==code]
            stock['date'] = pd.to_datetime(stock['date'])
            stock['date'] = stock['date'].dt.strftime("%Y%m")
            #stock['rtn'] = np.log(stock['price']) - np.log(stock['price'].shift(1))
            stock['rtnn1'] = stock['rtn'].shift(-1)
            stock = pd.merge(left=stock,right=self.cpi,on='date',how='inner')
            stock = pd.merge(left=stock,right=self.ppi,on='date',how='inner')
            #计算因子
            stock['EP'] = stock['eps']/stock['price']
            stock['BM'] = stock['naps']/stock['price']
            stock['exrtn'] = stock['rtn'] - stock['rf']
            stock['exrtn1'] = stock['rtnn1'] - stock['rf']
            stock['size'] = np.log(stock['price']*stock['amount'])
            stock['MA'] = stock['price'].rolling(window=12).mean()
            stock['TMA'] = stock['MA'].rolling(window=12).mean()
            stock['MBI']=(stock['price']-stock['MA'])/stock['MA']
            stock['SK']=(stock['price']-stock['price'].rolling(window=12).min())/(stock['price'].rolling(window=12).max()-stock['price'].rolling(window=12).min())
            stock['SD']=stock['SK'].rolling(window=3).mean()
            stock['PSY']=(stock['exrtn']>0).rolling(window=12).mean()
            stock['MA112'] = stock['price']>stock['price'].rolling(window=12).mean()
            stock['MOM3'] = stock['rtn'].rolling(window=3).sum()
            stock['REV12'] = stock['rtn'].shift(12)
            if len(stock)<150:
                continue
            stock = stock[['code','name','date','pe','pb','exrtn','size','MA','TMA','MBI','SK','SD','PSY','cpi','ppi','turn','MA112','MOM3','REV12','exrtn1']]
            stock.sort_values(by='date',inplace=True)
            stock.dropna(inplace=True)
            stock_list.append(stock)
        with open("stocks.pkl","wb") as f:
            pickle.dump(stock_list,f)
        return stock_list
    
    
    
            