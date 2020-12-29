# coding:utf-8
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

import requests
import pandas as pd
from QUANTAXIS.QAFetch.base import headers, _select_market_code

BusinessAnalysis_url = 'http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code={}{}'

headers_em = headers
headers_em['Host'] = 'emweb.securities.eastmoney.com'


def QA_fetch_get_stock_analysis(code):
    """
    'zyfw', 主营范围 'jyps'#经营评述 'zygcfx' 主营构成分析

    date 主营构成	主营收入(元)	收入比例cbbl	主营成本(元)	成本比例	主营利润(元)	利润比例	毛利率(%)
    行业 /产品/ 区域 hq cp qy
    """
    market = 'sh' if _select_market_code(code) == 1 else 'sz'
    null = 'none'
    data = eval(requests.get(BusinessAnalysis_url.format(
        market, code), headers=headers_em).text)
    zyfw = pd.DataFrame(data.get('zyfw', None))
    jyps = pd.DataFrame(data.get('jyps', None))
    zygcfx = data.get('zygcfx', [])
    temp = []
    for item in zygcfx:
        try:
            data_ = pd.concat([pd.DataFrame(item['hy']).assign(date=item['rq']).assign(classify='hy'),
                               pd.DataFrame(item['cp']).assign(
                                   date=item['rq']).assign(classify='cp'),
                               pd.DataFrame(item['qy']).assign(date=item['rq']).assign(classify='qy')])

            temp.append(data_)
        except:
            pass
    try:
        res_zyfcfx = pd.concat(temp).set_index(
            ['date', 'classify'], drop=False)
    except:
        res_zyfcfx = None

    return zyfw, jyps, res_zyfcfx


cpbidu = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/OperationsRequiredAjax?times=1&code=sz300059'

headers_em_OperationsRequired = headers
headers_em_OperationsRequired['Accept'] = '*/*'
headers_em_OperationsRequired['Referer'] = 'http://emweb.securities.eastmoney.com/PC_HSF10/OperationsRequired/Index?type=soft&code=sz300059'

headers_em_OperationsRequired['X-Requested-With'] = 'XMLHttpRequest'

research_report = 'http://emweb.securities.eastmoney.com/PC_HSF10/ResearchReport/ResearchReportAjax?code=sz300059&icode=447'

ggzj='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?\
type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4000&js=&\
token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=51144985'

#行业版块资金

bkzj="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?\
type=CT&cmd=C._BKHY&st=(BalFlowMain)&sr=-1&p=1&ps=100&js=\
&token=894050c76af8597a853f5b408b759f5d&cb=&sty=DCFFITA&rt=51144985"

#概念版块资金

gnzj="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?\
type=CT&cmd=C._BKGN&st=(BalFlowMain)&sr=-1&p=1&ps=300&\
js=&token=894050c76af8597a853f5b408b759f5d&cb=&sty=DCFFITA&rt=l51144985"

#版块个股资金code+markt

bklb="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?\
type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=500&js=\
&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA&rt=51181654&cmd=C."

#版块、个股历史资金流 code+market

gglszj="http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?\
type=hff&rtntype=2&js=&cb=&check=TMLBMSPROCR\
&acces_token=1942f5da9b46b069953c873404aad4b5&_=1535525712559&id="

#个股、版块分钟资金流code+maket

fzzjl="http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?type=ff\
&check=MLBMS&cb=&js=&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5\
&_=1535450561774&id="

