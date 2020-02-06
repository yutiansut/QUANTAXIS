# 账户/组合/策略的说明 QAARP模块


<!-- TOC -->

- [账户/组合/策略的说明 QAARP模块](#账户组合策略的说明-qaarp模块)
    - [账户/组合/策略的关系](#账户组合策略的关系)
    - [创建自定义的策略](#创建自定义的策略)
    - [深入了解策略的组成](#深入了解策略的组成)
    - [风险分析模块](#风险分析模块)
    - [组合视角 PORTFOLIO VIEW](#组合视角-portfolio-view)

<!-- /TOC -->
@yutiansut

2018/1/26
    
在1.0版本以后,回测的策略是以继承账户类来进行的

![](http://pic.yutiansut.com/%E9%87%8D%E6%9E%84%E6%96%87%E6%A1%A3-%E8%B4%A6%E6%88%B7.png)

## 账户/组合/策略的关系
```json
{
  "User A":{
    "PortfolioA1":{
      "Account A" : "Strategy 1",
      "Account B" : "Strategy 2"
  },"Portfolio A2":{
      "Account C" : "Strategy 3"
  },
  "User B":{
    "Portfolio B1":{
      "Account D" : "Strategy 4"
    }
  }
}
```

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


## 创建自定义的策略


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


## 深入了解策略的组成


QA_Strategy 类完全继承 QA_Account, 因此,策略可以完全调用account类中的属性

```python

self.history # dict形式 账户的历史交易
self.history_table #pd.Dataframe 形式 账户的交易表
self.cash # list格式 账户的现金表
self.cash_table #pd.Dataframe 形式 账户的现金流量表
self.hold #账户的最新持仓 
self.latest_cash #账户的最近一次成功交易后的现金
self.trade # 账户的每日/分钟交易表
self.daily_cash # 账户的每日结算时的现金
self.daily_hold # 账户每日结算的持仓
self.current_time # 账户的当前时间

# 账户的on_bar事件
self.on_bar(self,event)

event 事件封装了数据和方法*(包括 所需的行情数据/下单接口)


```



## 风险分析模块

QA_Risk 是一个风险计算模块

```python
R=QA.QA_Risk(ACCOUNT,benchmark_code='000300',benchmark_type=MARKET_TYPE.INDEX_CN)

#< QA_RISK ANALYSIS ACCOUNT-Acc_50wle3cY >

R()
# R() 是一个datafram形式的表达结果
    account_cookie	annualize_return	max_dropback	portfolio_cookie	profit	time_gap	user_cookie	    volatility
0	Acc_50wle3cY	-0.000458	        0.00012     	Portfolio_oAkrKvj9	-0.000011	6	    USER_l1CeBXog	64.696986

R.message

{'account_cookie': 'Acc_50wle3cY',
 'annualize_return': -0.0004582372482384578,
 'max_dropback': 0.00012000168002352033,
 'portfolio_cookie': 'Portfolio_oAkrKvj9',
 'profit': -1.1000154002127616e-05,
 'time_gap': 6,
 'user_cookie': 'USER_l1CeBXog',
 'volatility': 64.69698601944299}

```


## 组合视角 PORTFOLIO VIEW

QA_PortfolioView 是一个组合视角,只要输入account列表,就可以生成一个视角

```python

# 如果从数据库中获取:
accounts=[QA.QA_Account().from_message(x) for x in QA.QA_fetch_account()]
# 中间可以对时间等进行筛选以后再放进来 或者对于持仓股票进行筛选

accounts=[QA_Account1,QA_Account2,....]
PV=QA.QA_PortfolioView(accounts)

```
PV可以直接被加载到QA_Risk模块中

```python
risk_pv=QA.QA_Risk(PV)

#calc result

risk.message
```

