from typing import Union
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import requests as req
import numpy as np
from math import floor
from termcolor import colored as cl

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


def compute_ewm_rsi(close: Series, period: int=14) -> DataFrame:
    delta = close.diff()
    upwards = []
    downwards = []
    for i in range(len(delta)):
        if delta[i] < 0:
            upwards.append(0)
            downwards.append(delta[i])
        else:
            upwards.append(delta[i])
            downwards.append(0)
    up_series = pd.Series(upwards)
    down_series = pd.Series(downwards).abs()
    up_ewm = up_series.ewm(com=period - 1, adjust=False).mean()
    down_ewm = down_series.ewm(com=period - 1, adjust=False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(
        columns={0: 'rsi'}).set_index(close.index)
    rsi_df = rsi_df.dropna()
    return rsi_df[3:]


def trading_strategy(prices, rsi):
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range(len(rsi)):
        if rsi.iloc[i-1] > 30 and rsi.iloc[i] < 30:
            if signal != 1:
                buy_price.append(prices.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi.iloc[i-1] < 70 and rsi.iloc[i] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices.iloc[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)

    return buy_price, sell_price, rsi_signal


def rsi_plot(df: DataFrame, symbol: str = 'EQUITY'):
    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=4, colspan=1)
    ax2 = plt.subplot2grid((10, 1), (5, 0), rowspan=4, colspan=1)
    ax1.plot(df['Close'], linewidth=2.5)
    ax1.set_title(symbol + ' CLOSE PRICE')
    ax2.plot(df['RSI-14'], color='orange', linewidth=2.5)
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
    ax2.set_title(symbol + ' RELATIVE STRENGTH INDEX')
    plt.show()


def rsi_plot_with_signals(df: DataFrame, symbol: str='EQUITY'):
    buy_price, sell_price, rsi_signal = trading_strategy(df['Close'], df['RSI-14'])
    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=4, colspan=1)
    ax2 = plt.subplot2grid((10, 1), (5, 0), rowspan=4, colspan=1)
    ax1.plot(df['Close'], linewidth=2.5, color='skyblue', label='IBM')
    ax1.plot(df.index, buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
    ax1.plot(df.index, sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')
    ax1.set_title(symbol + 'RSI TRADE SIGNALS')
    ax2.plot(df['RSI-14'], color='orange', linewidth=2.5)
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
    plt.show()
