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

import datetime
import pandas as pd
from QUANTAXIS.QAUtil import DATABASE, QA_util_to_json_from_pandas
from QUANTAXIS.QAUtil.QASql import ASCENDING, DESCENDING


def QA_SU_save_order(orderlist, client=DATABASE):
    """存储order_handler的order_status

    Arguments:
        orderlist {[dataframe]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    if isinstance(orderlist, pd.DataFrame):

        collection = client.order
        collection.create_index(
            [('account_cookie',
              ASCENDING),
             ('realorder_id',
              ASCENDING)],
            unique=True
        )
        try:

            orderlist = QA_util_to_json_from_pandas(orderlist.reset_index())

            for item in orderlist:
                if item:
                    #item['date']= QA_util_get_order_day()
                    collection.update_one(
                        {
                            'account_cookie': item.get('account_cookie'),
                            'realorder_id': item.get('realorder_id')
                        },
                        {'$set': item},
                        upsert=True
                    )
        except Exception as e:
            print(e)
            pass


def QA_SU_save_deal(dealist, client=DATABASE):
    """存储order_handler的deal_status

    Arguments:
        dealist {[dataframe]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    if isinstance(dealist, pd.DataFrame):

        collection = client.deal

        collection.create_index(
            [('account_cookie',
              ASCENDING),
             ('trade_id',
              ASCENDING)],
            unique=True
        )
        try:
            dealist = QA_util_to_json_from_pandas(dealist.reset_index())
            collection.insert_many(dealist, ordered=False)
        except Exception as e:

            pass


def QA_SU_save_order_queue(order_queue, client=DATABASE):
    """增量存储order_queue

    Arguments:
        order_queue {[type]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    collection = client.order_queue
    collection.create_index(
        [('account_cookie',
          ASCENDING),
         ('order_id',
          ASCENDING)],
        unique=True
    )
    for order in order_queue.values():
        order_json = order.to_dict()
        try:
            collection.update_one(
                {
                    'account_cookie': order_json.get('account_cookie'),
                    'order_id': order_json.get('order_id')
                },
                {'$set': order_json},
                upsert=True
            )
        except Exception as e:
            print(e)
