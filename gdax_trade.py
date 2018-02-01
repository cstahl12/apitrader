import gdax
import json
import threading
import time
import datetime
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt

def get_data(client, pair, granularity=3600):
    df = pd.DataFrame(client.get_product_historic_rates(pair, granularity=granularity))
    df.columns = ['time', 'low', 'high', 'open', 'close', 'volume']
    df = df.sort_values(by='time', ascending=True)
    df = format_data(df)
    return(df)

def format_data(df):
    df['upper_channel'] = ta.MAX(df['close'].values, timeperiod=100)
    df['lower_channel'] = ta.MIN(df['close'].values, timeperiod=100)
    df['ma10'] = ta.EMA(df['close'].values, timeperiod=10)
    df['ma100'] = ta.EMA(df['close'].values, timeperiod=100)
    #df['slope10'] = ta.LINEARREG_SLOPE(df['close'].values, timeperiod=10)
    df['slope120'] = ta.LINEARREG_SLOPE(df['close'].values, timeperiod=120)
    df = df.drop(['open', 'high', 'low', 'volume'], axis=1)
    return df.dropna(axis=0)

def get_action(pair, row):
    print(pair)
    print('Buy: ' + str(row['ma10'] > row['ma100']))
    print('Sell: ' + str(row['ma10'] <= row['ma100']))

def main():
    public_client = gdax.PublicClient()

    granularity=3600

    eth_usd = get_data(public_client, 'ETH-USD', granularity)
    ltc_usd = get_data(public_client, 'LTC-USD', granularity)
    btc_usd = get_data(public_client, 'BTC-USD', granularity)

    #get_action('ETH-USD', eth_usd.iloc[0])
    #get_action('LTC-USD', ltc_usd.iloc[0])
    #get_action('BTC-USD', btc_usd.iloc[0])


    plt.plot(eth_usd['time'], eth_usd['ma10'], linewidth=2.0)
    plt.plot(eth_usd['time'], eth_usd['ma100'], linewidth=2.0)
    plt.plot(eth_usd['time'], eth_usd['upper_channel'], linewidth=2.0)
    plt.plot(eth_usd['time'], eth_usd['lower_channel'], linewidth=2.0)
    plt.show()

if __name__ == '__main__':
    main()
