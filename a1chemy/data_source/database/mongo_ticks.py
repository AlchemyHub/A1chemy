from a1chemy.common.constants import INDEX
from a1chemy.common.ticks import Ticks
import pandas as pd
import pymongo


class MongoTicks(object):

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

    def bulk_upsert(self, ticks_list=[]):
        upsert_list = []
        for ticks_data in ticks_list:
            query = {
                'symbol': ticks_data['symbol']
            }
            exchange = ticks_data.get('exchange')
            if exchange is not None:
                query['exchange'] = exchange
            new_value = {'$set': ticks_data['ticks'].to_dict()}
            ticks_update_one = pymongo.UpdateOne(query, new_value, upsert=True)
            upsert_list.append(ticks_update_one)
        return self.ticks_collection.bulk_write(upsert_list)

    def delete_multiple(self, symbols=[]):
        query = {
            'symbol': {
                '$in': symbols
            }
        }
        return self.ticks_collection.delete_many(query)

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
        return ticks_wrapper(self.ticks_collection.find_one(query))

    def find(self, query):
        data = self.ticks_collection.find(query)
        return [ticks_wrapper(d) for d in data]


def ticks_wrapper(data):
    ticks = Ticks.from_dict(data)
    ticks.raw_data[INDEX] = pd.to_datetime(
        ticks.raw_data[INDEX], unit='s').dt.tz_localize('Europe/London')
    return ticks
