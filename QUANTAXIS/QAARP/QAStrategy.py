# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAUtil.QAParameter import (
    AMOUNT_MODEL,
    FREQUENCE,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_MODEL,
    AMOUNT_MODEL
)


class QA_Strategy(QA_Account):
    """account

    [description]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frequence = FREQUENCE.FIFTEEN_MIN
        self.market_type = MARKET_TYPE.STOCK_CN
        self._market_data = []
        self._subscribe_list = []

    def on_bar(self, event):
        try:
            for item in event.market_data.code:

                if self.sell_available.get(item, 0) > 0:
                    event.send_order(
                        account_cookie=self.account_cookie,
                        amount=self.sell_available[item],
                        amount_model=AMOUNT_MODEL.BY_AMOUNT,
                        time=self.current_time,
                        code=item,
                        price=0,
                        order_model=ORDER_MODEL.MARKET,
                        towards=ORDER_DIRECTION.SELL,
                        market_type=self.market_type,
                        frequence=self.frequence,
                        broker_name=self.broker
                    )
                else:
                    event.send_order(
                        account_cookie=self.account_cookie,
                        amount=100,
                        amount_model=AMOUNT_MODEL.BY_AMOUNT,
                        time=self.current_time,
                        code=item,
                        price=0,
                        order_model=ORDER_MODEL.MARKET,
                        towards=ORDER_DIRECTION.BUY,
                        market_type=self.market_type,
                        frequence=self.frequence,
                        broker_name=self.broker
                    )
        except:
            pass

    def subscribe(self, code):
        pass

    def unsubscribe(self, code):
        pass

    def buy(self, code, price, order):
        pass

    def sell(self):
        pass

    def buy_open(self):
        pass

    def sell_close(self):
        pass

    def sell_open(self):
        pass

    def buy_close(self):
        pass

    def settle(self):
        pass
