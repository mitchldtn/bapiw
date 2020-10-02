import requests
import json
from datetime import datetime

# Official Binance API Docs
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md


class API:
    API_URL = 'https://api.binance.com/api'
    PUBLIC_API_VERSION = 'v3'
    PRIVATE_API_VERSION = 'v3'

    # Intervals used when calling kline data
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#enum-definitions    
    INTERVAL_1MIN = '1m'
    INTERVAL_3MIN = '3m'
    INTERVAL_5MIN = '5m'
    INTERVAL_15MIN = '15m'
    INTERVAL_30MIN = '30m'
    INTERVAL_1HR = '1h'
    INTERVAL_2HR = '2h'
    INTERVAL_4HR = '4h'
    INTERVAL_6HR = '6h'
    INTERVAL_8HR = '8h'
    INTERVAL_12HR = '12h'
    INTERVAL_1DAY = '1d'
    INTERVAL_3DAY = '3d'
    INTERVAL_1WEEK = '1w'
    INTERVAL_1MONTH = '1M'

    def __init__(self):
        # setup endpaths here so if they change in newer api versions
        # only need to update them here
        self.endpath = {
            # public api points
            'exchangeInfo': 'exchangeInfo',
            'tickerPrice': 'ticker/price?symbol=',
            'klines': 'klines?symbol=',
            '24hrTicker': 'ticker/24hr',
            'orderBook': 'depth?symbol=',
            'bookTickers': 'ticker/bookTicker',
            # order api points(Private)
            'order': 'order',
            'testOrder': 'order/test',
            'allOrders': 'allOrders',
        }

    def _create_api_uri(self, path, public=True, version=PUBLIC_API_VERSION):
        v = self.PRIVATE_API_VERSION if public else version
        return self.API_URL + '/' + v + '/' + path

    def _request_api(self, path, public=True, version=PUBLIC_API_VERSION, post=False, **kwargs):
        uri = self._create_api_uri(path, public, version)
        try:
            if not post:
                response = requests.get(uri)
                return json.loads(response.text)
            if post:
                response = requests.post(uri)
        except Exception as e:
            print('Error trying to access ' + uri)
            print(e)
            return []

    # get all exchange info
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#exchange-information
    def get_exchangeInfo(self):
        path = self.endpath['exchangeInfo']
        data = self._request_api(path=path)
        
        return data

    # get tick price of symbol
    # returns symbol and price
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-price-ticker
    def get_tickprice(self, symbol):
        tickpath = self.endpath['tickerPrice'] + symbol
        return self._request_api(path=tickpath)

    # get Kline data of a symbol
    # data limit set to 500 by default. Max is 1000
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
    def get_klines(self, symbol, interval, startTime='', endTime='', limit=500):
        if (symbol and interval) and not (startTime and endTime):
            kpath = self.endpath['klines'] + symbol + "&interval=" + interval + '&limit=' + str(limit)
            return self._request_api(path=kpath)

        if (symbol and interval) and (startTime and endTime):
            sTime = datetime.strptime(startTime, "%Y, %m, %d")
            eTime = datetime.strptime(endTime, "%Y, %m, %d")
            sMS = int(round(sTime.timestamp() * 1000))
            eMS = int(round(eTime.timestamp() * 1000))

            kpath = self.endpath['klines'] + symbol + "&interval=" + interval + '&startTime=' + str(
                sMS) + '&endTime=' + str(eMS) + '&limit=' + str(limit)
            return self._request_api(path=kpath)

    # get 24hr tick data from all symbols by default
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics
    def get_24hrticker(self, symbol=''):
        if symbol:
            tpath = self.endpath['24hrTicker'] + '?symbol=' + symbol
        if not symbol:
            tpath = self.endpath['24hrTicker']

        return self._request_api(path=tpath)
    
    # get orderbook data
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#order-book
    def get_orderbook(self, symbol, limit=100):
        opath = self.endpath['orderBook'] + symbol + '&limit=' + str(limit)
        return self._request_api(path=opath)

    # get best price/quantity on the order book for a symbol or all symbols by default
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker
    def get_bookticker(self, symbol=''):
        if symbol:
            bpath = self.endpath['bookTickers'] + '?symbol=' + symbol
        if not symbol:
            bpath = self.endpath['bookTickers']
        return self._request_api(path=bpath)

    def place_order(self, symbol: str, side: str, type: str, quantity: float, price: float, test: bool = True):
        return []