import backtrader as bt


class SmaCross(bt.Strategy):
    params = dict(
        short_interval=20,
        middle_interval=60,
        long_interval=120
    )

    def __init__(self):
        self.short_sma = bt.indicators.SMA(period=self.params.short_interval)
        self.middle_sma = bt.indicators.SMA(period=self.params.middle_interval)
        self.long_sma = bt.indicators.SMA(period=self.params.long_interval)
        self.trade_signal = bt.indicators.CrossOver(self.short_sma, self.middle_sma)

    def next(self):
        if self.short_sma > self.middle_sma:
            self.buy(size=10)
        elif self.trade_signal <= 0:
            self.close()
