# utf-8
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import AMOUNT_MODEL,ORDER_DIRECTION,ORDER_MODEL,MARKET_TYPE,MARKETDATA_TYPE


class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()

    def on_bar(self,event):
        #print(self.market_data)        
        if self.market_data.len>1:
            for item in event.market_data.code:
                event.send_order(account_id=self.account_cookie,
                    amount=1000, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                    time=self.current_time, code=item, price=0,
                    order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                    market_type=MARKET_TYPE.STOCK_DAY, data_type=MARKETDATA_TYPE.DAY,
                    broker_name=self.broker
                )
        

