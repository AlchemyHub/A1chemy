import xlrd

from a1chemy.util import write_data_to_json_file


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
