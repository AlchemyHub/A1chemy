import requests
import json

class BinanceClient(object):
    def __init__(self) -> None:
        self.headers = {
            'authority': 'www.binance.com',
            'x-trace-id': 'c829406a-6c1f-45b6-a55a-cec1bb858ad1',
            'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
            'x-ui-request-trace': 'c829406a-6c1f-45b6-a55a-cec1bb858ad1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'zh-CN',
            'fvideo-id': '31b3fe32b4dba62987d3203e5ad881d76b6fef2a',
            'sec-ch-ua-mobile': '?0',
            'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjI1NjAsMTQ0MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjI1NjAsMTM1MiIsInN5c3RlbV92ZXJzaW9uIjoiTWFjIE9TIDEwLjE1LjciLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6ImVuIiwidGltZXpvbmUiOiJHTVQrOCIsInRpbWV6b25lT2Zmc2V0IjotNDgwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTVfNykgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkyLjAuNDUxNS4xNTkgU2FmYXJpLzUzNy4zNiIsImxpc3RfcGx1Z2luIjoiQ2hyb21lIFBERiBQbHVnaW4sQ2hyb21lIFBERiBWaWV3ZXIsTmF0aXZlIENsaWVudCIsImNhbnZhc19jb2RlIjoiYTMxMWNjZTEiLCJ3ZWJnbF92ZW5kb3IiOiJJbnRlbCBJbmMuIiwid2ViZ2xfcmVuZGVyZXIiOiJJbnRlbCBJcmlzIFBybyBPcGVuR0wgRW5naW5lIiwiYXVkaW8iOiIxMjQuMDQzNDc2NTc4MDgxMDMiLCJwbGF0Zm9ybSI6Ik1hY0ludGVsIiwid2ViX3RpbWV6b25lIjoiQXNpYS9TaGFuZ2hhaSIsImRldmljZV9uYW1lIjoiQ2hyb21lIFY5Mi4wLjQ1MTUuMTU5IChNYWMgT1MpIiwiZmluZ2VycHJpbnQiOiIxYjJlNDcxMmQ0MTE2MjMyNzRmM2JmY2UyZWYwNDkwNSIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IiJ9',
            'bnc-uuid': 'bde6dfb0-cafa-4be3-988d-9cc313cddf26',
            'clienttype': 'web',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'accept': '*/*',
            'origin': 'https://www.binance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en'
        }
        main_page_response = requests.get('https://www.binance.com/', headers=self.headers)
        self.cookies = main_page_response.cookies

    def fund_rating(self, symbol):
        data = {
            "symbol": symbol,
            "page":1,
            "rows":10000
        }
        response = requests.post('https://www.binance.com/bapi/futures/v1/public/future/common/get-funding-rate-history', headers=self.headers, cookies=self.cookies, data=json.dumps(data))
        return response.json()