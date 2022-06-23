import requests
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs

from a1chemy.common import INDEX
from a1chemy.common.ticks import Ticks
from a1chemy.common import Statistics


class XueQiuDataParser(object):
    cookies = {}

    def __init__(self, cookies=None):
        if cookies is not None:
            self.cookies = cookies
        else:
            h = {
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'cache-control': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xueqiu.com',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            }
            response = requests.get('https://xueqiu.com/', headers=h)
            self.cookies = response.cookies

    def get_all_stocks(self, params=None, headers=None, url=None, exchange_extractor=None):
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
        if url is None:
            url = 'https://xueqiu.com/service/v5/stock/screener/quote/list'
        response = requests.get(url, headers=headers, params=params, cookies=self.cookies)
        data = response.json()
        return [dict_to_statistics(d, exchange_extractor) for d in data['data']['list']]

    def list(self, size=1000, pid=13, category=1, headers=None):
        if headers is None:
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
                'Origin': 'https://xueqiu.com',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://xueqiu.com/',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            }

        params = (
            ('size', str(size)),
            ('pid', str(pid)),
            ('category', str(category)),
        )
        response = requests.get('https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json',
                                headers=headers, params=params, cookies=self.cookies)
        data = response.json()

        def dict_convert(d):
            exchange = d['exchange']
            if exchange == 'HK':
                exchange = 'HKEX'
            return Statistics(
                name=d['name'],
                symbol=d['symbol'],
                exchange=exchange
            )

        return [dict_convert(d) for d in data['data']['stocks']]

    def _history_request_data(self, headers=None, cookies=None, symbol: str = None, exchange=None, period: str = None,
                              count=672):
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
        return {
            'headers': headers,
            'params': params,
            'cookies': post_cookies
        }

    def async_history_request(self, headers=None, cookies=None, symbol: str = None, exchange=None, period: str = None,
                              count=672,
                              tz="Asia/Shanghai"):
        request_data = self._history_request_data(headers=headers, cookies=cookies, symbol=symbol, exchange=exchange,
                                                  period=period, count=count)
        return grequests.get('https://stock.xueqiu.com/v5/stock/chart/kline.json',
                             headers=request_data['headers'], params=request_data['params'],
                             cookies=request_data['cookies'])

    def history(self, headers=None, cookies=None, symbol: str = None, exchange=None, period: str = None, count=672,
                tz="Asia/Shanghai") -> Ticks:
        request_data = self._history_request_data(headers=headers, cookies=cookies, symbol=symbol, exchange=exchange,
                                                  period=period, count=count)
        response = requests.get('https://stock.xueqiu.com/v5/stock/chart/kline.json',
                                headers=request_data['headers'], params=request_data['params'],
                                cookies=request_data['cookies'])
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

    # def historys(self, headers=None, cookies=None, underlying_list=[], period: str = None, count=672,
    #             tz="Asia/Shanghai"):
    #     grequests_list = [self.async_history_request(headers=headers, cookies=cookies, symbol=underlying['symbol'], exchange=underlying['exchange'], period=period, count=count) for underlying in underlying_list]
    #     grequests_result_list = grequests.map(requests=grequests_list, size=10)
    #     history_list = []
    #     for data in grequests_result_list:
    #         try:
    #             symbol = parse_qs(urlparse(data.url).query)['symbol'][0]
    #             exchange = symbol[0:2]
    #             history_list.append(self._history_to_ticks(data=data.json(), exchange=exchange, symbol=symbol, tz=tz))
    #         except Exception as e:
    #             print("exception when get data, name=" + symbol)
    #     return history_list


    def _history_to_ticks(self, data, exchange, symbol, tz):
        column_name = data['data']['column'][:6]
        column_name[0] = INDEX
        items = data['data']['item']
        new_items = []
        for item in items:
            item[0] = pd.Timestamp(item[0] / 1000, unit='s', tz=tz)
            new_items.append(item[:6])

        return Ticks(exchange=exchange, symbol=symbol, currency='CNY',
                     raw_data=pd.DataFrame(data=new_items, columns=column_name))


def dict_to_statistics(data, exchange_extractor):
    s = Statistics(name=data['name'], symbol=data['symbol'],
                   exchange=data['symbol'][0:2])
    s.exchange = exchange_extractor(data['symbol'])
    return s
