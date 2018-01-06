# utf-8
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE,
                                          MARKETDATA_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL)


class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()

    def on_bar(self, event):
        if self.market_data.len > 1:
            for item in event.market_data.code:
                if self.sell_available is None:
                    pass
                else:
                    if self.sell_available.get(item, 0) > 0:
                        event.send_order(account_id=self.account_cookie,
                                         amount=self.sell_available[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                         time=self.current_time, code=item, price=0,
                                         order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.SELL,
                                         market_type=MARKET_TYPE.STOCK_DAY, data_type=MARKETDATA_TYPE.DAY,
                                         broker_name=self.broker
                                         )
                    else:
                        event.send_order(account_id=self.account_cookie,
                                         amount=self.sell_available.get(item, 0), amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                         time=self.current_time, code=item, price=0,
                                         order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                         market_type=MARKET_TYPE.STOCK_DAY, data_type=MARKETDATA_TYPE.DAY,
                                         broker_name=self.broker)
