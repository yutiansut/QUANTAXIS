import datetime
import re

import empyrical as em
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfolio as pf
import pymongo
import QUANTAXIS as QA
from qaenv import mongo_ip

#mongo_ip = '192.168.2.117'


def mergex(dict1, dict2):
    dict1.update(dict2)
    return dict1


def promise_list(value):
    return value if isinstance(value, list) else [value]


class QA_QIFIMANAGER():
    """
    用于管理单 qifi 的历史交易情况

    --> 对标 QAAccount 的历史回测模式
    --> 需要增加 QARisk/ QAPerformance 部分的支持
    --> 需要增加对于 QAWEBSERVER 部分的支持
    --> 需要增加对于 web 前端部分的支持

    """

    def __init__(self, account_cookie, mongo_ip=mongo_ip, database='quantaxis', collection='history'):
        self.database = self.change_database(database, collection)
        self.database.create_index([("account_cookie", pymongo.ASCENDING),
                                    ("trading_day", pymongo.ASCENDING)], unique=True)

        self.account_cookie = account_cookie
        self.assets = self.get_historyassets()
        self.trade = self.get_historytrade()
        self.assets_start = self.assets.index[0]
        self.assets_end = self.assets.index[-1]
        self.benchmark_code = '000300'
        self.benchmark_assets = self.get_benchmark_assets(
            self.benchmark_code, self.assets_start, self.assets_end)

    def __expr__(self):
        return f"{self.account_cookie}- start: {self.assets_start} - end: {self.assets_end}- benchmark: {self.benchmark_code}"

    def get_benchmark_assets(self, code, start, end):
        return QA.QA_fetch_index_day_adv(code, start, end).data.reset_index(1).close

    def set_benchmark_assets(self, assets):
        self.benchmark_assets = assets.loc[self.assets_start, self.assets_end]

    def change_database(self, database_name, collection_name):

        return pymongo.MongoClient(mongo_ip).get_database(
            database_name).get_collection(collection_name)

    def get_qifislice(self, date):
        return self.database.find_one({'account_cookie': self.account_cookie, 'trading_day': date})

    @property
    def returns(self):
        returns = self.assets.pct_change()

        returns.index = returns.index
        return returns

    @property
    def benchmark_returns(self):
        returns = self.benchmark_assets.pct_change()
        try:
            returns.index = returns.index
        except:
            pass
        return returns

    @property
    def month_assets(self):
        return self.assets.resample('M').last()

    @property
    def month_assets_profit(self):
        res = pd.concat([pd.Series(self.assets.iloc[0]),
                         self.month_assets]).diff().dropna()
        res.index = res.index.map(str)
        return res

    def get_historyassets(self, start='1990-01-01', end=str(datetime.date.today())) -> pd.Series:
        b = [(item['accounts']['balance'], item['trading_day']) for item in self.database.find(
            {'account_cookie': self.account_cookie}, {'_id': 0, 'accounts': 1, 'trading_day': 1})]
        res = pd.DataFrame(b, columns=['balance', 'trading_day']).dropna()


        print(res.trading_day[0])
        res = res[res.trading_day.apply(lambda x: x!='')]
        res = res.assign(datetime=pd.to_datetime(
            res['trading_day']), balance=res.balance.apply(round, 2)).dropna().set_index('datetime').sort_index()
        res = res.balance
        res.name = self.account_cookie

        print(res)
        return res.bfill().ffill().sort_index().loc[start:end]

    def get_historytrade(self,):
        b = [item['trades'].values() for item in self.database.find(
            {'account_cookie': self.account_cookie}, {'_id': 0, 'trades': 1, 'trading_day': 1})]
        i = []
        for ix in b:
            i.extend(list(ix))
        res = pd.DataFrame(i)
        # print(res)
        res = res.assign(account_cookie=res['user_id'], code=res['instrument_id'], tradetime=res['trade_date_time'].apply(
            lambda x:  datetime.datetime.fromtimestamp(x/1000000000))).set_index(['tradetime', 'code']).sort_index()
        return res.drop_duplicates().sort_index()

    def get_sharpe(self):
        n = self.get_historyassets()
        a = ((n.iloc[-1]/n.iloc[0] - 1)/len(n)*365) / \
            abs((n.pct_change()*100).std())
        return 0 if np.isnan(a) else a

    def show_perf_stats(self, live_start_date=None):
        pf.show_perf_stats(self.returns, self.benchmark_returns,
                           live_start_date=live_start_date)

    def create_returns_tear_sheet(self, live_start_date=None):
        pf.create_returns_tear_sheet(
            self.returns,  benchmark_rets=self.benchmark_returns, live_start_date=live_start_date)
        plt.show()


class QA_QIFISMANAGER():
    """
    用于管理多 qifi 的历史交易情况

    --> 对标 QAAccount 的历史回测模式
    --> 需要增加 QARisk/ QAPerformance 部分的支持
    --> 需要增加对于 QAWEBSERVER 部分的支持
    --> 需要增加对于 web 前端部分的支持

    """

    def __init__(self, mongo_ip=mongo_ip, account_cookie='', model='BACKTEST'):

        if model =='REALTIME':
            self.database = pymongo.MongoClient(mongo_ip).QAREALTIME.account
        else:

            self.database = pymongo.MongoClient(mongo_ip).quantaxis.history
            self.database.create_index([("account_cookie", pymongo.ASCENDING),
                                        ("trading_day", pymongo.ASCENDING)], unique=True)

    def promise_list(self, value) -> list:
        return value if isinstance(value, list) else [value]

    def get_allportfolio(self) -> list:
        print(self.database)
        return list(set([i['portfolio'] for i in self.database.find({}, {'portfolio': 1, '_id': 0})]))

    def get_portfolio_account(self, portfolio) -> list:
        return list(set([i['account_cookie'] for i in self.database.find({'portfolio': portfolio}, {'account_cookie': 1, '_id': 0})]))

    def query_re(self, text) -> list:
        return list(set([i['account_cookie'] for i in self.database.find({'account_cookie': {"$regex": text}}, {'account_cookie': 1, '_id': 0})]))

    def get_portfolio_panel(self, portfolio) -> pd.DataFrame:
        r = self.get_portfolio_account(portfolio)
        
        rp = [self.database.find_one({'account_cookie': i}, {
                                     "accounts": 1, 'trading_day': 1, '_id': 0}) for i in r]
        return pd.DataFrame([mergex(i['accounts'], {'trading_day': i['trading_day']}) for i in rp]).query('user_id in {}'.format(r))

    def get_allaccountname(self) -> list:
        return list(set([i['account_cookie'] for i in self.database.find({}, {'account_cookie': 1, '_id': 0})]))

    def get_historyassets(self, account_cookie, start='1990-01-01', end=str(datetime.date.today())) -> pd.Series:
        b = [(item['accounts']['balance'], item['trading_day']) for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'accounts': 1, 'trading_day': 1})]
        res = pd.DataFrame(b, columns=['balance', 'trading_day'])
        res = res.assign(datetime=pd.to_datetime(
            res['trading_day']), balance=res.balance.apply(round, 2)).set_index('datetime').sort_index()
        res = res.balance
        res.name = account_cookie

        return res.bfill().ffill().loc[start:end]

    def get_sharpe(self, n):
        a = ((n.iloc[-1]/n.iloc[0] - 1)/len(n)*365) / \
            abs((n.pct_change()*100).std())
        return 0 if np.isnan(a) else a

    def get_portfolio_assets(self, portfolio, start='1990-01-01', end=str(datetime.date.today())) -> pd.Series:
        """
                        KTKS_t05_au2106_15min  KTKS_t04b_au2106_5min  KTKS_t12_au2106_30min  KTKS_t04_au2106_15min  ...  KTKS_t01_au2106_15min  KTKS_t03_au2106_15min  KTKS_t01b2_au2106_5min  KTKS_t15_au2106_5min
        datetime                                                                                                ...
        2020-01-02                 100000                 100000                 100000                 100000  ...                 100000                 100000                  100000                 99340
        2020-01-03                 100000                 100723                 100000                 100000  ...                 101080                 101099                  102880                104310
        2020-01-06                 100000                 108153                 100000                 100000  ...                 108510                 108529                  110310                108830       
        2020-01-07                 100000                 104813                 100000                 100000  ...                 104930                 105189                  110030                109790       
        """
        return pd.concat([self.get_historyassets(acc, start, end) for acc in portfolio], axis=1)

    def get_historytrade(self, account_cookie):
        b = [item['trades'].values() for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'trades': 1, 'trading_day': 1})]
        i = []
        for ix in b:
            i.extend(list(ix))
        res = pd.DataFrame(i)
        # print(res)
        res = res.assign(account_cookie=res['user_id'], code=res['instrument_id'], tradetime=res['trade_date_time'].apply(
            lambda x:  datetime.datetime.fromtimestamp(x/1000000000))).set_index(['tradetime', 'code']).sort_index()
        return res.drop_duplicates().sort_index()

    def get_historyorders(self, account_cookie):
        b = [item['orders'].values() for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'orders': 1, 'trading_day': 1})]
        i = []
        for ix in b:
            i.extend(list(ix))
        res = pd.DataFrame(i)
        res = res.assign(account_cookie=res['user_id'], code=res['instrument_id'], ordertime=res['insert_date_time'].apply(
            lambda x:  datetime.datetime.fromtimestamp(x/1000000000))).set_index(['ordertime', 'code']).sort_index()
        return res.drop_duplicates().sort_index()


    def rankstrategy(self, code):
        res = pd.concat([self.get_historyassets(i) for i in code], axis=1)
        res = res.fillna(method='bfill').ffill()
        rp = (res.apply(self.get_sharpe) + res.tail(50).apply(self.get_sharpe) +
              res.tail(10).apply(self.get_sharpe)).sort_values()

        return rp[rp > 0.5].sort_values().tail(2)

    def get_historypos(self, account_cookie):
        b = [mergex(list(item['positions'].values())[0], {'trading_day': item['trading_day']}) for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'positions': 1, 'trading_day': 1})]
        res = pd.DataFrame(b)
        res.name = account_cookie
        return res.set_index('trading_day')

    def get_lastpos(self, account_cookie):
        b = [mergex(list(item['positions'].values())[0], {'trading_day': item['trading_day']}) for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'positions': 1, 'trading_day': 1})]
        res = pd.DataFrame(b)
        res.name = account_cookie
        return res.iloc[-1]

    def get_historymargin(self, account_cookie):
        b = [(item['accounts']['margin'], item['trading_day']) for item in self.database.find(
            {'account_cookie': account_cookie}, {'_id': 0, 'accounts': 1, 'trading_day': 1})]
        res = pd.DataFrame(b, columns=['balance', 'trading_day'])
        res = res.assign(datetime=pd.to_datetime(
            res['trading_day'])).set_index('datetime').sort_index()
        res = res.balance
        res.name = account_cookie
        return res

    def get_holding_panel(self, account_cookie, trading_day):
        # print(self.database)
        # print(account_cookie)
        # print(trading_day)
        b = list(self.database.find_one(
            {'account_cookie': account_cookie, 'trading_day': trading_day}, {'_id': 0, 'positions': 1})['positions'].values())
        res = pd.DataFrame(b)
        res.name = account_cookie
        return res.assign(code=res.instrument_id).set_index('code')

    def get_holding_block(self, account_cookie, trading_day):
        b = list(self.database.find_one(
            {'account_cookie': account_cookie}, {'_id': 0, 'positions': 1})['positions'].values())
        res = pd.DataFrame(b)
        res.name = account_cookie

        return res.assign(code=res.instrument_id).set_index('code')

    def drop_account(self, account_cookie):
        self.database.delete_many({'account_cookie': account_cookie})

    def drop_many(self, account_cookies):
        account_cookies = promise_list(account_cookies)
        self.database.delete_many({'account_cookie': {'$IN': account_cookies}})


if __name__ == "__main__":
    manager = QA_QIFIMANAGER('192.168.2.124')
    # #acc = manager.get_allaccountname()
    # # print()
    # import matplotlib.pyplot as plt
    # manager.get_historyassets().plot()
    # plt.show()

    # r = manager.month_assets_profit
    # r.plot.bar()
    # plt.show()
    # print(r)
    # print(manager.get_holding_panel(
    #     '5c9b4ed1-8f13-4006-b24a-8fed6e1d5749', '2018-01-02'))
