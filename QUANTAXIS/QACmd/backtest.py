# coding:utf-8
import random

import QUANTAXIS as QA


class strategy:
    """
    携带一个函数句柄
    """
    @classmethod
    def setting(self):
        pass

    @classmethod
    def predict(self, market, account, hold,info):
        """
        一个极其简单的示例策略,随机 随机真的随机
        """

        if hold == 0:
            __dat = random.random()
            if __dat > 0.5:
                return {'if_buy': 1, 'amount':'mean'}
            else:
                return {'if_buy': 0,'amount': 'mean'}
        else:
            __dat = random.random()
            if __dat > 0.5:
                return {'if_buy': 1,'amount': 'mean'}
            else:
                
                return {'if_buy': 0,'amount': 'all'}


d = QA.QA_Backtest()
#d.QA_backtest_import_setting()
d.QA_backtest_init()
d.QA_backtest_start(strategy())
