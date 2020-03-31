import unittest
import urllib
import pandas as pd

from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
import time

from QUANTAXIS.QAUtil import (DATABASE)

from QUANTAXIS.QASU.crawl_eastmoney import QA_request_eastmoney_zjlx

class QACrawl_Test(unittest.TestCase):



    def test_QACrawl_Eastmoney(self):

        listStock = ['600001','600002','600003','600004','600005','600006','600007','600008','600009','6000010',
                    '600011','600012','600013','600014','600015','600016','600017','600018','600019','6000020',

                     ]

        QA_request_eastmoney_zjlx(listStock)

        # print(string_lines)
        # print("-----------------------------------------------------------------------------")
        #
        # stock_code = '002424'
        # market_code = '2'
        # req = "http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id="+stock_code+market_code
        #
        # response = urllib.request.urlopen(req)
        # content = response.read()
        # # print(type(content))
        # # print(content)
        # strings = content.decode("utf-8", "ignore")
        # string_lines = strings.split("\r\n")
        #
        # print(string_lines)
        # print("-----------------------------------------------------------------------------")
        #
        # stock_code = '002423'
        # market_code = '2'
        # req = "http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id=" + stock_code + market_code
        #
        # response = urllib.request.urlopen(req)
        # content = response.read()
        # # print(type(content))
        # # print(content)
        # strings = content.decode("utf-8", "ignore")
        # string_lines = strings.split("\r\n")
        #
        # print(string_lines)
        # print("-----------------------------------------------------------------------------")
        #
        #
        # stock_code = '002426'
        # market_code = '2'
        # req = "http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id=" + stock_code + market_code
        #
        # response = urllib.request.urlopen(req)
        # content = response.read()
        # # print(type(content))
        # # print(content)
        # strings = content.decode("utf-8", "ignore")
        # string_lines = strings.split("\r\n")
        #
        # print(string_lines)
        # print("-----------------------------------------------------------------------------")
        #
        pass