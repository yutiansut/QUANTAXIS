import QUANTAXIS as QA
try:
    a = QA.QAFetch.QATdx.QA_fetch_get_stock_day(
        '000001', '2017-01-01', '2017-07-31', '00', 'day', '100.0.0.1')
except Exception as e:
    print(e)
