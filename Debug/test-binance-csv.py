import pandas as pd
import datetime as dt
from datetime import datetime, timedelta, timezone

# import 路径修改
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backtrader_binance.binance_spot import Binance,Intervals

# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api_CN.md

def klinestodataframe(klines):
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'a', 'b', 'c', 'd', 'e', 'f'], dtype='float64')
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.set_index('time')
    df = df.drop(columns=['a', 'b', 'c', 'd', 'e', 'f'])

    return df

symbol = "BTCUSDT"
interval = "5m"
delta = Intervals[interval]
end = dt.datetime.now()
start = dt.datetime.now() - dt.timedelta(days=30)

api = Binance({})
# status, data = api.getklines(symbol, interval, 1000, int(start.timestamp() * 1000) if start != None else None, int(end.timestamp() * 1000))
status, data = api.getklines(symbol, interval, 1000, end = int(end.timestamp() * 1000))
df = klinestodataframe(data)

ohlc = df


# path = "data/{}_{}_{}_{}.csv".format(symbol, start.strftime('%Y%m%d-%H%M%S'), end.strftime('%Y%m%d-%H%M%S'), interval)
path = "data/binance_{}.csv".format(symbol)
# binance.btcusdt
os.makedirs("data/", exist_ok=True)
f = open(path, 'w+')
ohlc.to_csv(f)
f.close()

