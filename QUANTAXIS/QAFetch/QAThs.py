# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
from QUANTAXIS.QAUtil import trade_date_sse


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
        for i_ in range(start_year + 1, end_year + 1):
            data = pd.concat(
                [data, QA_fetch_get_stock_day_in_year(code, i_, if_fq)], axis=0)
    else:
        pass
    if data is None:
        return pd.DataFrame()
    else:
        return data[start:end]


if __name__ == '__main__':
    # print(get_k_data_year('000001','2016','01'))
    # print(get_k_data_year(600010,2016,'01'))
    print(QA_fetch_get_stock_day('000001', '2016-05-01', '2017-07-01', '01'))
