# coding:utf-8
from QUANTAXIS.QAData.QADataStruct import (QA_DataStruct_Index_day,
                                           QA_DataStruct_Index_min,
                                           QA_DataStruct_Stock_day,
                                           QA_DataStruct_Stock_min,
                                           QA_DataStruct_Stock_transaction)
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_xdxr

def QA_stock_day_warpper(func,*args,**kwargs):
    return QA_DataStruct_Stock_day(func(*args,**kwargs))


def QA_stock_min_warpper(func,*args,**kwargs):
    return QA_DataStruct_Stock_min(func(*args,**kwargs))


