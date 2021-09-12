# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
import json

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAARP import QA_User
from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil import QA_util_to_json_from_pandas
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting


class SignupHandler(QABaseHandler):

    def get(self):
        """注册接口

        Arguments:
            QABaseHandler {[type]} -- [description]

            user/signin?user=xxx&password=xx
        Return 
            'SUCCESS' if success
            'WRONG' if wrong
        """

        username = self.get_argument('user', default='admin')
        password = self.get_argument('password', default='admin')
        if QA_user_sign_up(username, password, DATABASE):
            user = QA_User(username=username, password=password)
            user.save()
            self.write('SUCCESS')
        else:
            self.write('WRONG')


class SigninHandler(QABaseHandler):

    def get(self):
        """登陆接口

        Arguments:
            QABaseHandler {[type]} -- [description]

            user/signup?user=xxx&password=xx
        Return 
            'SUCCESS' if success
            'WRONG' if wrong
        """

        username = self.get_argument('user', default='admin')
        password = self.get_argument('password', default='admin')
        res = QA_user_sign_in(username, password)
        if res is not None:
            self.write('SUCCESS')
        else:
            self.write('WRONG')


class UserHandler(QABaseHandler):
    """这个handler是QAUser的部分实现


    GET:

    http://ip:port/user?action={}&wechat_id={}&{}{}{}

    action:
        query(default)
        query_strategy |  status = all / running

    wechat_id:
        None(default)


    POST:

    http://ip:port/user?action={}&wechat_id={}&{}{}{}

    action:
        change_password: 更改账户密码| password={}
        change_phone: 更改手机号| phone={}
        change_coins: 更改积分| coins={}
        subscribe_strategy: 订阅策略| strategy_id={} | last={} | cost_coins={}
        unsubscribe_strategy: 取消订阅策略| strategy_id={}
        subscribe_code: 订阅品种| code={}
        change_wechatid: 修改wechat_id| wechat_id={}
        get_nodeview: 查看节点信息

    #TODO

    action:
        new_portfolio
        new_account


    DELETE

    http://ip:port/user?action={}&wechat_id={}&{}{}{}


    #TODO
    action:
        del_portfolio
        del_account

    """

    def get(self):
        action = self.get_argument('action', default='query')
        wechat_id = self.get_argument('wechat_id', default=None)
        model = self.get_argument('model', 'wechat')
        if wechat_id is None and model == 'wechat':
            self.write({
                'status':
                404,
                'result':
                'no wechat id'
            })

        else:
            if model == 'password':
                user = QA_User(username=self.get_argument(
                    'username'), password=self.get_argument('password'))
            else:
                user = QA_User(wechat_id=wechat_id)

            if action == 'query':
                self.write({"result": user.message})
            elif action == 'query_strategy':
                status = self.get_argument('status', 'all')
                if status == 'running':
                    self.write(
                        {
                            'status':
                            200,
                            'result':
                            QA_util_to_json_from_pandas(
                                user.subscribing_strategy)
                        }
                    )
                elif status == 'all':
                    self.write(
                        {
                            'status':
                            200,
                            'result':
                            QA_util_to_json_from_pandas(
                                user.subscribed_strategy)
                        }
                    )
            elif action == 'query_portfolio':
                """获取某个user下的所有portfolio

                """
                self.write({
                    'status': 200,
                    'result': user.portfolio_list
                })
            elif action == 'get_portfolio':
                """
                ?portfolio = xxxx

                这里主要展示这个portfolio的信息
                如果需要具体对portfolio进行控制, 则在aprhandlers.portfolio_handler中
                """
                try:
                    self.write({
                        'status': 200,
                        'result': user.get_portfolio(self.get_argument('portfolio')).message
                    })
                except Exception as e:
                    self.write({
                        'status': 404,
                        'result': str(e)
                    })
            elif action == 'get_nodeview':
                self.write({
                    'status': 200,
                    'result': user.node_view
                })

    def post(self):
        """动作修改
        """

        action = self.get_argument('action')
        wechat_id = self.get_argument('wechat_id', default=None)
        model = self.get_argument('model', 'wechat')
        if wechat_id is None and model == 'wechat':
            self.write({
                'status':
                404,
                'result':
                'no wechat id'
            })

        else:
            if model == 'password':
                user = QA_User(username=self.get_argument(
                    'username'), password=self.get_argument('password'))
            else:
                user = QA_User(wechat_id=wechat_id)

            try:
                if action == 'change_password':
                    user.password = str(
                        self.get_argument('password', '123456'))
                if action == 'change_name':
                    user.username = str(self.get_argument(
                        'username', 'default_name'))
                elif action == 'change_phone':
                    user.phone = str(self.get_argument('phone', '123456789'))
                elif action == 'change_coins':
                    user.coins = float(self.get_argument('coins'))
                elif action == 'subscribe_strategy':
                    user.subscribe_strategy(
                        self.get_argument('strategy_id'),
                        int(self.get_argument('last')),
                        cost_coins=int(self.get_argument('cost_coins'))
                    )
                elif action == 'unsubscribe_strategy':
                    user.unsubscribe_stratgy(self.get_argument('strategy_id'))
                elif action == 'subscribe_code':
                    user.sub_code(self.get_argument('code'))
                elif action == 'add_portfolio':
                    user.new_portfolio(
                        portfolio_cookie=self.get_argument('portfolio'))
                elif action == 'change_wechatid':
                    user.wechat_id = self.get_argument('wechat_id')
                user.save()
                #
                self.write({'status': 200})
            except:
                self.write({'status': 400})

    def delete(self):
        pass


class PersonBlockHandler(QABaseHandler):

    def get(self):
        """
        make table for user: user

        send in ==> {'block',[{'block':xxxx,'code':code}}
        """
        table = DATABASE.user_block
        data = table.find_one()
        print(data)
        data.pop('_id')
        self.write(data)
        # table.find_one_and_update('')

    def post(self):
        """
        make table for user: user

        send in ==> {'block',[{'block':xxxx,'code':code}}
        """
        param = eval(self.get_argument('block'))
        print(param)
        table = DATABASE.user_block
        table.insert({'block': param})
        # table.find_one_and_update('')


if __name__ == '__main__':
    app = Application(
        handlers=[
            (r"/user/signin",
             SigninHandler),
            (r"/user/signup",
             SignupHandler),
            (r"/user",
             UserHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
