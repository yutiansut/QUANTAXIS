"""
因子分析主模块，集成数据输入，数据处理，数据分析，画图等功能
"""

from typing import Callable, Iterable, List, Tuple, Union

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
from fastcache import lru_cache

from QUANTAXIS.QAFactor import performance as perf
from QUANTAXIS.QAFactor import plotting, preprocess, utils
from QUANTAXIS.QAFactor.parameters import FREQUENCE_TYPE
from QUANTAXIS.QAFactor.plotting_utils import GridFigure, customize
from QUANTAXIS.QAFactor.process import get_clean_factor_and_forward_returns


class FactorAnalyzer:
    """
    单因子分析器
    """

    def __init__(
            self,
            factor: Union[pd.Series,
                          pd.DataFrame],
            prices: Union[pd.Series,
                          pd.DataFrame,
                          Callable],
            groupby: Union[pd.Series,
                           pd.DataFrame,
                           Callable],
            stock_start_date: Union[pd.Series,
                                    pd.DataFrame,
                                    Callable],
            weights: Union[float,
                           pd.Series,
                           pd.DataFrame,
                           Callable] = 1.0,
            frequence: str = "DAY",
            quantiles: Union[int,
                             Tuple[float],
                             List[float]] = 5,
            bins: Union[int,
                        Tuple[float],
                        List[float]] = None,
            periods: Union[int,
                           Tuple[int],
                           List[int]] = (1,
                                         5,
                                         10),
            binning_by_group: bool = False,
            max_loss: float = 0.25,
            zero_aware: bool = False,
    ):
        """
        初始化输入

        参数
        ---
        :param factor: 即经过我们处理过的单因子数据
        :param prices: 价格数据
        :param groupby: 行业数据
        :param stock_start_date: 上市时间
        :param weights: 因子加权数据
        :param frequence: 因子频率，如果是季线，相应的为 `1q`, 日线，则为 `1d` 等
        :param quantiles: 分位处理，既可以是 int 值，将因子等分，也可以是 0 到 1 之间的非等分区间
        :param bins: 分位处理，与 `quantiles` 只能有一个为非空
        :param periods: 用于计算因子远期收益的期数
        :param binning_by_group: 是否按照行业分别进行分位处理
        :param max_loss: 在单因子处理时，能够忍受的最大的因子损失 (丢弃的 NaN 值比例)
        :param zero_aware: 是否按照因子正负值分别进行分位处理


        说明：
            - quantiles 与 bins 只能有一个为非空
        """

        self.factor = preprocess.QA_fmt_factor(factor)
        self.prices = prices
        self.groupby = groupby
        self.stock_start_date = stock_start_date
        self.weights = weights
        self.frequence = utils.get_frequence(frequence)

        self.quantiles = quantiles
        self.bins = bins
        if isinstance(periods, int):
            periods = (periods,)
        self.periods = periods
        self.binning_by_group = binning_by_group
        self.max_loss = max_loss
        self.zero_aware = zero_aware

        # 因子加工与添加因子远期收益
        self.__gen_clean_factor_and_forward_returns()

    def __gen_clean_factor_and_forward_returns(self):
        """
        格式化因子数据，附加因子远期收益，分组，权重信息
        """
        factor_data = self.factor

        # 股票代码: 默认转换为 QA 支持格式
        code_list = utils.QA_fmt_code_list(
            list(factor_data.index.get_level_values("code").drop_duplicates())
        )

        # 因子日期
        factor_time_range = list(factor_data.index.levels[0].drop_duplicates())
        start_time = min(factor_time_range)
        end_time = max(factor_time_range)

        # 附加数据
        if hasattr(self.prices, "__call__"):
            prices = self.prices(
                code_list=code_list,
                start_time=start_time,
                end_time=end_time,
                frequence=self.frequence,
            )
            prices = prices.loc[~prices.index.duplicated()]
        else:
            prices = self.prices

        self.prices = prices

        if hasattr(self.groupby, "__call__"):
            groupby = self.groupby(
                code_list=code_list,
                factor_time_range=factor_time_range
            )
        else:
            groupby = self.groupby
        self.groupby = groupby

        if hasattr(self.stock_start_date, "__call__"):
            stock_start_date = self.stock_start_date(
                code_list=code_list,
                factor_time_range=factor_time_range
            )
        else:
            stock_start_date = self.stock_start_date
        self.stock_start_date = stock_start_date

        if hasattr(self.weights, "__call__"):
            weights = self.weights(
                code_list=code_list,
                factor_time_range=factor_time_range,
                frequence=self.frequence
            )
        else:
            weights = self.weights
        self.weights = weights

        # 周期处理
        # self.interval = utils.get_interval(self.frequence)

        # 4. 因子处理
        self._clean_factor_data = get_clean_factor_and_forward_returns(
            factor=factor_data,
            prices=self.prices,
            groupby=self.groupby,
            stock_start_date=self.stock_start_date,
            weights=self.weights,
            binning_by_group=self.binning_by_group,
            quantiles=self.quantiles,
            bins=self.bins,
            periods=self.periods,
            max_loss=self.max_loss,
            zero_aware=self.zero_aware,
            frequence=self.frequence,
        )

    @property
    def clean_factor_data(self):
        return self._clean_factor_data

    @property
    def _factor_quantile(self):
        data = self.clean_factor_data
        if not data.empty:
            return max(data.factor_quantile)
        else:
            _quantiles = self.quantiles
            _bins = self.bins
            _zero_aware = self.zero_aware

            def get_len(x):
                return len(x) - 1 if isinstance(x, Iterable) else int(x)

            if _quantiles is not None and _bins is None and not _zero_aware:
                return get_len(_quantiles)
            elif _quantiles is not None and _quantiles is None and _zero_aware:
                return int(_quantiles) // 2 * 2
            elif _bins is not None and _quantiles is None and not _zero_aware:
                return get_len(_bins)
            elif _bins is not None and _quantiles is None and _zero_aware:
                return int(_bins) // 2 * 2

    @lru_cache(16)
    def calc_mean_return_by_quantile(
            self,
            by_datetime: bool = False,
            by_group: bool = False,
            demeaned: bool = False,
            group_adjust: bool = False,
    ):
        """
        计算按分位数分组因子收益与标准差

        参数
        ---
        :param by_datetime: 按日期计算分位收益
        :param by_group: 按行业计算分位收益
        :param demeaned: 按日期计算超额收益, 并用于计算各分位数超额收益
        :param group_adjust: 按日期，分组计算超额收益，并用于计算各分位超额收益
        """
        return perf.mean_return_by_quantile(
            self._clean_factor_data,
            by_datetime=by_datetime,
            by_group=by_group,
            demeaned=demeaned,
            group_adjust=group_adjust,
        )

    def calc_mean_returns_spread(
            self,
            upper_quant: int = None,
            lower_quant: int = None,
            by_datetime: bool = True,
            by_group: bool = False,
            demeaned: bool = False,
            group_adjust: bool = False,
    ):
        """
        计算两个分位数相减的因子收益和标准差

        参数
        --
        :param upper_quant: 高分位
        :param lower_quant: 低分位
        :param by_datetime: 按日期计算两个分位数相减的因子收益和标准差
        :param demeaned: 使用超额收益
        :param group_adjust: 使用行业中性
        """
        upper_quant = upper_quant if upper_quant is not None else self._factor_quantile
        lower_quant = lower_quant if lower_quant is not None else 1

        if (not 1 <= upper_quant <= self._factor_quantile) or (
                not 1 <= lower_quant <= self._factor_quantile):
            raise ValueError(
                f"upper quant 和 low quant 取值范围是 1 ~ {self._factor_quantile} 的整数"
            )

        mean, std = self.calc_mean_return_by_quantile(
            by_datetime=by_datetime,
            by_group=by_group,
            demeaned=demeaned,
            group_adjust=group_adjust,
        )

        mean = mean.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean.columns[0]
        )
        std = std.apply(
            utils.std_conversion,
            axis=0,
            base_period=std.columns[0]
        )

        return perf.mean_returns_spread(
            mean_returns=mean,
            upper_quant=upper_quant,
            lower_quant=lower_quant,
            std_err=std,
        )

    @lru_cache(4)
    def calc_factor_alpha_beta(
            self,
            returns: pd.DataFrame = None,
            demeaned: bool = True,
            group_adjust: bool = False,
            equal_weight: bool = False,
    ):
        """
        计算因子的 alpha 和 beta
        因子加权组合每日收益 = beta x 市场组合每期收益 + alpha

        参数
        ---
        :param returns: 构建多空组合的加权收益, 默认为 None,
             为 None 时，会调用 performance 的 factor_returns，
             根据因子值构建多空组合，计算相应的按日期[或按资产]收益
        :param demeaned: 使用超额收益
        :param group_adjust: 行业中性
        :param equal_weight: 默认为 False, 如果为 True,
             分别对因子中位数构建多空组合, 多空组合权重相等
        """
        return perf.factor_alpha_beta(
            factor_data=self._clean_factor_data,
            demeaned=demeaned,
            group_adjust=group_adjust,
        )

    @customize
    def create_summary_tear_sheet(
            self,
            by_datetime=True,
            by_group: bool = False,
            long_short: bool = True,
            group_neutral: bool = False,
    ):
        """
        创建一个小型的汇总表格，包括因子的收益率分析，IC 值，换手率等分析

        参数
        ---
        :param factor_data: 因子数据
        :param long_short: 是否构建多空组合，在该组合上进行进行分析。
        :param group_neutral: 是否进行行业中性
        """
        # Returns Analysis
        mean_quant_ret, std_quant = self.calc_mean_return_by_quantile(
            by_group=by_group, demeaned=long_short, group_adjust=group_neutral)
        mean_quant_rateret = mean_quant_ret.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean_quant_ret.columns[0]
        )

        mean_quant_ret_bydatetime, std_quant_bydatetime = self.calc_mean_return_by_quantile(
            by_datetime=True, demeaned=long_short, group_adjust=group_neutral)

        mean_quant_rateret_bydatetime = mean_quant_ret_bydatetime.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean_quant_ret_bydatetime.columns[0],
        )
        std_quant_rate_bydatetime = std_quant_bydatetime.apply(
            utils.rate_of_return,
            axis=0,
            base_period=std_quant_bydatetime.columns[0]
        )

        alpha_beta = self.calc_factor_alpha_beta(
            demeaned=long_short,
            group_adjust=group_neutral
        )

        mean_ret_spread_quant, std_spread_quant = self.calc_mean_returns_spread(
        )

        fr_cols = utils.get_forward_returns_columns(
            self._clean_factor_data.columns
        )

        vertical_sections = 2 + len(fr_cols) * 3
        gf = GridFigure(rows=vertical_sections, cols=1)

        plotting.plot_quantile_statistics_table(self._clean_factor_data)
        plotting.plot_returns_table(
            alpha_beta,
            mean_quant_rateret,
            mean_ret_spread_quant
        )
        plotting.plot_quantile_returns_bar(
            mean_quant_rateret,
            by_group=False,
            ylim_percentiles=None,
            ax=gf.next_row()
        )

        # Information Analysis
        ic = perf.factor_information_coefficient(self._clean_factor_data)
        plotting.plot_information_table(ic)

        # Turnover Analysis
        # FIXME: 股票是 T+1，意味着频率只能是 Day 及以上频率
        quantile_factor = self._clean_factor_data["factor_quantile"]
        quantile_turnover = {
            p: pd.concat(
                [
                    perf.quantile_turnover(quantile_factor,
                                           q,
                                           p)
                    for q in range(1,
                                   int(quantile_factor.max()) + 1)
                ],
                axis=1,
            )
            for p in self.periods
        }
        autocorrelation = pd.concat(
            [
                perf.factor_rank_autocorrelation(
                    self._clean_factor_data,
                    period
                ) for period in self.periods
            ],
            axis=1,
        )

        plotting.plot_turnover_table(autocorrelation, quantile_turnover)

        plt.show()
        gf.close()


#     @customize
#     def create_full_tear_sheet(
#         self,
#         factor_data: pd.DataFrame,
#         long_short: bool = True,
#         group_neutral: bool = False,
#         by_group: bool = False,
#     ):
#         """
#         详细统计图表
#         """
#         plotting.plot_quantile_statistics_table(self._clean_factor_data)
#         self.create_returns_tear_sheet(
#             self._clean_factor_data,
#             long_short,
#             group_neutral,
#             by_group,
#             set_context=False,
#         )
#
#     def create_returns_tear_sheet(
#         self,
#         facotr_data: pd.DataFrame,
#         long_short: bool = True,
#         group_neutral: bool = False,
#         by_group: bool = False,
#     ):
#         """
#         创建因子收益分析表
#         """
#         factor_returns = perf.factor_returns(
#             factor_data=self._clean_factor_data,
#             demeaned=long_short,
#             group_adjust=group_neutral,
#         )
#         mean_quant_ret, std_quantile = self.calc_mean_return_by_quantile(
#             by_group=False, demeaned=long_short, group_adjust=group_neutral
#         )
#         mean_quant_rateret = mean_quant_ret.apply(
#             utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
#         )
#
#         mean_quant_ret_bydatetime, std_quant_bydatetime = self.calc_mean_return_by_quantile(
#             by_datetime=True, demeaned=long_short, group_adjust=group_neutral
#         )
#
#         mean_quant_rateret_bydatetime = mean_quant_ret_bydatetime.apply(
#             utils.rate_of_return,
#             axis=0,
#             base_period=mean_quant_ret_bydatetime.columns[0],
#         )
#         compstd_quant_bydatetime = std_quant_bydatetime.apply(
#             utils.rate_of_return, axis=0, base_period=std_quant_bydatetime.columns[0]
#         )
#
#         alpha_beta = self.calc_factor_alpha_beta(
#             demeaned=long_short, group_adjust=group_neutral
#         )
#
#         mean_ret_spread_quant, std_spread_quant = self.calc_mean_returns_spread()
#
#         fr_cols = utils.get_forward_returns_columns(
#             self._clean_factor_data.columns)
#
#         vertical_sections = 2 + len(fr_cols) * 3
#         gf = GridFigure(rows=vertical_sections, cols=1)
#
#         plotting.plot_returns_table(
#             alpha_beta, mean_quant_rateret, mean_ret_spread_quant
#         )
#
#         plotting.plot_quantile_returns_bar(
#             mean_quant_rateret, by_group=False, ylim_percentiles=None, ax=gf.next_row()
#         )
#
#         plotting.plot_quantile_returns_violin(
#             mean_quant_rateret_bydatetime, ylim_percentiles=(1, 99), ax=gf.next_row()
#         )
#
#         for p in factor_returns:
#             title = (
#                 "Factor Weighted "
#                 + ("Group Neutral " if group_neutral else "")
#                 + ("Long/Short " if long_short else "")
#                 + f"Portfolio Cummulative Return ({p} Period)"
#             )
#
#             plotting.plot_cummulative_returns(
#                 factor_returns[p], period=p, title=title, ax=gf.next_row()
#             )
