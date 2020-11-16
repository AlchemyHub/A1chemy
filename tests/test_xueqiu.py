import a1chemy.data_source as data_source


def test_history():
    cookies = {
    'bid': '783ea5e048552adebcc2fb818cf94d7a_k3l4dhqh',
    'device_id': '8c96397a28a84671916e3a10765b3b41',
    's': 'do1967dh94',
    'remember': '1',
    'cookiesu': '441603901136468',
    'xq_a_token': 'c625f07916d11e93fbbc94b204031ebb04762c24',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjkzMDk1ODc2OTgsImlzcyI6InVjIiwiZXhwIjoxNjA2MTQyMTM0LCJjdG0iOjE2MDM5MDEyMDk0NTYsImNpZCI6ImQ5ZDBuNEFadXAifQ.F72ttDx_LKezd4kWKu0877GUGH7R5MNDI6Y-O51bezfNhGARCWJnnAynWhiIb98u6XvD0urJbrmtGT-k4lyi_baX6znnb2O-wQ3BP6d6crKZMGg4XnUD9hfLezJTCoLkVwdzW2wJu6hhq03w0AsRC8iJ2tDiil8L-3muUZT9kTeuKJj-9RzhsA1GsTa9PpwJZ-skIbCAba7n8c4qaS33wATL0nodFsF_Xmdyplx4nwMRnK7BPNylBNbN7YRhiXJVf98Qi4sKqlR3CNnTce53SyeQZT_S92f8QOH4QXH3Da6rhbfNBttPTHG26J5lwIHGAB8yLRXk8BBAu7-PBnsSYA',
    'xqat': 'c625f07916d11e93fbbc94b204031ebb04762c24',
    'xq_r_token': '2769c70d6b761b1a5bc663369f7b2809be64af2f',
    'xq_is_login': '1',
    'u': '9309587698',
    'is_overseas': '0',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1602947074,1602947745,1603636600,1604164676',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1604164680',
    }
    xueqiu_client = data_source.XueQiuDataParser(cookies=cookies)
    ticks = xueqiu_client.history(symbol='SH600036', period='day')
    print(ticks.index().iloc[-1].tz_convert(tz='Asia/Shanghai'))
