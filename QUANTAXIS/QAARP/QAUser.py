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
import pandas as pd
import datetime
import uuid
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QASetting import QA_Setting
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_next_day, QA_util_get_real_date


class QA_User():
    """QA_User 
    User-->Portfolio-->Account/Strategy

    :::::::::::::::::::::::::::::::::::::::::::::::::
    ::        :: Portfolio 1 -- Account/Strategy 1 ::
    ::  USER  ::             -- Account/Strategy 2 ::
    ::        :: Portfolio 2 -- Account/Strategy 3 ::
    :::::::::::::::::::::::::::::::::::::::::::::::::

    :: 需要增加对于QA_USER的支持

    USER作为一个单位实体, 可以自由创建 组合Portfolio (需要被记录),修改 组合Portfolio

    @yutiansut 
    2018/05/08

    @jerryw  添加注释，和 🛠todo list
    2018/05/16

    @royburns  1.根据指定的user_cookie创建user； 2.添加对应的测试代码； 3.添加注释
    2018/05/18
    """

    def __init__(
            self,
            user_cookie=None,
            username='defalut',
            phone='defalut',
            level='l1',
            utype='guests',
            password='default',
            coins=10000,
            money=0,
    ):
        """[summary]

        Keyword Arguments:
            user_cookie {[type]} -- [description] (default: {None}) 随机初始化 user_cookie 的值 Acc+4数字id+4位大小写随机
            username {str} -- [description] (default: {'defalut'})
            phone {str} -- [description] (default: {'defalut'})
            level {str} -- [description] (default: {'l1'})
            utype {str} -- [description] (default: {'guests'})
            password {str} -- [description] (default: {'default'})
            coins {int} -- [description] (default: {10000})

        关于积分系统:

        积分系统用于订阅策略, 取消订阅策略是不会增加积分的

        """

        self.setting = QA_Setting()
        self.portfolio_list = {}

        # ==============================
        self.phone = phone
        self.level = level
        self.utype = utype
        self.password = password
        self.username = username
        self.user_cookie = QA_util_random_with_topic(
            'USER'
        ) if user_cookie is None else user_cookie
        self.coins = coins  # 积分
        self.money = money  # 钱

        # ==============================
        self._subscribed_strategy = {}
        self._subscribed_code = []
        self._signals = []  # 预期收到的信号
        self._cash = []
        self._history = []

        # ===============================

        self.coins_history = []
        self.coins_history_headers = [
            'cost_coins',
            'strategy_id',
            'start',
            'last',
            'strategy_uuid',
            'event'
        ]
        self.sync()

    def __repr__(self):
        return '< QA_USER {} with {} portfolio: {} >'.format(
            self.user_cookie,
            len(self.portfolio_list.keys()),
            self.portfolio_list
        )

    @property
    def table(self):
        return pd.concat(
            [po.table for po in self.portfolio_list.values()],
            axis=1
        )

    def add_coins(self, coins):
        """积分充值
        Arguments:
            coins {[type]} -- [description]
        """

        self.coins += int(coins)

    @property
    def coins_table(self):
        return pd.DataFrame(
            self.coins_history,
            columns=self.coins_history_headers
        )

    def subscribe_strategy(
            self,
            strategy_id: str,
            last: int,
            today=datetime.date.today(),
            cost_coins=10
    ):
        """订阅一个策略

        会扣减你的积分

        Arguments:
            strategy_id {str} -- [description]
            last {int} -- [description]

        Keyword Arguments:
            today {[type]} -- [description] (default: {datetime.date.today()})
            cost_coins {int} -- [description] (default: {10})
        """

        if self.coins > cost_coins:
            order_id = str(uuid.uuid1())
            self._subscribed_strategy[strategy_id] = {
                'lasttime':
                last,
                'start':
                str(today),
                'strategy_id':
                strategy_id,
                'end':
                QA_util_get_next_day(
                    QA_util_get_real_date(str(today),
                                          towards=1),
                    last
                ),
                'status':
                'running',
                'uuid':
                order_id
            }
            self.coins -= cost_coins
            self.coins_history.append(
                [
                    cost_coins,
                    strategy_id,
                    str(today),
                    last,
                    order_id,
                    'subscribe'
                ]
            )
            return True, order_id
        else:
            # return QAERROR.
            return False, 'Not Enough Coins'

    def unsubscribe_stratgy(self, strategy_id):
        today = datetime.date.today()
        order_id = str(uuid.uuid1())
        if strategy_id in self._subscribed_strategy.keys():
            self._subscribed_strategy[strategy_id]['status'] = 'canceled'

        self.coins_history.append(
            [0,
             strategy_id,
             str(today),
             0,
             order_id,
             'unsubscribe']
        )

    @property
    def subscribed_strategy(self):

        return pd.DataFrame(list(self._subscribed_strategy.values()))

    @property
    def subscribing_strategy(self):
        res = self.subscribed_strategy.assign(
            remains=self.subscribed_strategy.end.apply(
                lambda x: pd.Timestamp(x) - pd.Timestamp(datetime.date.today())
            )
        )
        #res['left'] = res['end_time']
        # res['remains']
        res.assign(
            status=res['remains'].apply(
                lambda x: 'running'
                if x > datetime.timedelta(days=0) else 'timeout'
            )
        )
        return res.query('status=="running"')

    def sub_code(self, code):
        """关注的品种
        """
        self._subscribed_code.append(code)

    @property
    def subscribed_code(self):
        return list(set(self._subscribed_code))

    @property
    def client(self):
        '''
        'user.client to connect database'
        :return: pymongo.MongoClient 数据库连接
        '''
        return self.setting.client.quantaxis.user

    def connect_database(self, ip='127.0.0.1', port=27017):
        '''
        'connect is also a way to change database from IP_A to IP_B
        :param ip: 连接mongodb ip
        :param port: 连接mongodb 端口
        :return: None
        '''
        self.setting.change(ip, port)

    def login(self, username, password):
        '''
        login to a database
        🛠todo： fix 返回 是否成功
        :param username: 连接 mongodb 的用户名
        :param password:  连接 mongodb 的密码
        :return: Boolean 是否成功连接
        '''
        if self.setting.login(username, password):
            QA_util_log_info('SUCCESS')
            return True
        else:
            QA_util_log_info('FAILD')
            return False

    def new_portfolio(self, portfolio_cookie=None):
        '''
            根据 self.user_cookie 创建一个 portfolio
        :return:
             如果存在 返回 新建的 QA_Portfolio
             如果已经存在 不返回 None
        '''
        _portfolio = QA_Portfolio(
            user_cookie=self.user_cookie,
            portfolio_cookie=portfolio_cookie
        )
        if _portfolio.portfolio_cookie not in self.portfolio_list.keys():
            self.portfolio_list[_portfolio.portfolio_cookie] = _portfolio
            return _portfolio
        else:
            print(
                " prortfolio with user_cookie ",
                self.user_cookie,
                " already exist!!"
            )

    def get_portfolio(self, portfolio):
        '''
        'get a portfolio'
        从 portfolio_list dict字典中 根据 portfolio key 获取
        :param portfolio: QA_Portfolio类型
        :return: QA_Portfolio类型
        '''
        # return self.portfolio_list[portfolio]
        # fix here use cookie as key to find value in dict
        return self.portfolio_list[portfolio.portfolio_cookie]

    def get_portfolio_by_cookie(self, portfolio_cookie):
        '''
        'get a portfolio'
        从 portfolio_list dict字典中 根据 portfolio key 获取
        :param portfolio: porfolio_cookie string
        :return: QA_Portfolio类型
        '''
        return self.portfolio_list[portfolio_cookie]

    def generate_simpleaccount(self):
        """make a simple account with a easier way
        如果当前user中没有创建portfolio, 则创建一个portfolio,并用此portfolio创建一个account
        如果已有一个或多个portfolio,则使用第一个portfolio来创建一个account
        """
        if len(self.portfolio_list.keys()) < 1:
            po = self.new_portfolio()
        else:
            po = list(self.portfolio_list.values())[0]
        ac = po.new_account()
        return ac, po

    def register_account(self, account, portfolio_cookie=None):
        '''
        注册一个account到portfolio组合中
        account 也可以是一个策略类，实现其 on_bar 方法
        :param account: 被注册的account
        :return:
        '''
        # 查找 portfolio
        if len(self.portfolio_list.keys()) < 1:
            po = self.new_portfolio()
        elif portfolio_cookie is not None:
            po = self.portfolio_list[portfolio_cookie]
        else:
            po = list(self.portfolio_list.values())[0]
        # 把account 添加到 portfolio中去
        po.add_account(account)
        return (po, account)

    @property
    def message(self):
        return {'user_cookie': self.user_cookie,
                'username': self.username,
                'password': self.password,
                'phone': self.phone,
                'level': self.level,
                'utype': self.utype,
                'coins': self.coins,
                'coins_history': self.coins_history,
                'money': self.money,
                'subuscribed_strategy': self._subscribed_strategy,
                'subscribed_code': self.subscribed_code
                }

    def save(self):
        """
        将QA_USER的信息存入数据库
        """
        self.client.update({'username':self.username,'password':self.password}, {'$set': self.message}, upsert=True)

    def sync(self):
        """基于账户/密码去sync数据库
        """

        res = self.client.find_one(
            {'username': self.username, 'password': self.password})
        if res is None:
            self.client.insert_one(self.message)
        else:
            self.reload(res)

        return self

    def reload(self, message):
        self.phone = message.get('phone')
        self.level = message.get('level')
        self.utype = message.get('utype')
        self.coins = message.get('coins')
        self.coins_history = message.get('coins_history')
        self.money = message.get('money')
        self._subscribed_strategy = message.get('subuscribed_strategy')
        self._subscribed_code = message.get('subscribed_code')


if __name__ == '__main__':

    # 测试不对
    user = QA_User(user_cookie='user_admin')
    folio = user.new_portfolio('folio_admin')
    ac1 = user.get_portfolio(folio).new_account('account_admin')

    print(user)
    print(user.get_portfolio(folio))
    print(user.get_portfolio(folio).get_account(ac1))
