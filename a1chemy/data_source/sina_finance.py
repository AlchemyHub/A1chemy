import requests
class SinaFinanceClient(object):

    def option_chain(self, symbol_list=None):
        """
        docstring https://finance.yahoo.com/quote/T/options/
        """

        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            'Referer': 'https://stock.finance.sina.com.cn/',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        }
        list_value = ",".join(symbol_list)
        response = requests.get('https://hq.sinajs.cn/list=' + list_value, headers=headers)
        

        pass