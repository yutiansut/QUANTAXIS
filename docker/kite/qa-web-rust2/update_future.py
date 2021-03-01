#!/opt/conda/bin/python

#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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

from QUANTAXIS.QASU.main import (QA_SU_save_etf_day, QA_SU_save_etf_min,
                                 QA_SU_save_financialfiles,
                                 QA_SU_save_index_day, QA_SU_save_index_min,
                                 QA_SU_save_stock_block, QA_SU_save_stock_day,
                                 QA_SU_save_stock_info,
                                 QA_SU_save_stock_info_tushare,
                                 QA_SU_save_stock_list, QA_SU_save_stock_min,
                                 QA_SU_save_stock_xdxr,QA_SU_save_single_index_day,
                                 QA_SU_save_option_50etf_day,QA_SU_save_option_50etf_min,
                                 QA_SU_save_option_300etf_day,QA_SU_save_option_300etf_min,
                                 QA_SU_save_option_commodity_day,QA_SU_save_option_commodity_min,
                                 QA_SU_save_future_day,QA_SU_save_future_day_all,QA_SU_save_future_min,QA_SU_save_future_min_all)


QA_SU_save_future_min('tdx')
QA_SU_save_future_day('tdx')
QA_SU_save_option_50etf_day('tdx')
QA_SU_save_option_50etf_min('tdx')
QA_SU_save_option_300etf_day('tdx')
QA_SU_save_option_300etf_min('tdx')
QA_SU_save_option_commodity_day('tdx')
QA_SU_save_option_commodity_min('tdx')
QA_SU_save_single_index_day('000300','tdx')
