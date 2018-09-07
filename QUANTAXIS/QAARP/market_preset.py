#


class MARKET_PRESET:

    def __init__(self):
        pass

    # 手续费比例
    def get_commission_coeff(self, code, dtype):
        pass

    # 印花税系数
    def get_tax_coeff(self, code, dtype):
        pass

    # 交易时间
    def get_trade_time(self, code, dtype):
        pass

    # 交易日期
    def get_trade_day(self, code, dtype):
        pass

    # 交易规则( t0/sell_open)
    def get_trade_rules(self, code, dtypes):
        pass

    # 交易杠杆
    def get_trade_margin(self, code, dtypes):
        pass
