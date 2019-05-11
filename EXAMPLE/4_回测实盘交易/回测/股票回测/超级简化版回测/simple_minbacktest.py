
# coding: utf-8

# In[21]:


import QUANTAXIS as QA
import pandas as pd

data = QA.QA_fetch_stock_min_adv('601318', '2018-03-22', '2018-08-23', '30min')


res = data.add_func(QA.QA_indicator_KDJ)
sig = QA.CROSS(res.KDJ_J, res.KDJ_K)
sig2 = QA.CROSS(res.KDJ_K, res.KDJ_J)

User = QA.QA_User(username='quantaxis', password='quantaxis')
Portfolio = User.new_portfolio('qatestportfolio')
Account = Portfolio.new_account(account_cookie='supersimple', init_cash=100000, init_hold={'601318': 1000},
                                frequence=QA.FREQUENCE.THIRTY_MIN)
Broker = QA.QA_BacktestBroker()
QA.QA_SU_save_strategy(Account.account_cookie,
                       Account.portfolio_cookie, Account.account_cookie, if_save=True)

_date = None
for items in data.panel_gen:
    if _date != items.date[0]:
        print('try to settle')
        _date = items.date[0]
        Account.settle()

    for item in items.security_gen:
        if sig[item.index].iloc[0] > 0:
            order = Account.send_order(
                code=item.code[0],
                time=item.datetime[0],
                amount=1000,
                towards=QA.ORDER_DIRECTION.BUY,
                price=0,
                order_model=QA.ORDER_MODEL.CLOSE,
                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
            )
            if order:
                order.trade('unknownTrade', order.price,
                            order.amount, order.datetime)
        elif sig2[item.index].iloc[0] > 0:
            if Account.sell_available.get(item.code[0], 0) > 0:
                order1 = Account.send_order(
                    code=item.code[0],
                    time=item.datetime[0],
                    amount=1000,
                    towards=QA.ORDER_DIRECTION.SELL,
                    price=0,
                    order_model=QA.ORDER_MODEL.CLOSE,
                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                )
                if order1:
                    order1.trade('unknownTrade', order1.price,
                                 order1.amount, order1.datetime)


print(Account.history_table)


r = QA.QA_Risk(Account)


r.plot_assets_curve().show()

print(r.profit_construct)

Account.save()
r.save()
