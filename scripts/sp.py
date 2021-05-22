import pymongo
import a1chemy.data_source as data_source
from tqdm import tqdm
import random
import time
from a1chemy.common import Tag
from a1chemy.util import json_util
import json

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/", username='a1chemy', password='1B2C9046-E3CC-447F-9961-E125759BA44F')
mongo_ticks_client = data_source.MongoTicks(mongo_client=mongo_client)
mongo_tag_client = data_source.MongoTags(mongo_client=mongo_client)
mongo_fund = data_source.MongoFund(mongo_client=mongo_client)


xueqiu_client = data_source.XueQiuDataParser()
jisilu_client = data_source.Jisilu()

def grabNationData(nation_tag_id, params, url, exchange_extractor):
    mongo_tag_client.tags_collection.delete_many({'parent':nation_tag_id})
    all_stocks=xueqiu_client.get_all_stocks(params=params, url=url, exchange_extractor=exchange_extractor)
    print("stocks size=" + str(len(all_stocks)))
    nation_tag = Tag(id=nation_tag_id, parent=None)
    mongo_tag_client.insert(tag=nation_tag)
    for stock in tqdm(all_stocks):
        values = {
            'symbol': stock.symbol,
            'exchange': stock.exchange
        }
        #print("stock_info, exchange={}, symbol={}".format(stock.exchange, stock.symbol))
        tag = Tag(id=stock.to_tag_id(), parent=nation_tag.id, values=values)
        mongo_tag_client.insert(tag=tag)
        #print("tag: id={}, parent={}, values={}".format(tag.id, tag.parent, values))

def grabListData(pid, tag_id):
    mongo_tag_client.tags_collection.delete_many({'parent':tag_id})
    all_stocks=xueqiu_client.list(pid=pid)
    print("stocks size=" + str(len(all_stocks)))
    list_tag = Tag(id=tag_id, parent=None)
    mongo_tag_client.insert(tag=list_tag)
    for stock in tqdm(all_stocks):
        values = {
            'symbol': stock.symbol,
            'exchange': stock.exchange
        }
        #print("stock_info, exchange={}, symbol={}".format(stock.exchange, stock.symbol))
        tag = Tag(id=stock.to_tag_id(), parent=list_tag.id, values=values)
        mongo_tag_client.insert(tag=tag)
        #print("tag: id={}, parent={}, values={}".format(tag.id, tag.parent, values))

def grabTicksData(nation_tag_id, params, url, exchange_extractor):
    all_stocks=xueqiu_client.get_all_stocks(params=params, url=url, exchange_extractor=exchange_extractor)
    for stock in tqdm(all_stocks):
        try:
#             time.sleep(random.uniform(0.1,0.3))
            stock_ticks = xueqiu_client.history(symbol=stock.symbol, exchange=stock.exchange, period = 'day')
            stock_ticks.name = stock.name
            mongo_ticks_client.delete(exchange=None, symbol=stock.symbol)
            mongo_ticks_client.upsert(exchange=stock.exchange, symbol=stock.symbol, ticks=stock_ticks)
        except Exception as e:
            print("exception when get data, name=" + stock.name)
            
def grabFundData(nation_tag_id, params, url, exchange_extractor):
    all_stocks=xueqiu_client.get_all_stocks(params=params, url=url, exchange_extractor=exchange_extractor)
    for stock in tqdm(all_stocks):
        try:
#             time.sleep(random.uniform(0.1,0.3))
            fund_data = jisilu_client.get_fund_info(symbol=stock.symbol, exchange=stock.exchange, name=stock.name)
            mongo_fund.delete(exchange=None, symbol=fund_data.symbol)
            mongo_fund.upsert(exchange=fund_data.exchange, symbol=fund_data.symbol, fund=fund_data)
        except Exception as e:
            print("exception when get data, name=" + stock.name)
            print(e)
def grabLofData(nation_tag_id, params, url, exchange_extractor):
    all_stocks=xueqiu_client.get_all_stocks(params=params, url=url, exchange_extractor=exchange_extractor)
    for stock in tqdm(all_stocks):
        try:
#             time.sleep(random.uniform(0.1,0.3))
            fund_data = jisilu_client.get_lof_info(symbol=stock.symbol, exchange=stock.exchange, name=stock.name)
            mongo_fund.delete(exchange=None, symbol=fund_data.symbol)
            mongo_fund.upsert(exchange=fund_data.exchange, symbol=fund_data.symbol, fund=fund_data)
        except Exception as e:
            print("exception when get data, name=" + stock.name)
            print(e)

cn_stock_params = (
            ('page', 1),
            ('size', 5000),
            ('order', 'desc'),
            ('orderby', 'percent'),
            ('order_by', 'percent'),
            ('market', 'CN'),
            ('type', 'sh_sz'),
            ('_', str(int(round(time.time() * 1000)))),
        )
hk_stock_params = (
            ('page', 1),
            ('size', 5000),
            ('order', 'desc'),
            ('orderby', 'percent'),
            ('order_by', 'percent'),
            ('market', 'HK'),
            ('type', 'hk'),
            ('_', str(int(round(time.time() * 1000)))),
        )
cn_etf_params = (
    ('type', '18'),
    ('parent_type', '1'),
    ('order', 'desc'),
    ('order_by', 'percent'),
    ('page', '1'),
    ('size', '1000'),
    ('_', str(int(round(time.time() * 1000)))),
)
cn_lof_params = (
    ('type', '19'),
    ('parent_type', '1'),
    ('order', 'desc'),
    ('order_by', 'percent'),
    ('page', '1'),
    ('size', '1000'),
    ('_', str(int(round(time.time() * 1000)))),
)

etf_url='https://xueqiu.com/service/v5/stock/screener/fund/list'

cookies = json_util.read_json_from_file('/Users/line/workspace/freedom/A1chemy/data/xueqiu_cookies.json')
print(cookies)

grabNationData(nation_tag_id='cn_etf', params=cn_etf_params, url=etf_url, exchange_extractor=lambda x:x[0:2])
grabTicksData(nation_tag_id='cn_etf', params=cn_etf_params, url=etf_url, exchange_extractor=lambda x:x[0:2])
grabNationData(nation_tag_id='cn_lof', params=cn_lof_params, url=etf_url, exchange_extractor=lambda x:x[0:2])
grabTicksData(nation_tag_id='cn_lof', params=cn_lof_params, url=etf_url, exchange_extractor=lambda x:x[0:2])

grabFundData(nation_tag_id='cn_etf', params=cn_etf_params, url=etf_url, exchange_extractor=lambda x:x[0:2])
grabLofData(nation_tag_id='cn_lof', params=cn_lof_params, url=etf_url, exchange_extractor=lambda x:x[0:2])

grabNationData(nation_tag_id='cn_stock', params=cn_stock_params, url=None, exchange_extractor=lambda x:x[0:2])
grabTicksData(nation_tag_id='cn_stock', params=cn_stock_params, url=None, exchange_extractor=lambda x:x[0:2])
grabNationData(nation_tag_id='hk_stock', params=hk_stock_params, url=None, exchange_extractor=lambda x:'HKEX')
grabTicksData(nation_tag_id='hk_stock', params=hk_stock_params, url=None, exchange_extractor=lambda x:'HKEX')


xueqiu_client = data_source.XueQiuDataParser(cookies=cookies)

grabListData(pid=5, tag_id='ZH_ETF')
grabListData(pid=13, tag_id='TOP')
grabListData(pid=14, tag_id='CASH_COW')
grabListData(pid=11, tag_id='ZH_STOCK')
