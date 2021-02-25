import re
from typing import List, Tuple, Union

import numpy as np
import pandas as pd

from QUANTAXIS.QAFactor import utils
from QUANTAXIS.QAFactor import preprocess
from QUANTAXIS.QAFactor.utils import get_forward_returns_columns


def get_clean_factor_and_forward_returns(
        factor: Union[pd.Series, pd.DataFrame],
        prices: Union[pd.Series, pd.DataFrame],
        groupby: Union[dict, pd.Series, pd.DataFrame],
        stock_start_date: Union[dict, pd.Series, pd.DataFrame],
        weights: Union[dict, pd.Series, pd.DataFrame],
        binning_by_group: bool = False,
        quantiles: Union[int, Tuple[float], List[float]] = 5,
        bins: Union[int, Tuple[float], List[float]] = None,
        periods: Union[int, Tuple[int], List[int]] = (1, 5, 15),
        max_loss: float = 0.25,
        zero_aware: bool = False,
        frequence: str = "1D",
) -> pd.DataFrame:
    """
    根据输入的因子数据，价格数据，分组数据，加权数据，分位数据等，进行因子数据合成
    1. 输入的因子数据如果为:
    - pd.Series, 则索引应该为 ['日期' '资产'] 的 MultiIndex, 数据为因子的值
    - pd.DataFrame, 则索引应该为 ['日期'], 列索引为 ['资产'] 的因子数据透视表
    2. 输入的价格数据如果为:
    - pd.Series, 则索引应该为 ['日期', '资产'] 的 MultiIndex, 数据为价格数据
    - pd.DataFrame, 则索引应该为 ['日期'], 列索引为 ['资产'] 的价格透视表
    3. 输入的分组信息如果为:
    - dict, key 应该对应 '资产', value 对应 '行业名称' 或 '行业代码',
        默认在所有日期采用同一套数据
    - pd.Series, 索引为 ['日期', '资产'] 的 MultiIndex, 数据为行业信息
    - pd.DataFrame, 索引为 ['日期'], 列索引为 ['资产'] 的行业信息透视表
    4. 输入的权重信息如果为：
    - dict, key 应该对应 '资产', value 对应加权数据,
        默认在所有日期采用同一套数据
    - pd.Series, 索引为 ['日期', '资产'] 的 MultiIndex, 数据为加权数据
    - pd.DataFrame, 索引为 ['日期'], 列索引为 ['资产'] 的加权数据透视表

    参数
    ---
    :param factor: 因子数据，仅包含因子自身值
    :param prices: 价格数据，应只含有一种类型价格数据，譬如 'close' 或者 'open'
    :param groupby: 分组数据, 一般为行业分组
    :param stock_start_date: 上市时间
    :param weights: 加权数据，一般为市值加权
    :param binning_by_group: 是否按照分组进行分位处理
    :param quantiles: 分位数据，如果是 int 类型，将因子数据按照每个分组等间隔分位，
        否则按照 quantiles 提供的分位数据进行分位, 对应 pd.qcut
    :param bins: 分位数据，如果是 int 类型，将因子数据按照每个分组等间隔分位，
        否则按照 bins 提供的分位数据进行分位，对应 pd.cut
    :param periods: 远期收益对应的期数
    :param max_loss: 因子计算，如果丢弃的因子数据超过该值，抛出异常
    :param zero_aware: 如果因子有正负，是否按照正负区间分别进行分位处理

    返回值
    ---
    :return: 因子数据，包括因子值，因子远期收益，分位区间，分组，权重
    """
    # 1. 统一格式
    factor = preprocess.QA_fmt_factor(factor)
    factor = factor.unstack(level="code")

    if isinstance(prices, pd.Series):
        prices = prices.unstack(level="code")

    if isinstance(periods, int):
        periods = (periods, )

    # 2. 获取因子远期收益
    forward_returns = get_forward_returns(factor, prices, periods, frequence)

    # 3. 格式化因子数据
    factor_data = get_clean_factor(
        factor=factor,
        forward_returns=forward_returns,
        groupby=groupby,
        stock_start_date=stock_start_date,
        weights=weights,
        quantiles=quantiles,
        bins=bins,
        binning_by_group=binning_by_group,
        max_loss=max_loss,
        zero_aware=zero_aware,
    )

    return factor_data


def get_forward_returns(
        factor: pd.DataFrame,
        prices: pd.DataFrame,
        periods: Union[int, Tuple[int], List[int]] = (1, 5, 10),
        frequence: str = "1D",
) -> pd.DataFrame:
    """
    获取因子远期收益

    参数
    ---
    :param factor: 因子值
    :param prices: 价格数据
    :param periods: 收益周期
    :param frequence: 时间频率

    返回
    ---
    :return: 因子远期收益
    """
    factor_timelist = pd.to_datetime(factor.index, utc=False).tolist()
    factor_timelist = sorted(
        list(
            set(factor_timelist) & set(pd.to_datetime(prices.index, utc=False).tolist())))

    if len(factor_timelist) == 0:
        raise ValueError("错误：因子数据的日期索引与价格数据日期索引不匹配")

    # 检查因子与价格数据的资产索引
    factor_codelist = factor.columns.tolist()
    factor_codelist = sorted(
        list(set(factor_codelist) & set(prices.columns.tolist())))

    if len(factor_codelist) == 0:
        raise ValueError("错误：因子数据的股票索引与价格数据股票索引不匹配")

    forward_returns = pd.DataFrame(index=pd.MultiIndex.from_product(
        [factor_timelist, factor_codelist], names=["datetime", "code"]))

    # 周期处理
    if isinstance(periods, int):
        periods = (periods, )

    # 收益率计算
    for period in periods:
        # 假设因子数据是 3/31 的值，收益率计算应该是 9/30 与 6/30 价差
        delta = (prices.shift(-period - 1) / prices.shift(-1) -
                 1.0).reindex(factor_timelist)
        # delta = prices.pct_change(
        #     period).shift(-period).reindex(factor_timelist)
        pattern = re.compile(r"\d+")
        interval = pattern.findall(frequence)[0]
        period = period * int(interval)
        forward_returns[
            f"period_{period}{frequence.replace(interval, '')}"] = delta.stack(
                level=-1)

    return forward_returns


def get_clean_factor(
        factor: pd.DataFrame,
        forward_returns: pd.DataFrame,
        groupby: Union[dict, pd.Series, pd.DataFrame],
        stock_start_date: Union[dict, pd.Series, pd.DataFrame],
        weights: Union[dict, pd.Series, pd.DataFrame],
        binning_by_group: bool = False,
        quantiles: Union[int, Tuple[float], List[float]] = 5,
        bins: Union[int, Tuple[float], List[float]] = None,
        max_loss: float = 0.25,
        zero_aware: bool = False,
) -> pd.DataFrame:
    """
    将因子值与因子远期收益按照分组信息，加权信息，分位信息进行处理

    参数
    ---
    :param factor: 因子数据
    :param forward_returns: 因子远期收益
    :param groupby: 分组数据
    :param stock_start_date: 上市时间
    :param weights: 加权数据
    :param binning_by_group: 是否按分组进行分位
    :param quantiles: 分位数据，默认平局分为 5 个分位区间
    :param bins: 分位数据
    :param max_loss: 因子数据最大损失
    :param zero_aware: 是否按因子数据的正负区间分别进行分位

    返回值
    ---
    :return merged_data: 索引为 ['日期' '资产'] 的 MultiIndex, 列索引包括
        因子值，因子远期收益，因子分位数，因子分组 (可选), 因子权重 (可选)
    """
    factor_copy = factor.stack(level=-1)
    factor_copy.index = factor_copy.index.rename(["datetime", "code"])

    initial_amount = float(len(factor_copy.index))

    merged_data = forward_returns.copy()
    merged_data["factor"] = factor_copy

    if groupby is not None:
        if isinstance(groupby, dict):
            diff = set(factor_copy.index.get_level_values("code")) - set(
                groupby.keys())
            if len(diff) > 0:
                raise KeyError(f"股票 {list(diff)} 不在分组映射中")

            ss = pd.Series(groupby)
            groupby = pd.Series(
                index=factor_copy.index,
                data=ss[factor_copy.index.get_level_values("code")].values,
            )
        elif isinstance(groupby, pd.DataFrame):
            # 假设传入的如果是 dataframe, 格式为透视表, 列为股票代码，索引为日期
            groupby = groupby.stack(level=-1)
        groupby_tmp = groupby.reindex(merged_data.index).unstack().bfill().stack().dropna()
        if groupby_tmp.empty:
            groupby_tmp = pd.Series(index=merged_data.index.append(groupby.index), data=groupby).unstack().ffill().bfill().stack().reindex(merged_data.index)
        groupby = groupby_tmp.reindex(merged_data.index).unstack().bfill().stack()
        merged_data["group"] = groupby

    if stock_start_date is not None:
        if isinstance(stock_start_date, dict):
            diff = set(factor_copy.index.get_level_values("code")) - set(
                stock_start_date.keys())
            if len(diff) > 0:
                raise KeyError(f"股票 {list(diff)} 不在分组映射中")

            ss = pd.Series(stock_start_date)
            stock_start_date = pd.Series(
                index=factor_copy.index,
                data=ss[factor_copy.index.get_level_values("code")].values,
            )
        elif isinstance(stock_start_date, pd.DataFrame):
            # 假设传入的如果是 dataframe, 格式为透视表, 列为股票代码，索引为日期
            stock_start_date = stock_start_date.stack(level=-1)
        stock_start_date_tmp = stock_start_date.reindex(merged_data.index).unstack().bfill().stack().dropna()
        if stock_start_date_tmp.empty:
            stock_start_date_tmp = pd.Series(index=merged_data.index.append(stock_start_date.index),
                                    data=groupby).unstack().ffill().bfill().stack().reindex(merged_data.index)
        stock_start_date = stock_start_date_tmp.reindex(merged_data.index).unstack().bfill().stack()
        merged_data["start_date"] = stock_start_date

    if weights is not None:
        if isinstance(weights, dict):
            diff = set(factor_copy.index.get_level_values("code")) - set(
                weights.keys())
            if len(diff) > 0:
                raise KeyError("股票 {} 不在加权映射中".format(list(diff)))
            ww = pd.Series(weights)
            weights = pd.Series(
                index=factor_copy.index,
                data=ww[factor_copy.index.get_level_values("code")].values,
            )
        elif isinstance(weights, pd.DataFrame):
            weights = weights.stack(level=-1)
        weights_tmp = weights.reindex(merged_data.index).unstack().bfill().stack().dropna()
        if weights_tmp.empty:
            weights_tmp = pd.Series(index=merged_data.index.append(weights.index),
                                    data=weights).unstack().ffill().bfill().stack().reindex(merged_data.index)
        weights = weights_tmp.reindex(merged_data.index).unstack().bfill().stack()
        merged_data["weights"] = weights

    merged_data = merged_data.dropna()

    quantile_data = quantize_data(
        factor_data=merged_data,
        quantiles=quantiles,
        bins=bins,
        binning_by_group=binning_by_group,
        zero_aware=zero_aware,
        no_raise=True,
    )

    merged_data["factor_quantile"] = quantile_data
    merged_data = merged_data.dropna()
    merged_data["factor_quantile"] = merged_data["factor_quantile"].astype(int)

    if "weights" in merged_data.columns:
        # 按日期，分位进行权重归一，然后将分位索引删除
        merged_data["weights"] = (merged_data.set_index(
            "factor_quantile", append=True).groupby(
                level=["datetime", "factor_quantile"])["weights"].apply(
                    lambda s: s.divide(s.sum())).reset_index("factor_quantile",
                                                             drop=True))

    binning_amount = float(len(merged_data.index))
    tot_loss = (initial_amount - binning_amount) / initial_amount

    no_raise = True if max_loss == 0 else False
    if tot_loss > max_loss and not no_raise:
        raise ValueError(f"错误：因子损失率 {tot_loss} 超过最大允许损失 {max_loss}")

    return merged_data


def quantize_data(
        factor_data: pd.DataFrame,
        quantiles: Union[int, Tuple[float], List[float]] = 5,
        bins: Union[int, Tuple[float], List[float]] = None,
        binning_by_group: bool = False,
        zero_aware: bool = False,
        no_raise: bool = False,
) -> pd.Series:
    """
    对输入的因子数据进行分位处理
    注意： quantiles 与 bins 只能有一个非空

    参数
    ---
    :param factor_data: 因子数据，包括因子值，远期收益 [可选]，分组信息 [可选], 加权信息 [可选]
    :param quantiles: 分位数据
    :param bins: 分位数据
    :param binning_by_group: 是否按分组分别进行分位处理
    :param zero_aware: 是否对因子正负值分别进行分位处理

    返回值
    ---
    :return :
    """
    if not ((quantiles is not None and bins is None) or
            (quantiles is None and bins is not None)):
        raise ValueError("quantiles 与 bins 至少且只能输入一个")

    if zero_aware and not (isinstance(quantiles, int)
                           or isinstance(bins, int)):
        raise ValueError("当 zero_aware 为 True 时，quantiles 或者 bins 必须为 Int 类型")

    def quantile_calc(x, _quantiles, _bins, _zero_aware, _no_raise):
        try:
            if _quantiles is not None and _bins is None and not _zero_aware:
                return pd.qcut(x, _quantiles, labels=False) + 1
            if _quantiles is not None and _bins is None and _zero_aware:
                neg_quantiles = pd.qcut(
                    x[x < 0], _quantiles // 2, labels=False) + 1
                pos_quantiles = (
                    pd.qcut(x[x >= 0], _quantiles // 2, labels=False) +
                    _quantiles // 2 + 1)
                return pd.concat([neg_quantiles, pos_quantiles]).sort_index()
            if _bins is not None and _quantiles is None and not _zero_aware:
                return pd.cut(x, _bins, labels=False) + 1
            if _bins is not None and _quantiles is None and _zero_aware:
                pos_bins = pd.cut(x[x >= 0], _bins // 2,
                                  labels=False) + _bins // 2 + 1
                neg_bins = pd.cut(x[x < 0], _bins // 2, labels=False) + 1
                return pd.concat([neg_bins, pos_bins]).sort_index()
        except Exception as e:
            if _no_raise:
                return pd.Series(index=x.index)
            raise e

    grouper = ["datetime"]
    if binning_by_group:
        if "group" not in factor_data.columns:
            raise ValueError("只有存在分组信息时才能进行分组进行分位处理")
        grouper.append("group")

    factor_quantile = factor_data.groupby(grouper)["factor"].apply(
        quantile_calc, quantiles, bins, zero_aware, no_raise)

    return factor_quantile


def demean_forward_returns(factor_data: pd.DataFrame,
                           grouper: list = None) -> pd.DataFrame:
    """
    按照分组对因子远期收益进行去均值

    参数
    ---
    :param factor_data: 因子远期收益, 索引为 ['日期' '股票'] 的 MultiIndex,
        columns 为因子远期收益
    :param grouper: 分组信息，如果为 None, 则默认按日期进行去均值

    返回值
    ---
    :return adjust_forward_returns: 去均值后的因子远期收益
    """
    factor_data = factor_data.copy()

    if not grouper:
        grouper = ["datetime"]

    cols = get_forward_returns_columns(factor_data.columns)
    factor_data[cols] = factor_data.groupby(
        grouper, as_index=False)[cols.append(pd.Index(
            ["weights"]))].apply(lambda x: x[cols].subtract(np.average(
                x[cols], axis=0, weights=x["weights"].fillna(0.0).values),
                                                            axis=1))

    return factor_data
