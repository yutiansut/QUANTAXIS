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

from QUANTAXIS.QAUtil import QA_util_log_expection


def QA_SU_save_account_message(message, client):
    #header = message['header']
    #body = message['body']
    coll = client.quantaxis.backtest_history
    try:
        coll.insert({
            #'time': message['body']['time'],

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
        QA_util_log_expection('error in saving backtest account')
    # print(message)


def QA_SU_save_backtest_message(message, client):
    __coll = client.quantaxis.backtest_info

    __coll.insert(message)
