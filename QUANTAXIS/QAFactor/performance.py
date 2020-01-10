"""
分析模块
"""

import warnings
from typing import Tuple, Union
import re

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.api import OLS, add_constant
from QUANTAXIS.QAFactor import utils
from QUANTAXIS.QAFactor.parameters import DAYS_PER_MONTH, DAYS_PER_QUARTER, DAYS_PER_YEAR
from QUANTAXIS.QAFactor.process import demean_forward_returns
from QUANTAXIS.QAFactor.utils import get_forward_returns_columns


def mean_return_by_quantile(
        factor_data: pd.DataFrame,
        by_datetime: bool = False,
        by_group: bool = False,
        demeaned: bool = True,
        group_adjust: bool = False,
) -> Tuple:
    """
    按分位计算因子远期收益和标准差

    参数
    ---
    :param factor_data: 索引为 ['日期' '资产'] 的 MultiIndex, values 包括因子的值，各期因子远期收益，因子分位数, 因子分组 [可选], 因子权重 [可选]
    :param by_datetime: 按日期计算各分位数的因子远期收益均值
    :param by_group: 按分组计算各分位数的因子远期收益均值
    :param demeaned: 按日期计算超额收益
    :param group_adjust: 按日期和分组计算超额收益

    返回
    ---
    :return mean_ret: 各分位数因子远期收益均值
    :return std_error_ret: 各分位数因子远期收益标准差
    """

    if group_adjust:
        grouper = ["datetime", "group"]
        factor_data = demean_forward_returns(factor_data, grouper)
    elif demeaned:
        factor_data = demean_forward_returns(factor_data)
    else:
        factor_data = factor_data.copy()

    grouper = ["factor_quantile"]
    if by_datetime:
        grouper.append("datetime")

    if by_group:
        grouper.append("group")

    mean_ret, std_error_ret = weighted_mean_return(factor_data, grouper=grouper)

    return mean_ret, std_error_ret


def weighted_mean_return(factor_data: pd.DataFrame, grouper: list):
    """
    计算加权平均收益/标准差
    """
    forward_returns_columns = get_forward_returns_columns(factor_data.columns)

    def agg(values, weights):
        count = len(values)
        average = np.average(values, weights=weights, axis=0)
        variance = (
            np.average((values - average)**2,
                       weights=weights,
                       axis=0) * count / max((count - 1),
                                             1)
        )

        return pd.Series(
            [average,
             np.sqrt(variance),
             count],
            index=["mean",
                   "std",
                   "count"]
        )

    group_stats = factor_data.groupby(grouper)[forward_returns_columns.append(
        pd.Index(["weights"])
    )].apply(
        lambda x: x[forward_returns_columns].
        apply(agg,
              weights=x["weights"].fillna(0.0).values)
    )

    mean_ret = group_stats.xs("mean", level=-1)
    std_error_ret = group_stats.xs(
        "std",
        level=-1
    ) / np.sqrt(group_stats.xs("count",
                               level=-1))

    return mean_ret, std_error_ret


def mean_returns_spread(
        mean_returns: pd.DataFrame,
        upper_quant: int,
        lower_quant: int,
        std_err=None
):
    """
    计算 upper_quant 与 lower_quant 之间的收益差，与联合收益标准差

    参数
    ---
    :param mean_returns: 平均回报
    :param upper_quant: 上分位
    :param lower_quant: 下分位
    :param std_err: 收益标准差
    """
    mean_return_difference = mean_returns.xs(upper_quant
                                            ) - mean_returns.xs(lower_quant)

    if std_err is None:
        joint_std_err = None
    else:
        std1 = std_err.xs(upper_quant)
        std2 = std_err.xs(lower_quant)
        joint_std_err = np.sqrt(std1**2 + std2**2)

    return mean_return_difference, joint_std_err


def factor_alpha_beta(
        factor_data: pd.DataFrame,
        returns: pd.DataFrame = None,
        demeaned: bool = True,
        group_adjust: bool = False,
        equal_weight: bool = False,
):
    """
    计算因子的 alpha (超额收益), alpha 的 t-统计量 以及 beta 值

    参数
    ---
    :param factor_data: 索引为 ['日期' '股票'] 的 MultiIndex, values 包括因子值，远期收益，因子分位，因子分组 [可选]
    :param returns: 因子远期收益，默认为 None, 如果为 None 的时候，会通过调用 `factor_returns` 来计算相应的收益
    :param demeaned: 是否基于一个多空组合
    :param group_adjust: 是否进行行业中性处理
    :param equal_weight:

    返回
    ---
    """
    if returns is None:
        returns = factor_returns(
            factor_data,
            demeaned,
            group_adjust,
            equal_weight
        )

    universe_ret = (
        factor_data.groupby(level="datetime")[get_forward_returns_columns(
            factor_data.columns
        )].mean().loc[returns.index]
    )

    if isinstance(returns, pd.Series):
        returns.name = universe_ret.columns.values[0]
        returns = pd.DataFrame(returns)

    alpha_beta = pd.DataFrame()
    for period in returns.columns.values:
        x = universe_ret[period].values
        y = returns[period].values
        x = add_constant(x)

        reg_fit = OLS(y, x).fit()
        try:
            alpha, beta = reg_fit.params
        except ValueError:
            alpha_beta.loc["Ann. alpha", period] = np.nan
            alpha_beta.loc["beta", period] = np.nan
        else:
            freq_adjust = pd.Timedelta(days=DAYS_PER_YEAR) / pd.Timedelta(
                utils.get_period(period.replace("period_",
                                                ""))
            )
            alpha_beta.loc["Ann. alpha",
                           period] = (1 + alpha)**freq_adjust - 1.0
            alpha_beta.loc["beta", period] = beta
    return alpha_beta


def factor_returns(
        factor_data: pd.DataFrame,
        demeaned: bool = True,
        group_adjust: bool = False,
        equal_weight: bool = False,
        by_asset: bool = False,
):
    """
    计算按因子值加权的投资组合收益

    参数
    ---
    :param factor_data: 因子数据
    :param demeaned: 是否构建多空组合
    :param group_adjust: 是否按分组进行多空组合
    :param equal_weight: 针对因子中位数分别构建多空组合
    :param by_asset: 按股票展示组合收益, 默认为 False

    返回值
    ---
    """
    weights = factor_weights(factor_data, demeaned, group_adjust, equal_weight)

    weighted_returns = factor_data[get_forward_returns_columns(
        factor_data.columns
    )].multiply(
        weights,
        axis=0
    )

    if by_asset:
        returns = weighted_returns
    else:
        returns = weighted_returns.groupby(level="datetime").sum()

    return returns


def factor_weights(
        factor_data: pd.DataFrame,
        demeaned: bool = True,
        group_adjust: bool = False,
        equal_weight: bool = False,
):

    def to_weights(group, _demeaned, _equal_weight):

        if _equal_weight:
            group = group.copy()

            if _demeaned:
                # top assets positive weights, bottom ones negative
                group = group - group.median()

            negative_mask = group < 0
            group[negative_mask] = -1.0
            positive_mask = group > 0
            group[positive_mask] = 1.0

            if _demeaned:
                # positive weights must equal negative weights
                if negative_mask.any():
                    if negative_mask.sum() == 0:
                        group[negative_mask] = 0
                    group[negative_mask] /= negative_mask.sum()
                if positive_mask.any():
                    if positive_mask.sum() == 0:
                        group[positive_mask] = 0
                    group[positive_mask] /= positive_mask.sum()

        elif _demeaned:
            group = group - group.mean()
        if group.abs().sum() == 0: # 二分类可能和为 0
            return group * 0.0
        return group / group.abs().sum()

    grouper = ["datetime"]
    if group_adjust:
        grouper.append("group")

    weights = factor_data.groupby(grouper)["factor"].apply(
        to_weights,
        demeaned,
        equal_weight
    )

    if group_adjust:
        weights = weights.groupby(level="datetime"
                                 ).apply(to_weights,
                                         False,
                                         False)

    return weights


def factor_information_coefficient(
        factor_data: pd.DataFrame,
        group_adjust: bool = False,
        by_group: bool = False
):
    """
    Computes the Spearman Rank Correlation based Information Coefficient (IC)
    between factor values and N period forward returns for each period in
    the factor index.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    group_adjust : bool
        Demean forward returns by group before computing IC.
    by_group : bool
        If True, compute period wise IC separately for each group.

    Returns
    -------
    ic : pd.DataFrame
        Spearman Rank correlation between factor and
        provided forward returns.
    """

    def src_ic(group):
        f = group["factor"]
        _ic = group[get_forward_returns_columns(
            factor_data.columns
        )].apply(lambda x: stats.spearmanr(x,
                                           f)[0])
        return _ic

    factor_data = factor_data.copy()

    grouper = ["datetime"]

    if group_adjust:
        factor_data = demean_forward_returns(factor_data, grouper + ["group"])
    if by_group:
        grouper.append("group")

    ic = factor_data.groupby(grouper).apply(src_ic)

    return ic


def quantile_turnover(
        quantile_factor: pd.DataFrame,
        quantile: int,
        period: Union[int,
                      str] = 1
):
    """
    Computes the proportion of names in a factor quantile that were
    not in that quantile in the previous period.

    Parameters
    ----------
    quantile_factor : pd.Series
        DataFrame with date, asset and factor quantile.
    quantile : int
        Quantile on which to perform turnover analysis.
    period: string or int, optional
        Period over which to calculate the turnover. If it is a string it must
        follow pandas.Timedelta constructor format (e.g. '1 days', '1D', '30m',
        '3h', '1D1h', etc).
    Returns
    -------
    quant_turnover : pd.Series
        Period by period turnover for that quantile.
    """
    quant_names = quantile_factor[quantile_factor == quantile]
    quant_name_sets = quant_names.groupby(
        level=["datetime"]
    ).apply(lambda x: set(x.index.get_level_values("code")))

    if isinstance(period, int):
        name_shifted = quant_name_sets.shift(period)
    else:
        period = utils.get_period(period)
        shifted_idx = utils.add_custom_calendar_timedelta(
            quant_name_sets.index,
            -pd.Timedelta(period)
        )
        name_shifted = quant_name_sets.reindex(shifted_idx)
        name_shifted.index = quant_name_sets.index

    new_names = (quant_name_sets - name_shifted).dropna()
    quant_turnover = new_names.apply(lambda x: len(x)
                                    ) / quant_name_sets.apply(lambda x: len(x))
    quant_turnover.name = quantile
    return quant_turnover


def factor_rank_autocorrelation(
        factor_data: pd.DataFrame,
        period: Union[int,
                      str] = 1
):
    grouper = ["datetime"]

    ranks = factor_data.groupby(grouper)["factor"].rank()

    asset_factor_rank = ranks.reset_index().pivot(
        index="datetime",
        columns="code",
        values="factor"
    )

    if isinstance(period, int):
        asset_shifted = asset_factor_rank.shift(period)
    else:
        shifted_idx = utils.add_custom_calendar_timedelta(
            asset_factor_rank.index,
            -pd.Timedelta(period),
        )
        asset_shifted = asset_factor_rank.reindex(shifted_idx)
        asset_shifted.index = asset_factor_rank.index

    autocorr = asset_factor_rank.corrwith(asset_shifted, axis=1)
    autocorr.name = period
    return autocorr


def cumulative_returns(returns: pd.DataFrame, period, freq=None):
    if not isinstance(period, pd.Timedelta):
        period = pd.Timedelta(period)

    if freq is None:
        freq = returns.index.freq

    if freq is None:
        freq = pd.tseries.offsets.BDay()
        warnings.warn(
            "'freq' not set, using business day calendar",
            UserWarning
        )

    trades_idx = returns.index.copy()
    returns_idx = utils.add_custom_calendar_timedelta(trades_idx, period)
    full_idx = trades_idx.union(returns_idx)

    sub_returns = []
    while len(trades_idx) > 0:
        sub_idx = []
        next = trades_idx.min()
        while next <= trades_idx.max():
            sub_idx.append(next)
            next = utils.add_custom_calendar_timedelta(
                input=next,
                timedelta=period,
            )
            try:
                i = trades_idx.get_loc(next, method="bfill")
                next = trades_idx[i]
            except KeyError:
                break

        sub_idx = pd.DatetimeIndex(sub_idx, tz=full_idx.tz)
        subret = returns[sub_idx]

        subret = subret.reindex(full_idx)

        for pret_idx in reversed(sub_idx):
            pret = subret[pret_idx]
            pret_end_idx = utils.add_custom_calendar_timedelta(pret_idx, period)
            slice = subret[(subret.index > pret_idx)
                           & (subret.index <= pret_end_idx)].index

            if pd.isnull(pret):
                continue

            def rate_of_returns(ret, period):
                return ((np.nansum(ret) + 1)**(1.0 / period)) - 1

            for slice_idx in slice:
                sub_period = utils.diff_custom_calendar_timedeltas(
                    pret_idx,
                    slice_idx,
                    freq
                )
