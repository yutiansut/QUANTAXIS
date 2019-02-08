# utf-8
import time
import threading
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, FREQUENCE, MARKET_TYPE,
                                          ORDER_DIRECTION, ORDER_MODEL)


class MAStrategy(QA_Account):
    def __init__(self, user_cookie, portfolio_cookie, account_cookie,  init_cash=100000, init_hold={}):
        super().__init__(user_cookie=user_cookie, portfolio_cookie=portfolio_cookie, account_cookie= account_cookie,
                         init_cash=init_cash, init_hold=init_hold)
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN
        self.commission_coeff = 0.00015
        self.tax_coeff = 0.0001
        self.reset_assets(100000)  # 这是第二种修改办法

    def on_bar(self, event):
        print(threading.enumerate())
        sellavailable = self.sell_available
        try:
            for item in event.market_data.code:
                if sellavailable.get(item, 0) > 0:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=sellavailable[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.SELL,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker
                                     )
                else:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker)

        except Exception as e:
            print(e)
