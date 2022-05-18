import copy
import datetime
import json
import os
import re
import sys
import threading
import time
import uuid

import pandas as pd
import pymongo
import requests
from qaenv import (eventmq_amqp, eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip, mongo_uri)
from QUANTAXIS.QAPubSub.consumer import subscriber, subscriber_routing, subscriber_topic
from QUANTAXIS.QAPubSub.producer import publisher_routing, publisher_topic

import QUANTAXIS as QA
from QUANTAXIS.QAStrategy.util import QA_data_futuremin_resample
from QUANTAXIS.QIFI.QifiAccount import ORDER_DIRECTION, QIFI_Account
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, RUNNING_ENVIRONMENT


class QAStrategyCtaBase():
    def __init__(self, code='rb2005', frequence='1min', strategy_id='QA_STRATEGY', risk_check_gap=1, portfolio='default',
                 start='2020-01-01', end='2020-05-21', init_cash=1000000, send_wx=False,
                 data_host=eventmq_ip, data_port=eventmq_port, data_user=eventmq_username, data_password=eventmq_password,
                 trade_host=eventmq_ip, trade_port=eventmq_port, trade_user=eventmq_username, trade_password=eventmq_password,
                 taskid=None, mongo_ip=mongo_ip, model='py'):
        """
        code 可以传入单个标的 也可以传入一组标的(list)
        会自动基于code来判断是什么市场
        TODO: 支持多个市场同时存在

        self.trade_host 交易所在的eventmq的ip  [挂ORDER_ROUTER的]
        """
        self.username = 'admin'
        self.password = 'admin'

        self.trade_host = trade_host
        self.code = code
        self.frequence = frequence
        self.strategy_id = strategy_id

        self.portfolio = portfolio

        self.data_host = data_host
        self.data_port = data_port
        self.data_user = data_user
        self.data_password = data_password
        self.trade_host = trade_host
        self.trade_port = trade_port
        self.trade_user = trade_user
        self.trade_password = trade_password

        self.start = start
        self.end = end
        self.init_cash = init_cash
        self.taskid = taskid

        self.running_time = ''

        self.market_preset = MARKET_PRESET()
        self._market_data = []
        self.risk_check_gap = risk_check_gap
        self.latest_price = {}

        self.isupdate = False
        self.model = model
        self.new_data = {}
        self._systemvar = {}
        self._signal = []
        self.send_wx = send_wx
        if isinstance(self.code, str):

            self.last_order_towards = {self.code: {'BUY': '', 'SELL': ''}}
        else:
            self.last_order_towards = dict(
                zip(self.code, [{'BUY': '', 'SELL': ''} for i in range(len(self.code))]))
        self.dt = ''
        if isinstance(self.code, str):
            self.market_type = MARKET_TYPE.FUTURE_CN if re.search(
                r'[a-zA-z]+', self.code) else MARKET_TYPE.STOCK_CN
        else:
            self.market_type = MARKET_TYPE.FUTURE_CN if re.search(
                r'[a-zA-z]+', self.code[0]) else MARKET_TYPE.STOCK_CN

        self.bar_order = {'BUY_OPEN': 0, 'SELL_OPEN': 0,
                          'BUY_CLOSE': 0, 'SELL_CLOSE': 0}

        self._num_cached = 120
        self._cached_data = []
        self.user_init()

    @property
    def bar_id(self):
        return len(self._market_data)

    @property
    def BarsSinceEntryLong(self):
        return self.bar_id - self.bar_order.get('BUY_OPEN', self.bar_id)

    @property
    def BarsSinceEntryShort(self):
        return self.bar_id - self.bar_order.get('SELL_OPEN', self.bar_id)

    @property
    def EntryPriceLong(self):
        code = self.get_code()
        return self.get_positions(code).open_price_long

    @property
    def EntryPriceShort(self):
        code = self.get_code()
        return self.get_positions(code).open_price_short

    def on_sync(self):
        if self.running_mode != 'backtest':
            self.pubacc.pub(json.dumps(self.acc.message),
                            routing_key=self.strategy_id)

    def _debug_sim(self):

        self.running_mode = 'sim'

        if self.frequence.endswith('min'):

            if isinstance(self.code, str):
                self._old_data = QA.QA_fetch_get_future_min('tdx', self.code.upper(), QA.QA_util_get_last_day(
                    QA.QA_util_get_real_date(str(datetime.date.today()))), str(datetime.datetime.now()), self.frequence)[:-1].set_index(['datetime', 'code'])
                self._old_data = self._old_data.assign(volume=self._old_data.trade).loc[:, [
                    'open', 'high', 'low', 'close', 'volume']]
            else:

                self._old_data = pd.concat([QA.QA_fetch_get_future_min('tdx', item.upper(), QA.QA_util_get_last_day(
                    QA.QA_util_get_real_date(str(datetime.date.today()))), str(datetime.datetime.now()), self.frequence)[:-1].set_index(['datetime', 'code']) for item in self.code], sort=False)
                self._old_data = self._old_data.assign(volume=self._old_data.trade).loc[:, [
                    'open', 'high', 'low', 'close', 'volume']]
        else:
            self._old_data = pd.DataFrame()

        self.database = pymongo.MongoClient(mongo_ip).QAREALTIME

        self.client = self.database.account
        self.subscriber_client = self.database.subscribe

        self.acc = QIFI_Account(
            username=self.strategy_id, password=self.strategy_id, trade_host=mongo_ip, init_cash=self.init_cash)
        self.acc.initial()
        self.acc.on_sync = self.on_sync

        self.pub = publisher_routing(exchange='QAORDER_ROUTER', host=self.trade_host,
                                     port=self.trade_port, user=self.trade_user, password=self.trade_password)
        self.pubacc = publisher_topic(exchange='QAAccount', host=self.trade_host,
                                      port=self.trade_port, user=self.trade_user, password=self.trade_password)

        if isinstance(self.code, str):
            self.subscribe_data(self.code.lower(), self.frequence, self.data_host,
                                self.data_port, self.data_user, self.data_password, self.model)
        else:
            self.subscribe_multi(self.code, self.frequence, self.data_host,
                                 self.data_port, self.data_user, self.data_password, self.model)
        print('account {} start sim'.format(self.strategy_id))
        self.database.strategy_schedule.job_control.update(
            {'strategy_id': self.strategy_id},
            {'strategy_id': self.strategy_id, 'taskid': self.taskid,
             'filepath': os.path.abspath(__file__), 'status': 200}, upsert=True)

    def debug_sim(self):
        self._debug_sim()
        threading.Thread(target=self.sub.start, daemon=True).start()

    def run_sim(self):
        self._debug_sim()

        self.sub.start()

    def run_backtest(self):
        self.debug()
        self.acc.save()

        risk = QA_Risk(self.acc)
        risk.save()

        try:
            """add rank flow if exist

            QARank是我们内部用于评价策略ELO的库 此处并不影响正常使用
            """
            from QARank import QA_Rank
            QA_Rank(self.acc).send()
        except:
            pass

    def user_init(self):
        """
        用户自定义的init过程
        """
        pass

    def debug(self):
        self.running_mode = 'backtest'
        self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        user = QA_User(username=self.username, password=self.password)
        port = user.new_portfolio(self.portfolio)
        self.acc = port.new_accountpro(
            account_cookie=self.strategy_id, init_cash=self.init_cash, market_type=self.market_type, frequence=self.frequence)
        self.positions = self.acc.get_position(self.code)

        print(self.acc)
        print(self.acc.market_type)
        data = QA.QA_quotation(self.code.upper(), self.start, self.end, source=QA.DATASOURCE.MONGO,
                               frequence=self.frequence, market=self.market_type, output=QA.OUTPUT_FORMAT.DATASTRUCT)

        data.data.apply(self.x1, axis=1)

    def x1(self, item):
        self.latest_price[item.name[1]] = item['close']
        if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
            self.on_dailyclose()
            self.on_dailyopen()
            if self.market_type == QA.MARKET_TYPE.STOCK_CN:
                print('backtest: Settle!')
                self.acc.settle()
        self._on_1min_bar()
        self._market_data.append(copy.deepcopy(item))
        self.running_time = str(item.name[0])
        self.on_bar(item)

    def debug_t0(self):
        self.running_mode = 'backtest'
        # self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        # user = QA_User(username=self.username, password=self.password)
        # port = user.new_portfolio(self.portfolio)
        # self.acc = port.new_accountpro(
        #     account_cookie=self.strategy_id, init_cash=self.init_cash, init_hold={
        #         self.code: 100000},
        #     market_type=self.market_type, running_environment=RUNNING_ENVIRONMENT.TZERO)
        # self.positions = self.acc.get_position(self.code)
        data = QA.QA_quotation(self.code.upper(), self.start, self.end, source=QA.DATASOURCE.MONGO,
                               frequence=self.frequence, market=self.market_type, output=QA.OUTPUT_FORMAT.DATASTRUCT)

        def x1(item):
            self.latest_price[item.name[1]] = item['close']
            if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
                self.on_dailyclose()
                for order in self.acc.close_positions_order:
                    order.trade('closebySys', order.price,
                                order.amount, order.datetime)
                self.on_dailyopen()
                if self.market_type == QA.MARKET_TYPE.STOCK_CN:
                    print('backtest: Settle!')
                    self.acc.settle()
            self._on_1min_bar()
            self._market_data.append(copy.deepcopy(item))
            self.running_time = str(item.name[0])
            self.on_bar(item)

        data.data.apply(x1, axis=1)

    def debug_currenttick(self, freq):
        data = QA.QA_fetch_get_future_transaction_realtime(
            'tdx', self.code.upper())
        self.running_mode = 'backtest'
        self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        user = QA_User(username=self.username, password=self.password)
        port = user.new_portfolio(self.portfolio)
        self.strategy_id = self.strategy_id + \
            'currenttick_{}_{}'.format(str(datetime.date.today()), freq)
        self.acc = port.new_accountpro(
            account_cookie=self.strategy_id, init_cash=self.init_cash, market_type=self.market_type)
        self.positions = self.acc.get_position(self.code)
        data = data.assign(price=data.price/1000).loc[:, ['code', 'price', 'volume']].resample(
            freq).apply({'code': 'last', 'price': 'ohlc', 'volume': 'sum'}).dropna()
        data.columns = data.columns.droplevel(0)
        data = data.reset_index().set_index(['datetime', 'code'])

        def x1(item):
            self.latest_price[item.name[1]] = item['close']
            if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
                self.on_dailyclose()
                self.on_dailyopen()
            self._on_1min_bar()
            self._market_data.append(copy.deepcopy(item))
            self.running_time = str(item.name[0])
            self.on_bar(item)

        data.apply(x1, axis=1)

    def debug_histick(self, freq):
        data = QA.QA_fetch_get_future_transaction(
            'tdx', self.code.upper(), self.start, self.end)
        self.running_mode = 'backtest'
        self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        user = QA_User(username=self.username, password=self.password)
        port = user.new_portfolio(self.portfolio)
        self.strategy_id = self.strategy_id + \
            'histick_{}_{}_{}'.format(self.start, self.end, freq)
        self.acc = port.new_accountpro(
            account_cookie=self.strategy_id, init_cash=self.init_cash, market_type=self.market_type)
        self.positions = self.acc.get_position(self.code)
        data = data.assign(price=data.price/1000).loc[:, ['code', 'price', 'volume']].resample(
            freq).apply({'code': 'last', 'price': 'ohlc', 'volume': 'sum'}).dropna()
        data.columns = data.columns.droplevel(0)
        data = data.reset_index().set_index(['datetime', 'code'])

        def x1(item):
            self.latest_price[item.name[1]] = item['close']
            if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
                self.on_dailyclose()
                self.on_dailyopen()
            self._on_1min_bar()
            self._market_data.append(copy.deepcopy(item))
            self.running_time = str(item.name[0])
            self.on_bar(item)

        data.apply(x1, axis=1)

    def subscribe_data(self, code, frequence, data_host, data_port, data_user, data_password, model='py'):
        """[summary]

        Arguments:
            code {[type]} -- [description]
            frequence {[type]} -- [description]
        """

        if frequence.endswith('min'):
            if model == 'py':
                self.sub = subscriber(exchange='realtime_{}_{}'.format(
                    frequence, code), host=data_host, port=data_port, user=data_user, password=data_password)
            elif model == 'rust':
                self.sub = subscriber_routing(exchange='realtime_{}'.format(
                    code), routing_key=frequence, host=data_host, port=data_port, user=data_user, password=data_password)
            self.sub.callback = self.callback
        elif frequence.endswith('s'):

            import re
            self._num_cached = 2*int(re.findall(r'\d+', self.frequence)[0])
            self.sub = subscriber_routing(
                exchange='CTPX', routing_key=code, host=data_host, port=data_port, user=data_user, password=data_password)
            self.sub.callback = self.second_callback
        elif frequence.endswith('tick'):
            self._num_cached = 1
            self.sub = subscriber_routing(
                exchange='CTPX', routing_key=code, host=data_host, port=data_port, user=data_user, password=data_password)
            self.sub.callback = self.tick_callback

    def subscribe_multi(self, codelist, frequence, data_host, data_port, data_user, data_password, model='py'):
        if frequence.endswith('min'):
            if model == 'rust':
                self.sub = subscriber_routing(exchange='realtime_{}'.format(
                    codelist[0]), routing_key=frequence, host=data_host, port=data_port, user=data_user, password=data_password)
                for item in codelist[1:]:
                    self.sub.add_sub(exchange='realtime_{}'.format(
                        item), routing_key=frequence)
            elif model == 'py':
                self.sub = subscriber_routing(exchange='realtime_{}'.format(
                    codelist[0].lower()), routing_key=frequence, host=data_host, port=data_port, user=data_user, password=data_password)
                for item in codelist[1:]:
                    self.sub.add_sub(exchange='realtime_{}'.format(
                        item.lower()), routing_key=frequence)
            self.sub.callback = self.callback
        elif frequence.endswith('tick'):

            self._num_cached = 1
            self.sub = subscriber_routing(exchange='CTPX', routing_key=codelist[0].lower(
            ), host=data_host, port=data_port, user=data_user, password=data_password)
            for item in codelist[1:]:
                self.sub.add_sub(exchange='CTPX', routing_key=item.lower())

            self.sub.callback = self.tick_callback

    @property
    def old_data(self):
        return self._old_data

    def update(self):
        """
        此处是切换bar的时候的节点
        """
        self._old_data = self._market_data
        self._on_1min_bar()

    @property
    def market_datetime(self):
        """计算的market时间点  此api慎用 因为会惰性计算全市场的值

        Returns:
            [type] -- [description]
        """
        return self.market_data.index.levels[0]

    @property
    def market_data(self):

        if self.running_mode == 'sim':
            return self._market_data
        elif self.running_mode == 'backtest':
            return pd.concat(self._market_data[-100:], axis=1, sort=False).T

    def force_close(self):
        # 强平
        if self.positions.volume_long > 0:
            self.send_order('SELL', 'CLOSE', price=self.positions.last_price,
                            volume=self.positions.volume_long)
        if self.positions.volume_short > 0:
            self.send_order('BUY', 'CLOSE', price=self.positions.last_price,
                            volume=self.positions.volume_short)

    def upcoming_data(self, new_bar):
        """upcoming_bar :

        在这一步中, 我们主要进行的是

        1. 更新self._market_data
        2. 更新账户
        3. 更新持仓

        4. 通知on_bar


        Arguments:
            new_bar {pd.DataFrame} -- [description]
        """
        code = new_bar.index.levels[1][0]
        if len(self._old_data) > 0:
            self._market_data = pd.concat(
                [self._old_data, new_bar], sort=False)
        else:
            self._market_data = new_bar
        # QA.QA_util_log_info(self._market_data)

        if self.isupdate:
            self.update()
            self.isupdate = False

        self.update_account()
        if isinstance(self.code, str):
            self.positions.on_price_change(float(self.latest_price[code]))
        else:
            for item in self.code:
                self.acc.get_position(item).on_price_change(
                    float(self.latest_price[code]))
        self.on_bar(json.loads(
            new_bar.reset_index().to_json(orient='records'))[0])

    def ind2str(self, ind, ind_type):
        z = ind.tail(1).reset_index().to_dict(orient='records')[0]
        return json.dumps({'topic': ind_type, 'code': self.code, 'type': self.frequence, 'data': z})

    def second_callback(self, a, b, c, body):
        """在strategy的callback中,我们需要的是

        1. 更新数据
        2. 更新bar
        3. 更新策略状态
        4. 推送事件

        Arguments:
            a {[type]} -- [description]
            b {[type]} -- [description]
            c {[type]} -- [description]
            body {[type]} -- [description]

        second ==> 2*second tick

        b'{"ask_price_1": 4145.0, "ask_price_2": 0, "ask_price_3": 0, "ask_price_4": 0, "ask_price_5": 0, 
        "ask_volume_1": 69, "ask_volume_2": 0, "ask_volume_3": 0, "ask_volume_4": 0, "ask_volume_5": 0, 
        "average_price": 61958.14258714826, 
        "bid_price_1": 4143.0, "bid_price_2": 0, "bid_price_3": 0, "bid_price_4": 0, "bid_price_5": 0, 
        "bid_volume_1": 30, "bid_volume_2": 0, "bid_volume_3": 0, "bid_volume_4": 0, "bid_volume_5": 0, 
        "datetime": "2019-11-20 01:57:08", "exchange": "SHFE", "gateway_name": "ctp", 
        "high_price": 4152.0, "last_price": 4144.0, "last_volume": 0,
        "limit_down": 3872.0, "limit_up": 4367.0, "local_symbol": "ag1912.SHFE", 
        "low_price": 4105.0, "name": "", "open_interest": 277912.0, "open_price": 4140.0, 
        "preSettlementPrice": 4120.0, "pre_close": 4155.0, 
        "symbol": "ag1912", 
        "volume": 114288}'


        tick 会基于热数据的量 self._num_cached 来判断更新/重采样

        """

        self.new_data = json.loads(str(body, encoding='utf-8'))

        self._cached_data.append(self.new_data)
        self.latest_price[self.new_data['symbol']
                          ] = self.new_data['last_price']

        # if len(self._cached_data) == self._num_cached:
        #     self.isupdate = True

        if len(self._cached_data) > 3*self._num_cached:
            # 控制缓存数据量
            self._cached_data = self._cached_data[self._num_cached:]

        data = pd.DataFrame(self._cached_data).loc[:, [
            'datetime', 'last_price', 'volume']]
        data = data.assign(datetime=pd.to_datetime(data.datetime)).set_index('datetime').resample(
            self.frequence).apply({'last_price': 'ohlc', 'volume': 'last'}).dropna()
        data.columns = data.columns.droplevel(0)

        data = data.assign(volume=data.volume.diff(),
                           code=self.new_data['symbol'])
        data = data.reset_index().set_index(['datetime', 'code'])

        self.acc.on_price_change(
            self.new_data['symbol'], self.latest_price[self.new_data['symbol']])
        # .loc[:, ['open', 'high', 'low', 'close', 'volume', 'tradetime']]
        now = datetime.datetime.now()
        if now.hour == 20 and now.minute == 59 and now.second < 10:
            self.daily_func()
            time.sleep(10)

        self.running_time = self.new_data['datetime']
        # print(data.iloc[-1].index[0])
        if self.dt != data.index[-1][0]:
            self.isupdate = True
            self.dt = data.index[-1][0]
        self.upcoming_data(data.tail(1))

    def tick_callback(self, a, b, c, body):
        self.new_data = json.loads(str(body, encoding='utf-8'))
        self.latest_price[self.new_data['symbol']
                          ] = self.new_data['last_price']
        self.running_time = self.new_data['datetime']
        self.on_tick(self.new_data)

    def get_code_marketdata(self, code):
        return self.market_data.loc[(slice(None), code), :]

    def get_current_marketdata(self):
        return self.market_data.loc[(self.running_time, slice(None)), :]

    def callback(self, a, b, c, body):
        """在strategy的callback中,我们需要的是

        1. 更新数据
        2. 更新bar
        3. 更新策略状态
        4. 推送事件

        Arguments:
            a {[type]} -- [description]
            b {[type]} -- [description]
            c {[type]} -- [description]
            body {[type]} -- [description]
        """

        self.new_data = json.loads(str(body, encoding='utf-8'))
        self.latest_price[self.new_data['code']] = self.new_data['close']

        if self.dt != str(self.new_data['datetime'])[0:16]:
            # [0:16]是分钟线位数
            self.dt = str(self.new_data['datetime'])[0:16]
            self.isupdate = True

        self.acc.on_price_change(self.new_data['code'], self.new_data['close'])
        # .loc[:, ['open', 'high', 'low', 'close', 'volume', 'tradetime']]

        bar = pd.DataFrame([self.new_data]).set_index(['datetime', 'code'])

        now = datetime.datetime.now()
        if now.hour == 20 and now.minute == 59 and now.second < 10:
            self.daily_func()
            time.sleep(10)

        # res = self.job_control.find_one(
        #     {'strategy_id': self.strategy_id, 'strategy_id': self.strategy_id})
        # self.control_status(res)
        self.running_time = self.new_data['datetime']
        self.upcoming_data(bar)

    def control_status(self, res):
        print(res)

    def add_subscriber(self, qaproid):
        """Add a subscriber
        增加订阅者的QAPRO_ID

        """
        self.subscriber_client.insert_one(
            {'strategy_id': self.strategy_id, 'user_id': qaproid})

    @property
    def subscriber_list(self):
        """订阅者

        Returns:
            [type] -- [description]
        """

        return list(set([item['user_id'] for item in self.subscriber_client.find({'strategy_id': self.strategy_id})]))

    def load_strategy(self):
        raise NotImplementedError

    def on_dailyopen(self):
        pass

    def on_dailyclose(self):
        pass

    def on_bar(self, bar):
        raise NotImplementedError

    def on_tick(self, tick):
        raise NotImplementedError

    def _on_1min_bar(self):
        #raise NotImplementedError
        if len(self._systemvar.keys()) > 0:
            self._signal.append(copy.deepcopy(self._systemvar))
        try:
            self.on_1min_bar()
        except:
            pass

    def on_deal(self, order):
        """

        order is a dict type
        """
        print('------this is on deal message ------')
        print(order)

    def on_1min_bar(self):
        raise NotImplementedError

    def on_5min_bar(self):
        raise NotImplementedError

    def on_15min_bar(self):
        raise NotImplementedError

    def on_30min_bar(self):
        raise NotImplementedError

    def order_handler(self):
        self._orders = {}

    def daily_func(self):
        QA.QA_util_log_info('DAILY FUNC')

    def risk_check(self):
        pass

    def plot(self, name, data, format):
        """ plot是可以存储你的临时信息的接口, 后期会接入可视化



        Arguments:
            name {[type]} -- [description]
            data {[type]} -- [description]
            format {[type]} -- [description]
        """
        self._systemvar[name] = {'datetime': copy.deepcopy(str(
            self.running_time)), 'value': data, 'format': format}

    def get_code(self):
        if isinstance(self.code, str):
            return self.code
        else:
            return self.code[0]

    def check_order(self, direction, offset, code=None):
        """[summary]
        同方向不开仓  只对期货市场做限制

        buy - open
        sell - close
        """
        if code == None:
            code = self.get_code()

        if self.market_type == QA.MARKET_TYPE.FUTURE_CN:

            if self.last_order_towards[code][direction] == str(offset):
                return False
            else:
                return True
        else:
            return True

    def on_ordererror(self, direction, offset, price, volume):
        print('order Error ')

    def receive_simpledeal(self,
                           code: str,
                           trade_time,
                           trade_amount,
                           direction,
                           offset,
                           trade_price,
                           message='sell_open'):
        self.send_order(direction=direction, offset=offset,
                        volume=trade_amount, price=trade_price, order_id=QA.QA_util_random_with_topic(self.strategy_id))

    def send_order(self,  direction='BUY', offset='OPEN', price=3925, volume=10, order_id='', code=None):
        if code == None:
            code = self.get_code()

        towards = eval('ORDER_DIRECTION.{}_{}'.format(direction, offset))
        order_id = str(uuid.uuid4()) if order_id == '' else order_id

        if isinstance(price, float):
            pass
        elif isinstance(price, pd.Series):
            price = price.values[0]

        if self.running_mode == 'sim':
            # 在此处拦截无法下单的订单
            if (direction == 'BUY' and self.latest_price[code] <= price) or (direction == 'SELL' and self.latest_price[code] >= price):
                QA.QA_util_log_info(
                    '============ {} SEND ORDER =================='.format(order_id))
                QA.QA_util_log_info('direction{} offset {} price{} volume{}'.format(
                    direction, offset, price, volume))

                if self.check_order(direction, offset, code=code):
                    #self.last_order_towards = {'BUY': '', 'SELL': ''}
                    self.last_order_towards[code][direction] = offset
                    now = str(datetime.datetime.now())

                    order = self.acc.send_order(
                        code=code, towards=towards, price=price, amount=volume, order_id=order_id)
                    print(order)
                    order['topic'] = 'send_order'
                    self.pub.pub(
                        json.dumps(order), routing_key=self.strategy_id)

                    self.acc.make_deal(order)
                    self.on_deal(order)
                    self.bar_order['{}_{}'.format(
                        direction, offset)] = self.bar_id
                    if self.send_wx:
                        for user in self.subscriber_list:
                            QA.QA_util_log_info(self.subscriber_list)
                            try:
                                requests.post('http://www.yutiansut.com/signal?user_id={}&template={}&strategy_id={}&realaccount={}&code={}&order_direction={}&order_offset={}&price={}&volume={}&order_time={}'.format(
                                    user, "xiadan_report", self.strategy_id, self.acc.user_id, code.lower(), direction, offset, price, volume, now))
                            except Exception as e:
                                QA.QA_util_log_info(e)

                else:
                    QA.QA_util_log_info('failed in ORDER_CHECK')
            else:
                self.on_ordererror(direction, offset, price, volume)
        elif self.running_mode == 'backtest':

            self.bar_order['{}_{}'.format(direction, offset)] = self.bar_id

            if self.market_type == 'stock_cn':
                order = self.acc.send_order(
                    code=code, amount=volume, time=self.running_time, towards=towards, price=price)
                order.trade(order.order_id, order.price,
                            order.amount, order.datetime)
                self.on_deal(order.to_dict())
            else:
                self.acc.receive_simpledeal(
                    code=code, trade_time=self.running_time, trade_towards=towards, trade_amount=volume, trade_price=price, order_id=order_id, realorder_id=order_id, trade_id=order_id)

                self.on_deal({
                    'code': code,
                    'trade_time': self.running_time,
                    'trade_towards': towards,
                    'trade_amount': volume,
                    'trade_price': price,
                    'order_id': order_id,
                    'realorder_id': order_id,
                    'trade_id': order_id
                })
            self.positions = self.acc.get_position(code)

    def update_account(self):
        if self.running_mode == 'sim':
            QA.QA_util_log_info('{} UPDATE ACCOUNT'.format(
                str(datetime.datetime.now())))

            self.accounts = self.acc.account_msg
            self.orders = self.acc.orders
            if isinstance(self.code, str):
                self.positions = self.acc.get_position(self.code)
            else:
                pass
            self.trades = self.acc.trades
            self.updatetime = self.acc.dtstr

            self.on_sync()
        elif self.running_mode == 'backtest':
            if isinstance(self.code, str):
                self.positions = self.acc.get_position(self.code)
            else:
                pass

    def get_exchange(self, code):
        return self.market_preset.get_exchange(code)

    def get_positions(self, code):
        if self.running_mode == 'sim':
            self.update_account()
            return self.acc.get_position(code)
        elif self.running_mode == 'backtest':
            return self.acc.get_position(code)

    def get_cash(self):
        if self.running_mode == 'sim':
            self.update_account()
            return self.accounts.get('available', '')
        elif self.running_mode == 'backtest':
            return self.acc.cash_available

    def run(self):

        while True:
            time.sleep(self.risk_check_gap)
            self.risk_check()


if __name__ == '__main__':
    QAStrategyCTABase(code='rb2005').run()
