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
import csv
import sys

import QUANTAXIS as QA

coll = QA.QA_Setting.client.quantaxis.backtest_info
coll2 = QA.QA_Setting.client.quantaxis.stock_info
with open('info.csv', 'w', newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(['strategy', 'stock_list', 'start_time', 'end_time', 'account_cookie', 'total_returns', 'annualized_returns',
                        'benchmark_annualized_returns', 'win_rate', 'alpha', 'beta', 'sharpe', 'vol', 'benchmark_vol', 'max_drop', 'exist', 'outstanding', 'totals'])
    for item in coll.find():
        code = item['stock_list'][0]
        try:
            data = coll2.find_one({'code': code})
            outstanding = data['outstanding']
            totals = data['totals']
            csvwriter.writerow([item['strategy'], 'c' + str(item['stock_list'][0]), item['start_time'], item['end_time'], item['account_cookie'], item['total_returns'], item['annualized_returns'],
                                item['benchmark_annualized_returns'], item['win_rate'], item['alpha'], item['beta'], item['sharpe'], item['vol'], item['benchmark_vol'], item['max_drop'], item['exist'], outstanding, totals])
        except:
            info = sys.exc_info()
            print(info[0], ":", info[1])
            print(code)
