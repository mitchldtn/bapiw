from bapiw.api import API
from datetime import datetime, date
import pandas as pd
import numpy as np

bapiw = API()


class DataParser:
    # intervals used when calling kline data
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

    def getSymbols(self, onlyTrading=True, includes=''):
        # pulls all exchange info
        exchange = bapiw.get_exchangeInfo()

        # by default onlyTrading is set True which will only shows symbols
        # with a status of TRADING on binance. Anything else shows
        # all symbols.
        
        # look for symbols in exchanges data, check the status for TRADING and
        # add those symbols to a list
        symbol_list = []
        if onlyTrading:
            for zd in exchange['symbols']:
                if zd['status'] == 'TRADING':
                    symbol_list.append(zd['symbol'])
        else:
            for zd in exchange['symbols']:
                symbol_list.append(zd['symbol'])

        # create a dataframe with the symbols and rename the column from 0 to symbols
        symbols = pd.DataFrame(symbol_list)
        symbols = symbols.rename(columns={0: 'symbols'})

        # if includes isn't null it will only list symbols that include that string
        if includes:
            # searches for the symbols that contain string 'includes' and puts them in mysymbols var
            mysymbols = symbols[symbols['symbols'].str.contains(includes)]

            # replace those symbols in a Dataframe, reset the index
            # and delete the old unaccurate index
            mysymbols = pd.DataFrame(mysymbols['symbols'])
            mysymbols = mysymbols.reset_index()
            mysymbols = mysymbols.drop(columns=['index'])
            
            symbols = mysymbols
        
        return symbols

    def getKlines(self, symbol, interval, startTime='', endTime='', limit=500, data='ohlcv'):
        # pull data from api
        kdata = bapiw.get_klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime, limit=limit)

        # put data into dataframe and remove columns that aren't needed
        df = pd.DataFrame.from_dict(kdata)
        df = df.drop(range(6, 7), axis=1)
        df = df.drop(range(9, 12), axis=1)

        df_date = df[0]

        final_date = []
        # convert the date
        for time in df_date.unique():
            readable = datetime.fromtimestamp(int(time / 1000))
            final_date.append(readable)

        # remove the old date from the dataframe and add the new date as index
        df.pop(0)
        dateframe_final_date = pd.DataFrame({'Date': final_date})
        df = df.join(dateframe_final_date)
        df.set_index('Date', inplace=True)

        # rename the columns
        df = df.rename(columns={1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume', 7: 'Quote Volume', 8: '# Trades'})

        # convert the values into numeric so we can compute them easily
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Volume'] = pd.to_numeric(df['Volume'])
        df['Quote Volume'] = pd.to_numeric(df['Quote Volume'])
        df['# Trades'] = pd.to_numeric(df['# Trades'])

        # look in 'data' for what values to return
        if data.find('o') == -1:
            df = df.drop(columns=['Open'])
        if data.find('h') == -1:
            df = df.drop(columns=['High'])
        if data.find('l') == -1:
            df = df.drop(columns=['Low'])
        if data.find('c') == -1:
            df = df.drop(columns=['Close'])
        if data.find('v') == -1:
            df = df.drop(columns=['Volume'])
        if data.find('q') == -1:
            df = df.drop(columns=['Quote Volume'])
        if data.find('t') == -1:
            df = df.drop(columns=['# Trades'])

        return df

    def getOrderBookBids(self, symbol, limit=100):
        data = bapiw.get_orderbook(symbol=symbol, limit=limit)

        x = data['bids']
        bidprice, bidquantity = zip(*x)

        bdf = pd.DataFrame({'bidPrice0': bidprice, 'bidQuantity0': bidquantity})
        bdf['bidPrice0'] = pd.to_numeric(bdf['bidPrice0'])
        bdf['bidQuantity0'] = pd.to_numeric(bdf['bidQuantity0'])

        bdf['date0'] = datetime.today().strftime('%Y-%m-%d %X')

        return bdf

    def getOrderBookAsks(self, symbol, limit=100):
        data = bapiw.get_orderbook(symbol=symbol, limit=limit)

        y = data['asks']
        askprice, askquantity = zip(*y)

        adf = pd.DataFrame({'askPrice0': askprice, 'askQuantity0': askquantity})
        adf['askPrice0'] = pd.to_numeric(adf['askPrice0'])
        adf['askQuantity0'] = pd.to_numeric(adf['askQuantity0'])

        adf['date0'] = datetime.today().strftime('%Y-%m-%d %X')

        return adf

    def getBooktick(self):
        data = bapiw.get_bookticker()
        df = pd.DataFrame(data)
        return df

    def get24hrTick(self):
        data = bapiw.get_24hrticker()
        df = pd.DataFrame(data)
        return df

    def getDateToMS(self, date):
        dateObj = datetime.strptime(date, '%Y-%m-%d %X.%f')
        millisec = dateObj.timestamp() * 1000
        return millisec

    def getDateFromMS(self, date):
        return []