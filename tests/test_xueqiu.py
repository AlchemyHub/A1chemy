from a1chemy.data_source.xueqiu import XueQiuDataParser


def test_history():
    xueqiu_client = XueQiuDataParser()
    sz002352 = xueqiu_client.history(symbol='SZ002352', period='day', count=100)
    assert sz002352.symbol == 'SZ002352'
    assert sz002352.raw_data is not None
