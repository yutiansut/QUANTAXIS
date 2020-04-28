import jqdatasdk
import pandas as pd
import QUANTAXIS as QA

from QUANTAXIS.QAFactor.analyze import FactorAnalyzer
from QUANTAXIS.QAFactor.data import DataApi
import QUANTAXIS.QAFactor.preprocess as preprocess
import QUANTAXIS.QAFactor.tears as tears
import QUANTAXIS.QAFactor.utils as utils

jqdatasdk.auth("聚宽用户名", "聚宽密码")

# 因子股票池
code_list = QA.QA_fetch_stock_block_adv().get_block(
    "白酒").index.get_level_values("code").tolist()

# 数据时间范围
start_date = '2018-01-01'
end_date = '2019-09-30'

# 日线数据
# 注意：这里需要取出 dataframe 格式数据
stock_data = QA.QA_fetch_stock_day_adv(code=code_list,
                                       start=start_date,
                                       end=end_date).to_qfq().data

# 原始因子产生
kdj = stock_data.groupby("code").apply(
    QA.QAIndicator.QA_indicator_KDJ).droplevel(level=-1)
k_value = kdj["KDJ_K"]
d_value = kdj["KDJ_D"]
j_value = kdj["KDJ_J"]

# 原始因子处理
# 1. 测试 J 值
factor = d_value
# 因子格式化:
# - 修改因子索引 level 为先日期，后股票代码
# - 修改因子索引名称为 ['datetime', 'code']
factor = preprocess.QA_fmt_factor(factor)

# 上市日期过滤：这里使用了聚宽的数据源，需要提前导入聚宽本地数据源
# QA_fetch_get_factor_start_date 做了两件事
# 1. 因子格式化
# 2. 对因子股票池附加上市日期
factor_data = preprocess.QA_fetch_get_factor_start_date(factor)
factor_data = factor_data.reset_index()
factor_data = factor_data.loc[(factor_data.datetime - factor_data.start_date
                               ) > pd.Timedelta("200D")].set_index(
                                   ["datetime", "code"])
factor = factor_data['factor']

# 极值处理，默认使用 "MAD"
# QA_winsorize_factor 默认使用 “MAD” 极值处理方式, 按日期分组进行极值处理
factor = preprocess.QA_winsorize_factor(factor)

# 因子数据的日期索引作为参数传入 DataApi，方便其处理行业、权重数据
factor_time_range = factor.index.remove_unused_levels().get_level_values(
    "datetime").tolist()
# 量价数据、行业数据、权重数据导入
# 行业数据目前采用聚宽数据源，权重数据直接使用 QUANTAXIS 本地数据，由于 QA 对于权重计算使用的是前复权
# 计算方式，后复权计算远期收益可能会有纰漏，建议直接使用前复权数据计算远期收益率
# 注意：如果在单因子处理的时候已经分行业处理过，不建议直接采用聚宽数据源的行业数据，不同的行业分类标准
# 差异会很大，在 DataApi 支持直接输入行业数据，譬如这里我们也可以除了使用 industry_cls, 还可以直接
# 输入 industry_data, 权重处理一样支持直接输入 weight_data

# 方式一：使用聚宽支持的行业数据源
# dataapi = QA_data.DataApi(jq_username="聚宽用户名",
#                           jq_password="聚宽密码",
#                           factor_time_range=factor_time_range,
#                           industry_cls="sw_l1",
#                           weight_cls="mktcap",
#                           detailed=True,
#                           frequence='1d')

# # 方式二：直接输入行业数据
industry_data = pd.Series(index=factor.index, data='白酒')
dataapi = DataApi(jq_username="聚宽用户名",
                  jq_password="聚宽密码",
                  factor_time_range=factor_time_range,
                  industry_cls=None,
                  industry_data=industry_data,
                  weight_cls="mktcap",
                  detailed=True,
                  frequence='1d')

analyzer = FactorAnalyzer(factor=factor, **dataapi.apis, max_loss=0.9)

# 加工后的因子数据，包括因子值、行业、权重、远期收益以及而分位数据
clean_factor = analyzer.clean_factor_data

# 基于加工后的因子数据统计分析结果展示
analyzer.create_summary_tear_sheet()
