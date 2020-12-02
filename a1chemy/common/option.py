import operator


class Option(object):
    def __init__(self, **kargs):
        self.date = kargs['date']
        self.strike = kargs['strike']
        self.price = kargs['price']
        self.right = kargs['right']


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
