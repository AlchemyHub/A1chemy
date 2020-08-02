from a1chemy.data_source.csindex import parse_csi_index_xls


def test_parse_index_xls():
    parse_csi_index_xls('/Users/line/workspace/freedom/doc/000906cons.xls',
                    '/Users/line/workspace/freedom/A1chemy/data/sci_800.json')
    assert True
