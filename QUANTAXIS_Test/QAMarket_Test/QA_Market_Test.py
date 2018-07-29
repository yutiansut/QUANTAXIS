#
import datetime
import QUANTAXIS as QA
import time
market = QA.QA_Market(if_start_orderthreading=True)
market.connect(QA.BROKER_TYPE.SHIPANE)
market.start()
haitong_acc = 'account:141'
moni = 'account:1391'

# 实盘账户
if market.login(QA.BROKER_TYPE.SHIPANE, haitong_acc) and market.login(QA.BROKER_TYPE.SHIPANE, moni):
    market._update_orders()
    res = market.insert_order(haitong_acc, code='000001', amount=100, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, order_model=QA.ORDER_MODEL.LIMIT,
                              frequence=QA.FREQUENCE.CURRENT, broker_name=QA.BROKER_TYPE.SHIPANE, market_type=QA.MARKET_TYPE.STOCK_CN,
                              towards=QA.ORDER_DIRECTION.BUY, price=9, time=datetime.datetime.now())

    res2 = market.insert_order(moni, code='000001', amount=100, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, order_model=QA.ORDER_MODEL.LIMIT,
                               frequence=QA.FREQUENCE.CURRENT, broker_name=QA.BROKER_TYPE.SHIPANE, market_type=QA.MARKET_TYPE.STOCK_CN,
                               towards=QA.ORDER_DIRECTION.BUY, price=9, time=datetime.datetime.now())

    time.sleep(1)
    print(market.order_handler.order_status)

    market.cancel_all(QA.BROKER_TYPE.SHIPANE,haitong_acc)
    time.sleep(1)
    print(market.order_handler.order_status)
