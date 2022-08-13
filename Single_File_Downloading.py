import nsepy
import datetime
import pandas as pd 

#data, meta_data = ts.get_daily(symbol=EXCHANGE+':'+symbol,outputsize='full')

def histor(stockname):
    today = datetime.date.today()
    duration = 60
    start = today+datetime.timedelta(-duration)

    stockData = nsepy.get_history(symbol = stockname,start=start,end=today)
    return stockData

#Stock List Is the List Of Stocks for Which You Want to Download Data
# Sample Stock List Contains All FnO Stocks On NSE India   
#df=pd.read_csv("StockData.csv",engine='python')
 
#print("Downloading data of ",df.loc[i,"Symbol"])
try:
    dfstockdata=histor(stockname="FEDERALBNK")
    dfstockdata.to_csv("FEDERALBNK"+'.csv')
    print("Successfully downloaded data  of ","FEDERALBNK") 
except:
    print('Unable to Download data for ',"FEDERALBNK")
