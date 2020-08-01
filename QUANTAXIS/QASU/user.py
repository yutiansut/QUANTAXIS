# coding=utf-8
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


from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
#from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAUtil.QASetting import DATABASE


def QA_user_sign_in(username, password):
    """用户登陆
    不使用 QAUSER库
    只返回 TRUE/FALSE
    """
    #user = QA_User(name= name, password=password)
    cursor = DATABASE.user.find_one(
        {'username': username, 'password': password})
    if cursor is None:
        QA_util_log_info('SOMETHING WRONG')
        return False
    else:
        return True


def QA_user_sign_up(name, password, client):
    """只做check! 具体逻辑需要在自己的函数中实现

    参见:QAWEBSERVER中的实现
    
    Arguments:
        name {[type]} -- [description]
        password {[type]} -- [description]
        client {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    coll = client.user
    if (coll.find({'username': name}).count() > 0):
        print(name)
        QA_util_log_info('user name is already exist')
        return False
    else:
        return True
