import numpy as np
import yfinance as yf
import statistics
import pandas as pd
import matplotlib.pyplot as plt

def download_data(stock_name, start, end):

    stock = yf.Ticker(stock_name)
    data = stock.history(interval = '1d', start = start, end = end)

    return data

def find_inside_days(Open, Close, prevOpen, prevClose):
    if prevOpen < prevClose:
        if (Open > prevOpen) & (Close < prevClose):
            return True
    elif prevOpen > prevClose:
        if (Open > prevOpen) & (Close > prevClose):
            return 1
    else:
        return 0

st = download_data("MSFT", '2023-01-01', '2023-11-30')
iDays = []
returns = []
for i in range(1, len(st)):
    open = st.iloc[i, 0]
    close = st.iloc[i, 3]

    prevOpen = st.iloc[i-1, 0]
    prevClose = st.iloc[i-1, 3]

    sReturns = []
    sReturns.append(abs(open - close))
    result = find_inside_days(open, close, prevOpen, prevClose)
    if result == 1:
        iDays.append(i)
        returns.append(abs(close-open))

print(iDays)
print(statistics.mean(returns))
print(statistics.mean(sReturns))




