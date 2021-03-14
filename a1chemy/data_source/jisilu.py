import requests
import time
from a1chemy.common import FundTicks, Fund

class Jisilu(object):
    def __init__(self) -> None:
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.jisilu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.jisilu.cn/',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }

        response = requests.get('https://www.jisilu.cn/', headers=headers)
        self.cookies = response.cookies

    def get_fund_info(self, exchange=None, symbol=None, name=None, data=None):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.jisilu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.jisilu.cn/data/etf/detail/' + symbol[2:],
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }

        params = (
            ('___jsl', 'LST___t=' + str(int(time.time() * 1000.0))),
        )
        if data is None:
            data = {
                'is_search': '1',
                'fund_id': symbol[2:],
                'rp': '50',
                'page': '1'
            }
        else:
            data['fund_id'] = symbol[2:]
        response = requests.post('https://www.jisilu.cn/data/etf/detail_hists/', headers=headers, params=params, cookies=self.cookies, data=data)
        data = response.json()
        fund_history = [FundTicks(time=d['cell']['hist_dt'], amount=d['cell']['amount']) for d in reversed(data['rows'])]
        return Fund(exchange=exchange, symbol=symbol, history=fund_history)

    def get_lof_info(self, exchange=None, symbol=None, name=None, data=None):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.jisilu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.jisilu.cn/data/lof/hist_list/' + symbol[2:],
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }

        params = (
            ('___jsl', 'LST___t=' + str(int(time.time() * 1000.0))),
        )
        if data is None:
            data = {
                'rp': '500',
                'page': '1'
            }
        else:
            data['fund_id'] = symbol[2:]
        response = requests.post('https://www.jisilu.cn/data/lof/hist_list/' + symbol[2:], headers=headers, params=params, cookies=self.cookies, data=data)
        data = response.json()
        fund_history = [FundTicks(time=d['cell']['price_dt'], amount=d['cell']['amount']) for d in reversed(data['rows'])]
        return Fund(exchange=exchange, symbol=symbol, history=fund_history)