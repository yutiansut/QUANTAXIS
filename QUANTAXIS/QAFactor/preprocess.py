"""
因子数据处理时常用的一些函数
1. 上市时间过滤，剔除新股，默认剔除上市时间 200 天以内的股票, 暂时采用聚宽接口
2. 极值处理, 支持 MAD, STD, Quantile 方式
3. 标准化处理，暂时支持 std
4. 获取行业数据，暂时采用聚宽接口，支持 "sw_l1", "sw_l2", "sw_l3", "jq_l1", "jq_l2", "zjw"
5. 获取市值数据，使用本地接口，支持 'avg', 'mktcap', 'sqrt_mktcap', 'ln_mktcap',
    'cmktcap', 'sqrt_cmktcap', 'ln_cmktcap'
6. 行业中性化与市值中性化
"""
from functools import partial
from typing import List, Tuple, Union

try:
    import jqdatasdk
except:
    print("jqdatasdk not installed")
import numpy as np
import pandas as pd

import statsmodels.api as sm
from QUANTAXIS.QAAnalysis.QAAnalysis_block import QAAnalysis_block
from QUANTAXIS.QAFactor.utils import QA_fmt_code_list
from QUANTAXIS.QAFactor.fetcher import (QA_fetch_stock_basic, QA_fetch_industry_adv)

def QA_fmt_factor(factor: Union[pd.Series, pd.DataFrame]):
    """
    将 factor 格式化
    """
    # 索引设置
    if isinstance(factor, pd.DataFrame):
        factor = factor.stack(dropna=False)
    level_0 = 'datetime'
    try:
        pd.Timestamp(factor.index.levels[0][0])
    except:
        try:
            level_0 = 'code'
            pd.Timestamp(factor.index.levels[1][0])
        except:
            raise ValueError("错误，索引格式不正确")
    if level_0 == 'code':
        factor = factor.swaplevel()
    factor.index.names = ["datetime", "code"]
    factor.index = factor.index.map(lambda x: (pd.Timestamp(x[0]), x[1]))
    return factor.sort_index()


def QA_winsorize_factor(
        factor: Union[pd.Series,
                      pd.DataFrame],
        grouper: list = ["datetime"],
        extreme_scale: float = 1.4826,
        extreme_method: str = "mad",
        extreme_inclusive: bool = False,
        quant: list = None,
        inf2nan: bool = True,
        nan2mean: bool = True,
) -> pd.Series:
    """
    对输入的 Series 进行极值处理
    :param factor: 因子数据, ['日期' '资产'] 的 MultiIndex 或者 ['日期'] 为索引，['资产'] 为列索引的透视表
    :param grouper: 分组数据
    :param extreme_scale: 极值处理对应的 scale
    :param extreme_method: 极值处理方式
    :param extreme_inclusive: 是否保留边界外极值为边界值，默认不保留
    :param inf2nan: 是否将 np.inf -np.inf 转换为 np.nan
    :param quant: 0 ~ 1 之间的范围
    :param nan2mean: 是否将 np.nan 替换为行业平均值
    """

    def _mad_cut(x, scale, inclusive, nan2mean):
        diff = (x - x.median()).apply(abs)
        mad = diff.median()
        upper_limit = x.median() + scale * mad
        lower_limit = x.median() - scale * mad
        if inclusive:
            x.loc[x < lower_limit] = lower_limit
            x.loc[x > upper_limit] = upper_limit
            x.clip(lower_limit, upper_limit, inplace=True)
        else:
            x = x.loc[(x >= lower_limit) & (x <= upper_limit)]
        if nan2mean:
            return x.fillna(np.nanmean(x))
        return x

    def _std_cut(x, scale, inclusive, nan2mean):
        std = x.std()
        upper_limit = x.mean() + scale * std
        lower_limit = x.mean() - scale * std
        if inclusive:
            x.loc[x < lower_limit] = lower_limit
            x.loc[x > upper_limit] = upper_limit
            factor.clip(lower_limit, upper_limit, inplace=True)
        else:
            x = x.loc[(x > lower_limit) & (x < upper_limit)]
        if nan2mean:
            return x.fillna(np.nanmean(x))
        else:
            return x

    def _quant_cut(x, quant, inclusive, nan2mean):
        if inclusive:
            x.loc[x < quant[0]] = quant[0]
            x.loc[x > quant[1]] = quant[1]
            x = np.quantile(x, quant, interpolation="nearest")
        else:
            x = np.quantile(x, quant, interpolation="nearest")
        if nan2mean:
            return x.fillna(np.nanmean(x))
        else:
            return x

    if extreme_method not in ["mad", "std", "quant"]:
        raise ValueError("参数为 mad/std/quant, 仅支持这极值处理方式")
    # 对因子进行格式化
    factor = QA_fmt_factor(factor)
    # inf2nan
    if inf2nan:
        factor.replace([np.inf, -np.inf], np.nan, inplace=True)
    # 极值处理
    if extreme_method == "mad":
        factor = (
            factor.groupby(grouper).apply(
                lambda x:
                _mad_cut(x,
                         extreme_scale,
                         extreme_inclusive,
                         nan2mean)
            ).droplevel(level=1)
        )
        return factor
    elif extreme_method == "std":
        factor = (
            factor.groupby(grouper).apply(
                lambda x:
                _std_cut(x,
                         extreme_scale,
                         extreme_inclusive,
                         nan2mean)
            ).droplevel(level=1)
        )
        return factor
    elif extreme_method == "quant":
        if quant is None:
            raise ValueError("")
        factor = (
            factor.groupby(grouper)
            .apply(lambda x: _quant_cut(x,
                                        quant,
                                        extreme_inclusive,
                                        nan2mean)).droplevel(level=1)
        )
        return factor


def QA_standardize_factor(
        factor: pd.Series,
        standard_method: str = "normal",
        inf2nan: bool = True
) -> pd.Series:
    """
    对输入的因子值进行标准化处理，默认为 Z-score 处理, 其他处理方式待实现
    :param data: 输入的 DataFrame, 索引为股票代码
    :param standard_method: 标准化处理方法，目前接受 "normal"/"weighted"/"john"
    :param inf2nan: 是否将 np.inf 转换为 np.nan
    """
    factor = QA_fmt_factor(factor)
    if standard_method not in ["normal", "weighted", "john"]:
        raise ValueError("仅接受 normal/weighted/john 参数")
    if standard_method == "normal":
        std = factor.std()
        mean = factor.mean()
        factor = (factor - mean) / std
    elif standard_method == "weighted":
        # TODO: 市值加权标准化方法待实现
        raise ValueError("市值加权标准化方法待实现")
    else:
        # TODO: Johnson 变化法
        raise ValueError("John 变化法待实现")
    return factor


def QA_fetch_get_factor_groupby(
        factor: pd.Series,
        industry_cls: str = "sw_l1",
        detailed: bool = False
) -> pd.DataFrame:
    """
    获取因子的行业暴露, 注意，返回的值是 pd.DataFrame 格式，包含原因子值，附加一列
    因子对应的行业信息 (需先自行导入聚宽本地 sdk 并登陆)

    参数
    ---
    :param factor: 因子值，索引为 ['日期' '资产']
    :param industry_cls: 行业分类，默认为申万 1 级行业
    :param detailed: 是否使用详细模式，默认为 False, 即取因子日期最后一日的行业信息

    返回值
    ---
    :return: 因子数据, 包括因子值，因子对应行业
    """
    warnings.warn("请先自行导入聚宽本地 sdk 并登陆", UserWarning)
    # 因子格式化
    factor = QA_fmt_factor(factor)
    merged_data = pd.DataFrame(factor.copy().rename("factor"))
    # 股票代码格式化
    stock_list = QA_fmt_code_list(
        factor.index.get_level_values("code").drop_duplicates(),
    )
    # 非详细模式， 行业数据采用当前日期
    ss = pd.Series()
    if detailed:
        # start_time = str(min(factor.index.get_level_values("datetime")))[:10]
        # end_time = str(max(factor.index.get_level_values("datetime")))[:10]
        # date_range = list(
        #     map(pd.Timestamp, QA_util_get_trade_range(start_time, end_time))
        # )
        date_range = (
            factor.index.get_level_values(
                "datetime").drop_duplicates().tolist()
        )

        industry = pd.DataFrame()
        for cursor_date in date_range:
            df_tmp = QA_fetch_industry_adv(code = stock_list, cursor_date = cursor_date)[["code", "industry_name"]]
            df_tmp["date"] = cursor_date
            industry = industry.append(df_tmp)
        ss = industry.set_index(["date", "code"])["industry_name"]
        # industries = map(
        #     partial(jqdatasdk.get_industry,
        #             stock_list),
        #     date_range
        # )
        # industries = {
        #     d: {
        #         s: ind.get(s).get(industry_cls,
        #                           dict()).get("industry_name",
        #                                       "NA")
        #         for s in stock_list
        #     }
        #     for d,
        #     ind in zip(date_range,
        #                industries)
        # }
    else:
        end_time = str(max(factor.index.get_level_values("datetime")))[:10]
        date_range = [pd.Timestamp(end_time)]
        # industries = jqdatasdk.get_industry(stock_list, end_time)
        ss = QA_fetch_industry_adv(stock_list, end_time)[["code", "industry_name"]].set_index(["date", "code"])["industry_name"]
        # industries = {
        #     d: {
        #         s: industries.get(s).get(industry_cls,
        #                                  dict()).get("industry_name",
        #                                              "NA")
        #         for s in stock_list
        #     }
        #     for d in date_range
        # }
    # 可能历史上股票没有行业信息，用之后的行业信息往前填充
    merged_data["date"] = merged_data.index.get_level_values("datetime").map(
        lambda x: x.date()
    )
    merged_data = (
        merged_data.reset_index().set_index(
            ["date",
             "code"]
        ).assign(group=ss).reset_index().set_index(["datetime",
                                                          "code"]
                                                         ).drop("date",
                                                                axis=1)
    )
    group = merged_data["group"].unstack().bfill().stack()
    merged_data["group"] = group
    return merged_data


def QA_fetch_factor_weight(
        factor: pd.Series,
        weight_cls: str = "mktcap",
        detailed: bool = True
) -> pd.DataFrame:
    """
    获取因子的市值暴露, 注意，返回的值是 pd.DataFrame 格式，包含原因子值，附加一列
    因子对应的加权信息

    参数
    ---
    :param factor: 因子值，索引为 ['日期' '资产']
    :param weight_cls: 权重信息，默认加权方式为总市值加权
    :param detailed: 默认为 True, 如果为 False, 取因子最后一日的加权信息

    返回值
    ---
    :return: 因子数据, 包括因子值，因子对应行业
    """
    # 因子格式化
    factor = QA_fmt_factor(factor)
    merged_data = pd.DataFrame(factor.copy().rename("factor"))

    # 股票代码格式化
    code_list = factor.index.get_level_values(
        "code").drop_duplicates().tolist()
    # 非详细模式， 加权数据采用当前日期
    if detailed:
        # start_time = str(min(factor.index.get_level_values("datetime")))[:10]
        end_time = str(max(factor.index.get_level_values("datetime")))[:10]
        # date_range = list(
        #     map(pd.Timestamp, QA_util_get_trade_range(start_time, end_time))
        # )
        date_range = (
            factor.index.get_level_values(
                "datetime").drop_duplicates().tolist()
        )

    else:
        date_range = [pd.Timestamp(end_time)]

    if weight_cls == "avg":
        merged_data["weight"] = 1.0
        return merged_data

    df_local = QAAnalysis_block(
        code=code_list,
        start=date_range[0],
        end=date_range[-1]
    ).market_value
    if weight_cls == "mktcap":
        df_local = df_local.reset_index().pivot(
            index="date",
            columns="code",
            values="mv"
        )
    elif weight_cls == "sqrt_mktcap":
        df_local = (
            df_local.reset_index().pivot(
                index="date",
                columns="code",
                values="mv"
            ).transform("sqrt")
        )
    elif weight_cls == "ln_mktcap":
        df_local = (
            df_local.reset_index().pivot(
                index="date",
                columns="code",
                values="mv"
            ).transform("ln")
        )
    elif weight_cls == "cmktcap":
        df_local = df_local.reset_index().pivot(
            index="date",
            columns="code",
            values="liquidity_mv"
        )
    elif weight_cls == "sqrt_cmktcap":
        df_local = (
            df_local.reset_index().pivot(
                index="date",
                columns="code",
                values="liquidity_mv"
            ).transform("sqrt")
        )
    elif weight_cls == "ln_cmktcap":
        df_local = (
            df_local.reset_index().pivot(
                index="date",
                columns="code",
                values="liquidity_mv"
            ).transform("ln")
        )
    else:
        raise ValueError(f"{weight_cls} 加权方式未实现")
    merged_data["date"] = merged_data.index.get_level_values("datetime").map(
        lambda x: x.date()
    )
    merged_data = (
        merged_data.reset_index().set_index(
            ["date",
             "code"]
        ).assign(weight=df_local.stack()
                 ).reset_index().set_index(["datetime",
                                            "code"]).drop("date",
                                                          axis=1)
    )

    weight = merged_data["weight"].unstack().bfill().stack()
    merged_data["weight"] = weight
    return merged_data


def QA_fetch_get_factor_start_date(factor: pd.Series) -> pd.DataFrame:
    """
    获取因子池上市时间, 注意，请自行登陆聚宽本地 sdk

    参数
    ---
    :param factor: 因子值，索引为 ['日期' '资产']

    返回值
    ---
    :return: 因子数据
    """
    # 因子格式化
    factor = QA_fmt_factor(factor.copy())
    merged_data = pd.DataFrame(factor.rename("factor"))
    # 股票代码格式化
    stock_list = QA_fmt_code_list(
        factor.index.get_level_values("code").drop_duplicates(),
        style="jq"
    )
    # 上市时间获取
    df_local = jqdatasdk.get_all_securities(types="stock")
    intersection = df_local.index.intersection(stock_list)
    ss = df_local.loc[intersection]["start_date"]
    ss.index = ss.index.map(lambda x: x[:6])
    # 拼接上市时间
    merged_data = merged_data.loc[(slice(None), list(ss.index)), :]
    merged_data["start_date"] = merged_data.index.map(lambda x: ss.loc[x[1]]
                                                      ).tolist()
    return merged_data

def QA_fetch_factor_start_date(factor: pd.Series) -> pd.DataFrame:
    """
    获取因子池上市时间，本地获取接口，使用前先保存股票基本信息
    """
    factor = QA_fmt_factor(factor.copy())
    merged_data = pd.DataFrame(factor.rename("factor"))
    # 股票代码格式化
    stock_list = QA_fmt_code_list(
        factor.index.get_level_values("code").drop_duplicates()
    )
    # 上市时间获取
    df_local = QA_fetch_stock_basic(status=None).set_index("code")
    intersection = df_local.index.intersection(stock_list)
    ss = df_local.loc[intersection]["list_date"]
    # 拼接上市时间
    merged_data = merged_data.loc[(slice(None), list(ss.index)), :]
    merged_data["start_date"] = merged_data.index.map(lambda x: ss.loc[x[1]]
                                                      ).tolist()
    return merged_data


def QA_neutralize_factor(
        factor: pd.Series,
        weight_cls: str = "avg",
        industry: str = "sw_l1"
) -> pd.DataFrame:
    """
    行业中性处理

    参数
    ---
    :param factor: 因子值
    :param weight_cls: 加权方式
    :param industry_cls: 行业分类方式

    返回值
    ---
    :return: 中性化处理后的因子数据
    """
    if type(mkt_cap) == pd.Series:
        LnMktCap = mkt_cap.apply(lambda x: math.log(x))
        if industry:  # 行业、市值
            dummy_industry = get_industry_exposure(factor, date=date)
            x = pd.concat([LnMktCap, dummy_industry.T], axis=1)
        else:        # 仅市值
            x = LnMktCap
    elif industry:
        dummy_industry = get_industry_exposure(factor, date=date)
        x = dummy_industry.T
    return (sm.OLS(factor[factor], x.astype(float)).fit().resid.rename(factor),)
