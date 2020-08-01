# coding:utf-8
#
# The MIT License (MIT)
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
#
# Author:           604829050@qq.com
# Date:             2018-05-11
# Description:      Unit test for the fetch data

import unittest

from QUANTAXIS import QUANTAXIS as QA
from QUANTAXIS import *
from QUANTAXIS.QAFetch import QAEastMoney as QAEM
from QUANTAXIS.QAFetch import QAQuery_Advance as QAQueryAdv
from QUANTAXIS.QAFetch import QATdx as QATdx
from QUANTAXIS.QAFetch import QAThs as QAThs
from QUANTAXIS.QAFetch import QATushare as QATushare
from QUANTAXIS.QAFetch import QAWind as QAWind
from QUANTAXIS.QAFetch import QAQuery
from QUANTAXIS.QAUtil.QAParameter import (DATABASE_TABLE, DATASOURCE,
                                          FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting


class Test_Fetcher(unittest.TestCase):

    def test_QA_quotation(self):
        #print("ok start test")
        df_from_Tdx = QA_quotation('300439', '2018-04-01', '2018-04-10', frequence=FREQUENCE.DAY,
                                   market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME)

        # print(type(df_from_Tdx))
        print((df_from_Tdx))

        list_from_tushare = QA_quotation('300439', '2018-04-01', '2018-04-10', frequence=FREQUENCE.DAY,
                                         market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TUSHARE, output=OUTPUT_FORMAT.DATAFRAME)

        # print(type(list_from_tushare))
        print((list_from_tushare))

        for idx_df in df_from_Tdx.index:
            for dict_elem_in_list in list_from_tushare:

                if dict_elem_in_list["date"] == idx_df:

                    open_price1 = df_from_Tdx.loc[idx_df, "open"]
                    open_price2 = dict_elem_in_list["open"]
                    self.assertEqual(open_price1, open_price2)

                    close_price1 = df_from_Tdx.loc[idx_df, "close"]
                    close_price2 = dict_elem_in_list["close"]
                    self.assertEqual(close_price1, close_price2)

                    high_price1 = df_from_Tdx.loc[idx_df, "high"]
                    high_price2 = dict_elem_in_list["high"]
                    self.assertEqual(high_price1, high_price2)

                    low_price1 = df_from_Tdx.loc[idx_df, "low"]
                    low_price2 = dict_elem_in_list["low"]
                    self.assertEqual(low_price1, low_price2)

                    vol_price1 = df_from_Tdx.loc[idx_df, "vol"]
                    vol_price2 = dict_elem_in_list["volume"]
                    self.assertEqual(vol_price1, vol_price2)

            print("数据对比 tushare 和 tdx  日期 %s 数据一致  ❤️" % idx_df)
        print("--------------- ")

        pass


if __name__ == '__main__':
    unittest.main()
