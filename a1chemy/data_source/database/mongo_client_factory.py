import pymongo
from .mongo_ticks import MongoTicks
from .mongo_tags import MongoTags
from .mongo_fund import MongoFund
default_mongo_client = pymongo.MongoClient(
            "mongodb://localhost:27017/", username='a1chemy', password='1B2C9046-E3CC-447F-9961-E125759BA44F')


def mongo_client_factory():
    return default_mongo_client

def tags_client():
    return MongoTags(mongo_client=mongo_client_factory())

def fund_client():
    return MongoFund(mongo_client=mongo_client_factory())

def ticks_client():
    return MongoTicks(mongo_client=mongo_client_factory())
