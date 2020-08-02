import pandas as pd


def ema(data: pd.Series, day: int):
    return data.ewm(span=day, min_periods=0, adjust=False, ignore_na=False).mean()
