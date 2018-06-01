# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
B = QA.QA_BacktestBroker()
AC = QA.QA_Account()
"""
# 账户设置初始资金
AC.reset_assets(assets)

# 发送订单
Order=AC.send_order(code='000001',amount=1000,time='2018-03-21',towards=QA.ORDER_DIRECTION.BUY,price=0,order_model=QA.ORDER_MODEL.MARKET,amount_model=QA.AMOUNT_MODEL.BY_AMOUNT)
# 撮合订单
dealmes=B.receive_order(QA.QA_Event(order=Order,market_data=data))
# 更新账户
AC.receive_deal(dealmes)

# 分析结果

risk=QA.QA_Risk(AC)

"""

AC.reset_assets(20000000) #设置初始资金

def simple_backtest(AC, code, start, end):
    DATA = QA.QA_fetch_stock_day_adv(code, start, end).to_qfq()
    for items in DATA.panel_gen:  # 一天过去了
        
        for item in items.security_gen:
            if random.random()>0.5:# 加入一个随机 模拟买卖的
                if AC.sell_available.get(item.code[0], 0) == 0:
                    order=AC.send_order(
                        code=item.data.code[0], time=item.data.date[0], amount=1000, towards=QA.ORDER_DIRECTION.BUY, price=0, order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    if order:
                        AC.receive_deal(B.receive_order(QA.QA_Event(order=order,market_data=item)))

                else:
                    order=AC.send_order(
                        code=item.data.code[0], time=item.data.date[0], amount=1000, towards=QA.ORDER_DIRECTION.SELL, price=0, order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    if order:
                        AC.receive_deal(B.receive_order(QA.QA_Event(order=order,market_data=item)))
        AC.settle()


simple_backtest(AC, QA.QA_fetch_stock_block_adv().code[0:10], '2017-01-01', '2018-01-31')
print(AC.message)
AC.save()
risk = QA.QA_Risk(AC)
print(risk.message)
risk.save()