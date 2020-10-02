# Simple script that uses dataPaser.py to get symbols on Binance
# By default it only shows symbols with the status of 'TRADING'
# You can get all symbols by setting "onlyTrading=False" and
# use "includes='LTC|DAI'" to pull the symbols that include
# LTC and/or DAI. We use getKlines to retrieve the kline data
# of each of those symbols.

from bapiw.dataParser import DataParser
import pandas as pd

dp = DataParser()

# Puts list of all symbols on Binance into symbols var that 
# includes LTC and DAI in them.
# dataParser already put's them into a Dataframe
symbols = dp.getSymbols(includes='LTC|DAI')

# Print symbols list
print(symbols)

# Convert symbols dataframe column to a list
symbol_list = symbols['symbols'].tolist()

# Pull every symbols Kline data of 1min intervals and print them
# Using data='ohlcv' we get open, high, low, close and volume values
for symbol in symbol_list:
    df = dp.getKlines(symbol=symbol, interval=dp.INTERVAL_1MIN, data='ohlcv')
    print(symbol, "Kline data:")
    print(df)