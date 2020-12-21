"""
数据模块，可拓展，目前支持 QUANTAIXS 的数据源输入
FIXME: 给 QUANTAXIS 添加申万行业分级数据接口
FIXME: 聚宽的行业数据，准备移除
FIXME: 聚宽的上式公司上式时间，准备移除
"""

import datetime
import re
import warnings
from functools import partial
from typing import List, Tuple, Union
# try:
#     import jqdatasdk
# except ImportError:
#     print('QAFactor模块需要 jqdatasdk的支持 请使用pip install jqdatasdk 来安装')
import pandas as pd
from QUANTAXIS.QAFactor.fetcher import (QA_fetch_stock_basic, QA_fetch_industry_adv)


from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_index_day_adv, QA_fetch_stock_day_adv
from QUANTAXIS.QAAnalysis.QAAnalysis_block import QAAnalysis_block

from QUANTAXIS.QAFactor import utils
from QUANTAXIS.QAFactor.parameters import (
    FQ_TYPE,
    FREQUENCE_TYPE,
    INDUSTRY_CLS,
    PRICE_TYPE,
    WEIGHT_CLS
)


class DataApi:
    """
    数据类，提供数据接口，可独立使用
    """
    def __init__(
            self,
            jq_username: str = None,
            jq_password: str = None,
            price_type: str = "close",  # 价格类型
            fq: str = "qfq",  # 复权方式
            factor_time_range: list = None,
            industry_cls: str = "sw_l1",  # 行业分类
            industry_data: Union[dict, pd.Series, pd.DataFrame] = None,  # 行业信息
            weight_cls: str = "avg",  # 权重分类
            weight_data: Union[dict, pd.Series, pd.DataFrame] = None,  # 权重信息
            frequence: str = "DAY",  # 频率
            detailed: bool = False,  # 是否按日期进行行业查询
    ):
        """
        根据输入的参数进行初始化

        说明
        ---
        如果需要使用自定义的行业，权重信息，需要设置 industry_cls, weight_cls 为 None, 然后再输入 industry_data, weight_data

        参数
        ---
        :param jq_username: 聚宽账号
        :param jq_password: 聚宽密码
        :param price_type: 计算因子收益时，使用价格数据类型，支持 ['open', 'high', 'low', 'close', 'avg'], 默认为 'close'
        :param fq: 价格数据的复权方式
        :param factor_time_range: 因子对应的时间范围
        :param industry_cls: 行业类型，目前支持
            - "sw_l1": 申万一级
            - "sw_l2": 申万二级
            - "sw_l3": 申万三级
            - "jq_l1": 聚宽一级
            - "jq_l2": 聚宽二级
            - "zjw": 证监会
        :param indsutry_data: 行业数据 [可选], 为 industry_cls 只能有一个为非 None
        :param weight_cls: 权重类型，目前支持
            - "avg": 等权重
            - "mktcap": 总市值加权
            - "cmktcap": 流通市值加权
            - "ln_mktcap": 对数市值加权
            - "ln_cmktcap": 对数流通市值加权
            - "sqrt_mktcap": 市值平方根加权
            - "sqrt_cmktcap": 流通市值平方根加权
        :param weight_data: 权重数据 [可选], 与 weight_cls 两种只能有一个为非 None
        :param frequence: 频率
        :param detailed: 是否使用详细的按日期分类行业信息，默认使用 end_date 的行业数据
        """
        # jqdatasdk.auth(jq_username, jq_password)

        if price_type is None:
            price_type = "close"
            warnings.warn("没有指定使用的价格类型，采用收盘价进行计算", UserWarning)
        assert price_type.lower() in PRICE_TYPE
        self.price_type = price_type

        if fq is not None:
            assert fq.lower() in FQ_TYPE
        else:
            warnings.warn("使用不复权的价格数据进行计算，结果可能受到分红配股等影响而不准确")
        self.fq = fq

        self.start_time = min(factor_time_range)
        self.end_time = max(factor_time_range)

        if industry_cls is not None:
            assert industry_cls.lower() in INDUSTRY_CLS
            # 如果输入了指定行业分类方式，则忽略行业数据数据
            self.industry_cls = industry_cls
            self.industry_data = None
        else:
            self.industry_cls = industry_cls
            self.industry_data = industry_data
        if (self.industry_cls is None) and (self.industry_data is None):
            warnings.warn("没有指定行业分类方式，也没有输入行业数据", UserWarning)

        if weight_cls is not None:
            assert weight_cls.lower() in WEIGHT_CLS
            self.weight_cls = weight_cls
            self.weight_data = None
        else:
            self.weight_cls = weight_cls
            self.weight_data = weight_data
        if (self.weight_cls is None) and (self.weight_data is None):
            warnings.warn("没有指定加权方式，也没有输入加权数据，默认采用等权重方式", UserWarning)
            self.weight_cls = "avg"
            self.weight_data = None

        self.frequence = utils.get_frequence(frequence)
        self.detailed = detailed

    def get_prices(
            self,
            code_list: Union[str,
                             Tuple[str],
                             List[str]] = None,
            start_time: Union[str,
                              datetime.datetime] = None,
            end_time: Union[str,
                            datetime.datetime] = None,
            fq: str = None,
            frequence: str = None,
            price_type: str = None,
    ):
        """
        价格数据获取接口，单因子输入后，可以通过单因子获取股票代码，时间等参数信息

        参数
        ---
        :param code_list: 股票代码
        :param start_time: 起始时间
        :param end_time: 截止时间
        :param fq: 复权方式
        :param frequence: 时间频率
        """
        # 1. 股票池
        if isinstance(code_list, tuple):
            code_list = list(code_list)

        # 2. 时间频率
        if not frequence:
            frequence = self.frequence
        frequence = utils.get_frequence(frequence)

        if not start_time:
            start_time = self.start_time

        if not end_time:
            end_time = self.end_time

        if (not start_time) or (not end_time):
            raise ValueError("价格获取接口需要指定起始时间与结束时间")

        start_time = str(pd.Timestamp(start_time))[:19]
        end_time = str(pd.Timestamp(end_time))[:19]

        data = QA_fetch_stock_day_adv(
            code=code_list,
            start=start_time,
            end=end_time
        )
        index_data = QA_fetch_index_day_adv(
            code="000001",
            start=start_time,
            end=end_time
        )
        # 3. 复权
        if not fq:
            fq = self.fq

        if not fq:
            data = data
        elif fq.lower() in ["pre", "qfq", "前复权"]:
            data = data.to_qfq()
        elif fq.lower() in ["post", "hfq", "后复权"]:
            data = data.to_hfq()
        elif fq.lower() in ["none", "bfq", "不复权"]:
            data = data

        # 4. 重采样
        # 考虑到停牌退市等原因，重采样会有异常值，即日期与我们需要的日期不一致
        # 这里采用指数作为基准，对重采样数据进行再处理
        # 对于停牌数据缺失，采用前值作为填充
        if frequence == "1d":
            data = data.data.unstack().ffill().stack()
        else:
            index_data = index_data.resample(frequence).unstack()
            data = data.resample(frequence).unstack().ffill()
            data = data.reindex(index_data.index).stack()
            if frequence == '1q':
                data.index = data.index.map(
                    lambda x: (utils.QA_fmt_quarter(x[0]),
                               x[1])
                )

        # 5. 价格类型
        if not price_type:
            price_type = self.price_type

        if price_type.lower() == "avg":
            avg = data["amount"] / data["volume"] / 100.0
            return avg.unstack()
        return data[price_type.lower()].unstack()

    def get_groupby(
            self,
            code_list: Union[str,
                             Tuple[str],
                             List[str]],
            factor_time_range: list = None,
            industry_cls: str = None,
            industry_data: Union[dict,
                                 pd.Series,
                                 pd.DataFrame] = None,
            frequence: str = 'DAY',
            detailed: bool = False,
    ) -> pd.Series:
        """
        获取行业信息

        参数
        ---
        :param code_list: 股票代码
        :param factor_time_range: 因子时间范围
        :param industry_cls: 行业分类
        :param industry_data: 行业信息
        :param detailed: 如果按日期获取行业数据，对速度影响很大,
              设置该参数为 False, 则默认按照 end_time 的行业分类作为全部日期的行业信息

        返回
        ---
        :return: 以 ['日期' '股票'] 为索引的行业信息
        """
        # 1. 股票代码
        if isinstance(code_list, tuple):
            code_list = list(code_list)

        # 2. 日期处理
        if not detailed:
            date_range = [pd.Timestamp(max(factor_time_range)).date()]
        else:
            date_range = list(map(lambda x: x.date(), factor_time_range))

        # 3. 行业处理
        if not industry_cls:
            industry_cls = self.industry_cls

        if not industry_data:
            industry_data = self.industry_data

        if (industry_cls is None) and (industry_data is None):
            warnings.warn("没有指定行业分类方式，也没有输入行业分类信息", UserWarning)
            return pd.Series(
                index=pd.MultiIndex.from_product([date_range,
                                                  code_list]),
                name="group",
                data="NA",
            )

        # 4. 具体行业
        if not industry_cls:                                   # 没有输入行业分类信息
            df_local = pd.DataFrame()
            if isinstance(industry_data, dict):
                df_local = pd.DataFrame(
                    index=date_range,
                    data=[industry_data] * len(date_range)
                ).stack(level=-1)
            if isinstance(industry_data, pd.DataFrame):
                df_local = industry_data.stack(level=-1)
            else:
                df_local = industry_data
            df_local.index.names = ["date", "code"]
            return df_local
                                                               # 如果输入了行业分类信息，按行业分类信息进行处理
                                                               # FIXME: 暂时使用聚宽的行业数据
        # stock_list = utils.QA_fmt_code_list(code_list, style="jq")
        stock_list = utils.QA_fmt_code_list(code_list)
        df_local = pd.DataFrame()
        for cursor_date in date_range:
            df_tmp = QA_fetch_industry_adv(
                    code=code_list,
                    cursor_date = cursor_date,
                    levels=industry_cls.split('_')[1],
                    src=industry_cls.split("_")[0])[["code", "industry_name"]]
            df_tmp["date"] = cursor_date
            df_local = df_local.append(df_tmp)
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
        # df_local = pd.DataFrame(industries).T.sort_index()
        # df_local.columns = df_local.columns.map(lambda x: x[0:6])
        # df_local = df_local.stack(level=-1)
        # df_local.index.names = ["date", "code"]
        df_local = df_local.set_index(["date", "code"])
        return df_local["industry_name"]

    def get_weights(
            self,
            code_list: Union[str,
                             Tuple[str],
                             List[str]],
            factor_time_range: list = None,
            weight_cls: str = None,
            weight_data: Union[dict,
                               pd.Series,
                               pd.DataFrame] = None,
            detailed: bool = True,
            frequence: str = '1d'
    ):
        """
        获取权重信息
        """
        # 1. 股票池处理
        if isinstance(code_list, tuple):
            code_list = list(code_list)

        # 2. 日期处理
        if not detailed:
            date_range = [pd.Timestamp(max(factor_time_range)).date()]
        else:
            date_range = list(map(lambda x: x.date(), factor_time_range))
        start_time = str(min(factor_time_range))[:10]
        end_time = str(max(factor_time_range))[:10]

        # 3. 权重处理
        if not weight_cls:
            weight_cls = self.weight_cls

        if not weight_data:
            weight_data = self.weight_data

        if (not weight_cls) and (not weight_data):
            weight_cls = "avg"
            warnings.warn("没有指定加权分类方式，采用等权方式", UserWarning)
            return pd.Series(
                index=pd.MultiIndex.from_product([date_range,
                                                  code_list]),
                name="weight",
                data=1.0,
            )

        # 4. 具体权重处理
        if not weight_cls:                                         # 没有输入行业分类信息
            df_local = pd.DataFrame()
            if isinstance(weight_data, dict):
                df_local = pd.DataFrame(
                    index=date_range,
                    data=weight_data
                ).stack()
            elif isinstance(weight_data, pd.DataFrame):
                df_local = weight_data.stack()
            else:
                df_local = weight_data
            df_local.index.names = ["date", "code"]
            return df_local
        else:                                                      # 如果输入了权重分类信息，按权重分类信息进行处理
            df_local = pd.DataFrame()
            if weight_cls == "avg":
                df_local = pd.DataFrame(
                    index=date_range,
                    columns=code_list
                ).fillna(1.0)
                return df_local.stack()
            df_local = QAAnalysis_block(
                code=code_list,
                start=start_time,
                end=end_time
            ).market_value
            if frequence == '1q':
                mv = df_local["mv"].unstack().resample(frequence).agg('last')
                cmv = df_local['liquidity_mv'].unstack().resample(
                    frequence
                ).agg("last")
                mv.index = mv.index.map(utils.QA_fmt_quarter)
                cmv.index = cmv.index.map(utils.QA_fmt_quarter)
            else:
                mv = df_local["mv"].unstack()
                cmv = df_local["liquidity_mv"].unstack()
            if weight_cls == "mktcap":
                df_local = mv
            elif weight_cls == "sqrt_mktcap":
                df_local = mv.transform("sqrt")
            elif weight_cls == "ln_mktcap":
                df_local = mv.transform("log")
            elif weight_cls == "cmktcap":
                df_local = cmv
            elif weight_cls == "sqrt_cmktcap":
                df_local = cmv.transform("sqrt")
            elif weight_cls == "ln_cmktcap":
                df_local = cmv.transform("log")
            else:
                raise ValueError(f"{weight_cls} 加权方式未实现")
            df_local = df_local.stack()
            return df_local

    def get_start_date(
            self,
            code_list: Union[str,
                             Tuple[str],
                             List[str]],
            factor_time_range: list
    ):
        """
        获取上市时间
        """
        # stock_list = utils.QA_fmt_code_list(code_list, style="jq")
        # df_local = jqdatasdk.get_all_securities(types="stock")
        stock_list = utils.QA_fmt_code_list(code_list)
        df_local = QA_fetch_stock_basic(status=None).set_index("code")
        intersection = list(df_local.index.intersection(stock_list))
        ss = df_local.loc[intersection]["list_date"]
        # ss.index = ss.index.map(lambda x: x[:6])
        # 日期处理
        date_range = list(map(lambda x: x.date(), factor_time_range))

        multiindex = pd.MultiIndex.from_product(
            [date_range,
             utils.QA_fmt_code_list(intersection)]
        )
        values = multiindex.map(lambda x: ss.loc[x[1]]).tolist()
        df_local = pd.Series(index=multiindex, data=values)
        df_local.index.names = ["date", "code"]
        return df_local

    @property
    def apis(self):
        return dict(
            prices=self.get_prices,
            groupby=self.get_groupby,
            weights=self.get_weights,
            stock_start_date=self.get_start_date,
            frequence=self.frequence,
        )
