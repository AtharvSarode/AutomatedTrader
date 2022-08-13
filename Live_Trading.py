import pandas as pd
import yfinance as yf
import ta
from time import sleep
import datetime

Total_balance = 50000

j=0
#Stocks_list = []
#Portfolio = {""" Stock_name : Stock_status """}
buy_key = 0


def Buy(price,quantity):
    global Total_balance
    Total_balance = Total_balance - (price*quantity) - other_taxes(price,quantity,"Buy")
    print(Total_balance)
    print(other_taxes(price,quantity,"Buy"))
    print(Total_balance)
    #Buy the stock

def Sell(price,quantity):
    global Total_balance
    Total_balance = Total_balance + price*quantity - other_taxes(price,quantity,"Sell")
    print(Total_balance)
    print(other_taxes(price,quantity,"Sell"))
    print(Total_balance)
    #Sell the stock

def other_taxes(price,quantity,status):
    Net_price = price*quantity
    if(status == "Buy"):
        if((Net_price*0.05)/100 > 20) :
            tax = ((0.00345+0.003+0.05)/100)*Net_price + (18/100)*(((0.05+0.00345)/100)*Net_price)
            #print(((0.00345+0.003+0.05)/100)*Net_price , (18/100)*(((0.05+0.00345)/100)*Net_price))
        else:
            tax = 20 + ((0.00345+0.003)/100)*Net_price + (18/100)*(((0.00345)/100)*Net_price) + (18/100)*20
            #print(((0.00345+0.003+0.05)/100)*Net_price , (18/100)*((0.00345/100)*Net_price),(18/100)*20)
    else:
        if((Net_price*0.05)/100 > 20) :
            tax = ((0.00345+0.025+0.05)/100)*Net_price + (18/100)*(((0.05+0.00345)/100)*Net_price)
            #print(((0.00345+0.003+0.05)/100)*Net_price , (18/100)*(((0.05+0.00345)/100)*Net_price))
        else:
            tax = 20 + ((0.00345+0.025)/100)*Net_price + (18/100)*(((0.00345)/100)*Net_price) + (18/100)*20
            #print(((0.00345+0.003+0.05)/100)*Net_price , (18/100)*((0.00345/100)*Net_price),(18/100)*20)

    return tax

def candel(tick):
    if(tick["Open"]-tick["Close"]>0):
        return 0
    else:
        return 1

def rsi_indicator(data):
    #rsi = ta.momentum.RSIIndicator(data['Close'],n=14)
    j = len(data)
    rsi = ta.momentum.rsi(data['Close'],14)
    #print(rsi[-1])
    #print(rsi.iloc[j-1])
    """ if(rsi[-1]-rsi[-2] > 0):
        return 1
    else:
        return 0 """
    return (rsi[-1],rsi[-2])

i = 45

while(True):
    data = yf.download(tickers="PVR.NS",period="1d",interval="1m")
    #price = (data["Open"][-1] + data["Close"][-1])/2
    #print(pd.DataFrame(data)["Open"])
    #print(data.iloc[i].name)
    print(data.iloc[i].name,data.iloc[i]["Open"],data.iloc[i]["Close"])
    price = data["Close"][i]
    #print(price,+i+1)
    #print(price)
    #print(quantity)

    #For green candel = 1 and For red candel = 0
    key1 = candel(data.iloc[i])
    

    #Rsi_Indicator = ta.momentum.rsi(df['Close'],n=14)
    key2 = rsi_indicator(data.iloc[:i+1])[0] - rsi_indicator(data.iloc[:i+1])[1] > 0

    key3= rsi_indicator(data.iloc[:i+1])[0] < 40

    #print(key1,key2,key3)

    if(buy_key == 0):
        if(key1 and key2 and key3):
            quantity = int((Total_balance-10000)/price)
            print(quantity)
            Buy(price,quantity)
            buy_price = price
            buy_key = 1
            print("PVR is Buyed",price)

    elif(buy_key == 1):
        if(price - buy_price > 2.5):
            Sell(price,quantity)
            buy_key = 0
            print("PVR is Soled",price)
    i+=1
    #print(i)
    #print(str((datetime.datetime.now().hour)) + ":" + str((datetime.datetime.now().minute)),str(data.iloc[i].name)[10:16])
    if(j==0):
        if(str((datetime.datetime.now().hour)) + ":" + str((datetime.datetime.now().minute)) == str(data.iloc[i].name)[10:16]):
            sleep(datetime.datetime.now().second+1)
            j=1
    """ else:
        sleep(60) """











    