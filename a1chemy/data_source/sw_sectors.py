import re

from a1chemy.util import write_data_to_json_file


def parse_sw_sectors(source, target):
    fd = open(source)
    li = fd.readlines()
    print(len(li))
    result = []
    for i in range(1, len(li) - 1):
        row_data = re.split('<|>', li[i])
        symbol_suffix = row_data[8]
        exchange = 'SH' if symbol_suffix.startswith('600') or symbol_suffix.startswith(
            '601') or symbol_suffix.startswith('603') else 'SZ'
        result.append(
            {
                'symbol': exchange + symbol_suffix,
                'sector': row_data[4],
                'name': row_data[12]
            }
        )
    print("total row data length:" + str(len(result)))
    write_data_to_json_file(data=result, path=target)
