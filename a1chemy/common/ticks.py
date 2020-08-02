import pandas as pd

from a1chemy.common import OPEN, CLOSE, HIGH, LOW, AMOUNT, VOLUME, INDEX


class Ticks(object):
    exchange = ''
    symbol = ''
    name = ''
    currency = ''
    raw_data: pd.DataFrame

    def __init__(self, exchange=None, symbol=None, name=None, currency=None, raw_data=None) -> None:
        super().__init__()
        self.exchange = exchange
        self.symbol = symbol
        self.name = name
        self.currency = currency
        self.raw_data = raw_data

    def get_column_data(self, key: str):
        return self.raw_data[key]

    def index(self):
        return self.get_column_data(INDEX)

    def open(self):
        return self.get_column_data(OPEN)

    def close(self):
        return self.get_column_data(CLOSE)

    def high(self):
        return self.get_column_data(HIGH)

    def low(self):
        return self.get_column_data(LOW)

    def amount(self):
        """
        成交额
        @return:
        """
        return self.get_column_data(AMOUNT)

    def volume(self):
        """
        成交量
        @return:
        """
        return self.get_column_data(VOLUME)
