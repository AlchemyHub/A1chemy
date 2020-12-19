from a1chemy.common.ticks import Ticks
from a1chemy.common.fund import Fund, FundTicks

class MongoFund(object):
    def __init__(self, mongo_client) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client["a1chemy"]
        self.fund_collection = self.db['fund']

    def upsert(self, exchange: str, symbol: str, fund: Fund): 
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange

        new_value = {'$set': fund.to_dict()}
        return self.fund_collection.update_one(query, new_value, upsert=True)

    def delete(self, exchange: str, symbol: str):
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange
        return self.fund_collection.delete_many(query)

    def find_one(self, exchange, symbol) -> Ticks:
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange
        return dict_to_fund(self.fund_collection.find_one(query))

    def find(self, query):
        data = self.fund_collection.find(query)
        return [dict_to_fund(d) for d in data]
    

def dict_to_fund(data):
    fund_history = [FundTicks(time=d.get('time', None), amount=d.get('amount', None)) for d in data.get('history', None)]
    return Fund(exchange=data.get('exchange', None), symbol = data.get('symbol', None), history=fund_history)