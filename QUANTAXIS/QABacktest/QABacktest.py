# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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


from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker

from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAARP.QAAccount import QA_Account



class QA_Backtest():
    """BACKTEST
    
    BACKTEST的主要目的:

    - 引入时间轴环境,获取全部的数据,然后按生成器将数据迭代插入回测的BROKER
        (这一个过程是模拟在真实情况中市场的时间变化和价格变化)

    - BROKER有了新数据以后 会通知MARKET交易前置,MARKET告知已经注册的所有的ACCOUNT 有新的市场数据

    - ACCOUNT 获取了新的市场函数,并将其插入他已有的数据中(update)

    - ACCOUNT 底下注册的策略STRATEGY根据新的市场函数,产生新的买卖判断,综合生成信号

    - 买卖判断通过交易前置发送给对应的BROKER,进行交易

    - BROKER发送SETTLE指令 结束这一个bar的所有交易,进行清算

    - 账户也进行清算,更新持仓,可卖,可用现金等

    - 迭代循环直至结束回测

    - 回测去计算这段时间的各个账户收益,并给出综合的最终结果

    """
    
    def __init__(self,market_type,start,end,commission_fee,):
        self.user=QA_User()
        self.user.session
        
 
