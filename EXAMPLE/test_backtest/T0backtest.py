
# coding: utf-8

# In[1]:


from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE,
                                          FREQUENCE, ORDER_DIRECTION,
                                          ORDER_MODEL, RUNNING_ENVIRONMENT)


import random


# In[2]:


class MAMINT0Strategy(QA_Account):
    def __init__(self, user_cookie='default', portfolio_cookie='default', init_hold={'000001': 10000}):
        super().__init__(user_cookie, portfolio_cookie, init_hold=init_hold)
        self.account_cookie = 'T0BACKTEST'
        self.running_environment = RUNNING_ENVIRONMENT.TZERO
        self.frequence = FREQUENCE.ONE_MIN
        self.market_type = MARKET_TYPE.STOCK_CN

        self.result = {}

    def on_bar(self, event):

        # min5= self.market_data.min5
        # min15= self.market_data.min15

        # min5macd=QA.QA_indicator_MACD(min5)
        # min15macd=QA.QA_indicator_MACD(min15)
        # self.result['min5macd']=min5macd

        # self.cash_available # 当前剩余现金
        # self.sell_available # 当前可卖股票
        # self.history_table  # 当前的历史交易
        # self.hold_time      # 当前的持仓时间
        # self.hold_price     # 当前持仓的成本价格
        # self.get_orders     # 获取历史订单
        # self.allow_sellopen # 账户是否允许卖空
        # self.allow_t0       # 账户是否允许t0
        # self.commission_coeff  # 账户的手续费(可自行调整)

        try:
            for item in event.market_data.code:

                print('================')
                print(self.sell_available)
                print('================')
                print(self.hold_available)
                if self.sell_available.get(item, 0) > 0:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=self.sell_available[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
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


# In[3]:


from QUANTAXIS.QAARP.QARisk import QA_Risk
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAApplication.QABacktest import QA_Backtest
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE


class Backtest(QA_Backtest):
    '''
    多线程模式回测示例

    '''

    def __init__(self, market_type, frequence, start, end, code_list, commission_fee):
        super().__init__(market_type,  frequence, start, end, code_list, commission_fee)
        self.account = self.portfolio.add_account( MAMINT0Strategy(user_cookie=self.user.user_cookie, portfolio_cookie= self.portfolio.portfolio_cookie))

    def after_success(self):
        QA_util_log_info(self.account.history_table)
        risk = QA_Risk(self.account, benchmark_code='000300',
                       benchmark_type=MARKET_TYPE.INDEX_CN)

        print(risk().T)
        self.account.save()
        risk.save()
        risk.plot_assets_curve()
        print(risk.profit_construct)


# In[4]:


import QUANTAXIS as QA
backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
                    frequence=FREQUENCE.FIFTEEN_MIN,
                    start='2018-11-01',
                    end='2018-12-10',
                    code_list=['000001'],
                    commission_fee=0.00015)
backtest.start_market()

backtest.run()
backtest.stop()


# In[5]:


print(backtest.account.history_table)
