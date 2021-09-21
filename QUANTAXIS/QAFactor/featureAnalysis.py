from QUANTAXIS.QAData import base_datastruct
from functools import lru_cache
import re
import clickhouse_driver
import pandas as pd
from alphalens.tears import create_full_tear_sheet
from QUANTAXIS.QAFetch.QAClickhouse import QACKClient
from qaenv import (clickhouse_ip, clickhouse_password, clickhouse_port,
                   clickhouse_user)

from alphalens.tears import create_full_tear_sheet
from alphalens.utils import get_clean_factor_and_forward_returns
from copy import deepcopy
from functools import lru_cache
from statsmodels.api import OLS


class QAFeatureAnalysis():
    def __init__(self, featuredata, stock_data=None, host=clickhouse_ip, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password) -> None:
        self.feature = featuredata
        self.codelist = self.feature.index.levels[1].unique().tolist()
        self.start = self.feature.index.levels[0][0]
        self.end = self.feature.index.levels[0][-1]

        self._host = host
        self._port = port
        self._user = user
        self._password = password

        self.client = QACKClient(host=self._host, port=self._port, user=self._user, password=self._password,
                                 database='factor')
        if stock_data is None:
            self.stock_data = self.client.get_stock_day_qfq_adv(
                self.codelist, self.start, self.end)
        else:
            self.stock_data = stock_data

        self.returns = self.make_ret(self.stock_data.data)

    def remake_returns(self, model='next_open', day=5):
        self.returns = self.make_ret(self.stock_data.data, model, day)

    def get_benchmark(self, benchmarkcode='000905.XSHG'):
        return self.client.get_index_day(benchmarkcode, self.start, self.end)

    def get_barra(self, barra_data):
        return barra_data

    def make_ret(self, data, model='next_open', day=5):
        """
        use open data make ret
        """
        if model == 'next_open':
            r = data.groupby(level=1).open.apply(
                lambda x: x.pct_change(day).shift(-day))
            r.name = 'ret_{}'.format(day)
            return r
        elif model == 'close':
            r = data.groupby(level=1).close.apply(
                lambda x: x.pct_change(day).shift(-day))
            r.name = 'ret_{}'.format(day)
            return r

    @property
    @lru_cache()
    def rank(self):
        res = self.feature.groupby(level=0).rank()
        res.columns = [res.columns[0] + '_rank']
        return res

    def apply_rank(self):
        return QAFeatureAnalysis(self.rank, self.stock_data, host=self._host, port=self._port, user=self._user, password=self._password)

    @property
    @lru_cache()
    def factor_and_forward_returns(self):
        feature = self.feature.reset_index()
        feature = feature.assign(date=pd.to_datetime(
            feature.date)).set_index('date')
        feature.index = feature.index.tz_localize('UTC')
        feature = feature.reset_index().set_index(['date', 'code'])

        panelprice = deepcopy(self.stock_data.closepanel)
        panelprice.index = pd.to_datetime(panelprice.index).tz_localize('UTC')
        return get_clean_factor_and_forward_returns(feature,
                                                    panelprice,
                                                    groupby=None,
                                                    binning_by_group=False,
                                                    quantiles=10,
                                                    bins=None,
                                                    periods=(1, 5, 10),
                                                    filter_zscore=20,
                                                    groupby_labels=None,
                                                    max_loss=0.15,
                                                    zero_aware=False,
                                                    cumulative_returns=True)

    def create_tear_sheet(self):
        return create_full_tear_sheet(self.factor_and_forward_returns)

    @property
    @lru_cache()
    def concatRes(self):
        res = pd.concat([self.feature, self.returns], axis=1)
        return res

    @property
    @lru_cache()
    def ic(self):
        res = self.concatRes.dropna().groupby(level=0).apply(
            lambda x: x.corr('spearman').values[0, 1])
        res.names = 'ic'
        return res

    @property
    @lru_cache()
    def ir(self):
        return self.ic.rolling(20).apply(lambda x: x.mean()/x.std())
