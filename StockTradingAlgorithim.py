#!/usr/bin/env python
# coding: utf-8

# In[95]:


import os
import alpaca_trade_api as tradeapi
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def EMA_trading_algo(self):
#Specify paper trading enviornment
    os.environ["APCA_API_BASE_URL"]=("https://paper-api.alpaca.markets")
#Insert API Credentials
    api=tradeapi.REST('PKCTQ47YTNL73SJXQ9WO', 'WEq3Lxro//obIk3sy12qLC3cs2S2VsNG9PvRCuuZ', api_version='v2')
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
    stock1='AAPL'
    stock2='MSFT'
#Put historical data into variables
    stock1_barset=api.get_barset(stock1, '1D', limit)
    stock2_barset=api.get_barset(stock2, '1D', limit)
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
#Current prices
    stock1_curr=data_1[limit-1]
    stock2_curr=data_2[limit-1]
#Moving average 13
    move_avg_days1=48
#Moving average for stock 1
    stock1_last48=[]
    for i in range(move_avg_days1):
        stock1_last48.append(data_1[(limit-1)-i])
    stock1_hist48=pd.DataFrame(stock1_last48)
    stock1_hist48=stock1_hist48.iloc[::-1]
    stock1_ema48=stock1_hist48.ewm(span=move_avg_days1,adjust=False).mean()
#Moving average for stock 2
    stock2_last48=[]
    for i in range(move_avg_days1):
        stock2_last48.append(data_2[(limit-1)-i])
    stock2_hist48=pd.DataFrame(stock2_last48)
    stock2_hist48=stock2_hist48.iloc[::-1]
    stock2_ema48=stock2_hist48.ewm(span=move_avg_days1,adjust=False).mean()
#Moving average 13
    move_avg_days2=13
#Moving average for stock 1
    stock1_last13=[]
    for i in range(move_avg_days2):
        stock1_last13.append(data_1[(limit-1)-i])
    stock1_hist13=pd.DataFrame(stock1_last13)
    stock1_hist13=stock1_hist13.iloc[::-1]
    stock1_ema13=stock1_hist13.ewm(span=move_avg_days2,adjust=False).mean()
#Moving average for stock 2
    stock2_last13=[]
    for i in range(move_avg_days2):
        stock2_last13.append(data_2[(limit-1)-i])
    stock2_hist13=pd.DataFrame(stock2_last13)
    stock2_hist13=stock2_hist13.iloc[::-1]
    stock2_ema13=stock2_hist13.ewm(span=move_avg_days2,adjust=False).mean()
#Calculation of shares to trade
    cash=float(account.buying_power)
    SpendPerTrade=(0.05*cash)
    SpendPerStock=SpendPerTrade//2
    limit_stock1=int(SpendPerStock//stock1_curr)
    limit_stock2=int(SpendPerStock//stock2_curr)
#Calculation of differnce:
    DifStock1=((stock1_ema13-stock1_ema48).iloc[0])[0]
    DifStock2=((stock2_ema13-stock2_ema48).iloc[0])[0]
#Actual trading algorithim
    portfolio=api.list_positions()
    try: 
        Stock1Shares=int(api.get_position(stock1).qty)
    except:
        Stock1Shares=0
    try:
        Stock2Shares=int(api.get_position(stock2).qty)
    except:
        Stock2Shares=0
    clock=api.get_clock()
    something=False
    mail_content=("")
    NotDone=("Nothing Happened")
    if clock.is_open==True:
#No shares of Stock 1 try to buy
        if Stock1Shares==0:
#5MAVG crossing 13MAVG and 8MAVG positive BAC
            if DifStock1>=0: 
                api.submit_order(symbol=stock1,qty=limit_stock1,side='buy',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive trend, bought Stock1")
#5MAVG crossing 13MAVG and 8MAVG negative BAC
            elif DifStock1<=0:
                api.submit_order(symbol=stock1,qty=limit_stock1,side='sell',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, negative trend, sold Stock1")
#No shares of JPM try to buy
        if Stock2Shares==0:
#5MAVG crossing 13MAVG and 8MAVG positive JPM
            if DifStock2>=0:
                api.submit_order(symbol=stock1,qty=limit_stock1,side='buy',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive trend, bought Stock2")
#5MAVG crossing 13MAVG and 8MAVG negative JPM
            elif DifStock2<=0:
                api.submit_order(symbol=stock1,qty=limit_stock1,side='sell',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, negative trend, sold Stock1")
        else:
            mail_content=("Nothing was bought")
#If you have BAC stock look to sell positive
        if Stock1Shares>0:
#Sell other half when 13 crosses both
            if DifStock1<=0:
                api.submit_order(symbol=stock1,qty=Stock1Shares,side='sell',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive gain, sold Stock1")
#If you have BAC stock look to sell negative
        if Stock1Shares<0:
#Buy other half when 13 crosses both
            if DifStock1>=0:
                api.submit_order(symbol=stock1,qty=Stock1Shares,side='buy',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive short, bought Stock1")
#If you have JPM stock look to sell
        if Stock2Shares>0:
#Sell other half when 13 crosses both
            if DifStock2<=0:
                api.submit_order(symbol=stock2,qty=Stock2Shares,side='sell',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive gain, sold Stock2")
        if Stock2Shares<0:
#Buy other half when 13 crosses both
            if DifStock2>=0:
                api.submit_order(symbol=stock2,qty=Stock2Shares,side='buy',type='market',time_in_force='day')
                mail_content=("Trades have been made, 13EMA crossed 48EMA, positive short, bought Stock2")
        else:
            pass
    else:
        mail_content=("The Market is Closed")
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


# In[93]:


pairs_trading_algo(0)


# In[38]:





# In[ ]:




