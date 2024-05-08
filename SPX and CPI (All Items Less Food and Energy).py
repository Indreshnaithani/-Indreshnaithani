#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:00:50 2024

@author: indresh
"""


pip install yfinance
pip install fredapi

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


api_key = '05aa295724f5f9446dbb7a62f88c25aa'
from fredapi import Fred
fred = Fred(api_key=api_key)

#get data on GDP from fred and filter from 1985 onwards.
#spx data is only available from 1985 onwards in yahoo finance
CPI = fred.get_series('CPILFESL')['1985':]

#yahoo finance chosen for spx as it  provides an option for 1 month without need of data engineering
spx = yf.Ticker('^SPX')
spx = spx.history(start = '1985-01-01', interval = '1mo')['Close']

CPI = CPI['1985':]
spx.index = spx.index.map(str)
CPI.index = CPI.index.map(str)

spx_index=[]
for i in range(len(spx.index)):
    spx_index.append(spx.index[i][:10])
spx.index = spx_index

CPI_index=[]
for i in range(len(CPI.index)):
    CPI_index.append(CPI.index[i][:10])
CPI.index = CPI_index

df = pd.DataFrame({'SPX':spx,'CPI':CPI})
Correlation = df.corr()
print(Correlation)
df.index = pd.to_datetime(df.index)

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('SPX', color=color)
ax1.plot(df.index, df['SPX'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis='x', direction = 'out')

ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('CPI', color=color)  
ax2.plot(df.index, df['CPI'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('SPX and CPI over Time')
plt.show()