# 账户/组合/策略的说明 QAARP模块


<!-- vscode-markdown-toc -->
* 1. [账户/组合/策略的关系](#)
* 2. [创建自定义的策略](#-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
@yutiansut
2018/1/26
在1.0版本以后,回测的策略是以继承账户类来进行的

##  1. <a name=''></a>账户/组合/策略的关系

{
  UserA:{
    PortfolioA1:{
      AccountA : Strategy1,
      AccountB : Strategy2
  },PortfolioA2:{
      AccountC : Strategy3
  }
  UserB:{
    PortfolioB1:{
      AccountD : Strategy4
    }
  }
}

```python

# 在这里我们展示如何创建一个组合/创建账户/增加已有账户
import QUANTAXIS as QA

# 创建用户
userA=QA.QA_User()

# 创建两个组合 A1,A2
PortfolioA1=userA.new_portfolio()
PortfolioA2=userA.new_portfolio()

# A1里面增加两个策略(新建)
strategy1=PortfolioA1.new_account()
strategy2=PortfolioA1.new_account()

# 打印user的组合
In []: userA.portfolio_list
Out[]:
{'Portfolio_WpsaoQY6': < QA_Portfolio Portfolio_WpsaoQY6 with 0 Accounts >,
 'Portfolio_w5uJvtf7': < QA_Portfolio Portfolio_w5uJvtf7 with 2 Accounts >}


# 打印组合A1
In []: PortfolioA1
Out[]:  < QA_Portfolio Portfolio_w5uJvtf7 with 2 Accounts >


# 打印策略 本质是Account类
In []: strategy1
Out[]: < QA_Account Acc_qHL6dSC4>


# 创建一个策略 自定义on_bar事件
class Strategy3(QA.QA_Strategy):
  def __init__(self):
    super().__init__()

  def on_bar(self,event):
    print(event)

# 实例化该策略到strategy3
In []: strategy3=Strategy3()

# 打印strategy3
In []: strategy3
Out[]: < QA_Account Acc_AZPD18vS>

# 把该策略加载到A2组合中
In []: PortfolioA2.add_account(strategy3)

# 打印A2
In []: PortfolioA2
Out[]: < QA_Portfolio Portfolio_w7sx5Q31 with 1 Accounts >

# 打印组合列表

In []: userA.portfolio_list
Out[]:
{'Portfolio_WpsaoQY6': < QA_Portfolio Portfolio_WpsaoQY6 with 1 Accounts >,
 'Portfolio_w5uJvtf7': < QA_Portfolio Portfolio_w5uJvtf7 with 2 Accounts >}



```


##  2. <a name='-1'></a>创建自定义的策略


```python
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE,
                                          FREQUENCE, ORDER_DIRECTION,
                                          ORDER_MODEL)
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info

class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN

    def on_bar(self, event):
        sellavailable=self.sell_available
        try:
            for item in event.market_data.code:
                if sellavailable is None:

                    event.send_order(account_cookie=self.account_cookie,
                                     amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker)

                else:
                    if sellavailable.get(item, 0) > 0:
                        event.send_order(account_cookie=self.account_cookie,
                                         amount=sellavailable[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
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


```