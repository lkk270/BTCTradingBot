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

def sell_holdings(symbol, holdings_data):
    """ Place an order to sell all holdings of a stock.

    Args:
        symbol(str): Symbol of the stock we want to sell
        holdings_data(dict): dict obtained from get_modified_holdings() method
    """
    shares_owned = int(float(holdings_data[symbol].get("quantity")))
    if not debug:
        r.order_sell_market(symbol, shares_owned)
    print("####### Selling " + str(shares_owned) + " shares of " + symbol + " #######")