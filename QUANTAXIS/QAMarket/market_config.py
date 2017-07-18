#coding:utf-8
from .QAMarket_advance import QA_Market
class stock_market(QA_Market):
    # 设置交易细节

    #
    #self.init()
    
    # 手续费 Commission
    # 买卖规则  双向市场 平仓优先、时间优先（closing out position and time priority）
    # 返回code
    # 保证金（Margin） 初始保证金（Initial Margin）维持保证金(Maintenance Margin)
    # 结算价
    # 数据级别
    # 最小变动价位（Minimum Price Movement）
    # 每日价格最大波动限制(Daily Price Limit) 10%
    
    def init(self):
        pass
    
class future_market():
    def init(self):
        pass


class HK_stock_market():
    pass
class US_stock_market():
    pass