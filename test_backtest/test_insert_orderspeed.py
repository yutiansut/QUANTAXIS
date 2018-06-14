# utf-8
import QUANTAXIS as QA

market = QA.QA_Market()
user = QA.QA_Portfolio()
# 创建两个account
# 这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
# 然后返回的是这个账户的id
a_1 = user.new_account()
a_1.reset_assets(100000000)
a_1.frequence = QA.FREQUENCE.FIFTEEN_MIN
market.start()
market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)

# 打印market
print(market)


"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易


market.login(QA.BROKER_TYPE.BACKETEST, a_1.account_cookie, a_1)
for code in ['000001', '000002', '000004', '600010', '000007','000008']:
    market.insert_order(account_id=a_1.account_cookie, amount=100, price=0, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, time='2018-06-12 09:45:00', code=code,
                        order_model=QA.ORDER_MODEL.MARKET, towards=QA.ORDER_DIRECTION.BUY, market_type=QA.MARKET_TYPE.STOCK_CN,
                        frequence=QA.FREQUENCE.FIFTEEN_MIN, broker_name=QA.BROKER_TYPE.BACKETEST)
market.trade_engine.join()
market._settle(QA.BROKER_TYPE.BACKETEST)

print(a_1.history)
print(a_1.cash)
print(a_1.cash_available)
print(a_1.history_table)
print(a_1.hold)

market.trade_engine.stop_all()
market.trade_engine.stop()
