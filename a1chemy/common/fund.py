class FundTicks(object):

    def __init__(self, **kwargs) -> None:
        self.time = kwargs['time']
        self.amount = kwargs['amount']

    def to_dict(self):
        return {
            'time': self.time,
            'amount': self.amount
        }

class Fund(object):
    def __init__(self, **kwargs):
        self.exchange = kwargs.get('exchange', None)
        self.symbol = kwargs.get('symbol', None)
        self.name = kwargs.get('name', None)
        self.history = kwargs.get('history', None)
    
    def to_dict(self):
        return {
            'exchange': self.exchange,
            'symbol': self.symbol,
            'name': self.name,
            'history': [h.to_dict() for h in self.history]
        }