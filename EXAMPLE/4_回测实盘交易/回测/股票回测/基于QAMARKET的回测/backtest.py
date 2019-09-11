# coding=utf-8
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


from QUANTAXIS.QAARP.QARisk import QA_Risk
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAApplication.QABacktest import QA_Backtest
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE
from minstrategy import MAMINStrategy
from strategy import MAStrategy


class Backtest(QA_Backtest):
    '''
    多线程模式回测示例

    '''

    def __init__(self, market_type, frequence, start, end, code_list, commission_fee):
        super().__init__(market_type,  frequence, start, end, code_list, commission_fee)
        mastrategy = MAStrategy(user_cookie=self.user.user_cookie, portfolio_cookie= self.portfolio.portfolio_cookie, account_cookie= 'mastrategy')
        #maminstrategy = MAMINStrategy()
        self.account = self.portfolio.add_account(mastrategy)

    def after_success(self):
        QA_util_log_info(self.account.history_table)
        risk = QA_Risk(self.account, benchmark_code='000300',
                       benchmark_type=MARKET_TYPE.INDEX_CN)

        print(risk().T)
        fig=risk.plot_assets_curve()
        fig.show()
        fig=risk.plot_dailyhold()
        fig.show()
        fig=risk.plot_signal()
        fig.show()
        self.account.save()
        risk.save()


def run_daybacktest():
    import QUANTAXIS as QA
    backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
                        frequence=FREQUENCE.DAY,
                        start='2017-01-01',
                        end='2017-02-10',
                        code_list=QA.QA_fetch_stock_block_adv().code[0:5],
                        commission_fee=0.00015)
    print(backtest.account)
    backtest.start_market()

    backtest.run()
    backtest.stop()


def run_minbacktest():
    import QUANTAXIS as QA
    backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
                        frequence=FREQUENCE.FIFTEEN_MIN,
                        start='2017-11-01',
                        end='2017-11-10',
                        code_list=QA.QA_fetch_stock_block_adv().code[0:5],
                        commission_fee=0.00015)
    backtest.start_market()

    backtest.run()
    backtest.stop()


if __name__ == '__main__':
    run_daybacktest()
    #run_minbacktest()

