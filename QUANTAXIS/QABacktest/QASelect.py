# 一个选股用的api

"""
主要负责把一些筛选函数应用进来



负责加载函数句柄,并且可以自定义函数句柄进行筛选

"""


from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list,QA_fetch_stock_table_by_day

#
def select_by_func(func,*arg,**kwargs):
    func(*arg,**kwargs)



# 需要一个能够加载