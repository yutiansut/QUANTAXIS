# coding=utf-8

from datetime import datetime

import numpy as np

import QUANTAXIS as QA
from QUANTAXIS import QA_Backtest as QB


"""
写在前面:
===============QUANTAXIS BACKTEST STOCK_DAY中的变量
常量:
QB.backtest_type 回测类型 day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
QB.account.message  当前账户消息
QB.account.cash  当前可用资金
QB.account.hold  当前账户持仓
QB.account.history  当前账户的历史交易记录
QB.account.assets 当前账户总资产
QB.account.detail 当前账户的交易对账单
QB.account.init_assest 账户的最初资金
QB.strategy_gap 前推日期
QB.strategy_name 策略名称

QB.strategy_stock_list 回测初始化的时候  输入的一个回测标的
QB.strategy_start_date 回测的开始时间
QB.strategy_end_date  回测的结束时间

QB.setting.QA_setting_user_name = str('admin') #回测账户
QB.setting.QA_setting_user_password = str('admin') #回测密码

QB.today  在策略里面代表策略执行时的日期
QB.now  在策略里面代表策略执行时的时间
QB.benchmark_code  策略业绩评价的对照行情
QB.benchmark_type  对照行情是股票还是指数


QB.backtest_print_log = True  # 是否在屏幕上输出结果

函数:
获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today)
获取单个bar
QB.QA_backtest_get_market_data_bar(QB,code,QB.today/QB.now)

拿到开高收低量
Open,High,Low,Close,Volume=QB.QA_backtest_get_OHLCV(QB,QB.QA_backtest_get_market_data(QB,item,QB.today))

获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)

一键平仓:
QB.QA_backtest_sell_all(QB)

报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)

order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market  [其实是以bar的开盘价成交]
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C

#查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)
#查询当前一只股票的可卖数量
QB.QA_backtest_sell_available(QB,code)
#查询当前一只股票的持仓平均成本
QB.QA_backtest_hold_price(QB,code)

近期新增:
QB.QA_backtest_get_market_data_panel(QB,time,type_)

QB.QA_backtest_get_block(QB,block_list)  # 获取股票的板块代码  输入是一个板块的list ['钢铁','昨日涨停']  输出是不重复的股票列表
"""


@QB.backtest_init
def init():
    # 回测的类别
    # day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
    QB.backtest_type = 'day'
    # QB.backtest_type='5min' # 日线回测
    # 策略的名称
    QB.strategy_name = 'test_daily'
    # 数据库位置
    QB.setting.QA_util_sql_mongo_ip = '127.0.0.1'  # 回测数据库
    QB.setting.QA_setting_user_name = str('admin')  # 回测账户
    QB.setting.QA_setting_user_password = str('admin')  # 回测密码
    QB.topic_name = 'EXAMPLE'  # 回测的主题
    QB.stratey_version = 'V1'  # 回测的版本号

    QB.account.init_assest = 2000000  # 初始资金

    # benchmark
    QB.benchmark_code = '000300'
    # benchmark 可以是个股，也可以是指数
    QB.benchmark_type = 'index'
    # 手续费系数
    QB.commission_fee_coeff = 0.0015  # 千五的手续费(单向)

    QB.strategy_gap = 30  # 在取数据的时候 向前取多少个bar(会按回测的时间动态移动)
    """
    QB.strategy_stock_list 只需要是一个list即可
    可以用QB.QA_backtest_get_block(QB, ['MSCI成份'])来获取板块成份股代码进行回测
    也可以直接指定股票列表['000001','000002','000004']
    """
    #QB.strategy_stock_list = QB.QA_backtest_get_block(QB, ['MSCI成份'])
    QB.strategy_stock_list = ['000001','000002','000004']
    QB.strategy_start_date = '2017-06-01 10:30:00'  # 回测开始日期
    QB.strategy_end_date = '2017-10-01'  # 回测结束日期
    QB.backtest_print_log = False  # 是否在屏幕上输出结果


@QB.before_backtest
def before_backtest():
    global start_time
    start_time = datetime.now()
    global risk_position


@QB.load_strategy
def strategy():
    global risk_position  # 在这个地方global变量 可以拿到before_backtest里面的东西
    QA.QA_util_log_info(QB.account.sell_available)
    QA.QA_util_log_info('LEFT Cash: %s' % QB.account.cash_available)
    # QB.QA_backtest_get_market_data_panel(QB,time,type_) 面板数据
    # time 如果不填 就是默认的QB.now/QB.today
    # type_ 如果不填 默认是 'lt' 如果需要当日的数据 'lte'
    amounts = 1 if len(QB.strategy_stock_list) - len(QB.account.sell_available) == 0 else len(
        QB.strategy_stock_list) - len(QB.account.sell_available)
    each_capital = int(QB.account.cash_available / amounts)

    for item in QB.strategy_stock_list:
        if QB.QA_backtest_find_bar(QB, item, QB.today) is not None:  # 今日开盘-能取到数据
            market_data = QB.QA_backtest_get_market_data(
                QB, item, QB.today, type_='lte')  # type_='lte' 才能取到今日
            Open, High, Low, Close, Volume = QB.QA_backtest_get_OHLCV(
                QB, market_data)

            MA = market_data.add_func(QA.QA_indicator_MA, 10)
            MA_s = MA[0][-1]
            if not np.isnan(MA_s):
                if QB.QA_backtest_hold_amount(QB, item) == 0:  # 如果不持仓
                    if Close[-1] >= MA_s:
                        QB.QA_backtest_send_order(QB, code=item, amount=int(
                            each_capital / Close[-1] / 100) * 100, towards=1, order_type={'bid_model': 'c'})
                elif QB.QA_backtest_sell_available(QB, item) > 0:  # 如果可卖数量大于0
                    hold_price = QB.QA_backtest_hold_price(QB, item)

                    if Close[-1] <= MA_s:
                        QB.QA_backtest_send_order(QB, code=item, amount=QB.QA_backtest_sell_available(
                            QB, item), towards=-1, order_type={'bid_model': 'c'})

        else:
            QA.QA_util_log_info('{} HAS NO DATA IN {}'.format(
                item, QB.today))  # 如果是分钟回测 用QB.now
    pcg_total = len(QA.QA_util_get_trade_range(
        QB.strategy_start_date, QB.strategy_end_date))
    pcg_now = len(QA.QA_util_get_trade_range(QB.strategy_start_date, QB.today))
    QA.QA_util_log_info('Now Completed {}%'.format(
        int(100 * pcg_now / pcg_total)))


# #查询当前一只股票的持仓量
# QB.QA_backtest_hold_amount(QB,code)
# #查询当前一只股票的可卖数量
# QB.QA_backtest_sell_available(QB,code)
# #查询当前一只股票的持仓平均成本
# QB.QA_backtest_hold_price(QB,code)
@QB.end_backtest
def after_backtest():
    global start_time
    end_time = datetime.now()
    cost_time = (end_time - start_time).total_seconds()
    QA.QA_util_log_info('耗费时间 {} {}'.format(cost_time, 'seconds'))

    QB.if_save_to_csv = True
    QB.if_save_to_mongo = True
