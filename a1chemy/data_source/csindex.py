import json

import xlrd


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
    json_data = json.dumps(result, ensure_ascii=False)
    fh = open(target, 'w', encoding='utf-8')
    fh.write(json_data)
    fh.close()


class CSIndex(object):
    pass
