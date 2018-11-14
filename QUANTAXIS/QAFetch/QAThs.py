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

import numpy as np
import pandas as pd
import requests
from lxml import etree
from QUANTAXIS.QAFetch.base import headers


headers_ths = headers
headers_ths['Referer'] = 'http://www.10jqka.com.cn/'
headers_ths['Host'] = 'q.10jqka.com.cn'
headers_data = headers_ths
headers_data['X-Requested-With'] = 'XMLHttpRequest'


def QA_fetch_get_stock_day_in_year(code, year, if_fq='00'):
    data_ = []
    url = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js' % (
        str(code), str(if_fq), str(year))
    try:
        for item in requests.get(url).text.split('\"')[3].split(';'):
            data_.append(item.split(','))

        data = pd.DataFrame(data_, index=list(np.asarray(data_).T[0]), columns=[
                            'date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'factor'])
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        return data
    except:
        pass


def QA_fetch_get_stock_day(code, start, end, if_fq='00'):
    start_year = int(str(start)[0:4])
    end_year = int(str(end)[0:4])
    data = QA_fetch_get_stock_day_in_year(code, start_year, if_fq)
    if start_year < end_year:
        for i2 in range(start_year + 1, end_year + 1):
            data = pd.concat(
                [data, QA_fetch_get_stock_day_in_year(code, i2, if_fq)], axis=0)
    else:
        pass
    if data is None:
        return pd.DataFrame()
    else:
        return data[start:end]


def QA_fetch_get_stock_block():
    """ths的版块数据
    
    Returns:
        [type] -- [description]
    """

    url='https://gitee.com/yutiansut/QADATA/raw/master/ths_block.csv'
    try:
        return pd.read_csv(url).set_index('code', drop=False)
    except:
        return None
    # url_list = ['gn', 'dy', 'thshy', 'zjhhy']  # 概念/地域/同花顺板块/证监会板块
    # data = []
    # cookie=input('cookie')
    # for item in url_list:
    #     tree = etree.HTML(requests.get(
    #         'http://q.10jqka.com.cn/{}/'.format(item), headers=headers_ths).text)
    #     gn = tree.xpath('/html/body/div/div/div/div/div/a/text()')
    #     gpath = tree.xpath('/html/body/div/div/div/div/div/a/@href')
    #     headers_data['cookie']=cookie
    #     for r in range(len(gn)):
    #         headers_data['Referer'] = 'http://q.10jqka.com.cn/{}/detail/code/{}'.format(
    #             item, gpath[r].split('/')[-2])

    #         for i in range(1, 15):

    #             _data = etree.HTML(requests.get(
    #                 'http://q.10jqka.com.cn/{}/detail/order/desc/page/{}/ajax/1/code/{}'.format(item, i, gpath[r].split('/')[-2]), headers=headers_data).text)
    #             name = _data.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
    #             code = _data.xpath('/html/body/table/tbody/tr/td[3]/a/@href')

    #             for i2 in range(len(name)):
    #                 print(
    #                     'Now Crawling-{}-{}-{}-{}'.format(gn[r], code[i2].split('/')[-1], item, 'ths'))
    #                 data.append([gn[r], code[i2].split('/')[-1], item, 'ths'])

    # return pd.DataFrame(data, columns=['blockname',  'code', 'type', 'source']).set_index('code', drop=False)

def QA_fetch_get_stock_highlimit_reason(code):
    #http://basic.10jqka.com.cn/300139/
    pass


if __name__ == '__main__':
    # print(get_k_data_year('000001','2016','01'))
    # print(get_k_data_year(600010,2016,'01'))
    print(QA_fetch_get_stock_day('000001', '2016-05-01', '2017-07-01', '01'))
    