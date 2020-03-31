# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_future_day,
                                     QA_fetch_get_future_min,
                                     QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_min)
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAMarket.QADealer import QA_Dealer
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE


class QA_SimulatedBroker(QA_Broker):
    def __init__(self, *args, **kwargs):
        self.dealer = QA_Dealer()
        self.fetcher = {(MARKET_TYPE.STOCK_CN, FREQUENCE.DAY): QA_fetch_get_stock_day, (MARKET_TYPE.STOCK_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_stock_min,
                        (MARKET_TYPE.STOCK_CN, FREQUENCE.ONE_MIN): QA_fetch_get_stock_min, (MARKET_TYPE.STOCK_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_stock_min,
                        (MARKET_TYPE.STOCK_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_stock_min, (MARKET_TYPE.STOCK_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_stock_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.DAY): QA_fetch_get_index_day, (MARKET_TYPE.INDEX_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_index_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.ONE_MIN): QA_fetch_get_index_min, (MARKET_TYPE.INDEX_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_index_min,
                        (MARKET_TYPE.INDEX_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_index_min, (MARKET_TYPE.INDEX_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.DAY): QA_fetch_get_index_day, (MARKET_TYPE.FUND_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.ONE_MIN): QA_fetch_get_index_min, (MARKET_TYPE.FUND_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_index_min,
                        (MARKET_TYPE.FUND_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_index_min, (MARKET_TYPE.FUND_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_index_min}

    def get_market(self, order):
        try:
            data = self.fetcher[(order.market_type, order.frequence)](
                code=order.code, start=order.datetime, end=order.datetime).values[0]
            if 'vol' in data.keys() and 'volume' not in data.keys():
                data['volume'] = data['vol']
            elif 'vol' not in data.keys() and 'volume' in data.keys():
                data['vol'] = data['volume']
            return data
        except Exception as e:
            QA_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
            return None

    def receive_order(self, event):
        order = event.order

        if 'market_data' in event.__dict__.keys():
            self.market_data = self.get_market(
                order) if event.market_data is None else event.market_data
        else:
            self.market_data = self.get_market(order)

        order = self.warp(order)

        return self.dealer.deal(order, self.market_data)

    def query_data(self, code, start, end, frequence, market_type=None):
        """
        标准格式是numpy
        """
        try:
            return self.fetcher[(market_type, frequence)](
                code, start, end, frequence=frequence)
        except:
            pass
