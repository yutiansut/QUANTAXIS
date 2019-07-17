# coding:utf-8


try: 
    import jqdatasdk
    #jqdatasdk.auth(input('account:'),input('password:'))
except:
    raise ModuleNotFoundError


def get_price(code="600000.XSHG"):
    return jqdatasdk.get_price(code,end_date='2018-05-14')



if __name__ =='__main__':
    print(get_price())
"""

get_price

可查询股票、基金、指数、期货的历史及当前交易日的行情数据

可指定单位时间长度，如一天、一分钟、五分钟等

可查询开盘价、收盘价、最高价、最低价、成交量、成交额、涨停、跌停、均价、前收价、是否停牌

支持不同的复权方式

​

get_trade_days

查询指定时间范围的交易日

​

get_all_trade_days

查询所有的交易日

​

get_extras

查询股票是否是ST

查询基金的累计净值、单位净值

查询期货的结算价、持仓量

​

get_index_stocks

查询指定指数在指定交易日的成分股

​

get_industry_stocks

查询指定行业在指定交易日的成分股

​

get_industries

查询行业列表

​

get_concept_stocks

查询指定概念在指定交易日的成分股

​

get_concepts

查询概念列表

​

get_all_securities

查询股票、基金、指数、期货列表

​

get_security_info

查询单个标的的信息

​

get_money_flow

查询某只股票的资金流向数据

​

get_fundamentals

查询财务数据，包含估值表、利润表、现金流量表、资产负债表、银行专项指标、证券专项指标、保险专项指标

​

get_fundamentals_continuously

查询多日的财务数据

​

get_mtss

查询股票、基金的融资融券数据

​

get_billbord_list

查询股票龙虎榜数据

​

get_locked_shares

查询股票限售解禁股数据

​

get_margincash_stocks

获取融资标的列表


get_marginsec_stocks

获取融券标的列表

​

get_future_contracts

查询期货可交易合约列表

​

get_dominant_future

查询主力合约对应的标的

​

get_ticks

查询股票、期货的tick数据

​

normalize_code

归一化证券编码

​

macro.run_query

查询宏观经济数据，具体数据见官网API https://www.joinquant.com/data/dict/macroData

​

alpha101

查询WorldQuant 101 Alphas 因子数据，具体因子解释见官网API https://www.joinquant.com/data/dict/alpha101

​

alpha191

查询短周期价量特征 191 Alphas 因子数据，具体因子解释见官网API https://www.joinquant.com/data/dict/alpha191

​

technical_analysis

技术分析指标，具体因子解释见官网API https://www.joinquant.com/data/dict/technicalanalysis

​

​

baidu_factor

查询股票某日百度搜索量数据
"""