import re

from a1chemy.util import write_data_to_json_file


def parse_sw_sectors(source):
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
                'exchange': exchange,
                'symbol': exchange + symbol_suffix,
                'sector': row_data[4],
                'name': row_data[12]
            }
        )
    print("total row data length:" + str(len(result)))
    return result

def parse_sw_sectors_save_to_file(source, target):
    result = parse_sw_sectors(source=source)
    write_data_to_json_file(data=result, path=target)