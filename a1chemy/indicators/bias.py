import pandas as pd
import numpy as np


def _cal(row, aKey, bKey):
    a = row[aKey]
    b = row[bKey]
    if a == None or a == np.nan or b == None or b == np.nan:
        return np.nan
    return (a - b) / b


def bias(data: pd.DataFrame, n: str, d: str):
    """
    name 曲线名
    n numerator 分子
    d denominator 分母
    """
    return data.apply(lambda row: _cal(row, n, d), axis=1)
