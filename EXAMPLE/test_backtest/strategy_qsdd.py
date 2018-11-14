# -*- coding: utf-8 -*-
# Name: QSDD strategy

import QUANTAXIS as QA
import numpy as np
import pandas as pd
import talib
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# code_list = ['000001', '000002', '000004', '600000',
#              '600536', '000936', '002023', '600332',
#              '600398', '300498', '603609', '300673']
code_list = QA.QA_fetch_stock_block_adv().code[0:50]
start_date = '2017-01-01'
end_date = '2018-05-23'

'''
QSDD 
趋势顶底（QSDD）指标介绍

'''

# define the QSDD strategy


def QSDD(dataframe, SHORT=12, LONG=26, M=9):
    """
    1.line_mid向上突破line_long，买入信号参考。
    2.line_mid向下跌破line_long，卖出信号参考。
    """
    OPEN = dataframe.open
    HIGH = dataframe.high
    LOW = dataframe.low
    CLOSE = dataframe.close

    # QSDD策略
    # A = talib.MA(-100 * (talib.MAX(HIGH, 34) - CLOSE) / (talib.MAX(HIGH, 34) - talib.MIN(LOW, 34)), 19)
    # B = -100 * (talib.MAX(HIGH, 14) - CLOSE) / (talib.MAX(HIGH, 14) - talib.MIN(LOW, 14))
    # D = talib.EMA(-100 * (talib.MAX(HIGH, 34) - CLOSE) / (talib.MAX(HIGH, 34) - talib.MIN(LOW, 34)), 4)
    A = QA.MA(-100 * (QA.HHV(HIGH, 34) - CLOSE) /
              (QA.HHV(HIGH, 34) - QA.LLV(LOW, 34)), 19)
    B = -100 * (QA.HHV(HIGH, 14) - CLOSE) / \
        (QA.HHV(HIGH, 14) - QA.LLV(LOW, 14))
    D = QA.EMA(-100 * (QA.HHV(HIGH, 34) - CLOSE) /
               (QA.HHV(HIGH, 34) - QA.LLV(LOW, 34)), 4)

    line_long = A + 100
    line_short = B + 100
    line_mid = D + 100  # 信号线

    CROSS_JC = QA.CROSS(line_mid, line_long)
    CROSS_SC = QA.CROSS(line_long, line_mid)
    return pd.DataFrame({'line_mid': line_mid, 'line_long': line_long, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC})


# create account
Account = QA.QA_Account()
Broker = QA.QA_BacktestBroker()

Account.reset_assets(1000000)
Account.account_cookie = 'user_admin_qsdd'

# get data from mongodb
data = QA.QA_fetch_stock_day_adv(code_list, start_date, end_date)
data = data.to_qfq()

# add indicator
ind = data.add_func(QSDD)
# ind.xs('000001',level=1)['2018-01'].plot()

# data_forbacktest=data.select_time('2018-01-01','2018-05-20')
data_forbacktest = data

for items in data_forbacktest.panel_gen:
    for item in items.security_gen:
        daily_ind = ind.loc[item.index]
        if daily_ind.CROSS_JC.iloc[0] > 0:
            order = Account.send_order(
                code=item.code[0],
                time=item.date[0],
                amount=1000,
                towards=QA.ORDER_DIRECTION.BUY,
                price=0,
                order_model=QA.ORDER_MODEL.CLOSE,
                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
            )
            Broker.receive_order(QA.QA_Event(order=order, market_data=item))
            trade_mes = Broker.query_orders(Account.account_cookie, 'filled')
            res = trade_mes.loc[order.account_cookie, order.realorder_id]
            order.trade(res.trade_id, res.trade_price,
                        res.trade_amount, res.trade_time)
        elif daily_ind.CROSS_SC.iloc[0] > 0:
            if Account.sell_available.get(item.code[0], 0) > 0:
                order = Account.send_order(
                    code=item.code[0],
                    time=item.date[0],
                    amount=Account.sell_available.get(item.code[0], 0),
                    towards=QA.ORDER_DIRECTION.SELL,
                    price=0,
                    order_model=QA.ORDER_MODEL.MARKET,
                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                )
                Broker.receive_order(QA.QA_Event(
                    order=order, market_data=item))
                trade_mes = Broker.query_orders(
                    Account.account_cookie, 'filled')
                res = trade_mes.loc[order.account_cookie, order.realorder_id]
                order.trade(res.trade_id, res.trade_price,
                            res.trade_amount, res.trade_time)
    Account.settle()

print(Account.history)
print(Account.history_table)
print(Account.daily_hold)

# create Risk analysis
Risk = QA.QA_Risk(Account)
print(Risk.message)
print(Risk.assets)

# Risk.assets.plot()
# Risk.benchmark_assets.plot()
fig = Risk.plot_assets_curve()
fig.plot()
fig = Risk.plot_dailyhold()
fig.plot()
fig = Risk.plot_signal()
fig.plot()

# plt.style.use('ggplot')
# f, ax = plt.subplots(figsize=(20, 8))
# ax.set_title('SIGNAL TABLE --ACCOUNT: {}'.format(Account.account_cookie))
# ax.set_xlabel('Code')
# ax.set_ylabel('DATETIME', rotation=90)
# import matplotlib.patches as mpatches
# # x2 = Risk.benchmark_assets.x
#
# patch_assert = mpatches.Patch(color='red', label='assert')
# patch_benchmark = mpatches.Patch(label='benchmark')
# plt.legend(handles=[patch_assert, patch_benchmark], loc=0)
# plt.title('Assert and Benchmark')
#
#
# cmap = sns.cubehelix_palette(start=1, rot=3, gamma=0.8, as_cmap=True)
# ht = sns.heatmap(Account.trade.head(55), cmap=cmap, linewidths=0.05, ax=ax)
# # sns.heatmap(Account.trade.head(55), cmap="YlGnBu",linewidths = 0.05, ax = ax)
# # ht.set_xticklabels(rotation=90)
# # ht.set_yticklabels(rotation=90)
# plt.show()

# # save result
# Account.save()
# Risk.save()
#
# account_info=QA.QA_fetch_account({'account_cookie':'user_admin_macd'})
# account=QA.QA_Account().from_message(account_info[0])
# print(account)
