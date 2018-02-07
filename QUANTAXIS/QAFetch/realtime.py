from QUANTAXIS.QAFetch.QATdx import select_best_ip, QA_fetch_get_stock_day, QA_fetch_get_stock_list
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Stock_day
import pandas as pd
import datetime


def get_today_all(output='pd'):
    """today all

    Returns:
        [type] -- [description]
    """

    data = []
    today = str(datetime.date.today())
    codes = QA_fetch_get_stock_list('stock').code.tolist()
    bestip = select_best_ip()['stock']
    for code in codes:
        try:
            l = QA_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        except:
            bestip = select_best_ip()['stock']
            l = QA_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        if l is not None:
            data.append(l)

    res = pd.concat(data)
    if output in ['pd']:
        return res
    elif output in ['QAD']:
        return QA_DataStruct_Stock_day(res.set_index(['date', 'code'], drop=False))



