import numpy as np
import yfinance as yf
import pandas as pd
import datetime as dt
from pylab import mpl, plt

def download_data(stock_name, start, end):

    stock = yf.Ticker(stock_name)
    data = stock.history(interval = '1d', start = start, end = end)

    return data

result = download_data("TSLA", '2022-05-13', '2023-06-20')

sma1 = 9
sma2 = 21

result['sma1'] = result['Close'].rolling(sma1).mean()
result['sma2'] = result['Close'].rolling(sma2).mean()

result.dropna(inplace=True)

result['Position'] = np.where(result['sma1'] > result['sma2'], 1, -1)
result.tail()

# result['Close'].plot()
# result['sma1'].plot()
# result['sma2'].plot()
# ax = result['Position'].plot(secondary_y='Position')
# #ax = result.plot()
# #ax.get_legend().set_bbox_to_anchor((0.25, 0.85))

result['Returns'] = np.log(result['Close'] / result['Close'].shift(1))
result['Strategy'] = result['Position'].shift(1) * result['Returns']

print(result.round(4).head())

result.dropna(inplace=True)

np.exp(result[['Returns', 'Strategy']]).sum()

result[['Returns', 'Strategy']].std() * 252 ** 0.5

ax = result[['Returns', 'Strategy']].cumsum(
            ).apply(np.exp).plot()
result['Position'].plot(ax=ax, secondary_y='Position', style='--')
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))


plt.show()