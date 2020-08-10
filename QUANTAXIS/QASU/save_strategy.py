# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QASetting.QALocalize import strategy_path
import datetime
import os
import sys
import requests
"""对于策略的存储
"""


def QA_SU_save_strategy(name, portfolio_cookie='default', account_cookie='default', version=1, if_save=False, if_web_request=False, webreuquestsurl='http://localhost:8010/backtest/write'):
    absoult_path = '{}{}strategy_{}.py'.format(strategy_path, os.sep, name)
    with open(sys.argv[0], 'rb') as p:
        data = p.read()
        if if_web_request:
            try:
                requests.get(webreuquestsurl, {'strategy_content': data})
            except:
                pass

        collection = DATABASE.strategy
        collection.insert({'name': name, 'account_cookie': account_cookie,
                           'portfolio_cookie': portfolio_cookie, 'version': version,
                           'last_modify_time': str(datetime.datetime.now()),
                           'content': data.decode('utf-8'),
                           'absoultpath': absoult_path})
        if if_save:
            with open(absoult_path, 'wb') as f:
                f.write(data)


# print(os.path.basename(sys.argv[0]))
if __name__ == '__main__':
    QA_SU_save_strategy('test', if_save=True, if_web_request=True)
