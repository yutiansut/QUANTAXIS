# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
    os.chdir(os.path.join(os.getcwd(), 'EXAMPLE\test_backtest\FUTURE'))
    print(os.getcwd())
except:
    pass

# %%
import QUANTAXIS as QA
import sys


# %%
user = QA.QA_User(username='quantaxis', password='quantaxis')
portfolio = user.new_portfolio('qatestportfolio')
Account = portfolio.new_account(allow_sellopen=True, allow_margin=True, init_cash=5000, allow_t0=True,
                                account_cookie='future_testx', market_type=QA.MARKET_TYPE.FUTURE_CN, frequence=QA.FREQUENCE.FIFTEEN_MIN)


# %%
Broker = QA.QA_BacktestBroker()


# %%
rb_ds = QA.QA_fetch_future_min_adv(
    'RBL8', '2019-01-01', '2019-07-20', frequence='15min')


# %%
import numpy as np
import pandas as pd


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


ind = rb_ds.add_func(MACD_JCSC)


# %%
_date = None
for items in rb_ds.panel_gen:
    if _date != items.date[0]:
        print('try to settle')
        _date = items.date[0]
        Account.settle()

    for item in items.security_gen:
        daily_ind = ind.loc[item.index]
        if daily_ind.CROSS_JC.iloc[0] > 0:
            order = Account.send_order(
                code=item.code[0],
                time=item.datetime[0],
                amount=1,
                towards=QA.ORDER_DIRECTION.BUY_OPEN,
                price=0,
                order_model=QA.ORDER_MODEL.CLOSE,
                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
            )

            if order:
                print(order)
                print(item)
                Broker.receive_order(QA.QA_Event(
                    order=order, market_data=item))

                trade_mes = Broker.query_orders(
                    Account.account_cookie, 'filled')
                res = trade_mes.loc[order.account_cookie, order.realorder_id]
                order.trade(res.trade_id, res.trade_price,
                            res.trade_amount, res.trade_time)
        elif daily_ind.CROSS_SC.iloc[0] > 0:
            if Account.sell_available.get(item.code[0], 0) > 0:
                order = Account.send_order(
                    code=item.code[0],
                    time=item.datetime[0],
                    amount=Account.sell_available.get(item.code[0], 0),
                    towards=QA.ORDER_DIRECTION.SELL_CLOSE,
                    price=0,
                    order_model=QA.ORDER_MODEL.MARKET,
                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                )
                if order:
                    Broker.receive_order(QA.QA_Event(
                        order=order, market_data=item))

                    trade_mes = Broker.query_orders(
                        Account.account_cookie, 'filled')
                    res = trade_mes.loc[order.account_cookie,
                                        order.realorder_id]
                    order.trade(res.trade_id, res.trade_price,
                                res.trade_amount, res.trade_time)
    Account.settle()

# %%
Risk = QA.QA_Risk(Account)


# %%
Risk.plot_assets_curve()


# %%
Risk.profit_construct


Account.save()
Risk.save()
