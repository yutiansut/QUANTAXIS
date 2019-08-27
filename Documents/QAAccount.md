
# QAACCOUNT 账户类

QA_Account() 是quantaxis的核心类, 其作用是一个可以使用规则兼容各种市场的账户类

1.3.0以后, QA_Account需要由组合来进行创建(推荐)

```python

user = QA.QA_user(username ='quantaxis', password = 'quantaxis')
portfotlio=user.new_portfolio('x1')
account = portfolio.new_account(args)
```

## 调用方式


```python
import QUANTAXIS as QA

user = QA.QA_User(username ='quantaxis', password = 'quantaxis')
portfolio=user.new_portfolio('x1')
account = portfolio.new_account(account_cookie='test')
```

     prortfolio with user_cookie  USER_MkAQWd3E  already exist!!
    

## 参数详解


```python
# strategy_name=None,
# user_cookie=None,
# portfolio_cookie=None,
# account_cookie=None,
# market_type=MARKET_TYPE.STOCK_CN,
# frequence=FREQUENCE.DAY,
# broker=BROKER_TYPE.BACKETEST,
# init_hold={},
# init_cash=1000000,
# commission_coeff=0.00025,
# tax_coeff=0.001,
# margin_level={},
# allow_t0=False,
# allow_sellopen=False,
# allow_margin=False,
# running_environment=RUNNING_ENVIRONMENT.BACKETEST
```

## 基于规则实例化

基于不同市场的不同规则, 我们可以实例化不同的账户类

- 允许保证金交易:  allow_marigin = True

- 允许买入后当日卖出: allow_t0 = True

- 允许卖空开仓(裸卖空): allow_sellopen= True

### 股票普通账户


```python
stock_account= portfolio.new_account(account_cookie ='stock',allow_t0=False,allow_margin=False,allow_sellopen=False,running_environment=QA.MARKET_TYPE.STOCK_CN)
```

###   股票融资融券账户


```python
rzrq_account = portfolio.new_account(account_cookie ='rzrq',allow_t0=False,allow_margin=True,allow_sellopen=True,running_environment=QA.MARKET_TYPE.STOCK_CN)
```

###  期货账户


```python
future_account = portfolio.new_account(account_cookie ='future',allow_t0=True,allow_margin=True,allow_sellopen=True, running_environment=QA.MARKET_TYPE.FUTURE_CN)
```

### 期权账户


```python
option_account = portfolio.new_account(account_cookie ='options',allow_t0=True,allow_margin=True,allow_sellopen=True, running_environment=QA.MARKET_TYPE.OPTION_CN)
```

###  其他市场账户



```python
xxx = portfolio.new_account(account_cookie ='self_market',allow_t0=True,allow_margin=True,allow_sellopen=True, running_environment=QA.MARKET_TYPE.CRYPTOCURRENCY)
```

## 账户的初始资金/初始仓位

默认账户是无仓位, 默认现金 1000000 RMB



```python
stock_account.init_assets
```




    {'cash': 1000000, 'hold': {}}




```python
stock_account.init_cash
```




    1000000




```python
stock_account.init_hold
```




    Series([], Name: amount, dtype: float64)



###   在实例化的时候初始化仓位信息

使用json/dict的格式初始化  

```python
# init_hold参数
init_hold={code1:amount1,code2:amount2}
```

实例化完 会显示在 account.hold中

[注意] 在t+1的账户中, 初始化仓位依然可以当日交易


```python
stock_account= portfolio.new_account(account_cookie ='stock_init',init_hold={'000001':500}, allow_t0=False,allow_margin=False,allow_sellopen=False,running_environment=QA.MARKET_TYPE.STOCK_CN)
```

    QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE
    QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE
    


```python
stock_account.init_assets
```




    {'cash': 1000000, 'hold': {'000001': 500}}




```python
stock_account.hold
```




    code
    000001    500
    Name: amount, dtype: int64




```python
stock_account.sell_available
```




    code
    000001    500
    Name: amount, dtype: int64



### 在实例化的时候初始现金信息

```python
# init_cash 参数
init_cash= 200000
```



```python
stock_account= portfolio.new_account(account_cookie ='stock_init',init_cash= 200000,init_hold={'000002':500}, allow_t0=False,allow_margin=False,allow_sellopen=False,running_environment=QA.MARKET_TYPE.STOCK_CN)
```


```python
stock_account.init_assets
```




    {'cash': 1000000, 'hold': {'000001': 500}}




```python
stock_account.init_cash
```




    1000000




```python
stock_account.cash
```




    [1000000]




```python
stock_account.cash_available
```




    1000000



### 在已经实例化的账户中修改现金/ 重置现金操作

此操作无法撤销

- 现金记录全部消除
- 账户的持仓不会消除




```python
stock_account.reset_assets(init_cash=50000)
```


```python
stock_account.init_assets
```




    {'cash': 50000, 'hold': {'000001': 500}}




```python
stock_account.cash
```




    [50000]




```python
stock_account.cash_available
```




    50000



##  买入/卖出操作

有2种方式可以买入/卖出品种

1. send_order 接口 + Order类调用receive_deal 接口
2. receive_simpledeal 接口


其中 
- 1 是基于账户-发出订单- 订单成交回报的模式更新账户
- 2 是直接修改账户的模式, 由用户自行确认和保证成交


###  订单/更新账户的模式

在此我们只演示订单/成交, 至于order.trade怎么成交, 则是市场类/broker类的问题, 在此不去演示

#### 生成订单


```python
order=stock_account.send_order(code='000001',amount=100,time='2019-01-19',
                         amount_model=QA.AMOUNT_MODEL.BY_AMOUNT,order_model=QA.ORDER_MODEL.CLOSE,
                         price=10,towards=QA.ORDER_DIRECTION.BUY)
```


```python
future_order=future_account.send_order(code='RB1905',amount=100,time='2019-01-19',
                         amount_model=QA.AMOUNT_MODEL.BY_AMOUNT,order_model=QA.ORDER_MODEL.CLOSE,
                         price=3500,towards=QA.ORDER_DIRECTION.BUY_OPEN)
```

#### 订单类 QA_Order


```python
order
```




    < QA_Order realorder_id Order_pDfHZMiC datetime:2019-01-19 09:31:00 code:000001 amount:100.0 price:10.0 towards:1 btype:stock_cn order_id:Order_pDfHZMiC account:stock_init status:queued >




```python
future_order
```




    < QA_Order realorder_id Order_JsqmjZHf datetime:2019-01-19 09:31:00 code:RB1905 amount:100.0 price:3500.0 towards:2 btype:stock_cn order_id:Order_JsqmjZHf account:future status:queued >



#### 订单交易(成交在Market/Broker中判断,此处只演示成交回报)


```python
order.trade(trade_price=10.1,trade_amount=100,trade_id='example_trade1',trade_time='2019-01-19 15:00:00')
```

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!receive deal
    


```python
future_order.trade(trade_price=3600,trade_amount=100,trade_id='example_trade2',trade_time='2019-01-19 21:00:00')
```

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!receive deal
    

#### 账户成交表  QA_Account.history/QA_Account.history_table


```python
stock_account.history_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datetime</th>
      <th>code</th>
      <th>price</th>
      <th>amount</th>
      <th>cash</th>
      <th>order_id</th>
      <th>realorder_id</th>
      <th>trade_id</th>
      <th>account_cookie</th>
      <th>commission</th>
      <th>tax</th>
      <th>message</th>
      <th>frozen</th>
      <th>direction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-01-19 15:00:00</td>
      <td>000001</td>
      <td>10.1</td>
      <td>100</td>
      <td>48985.0</td>
      <td>Order_pDfHZMiC</td>
      <td>Order_pDfHZMiC</td>
      <td>example_trade1</td>
      <td>stock_init</td>
      <td>5</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
future_account.history_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datetime</th>
      <th>code</th>
      <th>price</th>
      <th>amount</th>
      <th>cash</th>
      <th>order_id</th>
      <th>realorder_id</th>
      <th>trade_id</th>
      <th>account_cookie</th>
      <th>commission</th>
      <th>tax</th>
      <th>message</th>
      <th>frozen</th>
      <th>direction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-01-19 21:00:00</td>
      <td>RB1905</td>
      <td>3600.0</td>
      <td>100</td>
      <td>675919.0</td>
      <td>Order_JsqmjZHf</td>
      <td>Order_JsqmjZHf</td>
      <td>example_trade2</td>
      <td>future</td>
      <td>81.0</td>
      <td>0</td>
      <td>None</td>
      <td>324000.0</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



#### 账户现金表/ 期货账户还会冻结资金(保证金)


```python
stock_account.cash
```




    [50000, 48985.0]




```python
future_account.cash
```




    [1000000, 675919.0]




```python
future_account.frozen
```




    {'RB1905': {'2': {'money': 3240.0, 'amount': 100, 'avg_price': 3600.0},
      '-2': {'money': 0, 'amount': 0, 'avg_price': 0}}}



#### 账户可用现金


```python
stock_account.cash_available
```




    48985.0




```python
future_account.cash_available
```




    675919.0



#### 账户持仓


```python
stock_account.hold
```




    code
    000001    600
    Name: amount, dtype: int64




```python
future_account.hold
```




    code
    RB1905    100
    Name: amount, dtype: int64



#### 账户可卖余额(股票T+1 因此可卖部分不增加/ 期货账户 t+0 因此可卖部分增加)


```python
stock_account.sell_available
```




    code
    000001    500
    Name: amount, dtype: int64




```python
future_account.sell_available
```




    code
    RB1905    100
    Name: amount, dtype: int64



###    直接操作账户模式

该模式直接操作账户


```python
stock_account.receive_simpledeal(code='000004',order_id='model2',realorder_id='model2_real',trade_id='trade2',trade_amount=1000,trade_price=16,trade_time='2019-01-21',trade_towards=QA.ORDER_DIRECTION.BUY,message='model2')
```


```python
stock_account.history_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datetime</th>
      <th>code</th>
      <th>price</th>
      <th>amount</th>
      <th>cash</th>
      <th>order_id</th>
      <th>realorder_id</th>
      <th>trade_id</th>
      <th>account_cookie</th>
      <th>commission</th>
      <th>tax</th>
      <th>message</th>
      <th>frozen</th>
      <th>direction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-01-19 15:00:00</td>
      <td>000001</td>
      <td>10.1</td>
      <td>100</td>
      <td>48985.0</td>
      <td>Order_pDfHZMiC</td>
      <td>Order_pDfHZMiC</td>
      <td>example_trade1</td>
      <td>stock_init</td>
      <td>5</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-01-21</td>
      <td>000004</td>
      <td>16.0</td>
      <td>1000</td>
      <td>32980.0</td>
      <td>model2</td>
      <td>model2_real</td>
      <td>trade2</td>
      <td>stock_init</td>
      <td>5</td>
      <td>0</td>
      <td>model2</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
stock_account.cash
```




    [50000, 48985.0, 32980.0]




```python
stock_account.cash_available
```




    32980.0




```python
stock_account.hold
```




    code
    000001     600
    000004    1000
    Name: amount, dtype: int64




```python
stock_account.sell_available
```




    code
    000001    500
    Name: amount, dtype: int64



##   结算

主要是股票账户的可卖股数的结算

目前期货账户不采用逐日盯市的结算方式(及无结算价/无当日盈亏)


```python
stock_account.settle()
```


```python
stock_account.sell_available
```




    code
    000001     600
    000004    1000
    Name: amount, dtype: int64




```python
future_account.settle()
```


```python
##  关于账户存储和恢复
```

##       存储


```python
#stock_account.save()
```
