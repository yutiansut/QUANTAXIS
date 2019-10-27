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



print('此测试文件需要配合jqdata使用, 详情请参考 QA_JQDATA')
JQ_USERNAME = input('JQDATA_USERNAME: ')
JQ_PASSWORD = input('JQDATA_PASSWORD: ')
jqdatasdk.auth(JQ_USERNAME, JQ_PASSWORD)

# code_list = QA.QA_fetch_stock_block_adv().get_block(
#     "白酒").index.get_level_values("code").tolist()
code_list = QA.QA_fetch_stock_block_adv(
).get_block("中证200").index.get_level_values("code").tolist()
df_finance = QA.QA_fetch_financial_report_adv(
    code=code_list,
    start='2016-01-01',
    end='2018-12-31'
).data

if len(df_finance) ==0:
    print('请先存储QUANTAXIS 财务数据 ==> 输入quantaxis进入cli后 输入save financialfiles')
else:
    factor = df_finance['ROE']

    # 因子格式化
    factor = preprocess.QA_fmt_factor(factor)

    # 上市日期过滤
    factor_data = preprocess.QA_fetch_get_factor_start_date(factor)
    factor_data = factor_data.reset_index()
    factor_data = factor_data.loc[(factor_data.datetime - factor_data.start_date
                                ) > pd.Timedelta("200D")].set_index(
                                    ["datetime",
                                    "code"]
                                )
    factor = factor_data['factor']

    # 极值处理，默认使用 "MAD"
    factor = preprocess.QA_winsorize_factor(factor)
    factor_time_range = factor.index.remove_unused_levels(
    ).get_level_values("datetime").tolist()
    # 数据导入
    dataapi = data.DataApi(
        jq_username=JQ_USERNAME,
        jq_password=JQ_PASSWORD,
        factor_time_range=factor_time_range,
        industry_cls="sw_l1",
        weight_cls="mktcap",
        detailed=True,
        frequence='1q'
    )
    analyzer = analyze.FactorAnalyzer(
        factor=factor,
        **dataapi.apis,
        periods=1,
        max_loss=0.9
    )

    # 因子数据
    factor_data = analyzer.clean_factor_data.head()

    # 简略分析
    tears.create_summary_tear_sheet(factor_data=analyzer.clean_factor_data)
