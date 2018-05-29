import unittest
import datetime

from QUANTAXIS.QAData import (QA_DataStruct_Index_day, QA_DataStruct_Index_min,
                              QA_DataStruct_Stock_block,
                              QA_DataStruct_Stock_day, QA_DataStruct_Stock_min,
                              QA_DataStruct_Stock_transaction)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day,
                                       QA_fetch_index_min,
                                       QA_fetch_stock_day,
                                       QA_fetch_stock_full,
                                       QA_fetch_stock_min)


from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day,
                                       QA_fetch_index_min,
                                       QA_fetch_stock_day,
                                       QA_fetch_stock_full,
                                       QA_fetch_stock_min)

from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv

import pandas as pd
from QUANTAXIS.QAData.base_datastruct import _quotation_base
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE, DATASOURCE, OUTPUT_FORMAT, DATABASE_TABLE

from QUANTAXIS import QUANTAXIS as QA



class quotation_base_test(unittest.TestCase):
    '''

    '''
    def test_quotation_base_class(self):


        df_from_Tdx = QA.QA_quotation('300439', '2018-04-01', '2018-04-10', frequence=FREQUENCE.DAY,
                                   market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME)



        # for iRow in range((df_from_Tdx)):
        #     print(iRow)

    def test_quotation_base_class_itera_(self):
        qaDAStruct = QA_fetch_stock_day_adv('300439')

        for iRow in qaDAStruct:
            print(iRow)

        iterObj = qaDAStruct.__iter__()

        i = iterObj.__next__()
        print(i)

        i = iterObj.__next__()
        print(i)

        i = iterObj.__next__()
        print(i)
