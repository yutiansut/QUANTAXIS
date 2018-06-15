import unittest
import urllib

class QACrawl_Test(unittest.TestCase):

    def test_QACrawl_Eastmoney(self):


        #改用 re 正则表达式做匹配
        #改用
        response = urllib.request.urlopen("http://data.eastmoney.com/zjlx/002433.html")
        content = response.read()

        strings = content.decode("utf-8", "ignore")
        string_lines = strings.split("\r\n")

        for aline in string_lines:
            aline = aline.strip()
            if '_stockCode' in aline:
                _stockCode = aline[len('var _stockCode = '):]
                _stockCode = _stockCode.strip("\"\"\,")


            if '_stockMarke' in aline:
                _stockMarke = aline[len('_stockMarke = '):]
                _stockMarke = _stockMarke.strip("\"\"\,")


            if '_stockName' in aline:
                _stockName = aline[len('_stockName = '):]
                _stockName = _stockName.strip("\"\"\,")


            if '_market' in aline:
                _market = aline[len('_market = '):]
                _market = _market.strip("\"\"\,")
                break

        # print(_stockCode)
        # print(_stockMarke)
        # print(_stockName)
        # print(_market)

        values = []
        for aline in string_lines:
            aline = aline.strip()
            if 'EM_CapitalFlowInterface' in aline:
                #print(aline)
                #print('------------------')
                aline = aline.strip()
                if aline.startswith('var strUrl = '):
                    if 'var strUrl = ' in aline:
                        aline = aline[len('var strUrl = '):]
                        values = aline.split('+')
                        #print(values)
                break
                #print('------------------')

        print(values)

        requestStr = ""
        for iItem in values:
            if '_stockCode' in iItem:
                requestStr = requestStr + _stockCode
            elif '_stockMarke' in iItem:
                requestStr = requestStr + _stockMarke
            else:
                if 'http://ff.eastmoney.com/' in iItem:
                    requestStr = 'http://ff.eastmoney.com/'
                else:
                    iItem = iItem.strip(' "')
                    iItem = iItem.rstrip(' "')
                    requestStr = requestStr + iItem

        #print(requestStr)

        response = urllib.request.urlopen(requestStr)
        content2 = response.read()

        #print(content2)
        strings = content2.decode("utf-8", "ignore")

        if 'var aff_data=({data:[["' in strings:
            leftChars = strings[len('var aff_data=({data:[["'):]
            #print(leftChars)
            dataArrays = leftChars.split(',')
            print(dataArrays)

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