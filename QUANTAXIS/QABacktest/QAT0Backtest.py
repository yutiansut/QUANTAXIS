# coding:utf-8

from QUANTAXIS.QABacktest.QABacktest import QA_Backtest

"""
日内t0的回测框架

1. 给定每日初始的股票/现金
2. 核查每日可用股票,以及是否平仓(及如果尾盘没有买回去,要在结转的时候自动买回/卖出)
3. t0是搭载在股票市场上, 而且必须是分钟线(tick也可以)
4. t0不存在卖空,是先指定底仓
5. 限额限制(ACCOUNT的sell_available, 以及结算事件)
"""


class QAT0Backtest(QA_Backtest):

    def __init__(self, market_type, frequence, start, end, code_list, raw_holding, commission_fee):
        super().__init__(market_type, frequence, start, end, code_list, commission_fee)

        self.raw_holding = raw_holding  # 初始持仓

    def _settle(self):
        pass

    def start_market(self):
        """
        start the market thread and register backtest broker thread
        QAMarket 继承QATrader， QATrader 中有 trade_engine属性 ， trade_engine类型是QA_Engine从 QA_Thread继承
        """
        # 启动 trade_engine 线程
        self.market.start()

        # 注册 backtest_broker ，并且启动和它关联线程QAThread 存放在 kernels 词典中， { 'broker_name': QAThread }
        self.market.register(self.broker_name, self.broker)

        # 通过 broke名字 新建立一个 QAAccount 放在的中 session字典中 session 是 { 'cookie' , QAAccount }
        self.market.login(self.broker_name,
                          self.account.account_cookie, self.account)

        # 账户初始化
        # t0 需要初始化账户(股票/现金)

        self.account.hold
