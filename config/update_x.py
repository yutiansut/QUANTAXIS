#!/usr/local/bin/python

#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""对应于save x
"""
from QUANTAXIS.QASU.main import (QA_SU_save_etf_day, QA_SU_save_etf_min,
                                 QA_SU_save_financialfiles,
                                 QA_SU_save_index_day, QA_SU_save_index_min,
                                 QA_SU_save_stock_block, QA_SU_save_stock_day,
                                 QA_SU_save_stock_info,
                                 QA_SU_save_stock_info_tushare,
                                 QA_SU_save_stock_list, QA_SU_save_stock_min,
                                 QA_SU_save_stock_xdxr,QA_SU_save_report_calendar_day,
                                 QA_SU_save_report_calendar_his,QA_SU_save_stock_divyield_day,
                                 QA_SU_save_stock_divyield_his)
from QUANTAXIS.QASU.save_binance import (QA_SU_save_binance,
                                         QA_SU_save_binance_1day,
                                         QA_SU_save_binance_1hour,
                                         QA_SU_save_binance_1min,
                                         QA_SU_save_binance_symbol)

if __name__ == '__main__':
    QA_SU_save_stock_day('tdx')
    QA_SU_save_stock_xdxr('tdx')
    QA_SU_save_stock_min('tdx')
    QA_SU_save_index_day('tdx')
    QA_SU_save_index_min('tdx')
    QA_SU_save_etf_day('tdx') 
    QA_SU_save_etf_min('tdx')
    QA_SU_save_stock_list('tdx')
    QA_SU_save_stock_block('tdx')
    QA_SU_save_stock_info('tdx')
    # QA_SU_save_stock_divyield_day()
    # QA_SU_save_report_calendar_day()
