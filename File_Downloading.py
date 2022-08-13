import nsepy
import datetime
import pandas as pd 
import os

#data, meta_data = ts.get_daily(symbol=EXCHANGE+':'+symbol,outputsize='full')

def histor(stockname):
    today = datetime.date.today()
    print(today)
    duration = 60
    start = today+datetime.timedelta(-duration)

    stockData = nsepy.get_history(symbol = stockname,start=start,end=today)
    return stockData

#Stock List Is the List Of Stocks for Which You Want to Download Data
# Sample Stock List Contains All FnO Stocks On NSE India   
df=pd.read_csv("Small_Cap_50.csv",engine='python')
for i in range(len(df)) :  
    print("Downloading data of ",df.loc[i,"Symbol"])
    try:
        dfstockdata=histor(stockname=df.loc[i,'Symbol'])
        #print(df.loc[i,"Symbol"])
        path='C:\\Users\\Acer\\Desktop\\Project_1\\Stock_files\\'
        dfstockdata.to_csv(os.path.join(path,df.loc[i,"Symbol"]+'.csv'))
        print("Successfully downloaded data  of ",df.loc[i,"Symbol"]) 
    except:
        print('Unable to Download data for ',df.loc[i,'Symbol'])

