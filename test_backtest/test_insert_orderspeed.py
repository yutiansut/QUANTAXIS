import QUANTAXIS as QA
import time
market = QA.QA_Market()
user = QA.QA_Portfolio()
# 创建两个account
# 这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
# 然后返回的是这个账户的id
a_1 = user.new_account()

market.start()
market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)

# 打印market
print(market)


"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易
market.login(QA.BROKER_TYPE.BACKETEST, a_1, user.get_account(a_1))
for i in range(10):
    market.insert_order(account_id=a_1, amount=100000, price=None, amount_model=QA.AMOUNT_MODEL.BY_PRICE, time='2017-12-01', code='600010',
                        order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY, market_type=QA.MARKET_TYPE.STOCK_DAY,
                        data_type=QA.MARKETDATA_TYPE.DAY, broker_name=QA.BROKER_TYPE.BACKETEST)


market._settle(QA.BROKER_TYPE.BACKETEST)
while True:
    if market.clear():
        break
print(user.get_account(a_1).history)
print(user.get_account(a_1).cash)
print(user.get_account(a_1).cash_available)
print(user.get_account(a_1).history_table)
print(user.get_account(a_1).hold)

market.trade_engine.stop_all()
market.trade_engine.stop()
