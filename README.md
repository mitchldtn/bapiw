# BAPIW(Binance API Wrapper)

## Things to do:
* Add more code notes, docs and script examples.
* Add feature to place, cancel and view orders.

## How to use
Install the package:
```
python3 setup.py install
```
Import API or/and DataParser:
```
from bapiw.api import API
from bapiw.dataParser import DataParser

bapiw = API()
dp = DataParser()
```

## Running Example Scripts
Some scripts may require other packages like `matplotlib`, `plotly` or `dash`.

## Difference between API and DP(Data Parser)?
I, personally, only import the Data Parser but technically I use both as the DP uses the API.

The reason I created both is to make my life(and maybe yours) simpler.

The API returns RAW data from the Binance API. It simply puts it in json format.

I felt it necessary to do this because in the DP I exclude some data like `Close time` and `Taker buy base asset volume` to name a few when getting Kline Data.

Some people may want that data and they can remove my `df.drop`'s from getKline in DP to get them OR pull from the API.

## API Current Usage

* [get_exchangeInfo](#api-get-exchange-info)
    * Example: `bapiw.get_exchangeInfo()`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#exchange-information
* [get_tickprice](#api-get-tick-price)
    * Example: `bapiw.get_tickprice(symbol='BTCUSDC')`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-price-ticker
* [get_klines](#api-get-klines)
    * Example: `bapiw.get_klines(symbol='BTCUSDC', interval=bapiw.INTERVAL_1HR)`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
* [get_24hrticker](#api-get-24hr-ticker)
    * Example: `bapiw.get_24hrticker(symbol='BTCUSDC')`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics
* [get_orderbook](#api-get-order-book)
    * Example: `bapiw.get_orderbook(symbol='BTCUSDC)`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#order-book
* [get_bookticker](#api-get-book-ticker)
    * Example: `bapiw.get_bookticker()`
    * Official Docs: https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker

## Data Parser Current Usage

* [getSymbols](#dp-get-symbols)
    * Example: `dp.getSymbols(includes='BTC')`
* [getKlines](#dp-get-klines)
    * Example: `dp.getKlines(symbol='BTCUSDC', interval=dp.INTERVAL_1HR, data='ohlcv')`

## Docs

### API Get Exchange Info
```
bapiw.get_exchangeInfo()
```
Retrieves every symbols exchange info on the Binance API.


### API Get Tick Price
```
bapiw.get_tickprice(symbol='BTCUSDC')
```
Pulls the current price data from the exchange for the specified symbol.


### API Get Klines
```
bapiw.get_klines(symbol='BTCUSDC', interval=bapiw.INTERVAL_12HR, startTime='2019, 12, 15', endTime='2020, 01, 15', limit=1000)
```
Returns Kline data for specifed symbol at the specified interval.

`startTime` and `endTime` must be in `'2020, 01, 20'` format. <br />

`interval` variables:
```
INTERVAL_1MIN
INTERVAL_3MIN
INTERVAL_5MIN
INTERVAL_15MIN
INTERVAL_30MIN
INTERVAL_1HR
INTERVAL_2HR
INTERVAL_4HR
INTERVAL_6HR
INTERVAL_8HR
INTERVAL_12HR
INTERVAL_1DAY
INTERVAL_3DAY
INTERVAL_1WEEK
INTERVAL_1MONTH
```

`limit` default is `500`, max is `1000`.


### API Get 24hr Ticker
```
bapiw.get_24hrticker()
```
Leave blank to return all ticker information.


### API Get Order Book
```
bapiw.get_orderbook(symbol='BTCUSDC)
```


### DP Get Symbols
```
dp.getSymbols(onlyTrading=False, includes='LTC|DAI')
dp.getSymbols()
```
Using `includes` we can retrieve specific symbols. The above example will list all symbols that include LTC OR DAI and both.

Using `onlyTrading=False`(set to true by default) we can list all symbols, even the ones that don't currently have a status of `TRADING`, on Binance.

Leave blank to return all symbols that are currently trading.

### DP Get Klines
```
dp.getKlines(symbol='BTCUSDC', interval=dp.INTERVAL_1MIN, data='ohlcvqt')
```
`interval` variables:
```
INTERVAL_1MIN
INTERVAL_3MIN
INTERVAL_5MIN
INTERVAL_15MIN
INTERVAL_30MIN
INTERVAL_1HR
INTERVAL_2HR
INTERVAL_4HR
INTERVAL_6HR
INTERVAL_8HR
INTERVAL_12HR
INTERVAL_1DAY
INTERVAL_3DAY
INTERVAL_1WEEK
INTERVAL_1MONTH
```
`data` variables:

`o` returns the `Open` price for that interval.

`h` returns the `High` price for that interval.

`l` returns the `Low` price for that interval.

`c` returns the `Close` price for that interval.

`v` returns the `Volume` for that interval.

`q` returns the `Quote Volume` for that interval.

`t` returns the `# Trades` for that interval.