import requests
import json
import datetime
from a1chemy.common import Option, OptionChain, Underlying, OptionConfig, OptionMap

class EastMoneyClient(object):
    def __init__(self) -> None:
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://quote.eastmoney.com/',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }

        main_page_response = requests.get('https://www.eastmoney.com/', headers=self.headers)
        self.cookies = main_page_response.cookies

    def get_option_data(self, underlying, config, option_map, symbol, time_to_expiry, filter_strike=False):
        params = (
            ('cb', 'jQuery112409759288850343608_1622469571884'),
            ('secid', '1.' + symbol[2:]),
            ('exti', '{}{:02d}'.format(time_to_expiry.year, time_to_expiry.month)),
            ('spt', '9'),
            ('fltt', '2'),
            ('invt', '2'),
            ('np', '1'),
            ('ut', 'bd1d9ddb04089700cf9c27f6f7426281'),
            ('fields', 'f1,f2,f3,f4,f5,f12,f13,f14,f108,f152,f161,f249,f250,f330,f334,f339,f340,f341,f342,f343,f344,f345,f346,f347'),
            ('fid', 'f161'),
            ('pn', '1'),
            ('pz', '100'),
            ('po', '0'),
            ('_', '1622469571889'),
        )
        print('secid:{} ,exti:{}'.format(params[1][1], params[2][1]))
        response = requests.get('http://13.push2.eastmoney.com/api/qt/slist/get', headers=self.headers, params=params, cookies=self.cookies, verify=False)
        data = json.loads(response.text.replace(params[0][1], '')[1:-2])['data']['diff']
        for item in data:
            strike = item['f161']
            if filter_strike and not (strike*20).is_integer():
                continue
            option_map.add_or_update_option(underlying=underlying, config=config, option_type='c', time_to_expiry=time_to_expiry, strike=strike, price=item['f2'])
            option_map.add_or_update_option(underlying=underlying, config=config, option_type='p', time_to_expiry=time_to_expiry, strike=strike, price=item['f341'])