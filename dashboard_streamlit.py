# imports
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from datetime import datetime
import yfinance as yf

import matplotlib.pyplot as plt
from matplotlib import gridspec


import streamlit as st



# Write a title
st.title('Stock Dashboard')

# text input to get the ticker symbol of the share
ticker_symbol = st.text_input('Ticker symbol of the share:')
st.write('The dashboard will be created for the following ticker symbol:', ticker_symbol)

# date input for start and end date
start_date = st.date_input('Start date:')
st.write('You selected:', start_date)

end_date = st.date_input('End date:', max_value=datetime.today())
st.write('You selected', end_date)

# get the price of the share and save it into a DataFrame 
df = yf.download(ticker_symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), progress=False)
df = df[['Adj Close', 'Volume']]

###################################
# Calculate indocators

# RSI
delta = df['Adj Close'].diff()
delta.dropna(inplace=True)
up = delta.copy()
up[up < 0] = 0
down = delta.copy()
down[down > 0] = 0
AVG_gain = up.rolling(window=14).mean()
AVG_loss = abs(down.rolling(window=14).mean())
RS = AVG_gain / AVG_loss
RSI = 100.0 - (100.0 / (1.0 + RS))
df['RSI'] = RSI

# MACD
ema_12 = df['Adj Close'].ewm(span=12, adjust=False).mean()
ema_26 = df['Adj Close'].ewm(span=26, adjust=False).mean()
MACD = ema_12 - ema_26
signal_line = MACD.ewm(span=9, adjust=False).mean()
df['MACD'] = MACD
df['MACD_signal'] = signal_line

##################################
# Define plot
plt.style.use('fivethirtyeight')
    
# drop rows with NaNs in RSI column
df.dropna(inplace=True)
    
# create figute
fig = plt.figure(figsize=(12,8))
    
# set hight ratios for subplots
gs = gridspec.GridSpec(4, 1, height_ratios=[2,1,1,1])
    
ax1 = plt.subplot(gs[0])
ax1.plot(df.index, df['Adj Close'])
plt.ylabel('Price')
ax1.set_title(f'{ticker_symbol} Stock Analysis')

ax2 = plt.subplot(gs[1], sharex = ax1)
ax2.bar(df.index, df['Volume'])
plt.ylabel('Volume')
    
ax3 = plt.subplot(gs[2], sharex = ax1)
ax3.plot(df.index, df['RSI'])
plt.axhline(30, linestyle='--', lw=1, alpha=0.5, color='red')
plt.axhline(70, linestyle='--', lw=1, alpha=0.5, color='red')
plt.ylabel('RSI')
    
ax4 = plt.subplot(gs[3], sharex = ax1)
ax4.plot(df.index, df['MACD'])
ax4.plot(df.index, df['MACD_signal'])
    
plt.ylabel('MACD')
    
# remove xticks
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)

st.pyplot()







