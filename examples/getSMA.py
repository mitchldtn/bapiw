# This script will pull the 1day kline data of BTCUSDC,
# calculate the 20 day Simple Moving Average and plot it
# using matplotlib.

from bapiw.dataParser import DataParser
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats

dp = DataParser()

df = dp.getKlines(symbol='BTCUSDC', interval=dp.INTERVAL_1DAY, data='c', limit=620)

close = df['Close']

time_period = 20
history = []
sma_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del (history[0])

    sma_values.append(stats.mean(history))

df['ClosePrice'] = close
df['SMA'] = sma_values

close_price = df['ClosePrice']
sma = df['SMA']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='BTCUSDC price in $')
close_price.plot(ax=ax1, color='g', lw=2, legend=True)
sma.plot(ax=ax1, color='r', lw=2, legend=True)
plt.show()