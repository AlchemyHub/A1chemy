import pandas as pd

from a1chemy.common import OPEN, CLOSE, HIGH, LOW, AMOUNT, VOLUME


class Stock(object):
    exchange = ''
    name = ''
    currency = ''
    __raw_data: pd.DataFrame

    def get_column_data(self, key: str):
        return self.__raw_data[key]

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
