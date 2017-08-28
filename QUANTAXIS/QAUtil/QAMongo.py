# coding=utf-8
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


import pymongo
from QUANTAXIS.QAUtil import QA_Setting,QA_util_log_info

def QA_util_mongo_initial(db=QA_Setting.client.quantaxis):

    db.drop_collection('stock_day')
    db.drop_collection('stock_list')
    db.drop_collection('stock_info')
    db.drop_collection('trade_date')
    db.drop_collection('stock_min')
    db.drop_collection('stock_transaction')
    db.drop_collection('stock_xdxr')

def QA_util_mongo_make_index(db=QA_Setting.client.quantaxis):
    try:
        db.stock_day.ensure_index('code')
        db.stock_min_five.ensure_index('code')
    except:
        pass



def QA_util_mongo_status(db=QA_Setting.client.quantaxis):
    QA_util_log_info(db.get_collection())
    QA_util_log_info(db.last_status())