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

import csv
import os

from QUANTAXIS.QAUtil import QA_util_log_expection


"""适用于老代码的回测
现在已经废弃
"""

"""
def QA_SU_save_account_message(message, client):
    coll = client.quantaxis.backtest_history
    try:
        coll.insert({
            'time_stamp': message['body']['date_stamp'],
            "cookie": message['header']['cookie'],
            'user': message['header']['session']['user'],
            'strategy': message['header']['session']['strategy'],
            'cash': message['body']['account']['cash'],
            'hold': message['body']['account']['hold'],
            'history': message['body']['account']['history'],
            'assets': message['body']['account']['assets'],
            'detail': message['body']['account']['detail']
        })
    except:
        QA_util_log_expection('QA error in saving backtest account')


def QA_SU_save_backtest_message(message, client):
    __coll = client.quantaxis.backtest_info

    __coll.insert(message)


def QA_SU_save_account_to_csv(message, path=os.getcwd()):

    __file_name_1 = '{}backtest-ca&history-{}.csv'.format(
        path, str(message['header']['cookie']))
    with open(__file_name_1, 'w', newline='') as C:
        csvwriter = csv.writer(C)
        csvwriter.writerow(['date', 'code', 'price', 'towards', 'amount',
                            'order_id', 'trade_id', 'commission_fee', 'cash', 'assets'])
        for i in range(0, max(len(message['body']['account']['cash']), len(message['body']['account']['assets']))):
            try:
                message['body']['account']['history'][i].append(
                    message['body']['account']['cash'][i])
                message['body']['account']['history'][i].append(
                    message['body']['account']['assets'][i])
                csvwriter.writerow(message['body']['account']['history'][i])
            except:
                pass


def QA_SU_save_pnl_to_csv(detail, cookie):
    __file_name_2 = 'backtest-pnl--' + \
        str(cookie) + '.csv'
    with open(__file_name_2, 'w', newline='') as E:
        csvwriter_1 = csv.writer(E)
        csvwriter_1.writerow(detail.columns)
        for item in detail:
            csvwriter_1.writerow(item)
"""