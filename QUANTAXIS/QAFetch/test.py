import QUANTAXIS as QA

# stock_day
# 不复权  
# data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31')
# 前复权
# data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','01')

# 分钟线

# 1min
#data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','1min')
# 5min
#data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','5min')
# 15min
#data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','15min')


# 除权除息
#data=QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr('00001')

# 股票列表

#data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('stock')
# 指数列表
#data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('index')
# 全部列表
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('all')
"""
QA.QAFetch.QATdx.QA_fetch_get_stock_list()
QA.QAFetch.QATdx.QA_fetch_get_index_day()
QA.QAFetch.QATdx.QA_fetch_get_index_min()
QA.QAFetch.QATdx.QA_fetch_get_stock_latest()
QA.QAFetch.QATdx.QA_fetch_get_stock_realtime()
"""
print(data)