import requests
import re
import datetime
from a1chemy.common import Option, OptionChain, Underlying, OptionConfig, OptionMap


class SinaFinanceClient(object):



    def add_option_to_option_map(self, option_map, underlying, config, option_data):
        option_type = option_data[45].lower()
        time_to_expiry = datetime.date.fromisoformat(option_data[46])
        strike = float(option_data[7])
        price = float(option_data[2])
        option = option_map.get_option(
            time_to_expiry=time_to_expiry, strike=strike, option_type=option_type)
        if option is None:
            option = Option(redefine_greeks=True,
                            underlying=underlying,
                            config=config,
                            option_type=option_type,
                            time_to_expiry=time_to_expiry,
                            strike=strike,
                            price=price
                            )
            option_map.add_option(option)
        else:
            option.update(redefine_greeks=True, price=price)
        return option

    def get_options(self, symbols=None):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': 'https://stock.finance.sina.com.cn/',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }

        response = requests.get(
            'https://hq.sinajs.cn/list=' + ','.join(symbols), headers=headers)
        return sina_finance_result_parser(response.text)

    def get_option_chain(self, symbol, year, month):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': 'https://stock.finance.sina.com.cn/',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }
        call_list_name = 'OP_UP_{}{}{:02d}'.format(symbol[2:], year, month)
        put_list_name = 'OP_DOWN_{}{}{:02d}'.format(symbol[2:], year, month)
        underlying_name = 's_{}'.format(symbol.lower())
        response = requests.get('https://hq.sinajs.cn/list=' + ','.join(
            [call_list_name, put_list_name, underlying_name]), headers=headers)
        chain_data = sina_finance_result_parser(response.text)
        return {
            'keys': {
                'underlying': underlying_name,
                'call': call_list_name,
                'put': put_list_name
            },
            'data': chain_data
        }

    def get_option_map(self, option_map, symbol, year, month, config):
        chain = self.get_option_chain(symbol=symbol, year=year, month=month)
        chain_data = chain['data']
        underlying_price = float(chain_data[chain['keys']['underlying']][1])
        underlying = Underlying(price=underlying_price)

        call_list_name = chain['keys']['call']
        put_list_name = chain['keys']['put']
        option_symbol_list = chain_data[call_list_name] + \
            chain_data[put_list_name]
        option_data_map = self.get_options(symbols=option_symbol_list)

        for symbol, o in option_data_map.items():
            option = self.add_option_to_option_map(
                option_map, underlying, config, o)

        return option_map


def sina_finance_result_parser(data):
    values = data.replace('\n', '').strip().split(';')
    result = {}
    for v in values:
        if len(v) <= 0:
            continue
        tmp = re.split('=|"', v)
        result[tmp[0][11:]] = tmp[2].split(',')
    return result