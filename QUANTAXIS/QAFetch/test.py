import QUANTAXIS as QA

# stock_day
# 不复权  
# data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','01')
print(data)
"""
QA.QAFetch.QATdx.QA_fetch_get_stock_min()
QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr()
QA.QAFetch.QATdx.QA_fetch_get_stock_list()
QA.QAFetch.QATdx.QA_fetch_get_index_day()
QA.QAFetch.QATdx.QA_fetch_get_index_min()
QA.QAFetch.QATdx.QA_fetch_get_stock_latest()
QA.QAFetch.QATdx.QA_fetch_get_stock_realtime()
"""