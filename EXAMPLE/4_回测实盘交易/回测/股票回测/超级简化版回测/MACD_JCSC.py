# -*- coding: utf-8 -*-
# Demo: MACD strategy
# src: ./test_backtest/MACD_JCSC.py
# jupyter: ./test_backtest/QUANTAXIS回测分析全过程讲解.ipynb
# paper: ./test_backtest/QUANTAXIS回测分析全过程讲解.md

import QUANTAXIS as QA
import numpy as np
import pandas as pd
import datetime
st1=datetime.datetime.now()
# define the MACD strategy
def MACD_JCSC(dataframe, SHORT=12, LONG=26, M=9):
    """
    1.DIF向上突破DEA，买入信号参考。
    2.DIF向下跌破DEA，卖出信号参考。
    """
    CLOSE = dataframe.close
    DIFF = QA.EMA(CLOSE, SHORT) - QA.EMA(CLOSE, LONG)
    DEA = QA.EMA(DIFF, M)
    MACD = 2*(DIFF-DEA)

    CROSS_JC = QA.CROSS(DIFF, DEA)
    CROSS_SC = QA.CROSS(DEA, DIFF)
    ZERO = 0
    return pd.DataFrame({'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})


# create account
user = QA.QA_User(username='quantaxis', password='quantaxis')
portfolio = user.new_portfolio('qatestportfolio')


Account = portfolio.new_account(account_cookie='macd_stock', init_cash=1000000)
Broker = QA.QA_BacktestBroker()

QA.QA_SU_save_strategy('MACD_JCSC','Indicator',Account.account_cookie)
# get data from mongodb
QA.QA_SU_save_strategy('MACD_JCSC', 'Indicator',
                       Account.account_cookie, if_save=True)
data = QA.QA_fetch_stock_day_adv(
    ['000001', '000002', '000004', '600000'], '2017-09-01', '2018-05-20')
data = data.to_qfq()

# add indicator
ind = data.add_func(MACD_JCSC)
# ind.xs('000001',level=1)['2018-01'].plot()

data_forbacktest=data.select_time('2018-01-01','2018-05-01')


for items in data_forbacktest.panel_gen:
    for item in items.security_gen:
        ###################
        daily_ind=ind.loc[item.index]

        if daily_ind.CROSS_JC.iloc[0]>0:
            order=Account.send_order(
                code=item.code[0], 
                time=item.date[0], 
                amount=1000, 
                towards=QA.ORDER_DIRECTION.BUY, 
                price=0, 
                order_model=QA.ORDER_MODEL.CLOSE, 
                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                )
            #print(item.to_json()[0])
            Broker.receive_order(QA.QA_Event(order=order,market_data=item))
            trade_mes=Broker.query_orders(Account.account_cookie,'filled')
            res=trade_mes.loc[order.account_cookie,order.realorder_id]
            order.trade(res.trade_id,res.trade_price,res.trade_amount,res.trade_time)
        elif daily_ind.CROSS_SC.iloc[0]>0:
            #print(item.code)
            if Account.sell_available.get(item.code[0], 0)>0:
                order=Account.send_order(
                    code=item.code[0], 
                    time=item.date[0], 
                    amount=Account.sell_available.get(item.code[0], 0), 
                    towards=QA.ORDER_DIRECTION.SELL, 
                    price=0, 
                    order_model=QA.ORDER_MODEL.MARKET, 
                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                #print
                Broker.receive_order(QA.QA_Event(order=order,market_data=item))
                trade_mes=Broker.query_orders(Account.account_cookie,'filled')
                res=trade_mes.loc[order.account_cookie,order.realorder_id]
                order.trade(res.trade_id,res.trade_price,res.trade_amount,res.trade_time)
    Account.settle()

print('TIME -- {}'.format(datetime.datetime.now()-st1))
print(Account.history)
print(Account.history_table)
print(Account.daily_hold)

# create Risk analysis
Risk = QA.QA_Risk(Account)

Account.save()
Risk.save()


# print(Risk.message)
# print(Risk.assets)
# Risk.plot_assets_curve()
# plt=Risk.plot_dailyhold()
# plt.show()
# plt1=Risk.plot_signal()
# plt.show()

# performance=QA.QA_Performance(Account)
# plt=performance.plot_pnlmoney(performance.pnl_fifo)
# plt.show()
# Risk.assets.plot()
# Risk.benchmark_assets.plot()

# save result

#account_info = QA.QA_fetch_account({'account_cookie': 'user_admin_macd'})
#account = QA.QA_Account().from_message(account_info[0])
#print(account)
