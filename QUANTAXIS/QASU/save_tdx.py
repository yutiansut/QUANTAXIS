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

from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, QA_fetch_get_stock_min, QA_fetch_get_stock_xdxr, QA_fetch_get_stock_transaction
from QUANTAXIS.QAUtil import QA_util_to_json_from_pandas, QA_Setting,QA_util_log_info
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_list
import datetime



def QA_SU_save_stock_all(client=QA_Setting.client):
    __stock_list=QA_fetch_get_stock_list()
    __coll = client.quantaxis.stock_day
    __coll.ensure_index('code')
    __err=[]
    def __saving_work(code):
        QA_util_log_info('Now Saving ==== %s' % (code))
        try:
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_day(
                        code, '1990-01-01', str(datetime.date.today()), '00')))
        except:
            __err.append(code)
    for i_ in range(len(__stock_list)):
        QA_util_log_info('The %s of Total %s' % (i_, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list[i_])

    if len(__err)>0:
        QA_util_log_info('ERROR! Try Again with \n')
        QA_util_log_info(__err)
        for i__ in __err:
            __saving_work(i__)

if __name__ == '__main__':
    QA_SU_save_stock_all()
