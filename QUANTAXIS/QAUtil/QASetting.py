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
from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_sql_mongo_setting


class QA_Setting():

    def __init__(self):

        self.QA_util_sql_mongo_ip = '127.0.0.1'
        self.QA_util_sql_mongo_port = '27017'
        self.client = QA_util_sql_mongo_setting(
            self.QA_util_sql_mongo_ip, self.QA_util_sql_mongo_port)

        self.QA_setting_user_name = ''
        self.QA_setting_user_password = ''
        self.user = {'username': '', 'password': '', 'login': False}

    def QA_setting_init(self):
        self.client = QA_util_sql_mongo_setting(
            self.QA_util_sql_mongo_ip, self.QA_util_sql_mongo_port)
        self.user = self.QA_setting_login()

    def QA_setting_login(self):
        self.username = self.QA_setting_user_name
        self.password = self.QA_setting_user_password
        QA_util_log_info('username:' + str(self.QA_setting_user_name))
        result = QA_user_sign_in(self.username, self.password, self.client)
        if result == True:
            self.user['username'] = self.username
            self.user['password'] = self.password
            self.user['login'] = True
            return self.user
        else:
            QA_util_log_info('failed to login')
