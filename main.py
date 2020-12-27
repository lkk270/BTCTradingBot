import robin_stocks as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from robinhood_crypto_api import RobinhoodCrypto
# from misc import *
# from tradingstats import *
# from config import *
import getpass
from robinhood_crypto_api import RobinhoodCrypto
import robin_stocks.helper as helper
import robin_stocks.urls as urls
btc_purchace_price = 0
btc_sell_price = 0


login = r.login(user,password)
r = RobinhoodCrypto(user, password)


def limit_btc_buy(current_price):
    btc_purchace_price = current_price * 0.995 
    limit_order_info = r.trade(
    'BTCUSD',
    # price=1.00,
    price=round(float(btc_purchace_price), 2),
    quantity="0.0001",
    side="buy",
    time_in_force="gtc",
    type="limit"
    
    )
    
    order_id = limit_order_info['id']
    print('limit order TRY BUY {} status: {}'.format(order_id, r.order_status(order_id)))
    # print('canceling limit BUY order {}: {}'.format(order_id, r.order_cancel(order_id)))

def limit_btc_sell(current_price):
    btc_sell_price = current_price * 1.005
    limit_order_info = r.trade(
    'BTCUSD',
    # price=1.00,
    price=round(float(btc_sell_price), 2),
    quantity="0.0001",
    side="sell",
    time_in_force="gtc",
    type="limit"
    
    )
    order_id = limit_order_info['id']
    print('limit order TRY SELL {} status: {}'.format(order_id, r.order_status(order_id)))
    # print('canceling limit SELL order {}: {}'.format(order_id, r.order_cancel(order_id)))


def golden_cross(current_price, history, stockTicker, n1, n2, days, direction=""):
    # if(direction == "above" and not five_year_check(stockTicker)):
    #     return False
    # history = r.get_historicals(stockTicker,span='year',bounds='regular')
    closingPrices = []
    dates = []
    total_price = 0
    count  = 0
    for item in history:
        # print(item)
        closingPrices.append(float(item['close_price']))
        dates.append(item['begins_at'])
        print(float(item['close_price']), item['begins_at'])
        total_price += float(item['close_price'])
        count+=1
    print('currenct_price: ', current_price)
    print('total_price: ', total_price)
    print('count: ', count)
    ema = total_price/count
    print('ema: ', ema)

    if current_price > ema:
        return 'buy'
    else:
        return 'sell'

    # price = pd.Series(closingPrices)
    # dates = pd.Series(dates)
    # dates = pd.to_datetime(dates)
    # sma1 = ta.volatility.bollinger_mavg(price, n1, fillna=False)
    # sma2 = ta.volatility.bollinger_mavg(price, n2, fillna=False)
    # series = [price.rename("Price"), sma1.rename("Indicator1"), sma2.rename("Indicator2"), dates.rename("Dates")]
    # df = pd.concat(series, axis=1)
    # cross = get_last_crossing(df, days, symbol=stockTicker, direction=direction)
    # if(cross) and plot:
    #     show_plot(price, sma1, sma2, dates, symbol=stockTicker, label1=str(n1)+" day SMA", label2=str(n2)+" day SMA")
    # return cross


def get_crypto_info(symbol, info=None):
    """Gets information about a crpyto currency.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then will return a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a strings representing the value of the key.
    :Dictionary Keys: * asset_currency
                      * display_only
                      * id
                      * max_order_size
                      * min_order_size
                      * min_order_price_increment
                      * min_order_quantity_increment
                      * name
                      * quote_currency
                      * symbol
                      * tradability

    """
    url = urls.crypto_currency_pairs()
    data = helper.request_get(url, 'results')
    data = [x for x in data if x['asset_currency']['code'] == symbol]
    if len(data) > 0:
        data = data[0]
    else:
        data = None
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_quote(symbol, info=None):
    """Gets information about a crypto including low price, high price, and open price

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * asset_currency
                      * display_only
                      * id
                      * max_order_size
                      * min_order_size
                      * min_order_price_increment
                      * min_order_quantity_increment
                      * name
                      * quote_currency
                      * symbol
                      * tradability

    """
    id = get_crypto_info(symbol, info='id')
    url = urls.crypto_quote(id)
    data = helper.request_get(url)
    return(helper.filter(data, info))


@helper.login_required
def get_crypto_historicals(symbol, interval, span, bounds, info=None):
    """Gets historical information about a crypto including open price, close price, high price, and low price.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param interval: The time between data points. Can be '15second', '5minute', '10minute', 'hour', 'day', or 'week'. Default is 'hour'.
    :type interval: str
    :param span: The entire time frame to collect data points. Can be 'hour', 'day', 'week', 'month', '3month', 'year', or '5year'. Default is 'week'
    :type span: str
    :param bound: The times of day to collect data points. 'Regular' is 6 hours a day, 'trading' is 9 hours a day, \
    'extended' is 16 hours a day, '24_7' is 24 hours a day. Default is '24_7'
    :type bound: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * begins_at
                      * open_price
                      * close_price
                      * high_price
                      * low_price
                      * volume
                      * session
                      * interpolated
                      * symbol

    """
    interval_check = ['15second', '5minute', '10minute', 'hour', 'day', 'week']
    span_check = ['hour', 'day', 'week', 'month', '3month', 'year', '5year']
    bounds_check = ['24_7', 'extended', 'regular', 'trading']

    if interval not in interval_check:
        print(
            'ERROR: Interval must be "15second","5minute","10minute","hour","day",or "week"', file=helper.get_output())
        return([None])
    if span not in span_check:
        print('ERROR: Span must be "hour","day","week","month","3month","year",or "5year"', file=helper.get_output())
        return([None])
    if bounds not in bounds_check:
        print('ERROR: Bounds must be "24_7","extended","regular",or "trading"', file=helper.get_output())
        return([None])
    if (bounds == 'extended' or bounds == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"', file=helper.get_output())
        return([None])


    symbol = helper.inputs_to_set(symbol)
    print(symbol)
    id_var = '3d961844-d360-45fc-989b-f6fca761d511'
    url = urls.crypto_historical(id_var, interval, span, bounds)
    payload = {'interval': interval,
               'span': span,
               'bounds': bounds}
    data = helper.request_get(url, 'regular', payload)

    histData = []
    cryptoSymbol = data['symbol']
    for subitem in data['data_points']:
        subitem['symbol'] = cryptoSymbol
        histData.append(subitem)

    return(helper.filter(histData, info))


def go():
    btc_bought = False
    wait_for_fall = False
    num_trades = 0
    while num_trades < 3:
        current_price = float(get_crypto_quote('BTC')['mark_price'])
        history = get_crypto_historicals('BTC', '5minute', 'day', '24_7', None)
        action = golden_cross(current_price, history[252:], 'BTC', 50, 200,  10, "")
        if btc_purchace_price > 0:
            if (current_price - btc_purchace_price)/btc_purchace_price >= 0.0025 and wait_for_fall == False:
                wait_for_fall = True
            elif (current_price - btc_purchace_price)/btc_purchace_price <= 0.0015 and (current_price - btc_purchace_price)/btc_purchace_price > 0 and wait_for_fall:
                    limit_btc_sell(current_price)
                    btc_bought = False
                    print('sell was falling')
                    num_trades+=1 
                    wait_for_fall = False
                    continue
        if action == 'buy':
            if not btc_bought:
                limit_btc_buy(current_price)
                btc_bought = True
                print('buy')
            else:
                print('hold')
        else:
            if btc_bought:
                limit_btc_sell(current_price)
                btc_bought = False
                num_trades+=1 
                print('sell')
            else:
                print('hold')
        print('============================')

go()