import robin_stocks as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from misc import *
from tradingstats import *
from config import *
import getpass
from robinhood_crypto_api import RobinhoodCrypto
import robin_stocks.helper as helper
import robin_stocks.urls as urls


def limit_btc_buy(current_price):
    btc_purchace_price = current_price * 0.95 
    limit_order_info = r.trade(
    'BTCUSD',
    # price=1.00,
    price=round(float(btc_purchace_price, 2)),
    quantity="0.0001",
    side="buy",
    time_in_force="gtc",
    type="limit"
    
    )
    
    order_id = limit_order_info['id']
    print('limit order TRY BUY {} status: {}'.format(order_id, r.order_status(order_id)))
    # print('canceling limit BUY order {}: {}'.format(order_id, r.order_cancel(order_id)))

def limit_btc_sell(current_price):
    btc_sell_price = current_price * 1.05
    limit_order_info = r.trade(
    'BTCUSD',
    # price=1.00,
    price=round(float(btc_sell_price, 2)),
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
