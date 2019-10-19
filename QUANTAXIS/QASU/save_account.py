# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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


from pymongo import DESCENDING, ASCENDING
from QUANTAXIS.QAUtil import DATABASE
"""对于账户的增删改查(QAACCOUNT/QAUSER/QAPORTFOLIO)
"""


def save_account(message, collection=DATABASE.account):
    """save account

    Arguments:
        message {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})
    """
    try:
        collection.create_index(
            [("account_cookie", ASCENDING), ("user_cookie", ASCENDING), ("portfolio_cookie", ASCENDING)], unique=True)
    except:
        pass
    collection.update(
        {'account_cookie': message['account_cookie'], 'portfolio_cookie':
            message['portfolio_cookie'], 'user_cookie': message['user_cookie']},
        {'$set': message},
        upsert=True
    )


def update_account(mes, collection=DATABASE.account):
    """update the account with account message

    Arguments:
        mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})
    """

    collection.find_one_and_update({'account_cookie': mes['account_cookie']})


def save_riskanalysis(message, collection=DATABASE.risk):
    # print(message)

    try:
        collection.create_index(
            [("account_cookie", ASCENDING), ("user_cookie", ASCENDING), ("portfolio_cookie", ASCENDING)], unique=True)
    except:
        pass
        
    collection.update(
        {'account_cookie': message['account_cookie'], 'portfolio_cookie':
            message['portfolio_cookie'], 'user_cookie': message['user_cookie']},
        {'$set': message},
        upsert=True
    )

