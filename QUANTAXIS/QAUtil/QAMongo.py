# coding=utf-8
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


import subprocess

import pandas as pd

from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info


def QA_util_mongo_initial(db=DATABASE):

    db.drop_collection('stock_day')
    db.drop_collection('stock_list')
    db.drop_collection('stock_info')
    db.drop_collection('trade_date')
    db.drop_collection('stock_min')
    db.drop_collection('stock_transaction')
    db.drop_collection('stock_xdxr')





def QA_util_mongo_status(db=DATABASE):
    QA_util_log_info(db.collection_names())
    QA_util_log_info(db.last_status())
    QA_util_log_info(subprocess.call('mongostat', shell=True))


def QA_util_mongo_infos(db=DATABASE):

    data_struct = []

    for item in db.collection_names():
        value = []
        value.append(item)
        value.append(eval('db.' + str(item) + '.find({}).count()'))
        value.append(list(eval('db.' + str(item) + '.find_one()').keys()))
        data_struct.append(value)
    return pd.DataFrame(data_struct, columns=['collection_name', 'counts', 'columns']).set_index('collection_name')


if __name__ == '__main__':
    print(QA_util_mongo_infos())
    QA_util_mongo_status()
