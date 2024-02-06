import ta
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def download_data(stock_name, start, end):

    stock = yf.Ticker(stock_name)
    data = stock.history(interval='1d', start= start, end= end)

    return data
result = download_data("NVDA", "2023-01-01", "2023-11-30")
#print(result.head())
def vwap_indicator(data, window):
    vwap = ta.volume.VolumeWeightedAveragePrice(high = data["High"], low = data['Low'],
                                                close = data['Close'], volume = data['Volume'],
                                                window = window)
    vwap_values = vwap.volume_weighted_average_price()
    return vwap_values

vwap = vwap_indicator(result, 30)
result["VWAP"] = vwap
#print(result)

def sma_indicator(data, window):
    sma = ta.trend.SMAIndicator(data['Close'], window = window)
    sma_values = sma.sma_indicator()
    return sma_values

sma = sma_indicator(result, 5)
result['SMA'] = sma
result = result.dropna()
print(result.head())


def calculate_signals(data):
    close_sma = data['Close'] - data['VWAP']
    close_vwap = data['SMA'] - data['VWAP']

    long_condition = (close_sma < 0) & (close_vwap < 0) & (data['Close'].shift(2) > data['Close'])
    short_condition = (close_sma > 0) & (close_vwap > 0) & (data['Close'].shift(2) < data['Close'])

    new_series = np.where(long_condition, 1, np.where(short_condition, -1, 0))

    return new_series

theSignals = calculate_signals(result)
result['Signal'] = theSignals
print(result['Signal'])

result["Daily Returns"] = result['Close'].pct_change() * result['Signal'].shift(1)
result["Cumulative Returns"] = (1. + result['Daily Returns']).cumprod() * 100
print(result[['Daily Returns', 'Cumulative Returns']].head(200))

stock_name = "KODK"
result['Benchmark'] = result["Close"]/result['Close'].iloc[0] * 100
result[["Cumulative Returns", "Benchmark"]].plot()
plt.title("Equity Curve: " + stock_name)
plt.xlabel("Time")
plt.ylabel("Cumulative Returns")
plt.show()