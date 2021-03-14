import pymongo
import a1chemy.data_source as data_source
from tqdm import tqdm
import random
import time
from a1chemy.common import Tag
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

cookies = {
    'device_id': '8c96397a28a84671916e3a10765b3b41',
    's': 'do1967dh94',
    'bid': '783ea5e048552adebcc2fb818cf94d7a_ki4lux2p',
    'remember': '1',
    'xq_a_token': '0be089f1b018e43e5cf4262b9095e0e2f9825a7a',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjkzMDk1ODc2OTgsImlzcyI6InVjIiwiZXhwIjoxNjE2ODIxOTYyLCJjdG0iOjE2MTQyNjU1ODQxNDksImNpZCI6ImQ5ZDBuNEFadXAifQ.lI3sXiFv1Nxb4rs0-9x9iXqjV_83TARi_HaMT0n821xppoHSnckiHFeuD7rJo0H0eHXiUQ4xZboDxEIWHy2cfWQ2xynbcTtNk3C3odcI5dBYZf1GGm2BaLYw4DZzeUVsG3LJPbmXdGWlRwS9dQZxwMi14wXnXNldvj3u7CDFiFkwFKDQE4ss7ozB0sHBcNwb-me6mTL9TyTzQt48FweEgOtmc4VQ35iNjkaBXpvRI81AvvFXzAUIXmX6pzQ61Fru4sjqG49hDIcdxoSFlPaN9DrLrkQZ2EmBjRdgaOGNSR6xUYc1dw6V0YS3BP_OoGgoAh2HbbVvIlGlw02hknmrqQ',
    'xqat': '0be089f1b018e43e5cf4262b9095e0e2f9825a7a',
    'xq_r_token': '1632327c73c2b2412669e8fa864ac81d27831b78',
    'xq_is_login': '1',
    'u': '9309587698',
    'is_overseas': '0',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1612363687,1612552532,1613748264,1614512799',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1614512804',
}

xueqiu_client = data_source.XueQiuDataParser(cookies=cookies)

grabListData(pid=5, tag_id='ZH_ETF')
grabListData(pid=13, tag_id='TOP')
grabListData(pid=14, tag_id='CASH_COW')
grabListData(pid=11, tag_id='ZH_STOCK')