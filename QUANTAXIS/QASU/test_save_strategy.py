

# utf-8
import time

from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, FREQUENCE, MARKET_TYPE,
                                          ORDER_DIRECTION, ORDER_MODEL)
from QUANTAXIS.QASU.save_strategy import QA_SU_save_strategy

# QA_SU_save_strategy('MA_strategy_day',portfolio_cookie='stock',version=1.5,if_save=True)


class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN
        self.commission_coeff = 0.00015
        self.tax_coeff = 0.0001

    def on_bar(self, event):
        sellavailable = self.sell_available
        try:
            for item in event.market_data.code:
                if sellavailable is None:

                    event.send_order(account_cookie=self.account_cookie,
                                     amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=item.high[0],
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker)

                else:
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

        except:
            pass
