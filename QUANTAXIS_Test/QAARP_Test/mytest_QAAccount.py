# coding:utf-8

import QUANTAXIS as QA
import uuid

user = QA.QA_User(username = 'quantaxis', password= 'quantaxis')

p = user.new_portfolio('test')


ac = p.new_account(account_cookie=str(uuid.uuid4()), market_type=QA.MARKET_TYPE.FUTURE_CN, init_cash=10000)

print('test_BUY/SELL')

ac.receive_simpledeal('RB1905',2800,1, QA.ORDER_DIRECTION.BUY_OPEN,'2019-01-21 09:35:00')

print(ac.hold_available)
ac.receive_simpledeal('RB1905',2803,1, QA.ORDER_DIRECTION.SELL_CLOSE,'2019-01-21 09:45:00')



print('left_cash')

print(ac.cash_available)
print(ac.hold_available)
print(ac.sell_available)

ac.receive_simpledeal('RB1905',2802,1, QA.ORDER_DIRECTION.SELL_OPEN,'2019-01-21 09:55:00')
print(ac.hold_available)
ac.receive_simpledeal('RB1905',2810,1, QA.ORDER_DIRECTION.BUY_CLOSE,'2019-01-21 11:05:00')

print(ac.history_table)

if int(ac.cash[-1]) == 9938:
    print('cash is  true')


print('TEST PORTFOLIO')

perf = QA.QA_Performance(ac)
print(perf.pnl)

from pprint import pprint

pprint(perf.message)