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
            stock['rtnn1'] = stock['rtn'].shift(-1)
            stock = pd.merge(left=stock,right=self.cpi,on='date',how='inner')
            stock = pd.merge(left=stock,right=self.ppi,on='date',how='inner')
            #计算因子
            stock['VOL'] = stock['trade']
            stock['PE'] = stock['pe']
            stock['TURN'] = stock['turn']
            stock['PB'] = stock['pb']
            stock['EPS'] =stock['eps']
            stock['ROE'] = stock['roe']
            stock['NAPS'] = stock['naps']
            stock['EXRET']  =stock['rtn']-stock['rf']
            stock['MA'] = stock['rtn'].rolling(window=3).sum()
            stock['TMA'] = stock['MA'].rolling(window=3).mean()
            stock['MBI']=(stock['price']-stock['MA'])/stock['MA'] 
            stock['SK']=(stock['price']-stock['price'].rolling(window=12).min())/(stock['price'].rolling(window=12).max()-stock['price'].rolling(window=12).min())
            stock['SD']=stock['SK'].rolling(window=3).mean()
            stock['PSY']=(stock['rtn']>0).rolling(window=12).mean()
            stock['CPI'] = stock['cpi']
            stock['PPI'] = stock['ppi']
            stock['exrtn1'] = stock['rtnn1'] - stock['rf']
            stock['size'] = stock['price']*stock['amount']
            if len(stock)<150:
                continue
            stock = stock[['code','name','date','size','VOL','PE','TURN','PB','EPS','ROE','NAPS','EXRET','MA','TMA','MBI','SK','SD','PSY','CPI','PPI','exrtn1']]
            stock.sort_values(by='date',inplace=True)
            stock.dropna(inplace=True)
            stock_list.append(stock)
        with open("stocks.pkl","wb") as f:
            pickle.dump(stock_list,f)
        return stock_list
    
    
    
            