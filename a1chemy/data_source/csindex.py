import re

import requests
import xlrd
from bs4 import BeautifulSoup

from a1chemy.util import write_data_to_json_file


def download_and_parse_csi_xls(url, xls_path, target):
    pattern = re.compile('.*成份列表.*')
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'lxml')
    results = soup.find_all(text=pattern)
    xls_url = results[0].parent['href'] if len(results) is 1 else None
    print("xls_url=" + xls_url)
    f = requests.get(xls_url)
    with open(xls_path, "wb") as target_file:
        target_file.write(f.content)
    parse_csi_index_xls(source=xls_path, target=target)


def parse_csi_index_xls(source, target):
    data = xlrd.open_workbook(source)
    table = data.sheets()[0]
    result = []
    for i in range(1, table.nrows):
        row = table.row_values(i)
        exchange = 'SH' if row[7] == 'SHH' else 'SZ'
        d = {
            'symbol': exchange + row[4],
            'name': row[5]
        }
        result.append(d)
    write_data_to_json_file(data=result, path=target)


class CSIndex(object):
    pass
