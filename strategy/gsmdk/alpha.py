# -*- coding: utf-8 -*-

from gmsdk.api import StrategyBase

class Mystrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(Mystrategy, self).__init__(*args, **kwargs)


    def on_login(self):
        pass

    def on_error(self, code, msg):
        pass

    def on_bar(self, bar):
        pass

    def on_execrpt(self, res):
        pass

    def on_order_status(self, order):
        pass

    def on_order_new(self, res):
        pass

    def on_order_filled(self, res):
        pass

    def on_order_partiall_filled(self, res):
        pass

    def on_order_stop_executed(self, res):
        pass

    def on_order_canceled(self, res):
        pass

    def on_order_cancel_rejected(self, res):
        pass


if __name__ == '__main__':
    myStrategy = Mystrategy(
        username='-',
        password='-',
        strategy_id='ffb98d74-fb5c-11e6-952a-e81132ed25bb',
        subscribe_symbols='CFFEX.IF1612.bar.15',
        mode=4,
        td_addr='localhost:8001'
    )
    myStrategy.backtest_config(
        start_time='2016-01-01 08:00:00',
        end_time='2016-12-31 23:55:00',
        initial_cash=100000,
        transaction_ratio=0.01,
        commission_ratio=0.0002,
        slippage_ratio=0.03,
        price_type=1)
    ret = myStrategy.run()
    print('exit code: ', ret)