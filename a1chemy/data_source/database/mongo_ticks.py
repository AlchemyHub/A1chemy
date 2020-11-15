from a1chemy.common.ticks import Ticks


class MongoTicks(object):
    mongo_client = None
    db = None
    ticks_collection = None

    def __init__(self, mongo_client) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client["a1chemy"]
        self.ticks_collection = self.db['ticks']

    def upsert(self, exchange: str, symbol: str, ticks: Ticks):
        """
        upsert ticks by exchange and symbol
        """
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange

        new_value = {'$set': ticks.to_dict()}
        return self.ticks_collection.update_one(query, new_value, upsert=True)

    def delete(self, exchange: str, symbol: str):
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange
        return self.ticks_collection.delete_many(query)

    def find_one(self, exchange, symbol) -> Ticks:
        query = {
            'symbol': symbol
        }
        if exchange is not None:
            query['exchange'] = exchange
        return Ticks.from_dict(self.ticks_collection.find_one(query))

    def find(self, query):
        data = self.ticks_collection.find(query)
        return [Ticks.from_dict(d) for d in data]
