import re

import requests
import xlrd
from bs4 import BeautifulSoup

from a1chemy.util import write_data_to_json_file


headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
}


def get_cookies():
    response = requests.get('http://www.csindex.com.cn/', headers=headers)
    return response.cookies

def download_csi_xls(url, xls_path):
    cookies = get_cookies()
    f = requests.get(url, headers=headers, cookies=cookies, verify=False)
    with open(xls_path, "wb") as target_file:
        target_file.write(f.content)

def download_csi_sectors_xls(url, xls_path):
    pattern = re.compile('.*中证行业分类表.*')
    cookies = get_cookies()
    html_page = requests.get(url, headers=headers, cookies=cookies, verify=False)
    soup = BeautifulSoup(html_page.content, 'lxml')
    results = soup.find_all(text=pattern)
    xls_url = results[0].parent['href'] if len(results) is 1 else None
    print("xls_url=" + xls_url)
    f = requests.get(xls_url, headers=headers, cookies=cookies, verify=False)
    with open(xls_path, "wb") as target_file:
        target_file.write(f.content)

def parse_csi_xls_file(source):
    data = xlrd.open_workbook(source)
    table = data.sheets()[0]
    result = []
    for i in range(1, table.nrows):
        row = table.row_values(i)
        exchange = 'SH' if row[7] == 'SHH' else 'SZ'
        d = {
            'exchange': exchange,
            'symbol': exchange + row[4],
            'name': row[5]
        }
        result.append(d)
    return result

def parse_csi_xls_file_and_write_to_file(source, target):
    result = parse_csi_xls_file(source=source)
    write_data_to_json_file(data=result, path=target)

class CSIndex(object):
    pass
