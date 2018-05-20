# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market


from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_random_with_topic
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, TRADE_STATUS


"""撮合类


输入是

self.market_data
self.order
rules

输出是

standard message

"""


class commission():
    if_buyside_commission = False
    if_sellside_commission = True
    if_commission = if_buyside_commission and if_sellside_commission


class dealer_preset():
    def __init__(self, market_type, *args, **kwargs):

        self.market_type = market_type
        self.if_price_limit = None  # 是否限制涨跌停(美股/加密货币不限制)
        self.if_commission = None  # 是否收手续费(部分合约/部分加密货币不收手续费)
        self.if_tax = None  # 是否收税
        self.if_t0 = None  # 是否t+0
        self.if_sellopen = None  # 是否允许卖空
        self.trading_time = None  # 交易时间
        self.commission_coeff = None  # 手续费比例
        self.tax_coeff = None  # 费率

    def load_preset(self):
        if self.market_type is MARKET_TYPE.STOCK_CN:
            self.if_price_limit = True  # 是否限制涨跌停(美股/加密货币不限制)
            self.if_commission = True  # 是否收手续费(部分合约/部分加密货币不收手续费)
            self.if_tax = True  # 是否收税
            self.if_t0 = False  # 是否t+0
            self.if_sellopen = False  # 是否允许卖空
            self.trading_time = [[930, 1130], [1300, 1500]]  # 交易时间
            self.commission_coeff = 0.00025  # 手续费比例
            self.tax_coeff = 0.001  # 费率
            return self
        elif self.market_type is MARKET_TYPE.FUTURE_CN:
            self.if_price_limit = True  # 是否限制涨跌停(美股/加密货币不限制)
            self.if_commission = True  # 是否收手续费(部分合约/部分加密货币不收手续费)
            self.if_tax = False  # 是否收税
            self.if_t0 = True  # 是否t+0
            self.if_sellopen = True  # 是否允许卖空
            self.trading_time = [[930, 1130], [1300, 1500]]  # 交易时间
            self.commission_coeff = 0.00025  # 手续费比例
            self.tax_coeff = 0  # 费率
        else:
            pass
        return self


class QA_Dealer():

    """[summary]


    对于不同的市场规则:
    股票市场 t+1
    期货/期权/加密货币市场 t+0

    股票/加密货币市场不允许卖空
    期货/期权市场允许卖空

    t+1的市场是
    当日的买入 更新持仓- 不更新可卖数量- 资金冻结
    当日的卖出 及时更新可用资金

    t+0市场是:
    当日买入 即时更新持仓和可卖
    当日卖出 即时更新

    卖空的规则是
    允许无仓位的时候卖出证券(按市值和保证金比例限制算)
    """

    def __init__(self, commission_fee_coeff=0.00025, tax_coeff=0.001, *args, **kwargs):
        self.commission_fee_coeff = commission_fee_coeff
        self.tax_coeff = tax_coeff
        self.deal_name = ''
        self.deal_engine = {'0x01': self.backtest_stock_dealer}
        self.session = {}
        self.order = None
        self.market_data = None
        self.commission_fee = None
        self.tax = None
        self.status = None

    def deal(self, order, market_data):
        self.order = order
        self.market_data = market_data
        self.deal_price = 0
        self.deal_amount = 0
        self.commission_fee_coeff=order.commission_coeff
        self.tax_coeff=order.tax_coeff
        if order.market_type == MARKET_TYPE.STOCK_CN:
            return self.backtest_stock_dealer()
    @property
    def callback_message(self):
        # 这是标准的return back message
        message = {
            'header': {
                'source': 'market',
                'status': self.status,
                'code': self.order.code,
                'session': {
                    'user': self.order.user,
                    'strategy': self.order.strategy,
                    'account': self.order.account_cookie
                },
                'order_id': self.order.order_id,
                'trade_id': QA_util_random_with_topic('Trade')
            },
            'body': {
                'order': {
                    'price': float("%.2f" % float(self.deal_price)),
                    'code': self.order.code,
                    'amount': self.deal_amount,
                    'date': self.order.date,
                    'datetime': self.order.datetime,
                    'towards': self.order.towards
                },
                # 'market': {
                #     'open': self.market_data.get('open'),
                #     'high': self.market_data.get('high'),
                #     'low': self.market_data.get('low'),
                #     'close': self.market_data.get('close'),
                #     'volume': self.market_data.get('volume'),
                #     'code': self.market_data.get('code')
                # },
                'fee': {
                    'commission': self.commission_fee,
                    'tax': self.tax
                }
            }
        }
        return message

    def cal_fee(self):
        if self.order.market_type == MARKET_TYPE.STOCK_CN:
            if int(self.order.towards) > 0:
                commission_fee = self.commission_fee_coeff * \
                    float(self.deal_price) * float(self.order.amount)
                self.commission_fee = 5 if commission_fee < 5 else commission_fee

                self.tax = 0  # 买入不收印花税
            else:
                commission_fee = self.commission_fee_coeff * \
                    float(self.deal_price) * float(self.order.amount)

                self.commission_fee = 5 if commission_fee < 5 else commission_fee

                self.tax = self.tax_coeff * \
                    float(self.deal_price) * float(self.order.amount)
        elif self.order.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制
            self.commission_fee = self.commission_fee_coeff * \
                float(self.deal_price) * float(self.order.amount)
            #self.commission_fee = 5 if commission_fee < 5 else commission_fee

            self.tax = 0  # 买入不收印花税

    def backtest_stock_dealer(self):
        # 新增一个__commission_fee_coeff 手续费系数
        """MARKET ENGINE STOCK

        在拿到市场数据后对于订单的撮合判断 生成成交信息


        trading system
        step1: check self.market_data
        step2: deal
        step3: return callback
        """
        try:
            if float(self.market_data.get('open')) == float(self.market_data.get('high')) == float(self.market_data.get('close')) == float(self.market_data.get('low')):

                self.status = TRADE_STATUS.PRICE_LIMIT
                self.deal_price = 0
                self.deal_amount = 0
                self.cal_fee()
                return self.callback_message
            elif ((float(self.order.price) < float(self.market_data.get('high')) and
                    float(self.order.price) > float(self.market_data.get('low'))) or
                    float(self.order.price) == float(self.market_data.get('low')) or
                    float(self.order.price) == float(self.market_data.get('high'))):
                '能成功交易的情况 有滑点调整'
                if float(self.order.amount) < float(self.market_data.get('volume')) * 100 / 16:
                    self.deal_price = self.order.price
                    self.deal_amount = self.order.amount
                elif float(self.order.amount) >= float(self.market_data.get('volume')) * 100 / 16 and \
                        float(self.order.amount) < float(self.market_data.get('volume')) * 100 / 8:
                    """
                    add some slippers

                    buy_price=mean(max{open,close},high)
                    sell_price=mean(min{open,close},low)
                    """
                    if int(self.order.towards) > 0:
                        self.deal_price = (max(float(self.market_data.get('open')), float(
                            self.market_data.get('close'))) + float(self.market_data.get('high'))) * 0.5
                    else:
                        self.deal_price = (min(float(self.market_data.get('open')), float(
                            self.market_data.get('close'))) + float(self.market_data.get('low'))) * 0.5
                    self.deal_amount = self.order.amount

                else:
                    self.deal_amount = float(self.market_data.get('volume')) / 8
                    if int(self.order.towards) > 0:
                        self.deal_price = float(self.market_data.get('high'))
                    else:
                        self.deal_price = float(self.market_data.get('low'))

                self.cal_fee()
                self.status = TRADE_STATUS.SUCCESS
                return self.callback_message
            else:
                self.status = TRADE_STATUS.FAILED
                self.deal_price = 0
                self.deal_amount = 0
                self.cal_fee()
                return self.callback_message

        except Exception as e:
            QA_util_log_info('MARKET ENGINE ERROR: {}'.format(e))
            self.status = TRADE_STATUS.NO_MARKET_DATA
            return self.callback_message



class Stock_Dealer(QA_Dealer):
    def __init__(self, *args, **kwargs):
        super().__init__()

if __name__ == '__main__':
    pass
