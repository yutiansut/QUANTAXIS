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
import os

from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting


class QA_Setting():

    QA_util_sql_mongo_ip = os.getenv(
        'MONGO_IP') if os.getenv('MONGO_IP') else '127.0.0.1'
    QA_util_sql_mongo_port = os.getenv(
        'MONGO_PORT') if os.getenv('MONGO_PORT') else '27017'
    client = QA_util_sql_mongo_setting(
        QA_util_sql_mongo_ip, QA_util_sql_mongo_port)

    QA_setting_user_name = ''
    QA_setting_user_password = ''
    user = {'username': '', 'password': '', 'login': False}

    def QA_setting_init(self, ip='127.0.0.1', port=27017):
        self.QA_util_sql_mongo_ip = ip
        self.QA_util_sql_mongo_port = port
        self.client = QA_util_sql_mongo_setting(
            self.QA_util_sql_mongo_ip, self.QA_util_sql_mongo_port)

        # return self
        self.user = self.QA_setting_login()

    def set_ip(self, ip='127.0.0.1'):
        self.QA_util_sql_mongo_ip = ip
        self.client = QA_util_sql_mongo_setting(
            self.QA_util_sql_mongo_ip, self.QA_util_sql_mongo_port)
        return self

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


info_ip_list = ['101.227.73.20',
                '101.227.77.254',
                '114.80.63.12',
                '114.80.63.35',
                '115.238.56.198',
                '115.238.90.165',
                '124.160.88.183',
                '14.17.75.71',
                '14.215.128.18',
                '180.153.18.170',
                '180.153.18.171',
                '180.153.18.172',
                '180.153.39.51',
                '202.108.253.130',
                '202.108.253.131',
                '202.108.253.139',
                '218.108.47.69',
                '218.108.98.244',
                '218.57.11.101',
                '218.75.126.9',
                '221.231.141.60',
                '223.94.89.115',
                '58.58.33.123',
                '59.173.18.140',
                '60.12.136.250',
                '60.191.117.167',
                '60.28.23.80']
