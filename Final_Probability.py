import ta
import pandas as pd 
import datetime  
import os
#import numpy as np

#dates = pd.date_range('16/6/2020',periods = 90)
#df = pd.DataFrame(np.random.randint(200,300,(90,4)),index = dates, columns = ['Open','High','Low','close'])
Final_buy_list=[]
Final_sell_list=[]
q=0
    #File reading
dfs=pd.read_csv("Small_Cap_50.csv",engine='python')
#print(dfs)
path='C:\\Users\\Acer\\Desktop\\Project_1\\Stock_files\\'
for i in range(len(dfs)) : 
    if(len(pd.read_csv(os.path.join(path,dfs.loc[i,"Symbol"]+'.csv'),engine='python'))==44):
        #print("Downloading data of ",df.loc[i,"Symbol"])   
        df = pd.read_csv(os.path.join(path,dfs.loc[i,"Symbol"]+'.csv'),engine='python')

        #print("you are in the loop")
        #MACD
        indicator_macd = ta.trend.MACD(df['Close'], 26,  12, 9,False)
        df['macd_line']        = indicator_macd.macd()
        df['macd_signal_line'] = indicator_macd.macd_signal()
        df['histogram']        = indicator_macd.macd_diff()
        n = len(df)

        a = df.histogram[n-1]
        b = df.histogram[n-2]
        c = df.histogram[n-3]

        #print(a,b)

        if((a>0 and b>0 and c>0) and (a-b > b-c)):
            if(b>c):
                macd_prob_buy = 20 
            else:
                macd_prob_buy = 15   

        elif((a>0 and b>0 and c>0) and (b-c > b-a) and (b>a)):
            macd_prob_buy = 13

        elif(a>0 and b>0 and c<0):
            if(a>b):
                macd_prob_buy = 20
            else:
                macd_prob_buy = 12 

        else :
            macd_prob_buy = 5
        
        if((a<0 and b<0 and c<0) and (b-a > c-b)):
            if(b<c):
                macd_prob_sell = 20 
            else:
                macd_prob_sell = 15  

        elif((a<0 and b<0 and c<0) and (b-c < b-a) and (b<a)):
            macd_prob_sell = 13         

        elif(a<0 and b<0 and c>0):
            if(a<b):
                macd_prob_sell = 20
            else:
                macd_prob_sell = 12 

        else :
            macd_prob_sell = 5

        

        #Bollinger_Band Probability
        indicator_bb = ta.volatility.BollingerBands(df['Close'],15,2)

        df['mid'] = (((df['Close']-df['Open'])/2) + df['Open'])
        df['bb_bbm'] = indicator_bb.bollinger_mavg()
        df['bb_bbh'] = indicator_bb.bollinger_hband()
        df['bb_bbl'] = indicator_bb.bollinger_lband()
        df['bb_width'] = (df['bb_bbh'] - df['bb_bbl'])

        a = df.mid[n-1]
        b = df.mid[n-2]
        c = df.mid[n-3]
        

        if(a>b>c and (df.bb_width[n-1] > df.bb_width[n-3])):
            if(df.Open[n-1] > df.bb_bbh[n-1] or df.Close[n-1] > df.bb_bbh[n-1] or df.High[n-1] > df.bb_bbh[n-1]):
                bb_prob_buy = 20
            else :
                bb_prob_buy = 15

        elif((c>b and a>b and a>c) and (df.bb_width[n-1] > df.bb_width[n-3])) :
            bb_prob_buy= 12
        else:
            bb_prob_buy=5

        if(c>b>a and (df.bb_width[n-1] > df.bb_width[n-3])):
            if(df.Open[n-1] < df.bb_bbl[n-1] or df.Close[n-1] < df.bb_bbl[n-1] or df.Low[n-1] < df.bb_bbl[n-1]):
                bb_prob_sell = 20
            else :
                bb_prob_sell = 15  

        elif((c<b and a<b and a<c) and (df.bb_width[n-1] > df.bb_width[n-3])) :
            bb_prob_sell = 12
        else:
            bb_prob_sell = 5


        #EMA
        indicator_EMA_5period = ta.trend.EMAIndicator(df['Close'],5)
        indicator_EMA_8period = ta.trend.EMAIndicator(df['Close'],8)
        indicator_EMA_13period = ta.trend.EMAIndicator(df['Close'],13)

        df['mid']    = (df.Open + df.Close)/2
        df['ema_5']  = indicator_EMA_5period.ema_indicator()
        df['ema_8']  = indicator_EMA_8period.ema_indicator()
        df['ema_13']  = indicator_EMA_13period.ema_indicator()
        
        a = df.Open[n-1]
        b = df.Close[n-1]

        if( (a > df.ema_8[n-1]) and (b > df.ema_8[n-1])):
            if((a > df.ema_5[n-1]) and (b > df.ema_5[n-1])):
                ema_prob_buy = 20
            else :
                ema_prob_buy = 17

        elif((df.mid[n-1] > df.ema_8[n-1])) :
            if((df.mid[n-1] > df.ema_5[n-1])):
                ema_prob_buy = 18
            else :
                ema_prob_buy = 15 

        elif((df.mid[n-1] > df.ema_13[n-1]) and (df.mid[n-2] > df.ema_13[n-1]) and (df.mid[n-1] > df.mid[n-2])) :
            if((df.mid[n-1] > df.ema_8[n-1])):
                ema_prob_buy = 15
            else :
                ema_prob_buy = 12  

        else :
            ema_prob_buy = 5



        if( (a < df.ema_8[n-1]) and (b < df.ema_8[n-1])):
            if((a < df.ema_5[n-1]) and (b < df.ema_5[n-1])):
                ema_prob_sell = 20
            else :
                ema_prob_sell = 17

        elif((df.mid[n-1] < df.ema_8[n-1])) :
            if((df.mid[n-1] < df.ema_5[n-1])):
                ema_prob_sell = 18
            else :
                ema_prob_sell = 15 

        elif((df.mid[n-1] < df.ema_13[n-1]) and (df.mid[n-2] < df.ema_13[n-1]) and (df.mid[n-1] < df.mid[n-2])) :
            if((df.mid[n-1] < df.ema_8[n-1])):
                ema_prob_sell = 15
            else :
                ema_prob_sell = 12       

        else :
            ema_prob_sell = 5


        #Stochastic_RSI
        indicator_rsi = ta.momentum.rsi(df['Close'],14)

        df['rsi']   = indicator_rsi

        #l_rsi = tuple(df.rsi[-1] for i in range(-1:-6))
        if(df.rsi[n-1] > 0 and df.rsi[n-1] < 30):
            if((df.rsi[n-1]>0 and df.rsi[n-1]<25) and (df.rsi[n-1] > df.rsi[n-2] > df.rsi[n-3])):
                rsi_prob_buy = 20
            elif((df.rsi[n-1]>0 and df.rsi[n-1]<25) and (df.rsi[n-1] > df.rsi[n-2])):
                rsi_prob_buy = 18
            elif(df.rsi[n-1]>0 and df.rsi[n-1]<25):
                rsi_prob_buy = 15
            else:
                rsi_prob_buy = 15
        elif(df.rsi[n-1] > 30 and df.rsi[n-1] < 45):
            if(df.rsi[n-1] > df.rsi[n-2] > df.rsi[n-3]):
                rsi_prob_buy = 17
            if(df.rsi[n-1] > df.rsi[n-2]):
                rsi_prob_buy = 15
            else:
                rsi_prob_buy = 13
        else:
            rsi_prob_buy = 5


        if(df.rsi[n-1] > 70 and df.rsi[n-1] < 90):
            if((df.rsi[n-1]<90 and df.rsi[n-1]<65) and (df.rsi[n-1] < df.rsi[n-2] < df.rsi[n-3])):
                rsi_prob_sell = 20
            elif((df.rsi[n-1]<90 and df.rsi[n-1]<65) and (df.rsi[n-1] < df.rsi[n-2])):
                rsi_prob_sell = 18
            elif(df.rsi[n-1]<90 and df.rsi[n-1]<65):
                rsi_prob_sell = 16
            else:
                rsi_prob_sell = 15
        elif(df.rsi[n-1] < 70 and df.rsi[n-1] > 45):
            if(df.rsi[n-1] < df.rsi[n-2] < df.rsi[n-3]):
                rsi_prob_sell = 17
            if(df.rsi[n-1] < df.rsi[n-2]):
                rsi_prob_sell = 15
            else:
                rsi_prob_sell = 13
        else:
            rsi_prob_sell = 5


        #Vortex
        indicator_vortex_pos= ta.trend.vortex_indicator_pos(df['High'],df['Low'],df['Close'],5)
        indicator_vortex_neg = ta.trend.vortex_indicator_neg(df['High'],df['Low'],df['Close'],5)

        df['pos_line'] = indicator_vortex_pos
        df['neg_line'] = indicator_vortex_neg

        l_pos = [df.pos_line[n-1-i] for i in range(0,3)]
        l_neg = [df.neg_line[n-1-i] for i in range(0,3)]

        if((l_pos[0]>1 and l_pos[1]>1 and l_pos[2]>1) and (l_neg[0]<1 and l_neg[1]<1 and l_neg[2]<1)):
            if((l_pos[0]>l_pos[1]>l_pos[2]) and(l_neg[0]<l_neg[1]<l_neg[2])):
                vortex_prob_buy = 20
            elif((l_pos[0]>l_pos[1]) and(l_neg[0]<l_neg[1])):
                vortex_prob_buy = 15
            else:
                vortex_prob_buy = 12   

        elif((l_pos[0]>l_pos[1]>l_pos[2]) and(l_neg[0]<l_neg[1]<l_neg[2])):
            vortex_prob_buy = 18    
        else:
            vortex_prob_buy = 5


        if((l_neg[0]>1 and l_neg[1]>1 and l_neg[2]>1) and (l_pos[0]<1 and l_pos[1]<1 and l_pos[2]<1)):
            if((l_neg[0]>l_neg[1]>l_neg[2]) and(l_pos[0]<l_pos[1]<l_pos[2])):
                vortex_prob_sell = 20
            elif((l_neg[0]>l_neg[1]) and(l_pos[0]<l_pos[1])):
                vortex_prob_sell = 15
            else:
                vortex_prob_sell = 12   

        elif((l_neg[0]>l_neg[1]>l_neg[2]) and(l_pos[0]<l_pos[1]<l_pos[2])):
            vortex_prob_sell = 18    
        else:
            vortex_prob_sell = 5

        Final_prob_buy = macd_prob_buy + bb_prob_buy + ema_prob_buy + rsi_prob_buy + vortex_prob_buy
        Final_prob_sell = macd_prob_sell + bb_prob_sell + ema_prob_sell + rsi_prob_sell + vortex_prob_sell

        #file_buy=open("Final_list_buy.txt",'a')
        #file_sell=open("Final_list_sell.txt",'a')

        #print(Final_prob_buy)
        #print(Final_sell_list)

        #print(Final_prob_buy , Final_prob_sell)
        if(Final_prob_buy > 62):
            #file_buy.write(dfs.loc[i,"Symbol"])
            #file_buy.write("\n")
            Final_buy_list.append(dfs.loc[i,"Symbol"])
        
        if(Final_prob_sell > 62):
            #file_sell.write(dfs.loc[i,"Symbol"])
            #file_sell.write("\n")
            Final_sell_list.append(dfs.loc[i,"Symbol"])


    
#file_buy.close()
#file_sell.close()
Final_df = pd.DataFrame({'Buy':pd.Series(Final_buy_list),'Sell':pd.Series(Final_sell_list)})
print(Final_df)
Final_df.to_csv('Final_list.csv')
