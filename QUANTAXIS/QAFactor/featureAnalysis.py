from copy import deepcopy
from functools import lru_cache

import clickhouse_driver
import pandas as pd
import statsmodels.api as sm
from alphalens.tears import create_full_tear_sheet
from alphalens.utils import get_clean_factor_and_forward_returns
from qaenv import (clickhouse_ip, clickhouse_password, clickhouse_port,
                   clickhouse_user)
from QUANTAXIS.QAFetch.QAClickhouse import QACKClient
from scipy import stats

"""
本模块大量基于 QACkClient 目前 ck 的公共服务器暂时尚未开放, 仅供参考和测试使用


当你使用自建的数据库时, 因子数据一定是保存在 factor 这个因子库中的

如果你需要更换数据源, 可以直接复用基类, 替换以下方法:

get_benchmark
get_industry
get_barra
"""


class QAFeatureAnalysis():
    def __init__(self, featuredata, feature_name=None, stock_data=None, returnday=5,
                 host=clickhouse_ip, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password) -> None:

        self.feature = featuredata
        self.featurename = featuredata.name if feature_name is None else feature_name
        self.feature.name = self.featurename

        self.codelist = self.feature.index.levels[1].unique().tolist()
        self.start = self.feature.index.levels[0][0]
        self.end = self.feature.index.levels[0][-1]

        self._host = host
        self._port = port
        self._user = user
        self._password = password

        self.factorclient = clickhouse_driver.Client(host=self._host, port=self._port, user=self._user, password=self._password,
                                                     database='factor')

        self.dataclient = QACKClient(
            host=self._host, port=self._port, user=self._user, password=self._password)

        if stock_data is None:
            self.stock_data = self.dataclient.get_stock_day_qfq_adv(
                self.codelist, self.start, self.end)
        else:
            self.stock_data = stock_data

        self.returns = self.make_ret(self.stock_data.data, returnday)

    def remake_returns(self, model='next_open', day=5):
        self.returns = self.make_ret(self.stock_data.data, model, day)



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
        return QAFeatureAnalysis(self.rank, stock_data=self.stock_data, host=self._host, port=self._port, user=self._user, password=self._password)

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

    def get_benchmark(self, benchmarkcode='000905.XSHG'):
        return self.dataclient.get_index_day(benchmarkcode, self.start, self.end)

    def get_industry(self):
        """
        index: stock
        columns: industry

                 industry
        stock1      A
        stock2      B

        """
        return self.dataclient.get_stock_industry(self.codelist, self.start, self.end)

    def categorical(self, data: pd.DataFrame, key='industry'):
        """

        pd.DataFrame


        index : stock

        columns : key must be some of the columns, default: industry

                 industry    factor_i   ....   marketvalue
        stock1      A
        stock2      B


        return panel data

                    农林牧渔   非银金融   industry3 industry4 .....   industry29
        stock1          0       1           0       0               0
        stock2          1       0           0       0               0


        """
        return pd.DataFrame(sm.categorical(data[key].values, drop=True), index=data.index, columns=data[key].sort_values().unique())

    def standardize(self, data):
        """
        Data sample standardize 
        """
        return (data-data.mean())/data.std()

    def winsorize(self, data,
                  upper_q=0.99,
                  lower_q=0.01):
        upper_end = data.quantile(upper_q)
        lower_end = data.quantile(lower_q)
        data.where(data < upper_end, upper_end, inplace=True)
        data.where(data > lower_end, lower_end, inplace=True)
        return data

    def neut(neuted_data,
             neut_data,
             weight_data=None):

        X = sm.add_constant(neut_data)
        results = sm.WLS(neuted_data, X, weights=weight_data).fit()
        return results.resid

    def ic_statistic(self):
        """
        使用 concatRes 保证数据对齐
        """

        feature_data = self.concatRes.iloc[:, 0]
        return_data = self.concatRes.iloc[:, 1]

        cor_pearson = feature_data.corr(return_data, method='pearson')
        cor_spearman = feature_data.corr(return_data, method='spearman')
        t_stat = stats.ttest_ind(feature_data, return_data).statistic
        p_value = stats.ttest_ind(feature_data, return_data).pvalue

        return pd.DataFrame({
            'cor_pearson': [cor_pearson],
            'cor_spearman': [cor_spearman],
            't_stat': [t_stat],
            'p_value': [p_value]})
