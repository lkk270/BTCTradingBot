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
