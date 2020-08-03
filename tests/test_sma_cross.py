## 获取数据
from datetime import datetime

import backtrader as bt
import pandas as pd
import tushare as ts
from pylab import mpl

from a1chemy.strategy.sma_cross import SmaCross


def get_data(code, start='2010-01-01', end='2020-03-31'):
    df = ts.get_k_data(code, autype='qfq', start=start, end=end)
    df.index = pd.to_datetime(df.date)
    df['openinterest'] = 0
    df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
    return df


def test_next():
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    dataframe = get_data('600519')

    # 回测期间
    start = datetime(2010, 3, 31)
    end = datetime(2020, 3, 31)
    # 加载数据
    data = bt.feeds.PandasData(dataname=dataframe, fromdate=start, todate=end)

    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    # 将数据传入回测系统
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    cerebro.addstrategy(SmaCross)
    # 设置初始资本为10,000
    startcash = 10000
    cerebro.broker.setcash(startcash)
    # 设置交易手续费为 0.2%
    cerebro.broker.setcommission(commission=0.002)

    d1 = start.strftime('%Y%m%d')
    d2 = end.strftime('%Y%m%d')
    print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
    # 运行回测系统
    cerebro.run()
    # 获取回测结束后的总资金
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    # 打印结果
    print(f'总资金: {round(portvalue, 2)}')

    # cerebro.plot(style='candlestick')
    cerebro.plot()
    assert True
