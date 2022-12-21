# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 18:24:05 2022

@author: stran
"""
#%% inport package
import yfinance as yf
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


# 歷史模擬法(Historical simulation approach)
#%% import data(Historical simulation approach)
BTC_price = yf.download('BTC-USD', start = '2022-03-21', end = '2022-11-30')

#%% data cleansing(Historical simulation approach)
#過去251天的收盤價
BTC_close = BTC_price[['Close']]
#計算報酬率 Ri = (Pi+1 - Pi)/Pi
BTC_close['Close_lag1'] = BTC_close['Close'].shift(1)
BTC_close['Close_lag5'] = BTC_close['Close'].shift(5)
BTC_close['Return1'] = round((BTC_close['Close'] - BTC_close['Close_lag1']) / BTC_close['Close_lag1'], 4)
BTC_close['Return5'] = round((BTC_close['Close'] - BTC_close['Close_lag5']) / BTC_close['Close_lag5'], 4)
#將報酬率由小到大排序
BTC_close_H = BTC_close.sort_values(by = 'Return5')
BTC_close1 = BTC_close_H.dropna()

#%% find critical value(Historical simulation approach)
critical_value_H = round(np.percentile(BTC_close1['Return5'], 5), 4)

#%% compute VaR(Historical simulation approach)
V = 10000000
VaR_H = -V * critical_value_H

# 蒙地卡羅模擬法(Monte Carlo simulation approach)
#%% compute parameters(Monte Carlo simulation approach)
mu = np.nanmean(BTC_close['Return1'])
sigma = np.nanstd(BTC_close['Return1'])
days = 255
z = np.random.normal(size = days)
dt = 1/255
daily_return = np.exp((mu - 0.5 * sigma**2) + sigma * z)

#%% monte carlo simulation(Monte Carlo simulation approach)
BTC_path = np.zeros_like(daily_return)
BTC_path[0] = BTC_price['Close'][-1]
for i in range(1, days):
    BTC_path[i] = BTC_path[i-1]*daily_return[i]
    
plt.plot(BTC_path)
#%% data cleansing(Monte Carlo simulation approach)
BTC_path = pd.DataFrame(BTC_path)
BTC_path.columns = ['Close']
BTC_path['Close_lag5'] = BTC_path['Close'].shift(5)
BTC_path['Return5'] = round((BTC_path['Close'] - BTC_path['Close_lag5']) / BTC_path['Close_lag5'], 4)
BTC_close_M = BTC_path.sort_values(by = 'Return5')
BTC_close2 = BTC_close_M.dropna()

#%% find critical value(Historical simulation approach)
critical_value_M = round(np.percentile(BTC_close2['Return5'], 5), 4)

#%% compute VaR(Historical simulation approach)
VaR_M = -V * critical_value_M