import requests
import pandas as pd
import time

from a1chemy.common import INDEX
from a1chemy.common.ticks import Ticks
from a1chemy.common import Statistics


class XueQiuDataParser(object):
    cookies = {}

    def __init__(self, cookies=None, headers=None):
        if cookies is not None:
            self.cookies = cookies
        else:
            self.cookies = {
                'bid': '783ea5e048552adebcc2fb818cf94d7a_k3l4dhqh',
                'device_id': '8c96397a28a84671916e3a10765b3b41',
                'remember': '1',
                'xq_a_token': 'f972669f35f84421759fc9a83064e421b241699e',
                'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjkzMDk1ODc2OTgsImlzcyI6InVjIiwiZXhwIjoxNTk4MTc1NDAwLCJjdG0iOjE1OTU2NTQ5MjIzNjIsImNpZCI6ImQ5ZDBuNEFadXAifQ.Wy1Mk7nLW58sLAkQgVcL7TfTWuQUk0BlV78pDxYQO5QRFqD3UTgGQfy7CRNpkbdJxjw8tUH5xdnpUIAcDaEVqMdt4yqQ26odGoBvsyhXpA7oSTjiLVrzvkHuMBj9DrAiIasXvt62PI_TuBzLYbr-0NYuhEwxTfO_kVPjVEtx_C5T-9Hx8WeejJMH3q4VGaN0A87KYvsP2TYU086bLbU6DgprozPYKF2DRFVXtSneyHurbtZVfdd8xxlRzXli_SQeOqpzl_LdDzG_3Aig-v3iW2ZNadbKLSgd5RnAHv4KVYFL9-rO-WB0fteFhhhJ-7-ipph96fa8QU7jzYV7fJwXhg',
                'xqat': 'f972669f35f84421759fc9a83064e421b241699e',
                'xq_r_token': '166d455e8c8f9bf3e6a41873d6d9aeff8a1a378f',
                'xq_is_login': '1',
                'u': '9309587698',
                's': 'do1967dh94',
                # 'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1595653582,1595756736,1595758371,1595758396',
                'is_overseas': '0',
                # 'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1595772143',
            }

    def get_all_stocks(self, page=1, size=5000, headers=None):
        if headers is None:
            headers = {
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'cache-control': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xueqiu.com/hq',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            }
        params = (
            ('page', page),
            ('size', size),
            ('order', 'desc'),
            ('orderby', 'percent'),
            ('order_by', 'percent'),
            ('market', 'CN'),
            ('type', 'sh_sz'),
            ('_', str(int(round(time.time() * 1000)))),
        )
        response = requests.get('https://xueqiu.com/service/v5/stock/screener/quote/list',
                                headers=headers, params=params, cookies=self.cookies)
        data = response.json()
        return [dict_to_statistics(d) for d in data['data']['list']]

    def history(self, headers=None, cookies=None, symbol: str = None, exchange=None, period: str = None, count=672,
                tz="Asia/Shanghai") -> Ticks:
        if headers is None:
            headers = {
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Origin': 'https://xueqiu.com',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': f'https://xueqiu.com/S/{symbol}',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            }

        params = (
            ('symbol', symbol),
            ('begin', str(int(time.time() * 1000.0))),
            ('period', period),
            ('type', 'before'),
            ('count', str(0 - count)),
            ('indicator', 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'),
        )

        post_cookies = cookies if cookies is not None else self.cookies
        response = requests.get('https://stock.xueqiu.com/v5/stock/chart/kline.json',
                                headers=headers, params=params, cookies=post_cookies)
        data = response.json()
        column_name = data['data']['column'][:6]
        column_name[0] = INDEX
        items = data['data']['item']
        new_items = []
        for item in items:
            item[0] = pd.Timestamp(item[0] / 1000, unit='s', tz=tz)
            new_items.append(item[:6])

        return Ticks(exchange=exchange, symbol=symbol, currency='CNY',
                     raw_data=pd.DataFrame(data=new_items, columns=column_name))


def dict_to_statistics(data):
    return Statistics(name=data['name'], symbol=data['symbol'], exchange=data['symbol'][0:2])
