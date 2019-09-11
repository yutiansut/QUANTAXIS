# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import QUANTAXIS as QA
import random
"""
单线程模式回测示例
该代码旨在给出一个极其容易实现的小回测 高效 无事件驱动
"""
Broker = QA.QA_BacktestBroker()
User = QA.QA_User(username='quantaxis', password='quantaxis')
Portfolio = User.new_portfolio('qatestportfolio')
AC = Portfolio.new_account(account_cookie='simplebacktest', init_cash=200000)
"""
# 账户设置初始资金
AC.reset_assets(assets)

# 发送订单
Order=AC.send_order(code='000001',amount=1000,time='2018-03-21',towards=QA.ORDER_DIRECTION.BUY,price=0,order_model=QA.ORDER_MODEL.MARKET,amount_model=QA.AMOUNT_MODEL.BY_AMOUNT)
# 撮合订单
B.receive_order(QA.QA_Event(order=Order,market_data=data))

# 查询账户的订单状态
trade_mes=Broker.query_orders(AC.account_cookie, 'filled')
res=trade_mes.loc[order.account_cookie, order.realorder_id]

# 更新订单

order.trade(res.trade_id, res.trade_price,res.trade_amount, res.trade_time)

# 查询订单的状态

order.status


# 分析结果

risk=QA.QA_Risk(AC)

"""

QA.QA_SU_save_strategy('test','test_day',AC.account_cookie,if_save=True)

def simple_backtest(AC, code, start, end):
    DATA = QA.QA_fetch_stock_day_adv(code, start, end).to_qfq()
    for items in DATA.panel_gen:  # 一天过去了

        for item in items.security_gen:
            if random.random() > 0.5:  # 加入一个随机 模拟买卖的
                if AC.sell_available.get(item.code[0], 0) == 0:
                    order = AC.send_order(
                        code=item.code[0], time=item.date[0], amount=1000, towards=QA.ORDER_DIRECTION.BUY, price=0, order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    if order:
                        Broker.receive_order(QA.QA_Event(
                            order=order, market_data=item))
                        trade_mes = Broker.query_orders(
                            AC.account_cookie, 'filled')
                        res = trade_mes.loc[order.account_cookie,
                                            order.realorder_id]
                        print('order {} {} {} {}'.format(
                            res.trade_id, res.trade_price, res.trade_amount, res.trade_time))
                        order.trade(res.trade_id, res.trade_price,
                                    res.trade_amount, res.trade_time)

                else:
                    order = AC.send_order(
                        code=item.code[0], time=item.date[0], amount=1000, towards=QA.ORDER_DIRECTION.SELL, price=0, order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    if order:
                        Broker.receive_order(QA.QA_Event(
                            order=order, market_data=item))
                        trade_mes = Broker.query_orders(
                            AC.account_cookie, 'filled')
                        res = trade_mes.loc[order.account_cookie,
                                            order.realorder_id]
                        print('order {} {} {} {}'.format(
                            res.trade_id, res.trade_price, res.trade_amount, res.trade_time))
                        order.trade(res.trade_id, res.trade_price,
                                    res.trade_amount, res.trade_time)
        AC.settle()


simple_backtest(AC, QA.QA_fetch_stock_block_adv(
).code[0:10], '2017-01-01', '2018-01-31')
print(AC.message)
AC.save()
risk = QA.QA_Risk(AC)
print(risk.message)
risk.save()
