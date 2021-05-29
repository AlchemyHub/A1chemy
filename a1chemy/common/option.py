import operator
import datetime
from a1chemy.util.option_greeks_calculator import merton, euro_implied_vol
import numpy as np

class Underlying(object):
    def __init__(self, price) -> None:
        self.price = price


class Option(object):
    def __init__(self, redefine_greeks=False, **kargs):
        self.underlying= kargs['underlying']

        self.option_type = kargs['option_type']
        self.date = kargs['date']
        self.strike = kargs['strike']
        self.price = kargs['price']

        self.iv = kargs.get('iv')
        self.delta = kargs.get('delta')
        self.gamma = kargs.get('gamma')
        self.theta = kargs.get('theta')
        self.vega = kargs.get('vega')
        self.rho = kargs.get('rho')

    def recalculate_greeks(self, r, q):
        current_price = self.underlying.price
        t = float(np.busday_count( datetime.date.today(), self.date))/256
        self.iv = euro_implied_vol(self.option_type, fs=current_price, x=self.strike, t=t, r=r, q=q, cp=self.price)
        _, self.delta, self.gamma, self.theta, self.vega, self.rho = merton(self.option_type, fs=current_price, x=self.strike, t=t, r=r, q=q, v=self.iv)
        

class OptionChain(object):
    def __init__(self, date):
        self.date = date
        self.straddles = []
        self.index = {}

    def add(self, strike, call, put):
        straddle = (strike, call, put)
        self.straddles.append(straddle)
        self.straddles = sorted(self.straddles, key=operator.itemgetter(0))
        self.index[strike] = straddle


class OptionMap(object):
    def __init__(self):
        self.index = {}
        self.chains = []

    def add(self, date, chain):
        self.chains.append(chain)
        self.chains = sorted(self.chains, key=lambda c: c.date)
        self.index[date] = chain
