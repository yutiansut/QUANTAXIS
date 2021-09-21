from functools import lru_cache
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


class QAFeatureAnalysis():
    def __init__(self, featuredata, stock_day=None, host=clickhouse_ip, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password) -> None:
        self.feature = featuredata
        codelist = self.feature.index.levels[1].unique().tolist()
        start = self.feature.index.levels[0][0]
        end = self.feature.index.levels[0][-1]

        self.client = QACKClient(host=host, port=port, user=user, password=password,
                                 database='factor')
        if stock_day is None:
            self.stock_data = self.client.get_stock_day_qfq_adv(
                codelist, start, end)

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
                                                    quantiles=5,
                                                    bins=None,
                                                    periods=(1, 5, 10),
                                                    filter_zscore=20,
                                                    groupby_labels=None,
                                                    max_loss=0.35,
                                                    zero_aware=False,
                                                    cumulative_returns=True)

    def create_tear_sheet(self):
        return create_full_tear_sheet(self.factor_and_forward_returns)
