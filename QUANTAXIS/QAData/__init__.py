# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAData.QASeriesStruct import QA_DataStruct_Series
from QUANTAXIS.QAData.data_fq import QA_data_stock_to_fq, QA_data_make_qfq, QA_data_make_hfq
from QUANTAXIS.QAData.data_marketvalue import QA_data_calc_marketvalue, QA_data_marketvalue
from QUANTAXIS.QAData.data_resample import QA_data_tick_resample, QA_data_min_resample, QA_data_day_resample
from QUANTAXIS.QAData.QADataStruct import (QA_DataStruct_Index_day,
                                           QA_DataStruct_Index_min,
                                           QA_DataStruct_Stock_day,
                                           QA_DataStruct_Stock_min,
                                           QA_DataStruct_Future_day,
                                           QA_DataStruct_Future_min,
                                           QA_DataStruct_Stock_realtime,
                                           QA_DataStruct_Stock_transaction)
from QUANTAXIS.QAData.QABlockStruct import QA_DataStruct_Stock_block

from QUANTAXIS.QAData.QAFinancialStruct import QA_DataStruct_Financial
from QUANTAXIS.QAData.QAIndicatorStruct import QA_DataStruct_Indicators
from QUANTAXIS.QAData.dsmethods import QDS_StockDayWarpper, QDS_StockMinWarpper, QDS_IndexDayWarpper, QDS_IndexMinWarpper, from_tushare, concat
