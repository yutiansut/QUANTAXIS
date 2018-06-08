# utf-8
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE,
                                          FREQUENCE, ORDER_DIRECTION,
                                          ORDER_MODEL)


class MAMINStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.FIFTEEN_MIN
        self.market_type = MARKET_TYPE.STOCK_CN

    def on_bar(self, event):
        try:
            for item in event.market_data.code:

                if self.sell_available.get(item, 0) > 0:
                    event.send_order(account_id=self.account_cookie,
                                     amount=self.sell_available[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.SELL,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker
                                     )
                else:
                    event.send_order(account_id=self.account_cookie,
                                     amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker)
        except:
            pass
