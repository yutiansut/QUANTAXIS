"""
测试文件
"""
import jqdatasdk
import pandas as pd
import QUANTAXIS as QA

import QUANTAXIS.QAFactor.analyze as analyze
import QUANTAXIS.QAFactor.data as data
import QUANTAXIS.QAFactor.preprocess as preprocess
import QUANTAXIS.QAFactor.tears as tears
import QUANTAXIS.QAFactor.utils as utils

jqdatasdk.auth("聚宽用户名", "聚宽密码")

code_list = QA.QA_fetch_stock_block_adv().get_block(
    "白酒").index.get_level_values("code").tolist()
# code_list = QA.QA_fetch_stock_block_adv().get_block(
#     "中证200").index.get_level_values("code").tolist()
df_finance = QA.QA_fetch_financial_report_adv(code=code_list,
                                              start='2016-01-01',
                                              end='2019-09-30').data
factor = df_finance['ROE']

# 因子格式化
factor = preprocess.QA_fmt_factor(factor)

# 上市日期过滤
factor_data = preprocess.QA_fetch_get_factor_start_date(factor)
factor_data = factor_data.reset_index()
factor_data = factor_data.loc[(factor_data.datetime - factor_data.start_date
                               ) > pd.Timedelta("200D")].set_index(
                                   ["datetime", "code"])
factor = factor_data['factor']


# 极值处理，默认使用 "MAD"
factor = preprocess.QA_winsorize_factor(factor)
factor_time_range = factor.index.remove_unused_levels().get_level_values(
    "datetime").tolist()

# 数据导入
dataapi = data.DataApi(jq_username="聚宽用户名",
                       jq_password="聚宽密码",
                       factor_time_range=factor_time_range,
                       industry_cls="sw_l1",
                       weight_cls="mktcap",
                       detailed=True,
                       frequence='1q')
analyzer = analyze.FactorAnalyzer(factor=factor,
                                  **dataapi.apis,
                                  periods=(1, 2),
                                  max_loss=0.9)

# 因子数据
factor_data = analyzer.clean_factor_data.head()

# 简略分析
tears.create_summary_tear_sheet(factor_data=analyzer.clean_factor_data)
