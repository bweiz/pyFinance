import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import finplot as fp


def download_data(stock_name, start, end):

    stock = yf.Ticker(stock_name)
    data = stock.history(interval = '1d', start = start, end = end)

    return data

result = download_data("TSLA", '2023-01-01', '2023-11-30')

print(result.iloc[0,0])
print(result.iloc[0,3])
print(result.iloc[1,0])
print(result.iloc[1,3])
print(result['Open'])
print(result['Close'])