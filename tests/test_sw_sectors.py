from a1chemy.data_source.sw_sectors import parse_sw_sectors


def test_parse_sw_sectors():
    parse_sw_sectors('/Users/line/workspace/freedom/doc/SwClass.xls',
                     '/Users/line/workspace/freedom/A1chemy/data/sw_sector.json')
    assert True
