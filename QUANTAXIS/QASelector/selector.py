# coding:utf-8

import datetime
from functools import lru_cache
from QUANTAXIS.QAData.financial_mean import financial_dict
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_financial_report
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_stock_block_adv, QA_fetch_stock_list_adv
from QUANTAXIS.QAIndicator.indicators import QA_indicator_BOLL, QA_indicator_MACD


"""选股器
"""


class QA_Selector():
    def __init__(self, code=None, start=None, end=None, if_whole_market=True):
        """选股器
        
        Keyword Arguments:
            code {[type]} -- [description] (default: {None})
            start {[type]} -- [description] (default: {None})
            end {[type]} -- [description] (default: {None})
            if_whole_market {bool} -- [description] (default: {True})
        """

        self.code_list = QA_fetch_stock_list_adv().code.tolist() if code is None and if_whole_market else code
        
    @property
    @lru_cache()
    def block(self):
        return QA_fetch_stock_block_adv(code=self.code_list)

    
