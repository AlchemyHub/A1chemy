import csv
import pandas as pd
import numpy as np
import datetime
from scipy.stats import norm
import time
from scipy import stats
from math import exp, log, sqrt

"""
# 基于BS的定价模型
def get_price_bs(S0, K, r, T, iv, type):
    # 无股利欧式期权定价公式
    '''
    S0: 标的资产价格
    K: 执行价
    T: 合约到期剩余时间，构造函数会自动计算年化时间
    iv: 期权的隐含波动率
    type: call(1) or put(0)
    output：price 期权的理论价格
    '''
    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * iv ** 2) * T) / (iv * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * iv ** 2) * T) / (iv * sqrt(T))
    if type == 1:
        price = S0 * stats.norm.cdf(d1) - K * exp(-r * T) * stats.norm.cdf(d2)
    elif type == 0:
        price = K * exp(-r * T) * stats.norm.cdf(-d2) - S0 * stats.norm.cdf(-d1)
    return price
"""

# BSM广义定价公式构造函数
def get_price_bs(S0, K, r, T, v, call_put_type,option_type):
    '''
	bs定价
    input：
    S0: 标的资产价格
    K: 执行价
    T: Time To Maturity,到期时间(年化)
    b: 计算ETF股票期权，b值为0，计算商品期权b=0 ,r=0
    v: 期权的隐含波动率
    call_put_type: call(1) or put(0)
    option_type: 1为欧式股票期权，0为期货期权或远期期权
    output：price 期权的理论价格
    '''
    if option_type == 1:
        b = r
    elif option_type == 0:
        b = 0
        r = 0
    t = T/365
    S0 = float(S0)
    d1 = (log(S0 / K) + (b + 0.5 * v ** 2) * t) / (v * sqrt(t))
    d2 = (log(S0 / K) + (b - 0.5 * v ** 2) * t) / (v * sqrt(t))
    if call_put_type == 1:
        price = (S0 * exp((b - r) * t) * stats.norm.cdf(d1) - K * exp(-r * t) * stats.norm.cdf(d2))
    elif call_put_type == 0:
        price = K * exp(-r * t) * stats.norm.cdf(-d2) - (S0 * exp((b - r) * t) * stats.norm.cdf(-d1))
    return price



# 牛顿-拉夫森法计算隐含波动率种子值(初始值)
def init_implied_volatility(S0,K,r,T,type):
    """
    :param S0: 标的物价格
    :param K: 期权行权价
    :param r: 无风险利率
    :param T: 距离到期日剩余时间，注：构造函数会自主计算年化
    :param type: 1为欧式股票期权，0为期货期权或远期期权
    :return: init_iv 初始隐含波动率
    """
    if type == 1:
        t = T/365
        init_iv = sqrt(abs(log(S0/K)+r*t)*(2/t))

    elif type == 0:
        t = T/365
        init_iv = sqrt(abs(log(S0/K))*(2/t))

    return init_iv

def calculate_vega(S0,K,r,T,iv):
    """
    :param S0: 标的物价格
    :param K: 行权价
    :param r: 无风险利率
    :param T: 到期日剩余日期，构造函数自动转换为年化
    :param iv: 期权隐含波动率
    :return:
    """
    if iv < 0:
        return 0
    t = T/365

    d1 = (log(S0 / K) + (0.5 * iv ** 2) * t) / (iv * sqrt(t))
    vega = S0 * exp(-r * t) * stats.norm.pdf(d1) * sqrt(t)

    return vega

# 牛顿-拉夫森法迭代隐含波动率
def newton_raphson_method(S0, price,K, r, T, epsilon,call_put_type,option_type):
    """

    :param S0: 标的物价格
    :param price: 期权的市场价格
    :param K: 期权行权价
    :param r: 无风险利率
    :param b: 计算ETF股票期权，b值为0，计算商品期权b=0 ,r=0
    :param T: 到期日剩余时间，构造函数会自动转换为年化
    :param epsilon: 期望精度
    :param call_put_type: call为1，put为0
    :param option_type: 1为欧式股票期权，0为期货期权或远期期权
    :return: result_iv
    """

    # 检查期权价格为正数
    if price <= 0:
        return 0

    # 检查期权价格高于其空间价值
    meet: bool = False
    t = T/365
    if call_put_type == 1 and (price > S0 - K * exp(-r * t)):
        meet = True

    elif call_put_type == 0 and (price > K * exp(-r * t) - S0):
        meet = True

    # 如果不满足，则返回0
    if not meet:
        return 0

    # 计算马纳斯特--科勒初始值(隐含波动率种子值)
    result_iv = init_implied_volatility(S0=S0,K=K,r=r,T=T,type=option_type)
    # 基于牛顿法或牛顿-拉夫森法计算隐含波动率
    # 当牛顿-拉夫森计算无法收敛隐含波动率估计值，则牛顿法迭代50次去收敛，获得隐含波动率估计值
    for i in range(1000):
        # 限制隐含波动率数值最小为1%
        result_iv = max(result_iv,0.01)

        # 计算本轮理论价和vega
        theory_price = float(get_price_bs(S0, K, r, T, result_iv, call_put_type,option_type))
        vega = calculate_vega(S0,K,r,T,result_iv)

        # 如果vega过小(或者为0)，则退出循环
        if not vega or vega < epsilon:
            break

        # 计算本轮误差值
        minDiff = (price - theory_price) / vega

        # 检查误差值是否满足精度要求
        if abs(minDiff) < epsilon:
            break

        # 计算新一轮隐含波动率的估计值
        result_iv += minDiff

    # 保留四位小数
    result_iv = round(result_iv,4)

    return result_iv


# 希腊值
# string: 'c'-- call; 'p'-- put
# S: 股票价格
# X: 期权的行权价格
# T: 距离到期的年化时间
# r: 无风险利率
# b: 持有成本率 (b=r:无股利欧式期权定价公式； b=r-q: 连续股利欧式期权定价公式；
#              b=0：期货期权定价公式； b=r=0：权利金计息下的期货期权定价公式； b=r-rf: 外汇期权定价公式）
# cm: 期权的市场价格
# eps: 期望精度
# v: 波动率 （将参数v改成cm,eps后，第一行代码可以计算出隐含波动率）
def greeks(string, S, X, T, r, b, v):
    # v = vol(string, S, X, T, r, b, cm, eps)
    d1 = (np.log(S / X) + (b + pow(v, 2) / 2) * T) / (v * np.sqrt(T))
    d2 = d1 - v * np.sqrt(T)
    if string == 'c':
        delta = np.exp((b - r) * T) * norm.cdf(d1)
        delta = round(delta, 4)
        theta = -(S * np.exp((b - r) * T) * norm.pdf(d1) * v) / (2 * np.sqrt(T)) - (b - r) * S * np.exp((b - r) * T) * norm.cdf(d1) - r * X * np.exp(-r * T) * norm.cdf(d2)
        theta = round(theta, 4)
        rho = T * X * np.exp(-r * T) * norm.cdf(d2)
        rho = round(rho, 4)
    else:
        delta = np.exp((b - r) * T) * (norm.cdf(d1) - 1)
        delta = round(delta, 4)
        theta = -(S * np.exp((b - r) * T) * norm.pdf(d1) * v) / (2 * np.sqrt(T)) + (b - r) * S * np.exp((b - r) * T) * norm.cdf(-d1) + r * X * np.exp(-r * T) * norm.cdf(-d2)
        theta = round(theta, 4)
        rho = -T * X * np.exp(-r * T) * norm.cdf(-d2)
        rho = round(rho, 4)

    gamma = (norm.pdf(d1) * np.exp((b - r) * T)) / (S * v * np.sqrt(T))
    gamma = round(gamma, 4)
    vega = S*np.exp((b-r)*T)*norm.pdf(d1)*np.sqrt(T)
    vega = round(vega, 4)
    return [delta, theta, gamma, vega, rho]


# time_to_expiry = datetime.date.fromisoformat('2021-07-28')
# # t = (float(np.busday_count(
# #             datetime.date.today(), )) + time_diff)/256
# # t = float(np.busday_count(
# #             datetime.date.today(), time_to_expiry))
# t = float((time_to_expiry - datetime.date.today()).days)
# print('{}'.format(t))
# # new_t = float(np.busday_count(
# #             datetime.date.today(), time_to_expiry))/256
# iv = newton_raphson_method(S0=5.1260, price=0.0738, K=5.25, r=0.03, T=t, epsilon=0.001, call_put_type=1, option_type=1)
# print('{}'.format(iv))
# greeks(string='c', S=5.1260, X=5.25, T=t / 365, r=0.03, b=0, v=iv)
