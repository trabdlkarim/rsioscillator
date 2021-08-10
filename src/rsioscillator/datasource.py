from typing import Union
import pandas as pd 
from pandas.core.frame import DataFrame
import requests as req


def read_excel(path: str) -> DataFrame:
    df = pd.read_excel(path)
    return df

def __format_date(date):
    d = date.split('.')
    return d[2] + '-' + d[1] + '-' + d[0]

def process_data(df):
    df['Date'] = df['Date'].apply(__format_date)
    index = df['Date'].astype(str) + ' ' + df['Time'].astype(str)
    df.index = pd.core.indexes.datetimes.DatetimeIndex(index)
    df.columns = [c.strip() for c in df.columns]
    return df.loc[:,['Open', 'High', 'Low', 'Close', 'Overall']]

def fetch_alphavantage_data(symbol: str, start_date: Union[str, None] = None) -> DataFrame:
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=77QBDOJ4OF0SDCUA&outputsize=full'
    json_data = req.get(api_url).json()
    df = pd.DataFrame(json_data[f'Time Series (Daily)']).T
    df = df.rename(columns = {'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'Adj Close', '6. volume': 'Volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['7. dividend amount', '8. split coefficient'], axis = 1)
    if start_date:
        df = df[df.index >= start_date]
    return df 