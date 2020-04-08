#!/usr/bin/env python
# coding: utf-8

# In[80]:


import os
import alpaca_trade_api as tradeapi
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Reset global variables
negative1=0
negative2=0
positive1=0
positive2=0
SellHalf=0
BoughtAtStock1=0
BoughtAtStock2=0
SoldAtStock1=0
SoldAtStock2=0
sold1=0
sold2=0

def pairs_trading_algo(self):
    global negative1
    global negative2
    global positive1
    global positive2
    global SellHalf
    global BoughtAtStock1
    global BoughtAtStock2
    global SoldAtStock1
    global SoldAtStock2
    global sold1
    global sold2

#Specify paper trading enviornment
    os.environ["APCA_API_BASE_URL"]=("https://paper-api.alpaca.markets")
#Insert API Credentials
    api=tradeapi.REST('PKIY4IASGVU5ABBO6QGH', '1EBDOv3enVBVQeYlVJfPMF1vzuTQqNQI5uagGxlQ', api_version='v2')
    account=api.get_account()
#Email return enviornment
    sender_address='mattalgotrader@gmail.com'
    sender_password='AlgoMJN10299'
    receiver_address='mjnealon@noctrl.edu'
#Setup the mime
    message=MIMEMultipart()
    message['From']=("Trading Bot")
    message['To']=receiver_address
    message['Subject']=("Your Trading Bot Has a Message:")
#Selection of stocks
    limit=1000
    stock1='JPM'
    stock2='BAC'
#Put historical data into variables
    stock1_barset=api.get_barset(stock1, '1Min', limit)
    stock2_barset=api.get_barset(stock2, '1Min', limit)
    stock1_bars=stock1_barset[stock1]
    stock2_bars=stock2_barset[stock2]
    data_1=[]
    times_1=[]
    for i in range(limit):
        stock1_close=stock1_bars[i].c
        stock1_time=stock1_bars[i].t
        data_1.append(stock1_close)
        times_1.append(stock1_time)
    data_2=[]
    times_2=[]
    for i in range(limit):
        stock2_close=stock2_bars[i].c
        stock2_time=stock2_bars[i].t
        data_2.append(stock2_close)
        times_2.append(stock2_time)
#Putting them together
    hist_close=pd.DataFrame(data_1, columns=[stock1])
    hist_close[stock2]=data_2
#Moving average 13
    move_avg_minutes1=13
#Moving average for stock 1
    stock1_last13=[]
    for i in range(move_avg_minutes1):
        stock1_last13.append(data_1[(limit-1)-i])
    stock1_hist13=pd.DataFrame(stock1_last13)
    stock1_mavg13=stock1_hist13.mean()
#Moving average for stock 2
    stock2_last13=[]
    for i in range(move_avg_minutes1):
        stock2_last13.append(data_2[(limit-1)-i])
    stock2_hist13=pd.DataFrame(stock2_last13)
    stock2_mavg13=stock2_hist13.mean()
#Moving average 8
    move_avg_minutes2=8
#Moving average for stock 1
    stock1_last8=[]
    for i in range(move_avg_minutes2):
        stock1_last8.append(data_1[(limit-1)-i])
    stock1_hist8=pd.DataFrame(stock1_last8)
    stock1_mavg8=stock1_hist8.mean()
#Moving average for stock 2
    stock2_last8=[]
    for i in range(move_avg_minutes2):
        stock2_last8.append(data_2[(limit-1)-i])
    stock2_hist8=pd.DataFrame(stock2_last8)
    stock2_mavg8=stock2_hist8.mean()
#Moving average 5
    move_avg_minutes3=5
#Moving average for stock 1
    stock1_last5=[]
    for i in range(move_avg_minutes3):
        stock1_last5.append(data_1[(limit-1)-i])
    stock1_hist5=pd.DataFrame(stock1_last5)
    stock1_mavg5=stock1_hist5.mean()
#Moving average for stock 2
    stock2_last5=[]
    for i in range(move_avg_minutes3):
        stock2_last5.append(data_2[(limit-1)-i])
    stock2_hist5=pd.DataFrame(stock2_last5)
    stock2_mavg5=(stock2_hist5.mean())
#Calculation of shares to trade
    stock1_curr=data_1[limit-1]
    stock2_curr=data_2[limit-1]
    cash=float(account.buying_power)
    SpendPerTrade=(0.075*cash)
    SpendPerStock=SpendPerTrade//2
    limit_stock1=int(SpendPerStock//stock1_curr)
    limit_stock2=int(SpendPerStock//stock2_curr)
#Calculation of differnce:
    FiveOverEightStock1=min(stock1_mavg5-stock1_mavg8)
    FiveOverThirteenStock1=min(stock1_mavg5-stock1_mavg13)
    FiveOverEightStock2=min(stock2_mavg5-stock2_mavg8)
    FiveOverThirteenStock2=min(stock2_mavg5-stock2_mavg13)
    EightOverFiveStock1=min(stock1_mavg8-stock1_mavg5)
    ThirteenOverEightStock1=min(stock1_mavg13-stock1_mavg8)
    EightOverFiveStock2=min(stock2_mavg8-stock2_mavg5)
    ThirteenOverEightStock2=min(stock2_mavg13-stock2_mavg8)
    EightOverThirteenStock1=min(stock1_mavg8-stock1_mavg13)
    CurrOverThirteenStock1=min(stock1_curr-stock1_mavg13)
    EightOverThirteenStock2=min(stock2_mavg8-stock2_mavg13)
    CurrOverThirteenStock2=min(stock2_curr-stock2_mavg13)
#Actual trading algorithim
    portfolio=api.list_positions()
    try: 
        JPMShares=int(api.get_position('JPM').qty)
    except:
        JPMShares=0
    try:
        BACShares=int(api.get_position('BAC').qty)
    except:
        BACShares=0
    clock=api.get_clock()
    something=False
    mail_content=("")
    if clock.is_open==True:
#No shares of BAC try to buy
        if BACShares==0:
            negative2=0
            positive2=0
            BoughtAtStock2=0
            SoldAtStock2=0
            sold2=0
#5MAVG crossing 13MAVG and 8MAVG positive BAC
            if FiveOverEightStock2>=0 and FiveOverThirteenStock2>=0 and EightOverThirteenStock2>=0 and CurrOverThirteenStock2>=0: 
                BoughtAtStock2+=stock2_curr
                api.submit_order(symbol=stock2,qty=limit_stock2,side='buy',type='market',time_in_force='day', client_order_id='BAC_Positive'+str(BoughtAtStock2))
                positive2+=1
                mail_content=("Trades have been made, 5MAVG crossed 8MAVG and 13MAVG, positive trend, bought BAC")
                something=True
#5MAVG crossing 13MAVG and 8MAVG negative BAC
            elif FiveOverEightStock2<=0 and FiveOverThirteenStock2<=0 and EightOverThirteenStock2<=0 and CurrOverThirteenStock2<=0: 
                SoldAtStock2+=stock2_curr
                api.submit_order(symbol=stock2,qty=limit_stock2,side='sell',type='market',time_in_force='day', client_order_id='BAC_Negative'+str(SoldAtStock2))
                negative2+=1
                mail_content=("Trades have been made, 5MAVG crossed 8MAVG and 13MAVG, negative trend, sold BAC")
                something=True
#No shares of JPM try to buy
        if JPMShares==0:
            negative1=0
            positive1=0
            SellHalf=0
            BoughtAtStock1=0
            SoldAtStock1=0
            sold1=0
#5MAVG crossing 13MAVG and 8MAVG positive JPM
            if FiveOverEightStock1>=0 and FiveOverThirteenStock1>=0 and EightOverThirteenStock1>=0 and CurrOverThirteenStock1>=0:
                BoughtAtStock1+=stock1_curr
                api.submit_order(symbol=stock1,qty=limit_stock1,side='buy',type='market',time_in_force='day', client_order_id='JPM_Positive'+str(BoughtAtStock1))
                positive1+=1
                mail_content=("Trades have been made, 5MAVG crossed 8MAVG and 13MAVG, positive trend, bought JPM")
                something=True
#5MAVG crossing 13MAVG and 8MAVG negative JPM
            elif FiveOverEightStock1<=0 and FiveOverThirteenStock1<=0 and EightOverThirteenStock1<=0 and CurrOverThirteenStock1<=0:
                SoldAtStock1+=stock1_curr
                api.submit_order(symbol=stock1,qty=limit_stock1,side='sell',type='market',time_in_force='day', client_order_id='JPM_Negative'+str(SoldAtStock1))
                negative1+=1
                mail_content=("Trades have been made, 5MAVG crossed 8MAVG and 13MAVG, negative trend, sold JPM")
                something=True
        else:
            mail_content=("Nothing was bought")
#If you have BAC stock look to sell
        if BACShares!=0:
#Sell half when 8 crosses 5 BAC  
            if EightOverFiveStock2>=0 and positive2==1 and sold2==0:
                my_order = api.get_order_by_client_order_id('BAC_Positive'+str(BoughtAtStock2))
                SellHalf+=int(my_order.filled_qty)//2
                if SellHalf*2 != int(my_order.filled_qty):
                    api.submit_order(symbol=stock2,qty=(SellHalf+1),side='sell',type='market',time_in_force='day')
                    sold2+=1
                else:
                    api.submit_order(symbol=stock2,qty=SellHalf,side='sell',type='market',time_in_force='day')
                    sold2+=1
#Sell other half when 13 crosses both
            if EightOverFiveStock2>=0 and ThirteenOverEightStock2>=0 and positive2==1:
                api.submit_order(symbol=stock2,qty=SellHalf,side='sell',type='market',time_in_force='day')
                sold2=0
                mail_content=("Trades have been made, 13MAVG crossed 8MAVG and 5MAVG, positive gain, sold BAC")
                something=True
#Buy half when 8 crosses 5 BAC
            if FiveOverEightStock2>=0 and negative2==1 and sold2==0:
                my_order = api.get_order_by_client_order_id('BAC_Negative'+str(SoldAtStock2))
                SellHalf+=int(my_order.filled_qty)//2
                if SellHalf*2 != int(my_order.filled_qty):
                    api.submit_order(symbol=stock2,qty=(SellHalf+1),side='buy',type='market',time_in_force='day')
                    sold2+=1
                else:
                    api.submit_order(symbol=stock2,qty=SellHalf,side='buy',type='market',time_in_force='day')
                    sold2+=1
#Buy other half when 13 crosses both
            if FiveOverEightStock2>=0 and EightOverThirteenStock2>=0 and negative2==1:
                api.submit_order(symbol=stock2,qty=SellHalf,side='buy',type='market',time_in_force='day')
                sold2=0
                mail_content=("Trades have been made, 13MAVG crossed 8MAVG and 5MAVG, positive short, bought BAC")
                something=True
#If you have JPM stock look to sell
        if JPMShares!=0:
#Sell half when 8 crosses 5 JPM
            if EightOverFiveStock1>=0 and positive1==1 and sold1==0:
                my_order = api.get_order_by_client_order_id('JPM_Positive'+str(BoughtAtStock1))
                SellHalf+=int(my_order.filled_qty)//2
                if SellHalf*2 != int(my_order.filled_qty):
                    api.submit_order(symbol=stock1,qty=(SellHalf+1),side='sell',type='market',time_in_force='day')
                    sold1+=1
                else:
                    api.submit_order(symbol=stock1,qty=(SellHalf),side='sell',type='market',time_in_force='day')
                    sold1+=1
#Sell other half when 13 crosses both
            if EightOverFiveStock1>=0 and ThirteenOverEightStock1>=0 and positive1==1:
                api.submit_order(symbol=stock1,qty=SellHalf,side='sell',type='market',time_in_force='day')
                sold1=0
                mail_content=("Trades have been made, 13MAVG crossed 8MAVG and 5MAVG, positive gain, sold JPM")
                something=True
#Buy half when 8 crosses 5 JPM
            if FiveOverEightStock1>=0 and negative1==1 and sold==0:
                my_order = api.get_order_by_client_order_id('JPM_Negative'+str(SoldAtStock1))
                SellHalf+=int(my_order.filled_qty)//2
                if SellHalf*2 != int(my_order.filled_qty):
                    api.submit_order(symbol=stock1,qty=(SellHalf+1),side='buy',type='market',time_in_force='day')
                    sold1+=1
                else:
                    api.submit_order(symbol=stock1,qty=SellHalf,side='buy',type='market',time_in_force='day')
                    sold1+=1
#Buy other half when 13 crosses both
            if FiveOverEightStock1>=0 and EightOverThirteenStock1>=0 and negative1==1:
                api.submit_order(symbol=stock1,qty=SellHalf,side='buy',type='market',time_in_force='day')
                sold1=0
                mail_content=("Trades have been made, 13MAVG crossed 8MAVG and 5MAVG, positive short, bought JPM")
                something=True
        else:
            pass
    else:
        mail_content=("The Market is Closed")
        something=True
        NotDone=str('Nothing Happened, '+str(mail_content)+', JPM:'+str(JPMShares)+' BAC:'+str(BACShares))
    if something==True:
#The body and attachments for the email
        SendOut=str(mail_content+', JPM:'+str(JPMShares)+' BAC:'+str(BACShares))
        message.attach(MIMEText(SendOut, "plain"))
#Create SMTP session for sending the mail
        session=smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.login(sender_address, sender_password)
        text=message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        done=str('Mail Sent, '+(SendOut))
        return done
    else:
        return NotDone


# In[79]:


pairs_trading_algo(0)


# In[64]:





# In[ ]:




