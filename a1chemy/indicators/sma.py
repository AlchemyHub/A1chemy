import pandas as pd


def sma(data: pd.Series, day: int):
    return data.rolling(day).mean()
