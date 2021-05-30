import operator
import datetime
from a1chemy.option.pricing import black_scholes
import numpy as np
import json


class Underlying(object):
    def __init__(self, price) -> None:
        self.price = price


class OptionConfig(object):
    def __init__(self, **kargs) -> None:
        self.interest_rate = kargs['interest_rate']
        self.pricing_model = kargs.get('pricing_model', black_scholes)


class Option(object):
    def __init__(self, redefine_greeks=False, **kargs):
        self.underlying = kargs['underlying']
        self.config = kargs['config']

        self.option_type = kargs['option_type']
        self.time_to_expire = kargs['time_to_expire']
        self.strike = kargs['strike']

        self.update(redefine_greeks=redefine_greeks, **kargs)

    def update(self, redefine_greeks=False, **kargs):
        self.price = kargs['price']
        self.iv = kargs.get('iv')
        self.delta = kargs.get('delta')
        self.gamma = kargs.get('gamma')
        self.theta = kargs.get('theta')
        self.vega = kargs.get('vega')
        self.rho = kargs.get('rho')

        if redefine_greeks:
            self.recalculate_greeks()

    def recalculate_greeks(self):
        underlying_price = self.underlying.price
        t = float(np.busday_count(
            datetime.date.today(), self.time_to_expire))/256
        # self.iv = euro_implied_vol(self.option_type, fs=current_price, x=self.strike, t=t, r=r, q=q, cp=self.price)
        # _, self.delta, self.gamma, self.theta, self.vega, self.rho = merton(self.option_type, fs=current_price, x=self.strike, t=t, r=r, q=q, v=self.iv)
        pricing_model = self.config.pricing_model
        cp = 1 if self.option_type == 'c' else -1
        try:
            self.iv = pricing_model.calculate_impv(self.price, underlying_price, self.strike, self.config.interest_rate, t, cp)
            if self.iv <= 0:
                self.iv = 0.0001
        except:
            self.iv = 0.0001
            print('get iv failed, set 0.0001 default,option: {} {}'.format(self.time_to_expire, self.strike))
        
        _, self.delta, self.gamma, self.theta, self.vega = pricing_model.calculate_greeks(underlying_price, self.strike, self.config.interest_rate, t, self.iv, cp)

    def toString(self):
        return 'expire:{} strike:{} type:{} iv:{} delta:{} gamma:{} theta:{} vega:{}'.format(self.time_to_expire, self.strike,  self.option_type, self.iv, self.delta, self.gamma, self.theta, self.vega)


class OptionStraddle(object):
    def __init__(self, strike) -> None:
        self.strike = strike
        self.call = None
        self.put = None

    def add_option(self, option: Option):
        if option.option_type == 'c':
            self.call = option
        else:
            self.put = option

    def get_option(self, option_type):
        if option_type == 'c':
            return self.call
        else:
            return self.put


class OptionChain(object):
    def __init__(self, time_to_expire):
        self.time_to_expire = time_to_expire
        self.straddles = []
        self.index = {}

    def add_option(self, option: Option):
        straddle = self.index.get(option.strike, None)
        if straddle is None:
            straddle = OptionStraddle(strike=option.strike)
            self.index[option.strike] = straddle
            self.straddles.append(straddle)
            self.straddles = sorted(
                self.straddles, key=operator.attrgetter('strike'))

        straddle.add_option(option=option)

    def get_option(self, strike, option_type):
        straddle = self.index.get(strike, None)
        if straddle is None:
            return None
        else:
            return straddle.get_option(option_type)


class OptionMap(object):
    def __init__(self):
        self.index = {}
        self.chains = []

    def add_option(self, option: Option):
        chain = self.index.get(option.time_to_expire)
        if chain is None:
            chain = OptionChain(time_to_expire=option.time_to_expire)
            self.chains.append(chain)
            self.chains = sorted(
                self.chains, key=operator.attrgetter('time_to_expire'))
            self.index[option.time_to_expire] = chain

        chain.add_option(option=option)

    def get_option(self, time_to_expire, strike, option_type):
        chain = self.index.get(time_to_expire, None)
        if chain is None:
            return None
        else:
            return chain.get_option(strike, option_type)
