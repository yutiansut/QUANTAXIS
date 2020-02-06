

```python
import QUANTAXIS as QA
```

    QUANTAXIS>> start QUANTAXIS
    QUANTAXIS>> Selecting the Best Server IP of TDX
    

    Bad REPSONSE 60.28.29.69
    Bad REPSONSE 180.153.18.17
    Bad REPSONSE 59.173.18.69
    Bad REPSONSE 61.153.144.179
    

    QUANTAXIS>> === The BEST SERVER ===
     stock_ip 60.191.117.167 future_ip 58.246.109.27
    QUANTAXIS>> Welcome to QUANTAXIS, the Version is 1.0.30
    QUANTAXIS>>  
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
      ``########`````##````````##``````````##`````````####````````##```##########````````#``````##``````###```##`````######`` 
      `##``````## ```##````````##`````````####````````##`##```````##```````##```````````###``````##````##`````##```##`````##` 
      ##````````##```##````````##````````##`##````````##``##``````##```````##``````````####```````#```##``````##```##``````## 
      ##````````##```##````````##```````##```##```````##```##`````##```````##`````````##`##```````##`##```````##````##``````` 
      ##````````##```##````````##``````##`````##``````##````##````##```````##````````##``###```````###````````##`````##`````` 
      ##````````##```##````````##``````##``````##`````##`````##```##```````##```````##````##```````###````````##``````###```` 
      ##````````##```##````````##`````##````````##````##``````##``##```````##``````##``````##`````##`##```````##````````##``` 
      ##````````##```##````````##````#############````##```````##`##```````##`````###########`````##``##``````##`````````##`` 
      ###```````##```##````````##```##```````````##```##```````##`##```````##````##`````````##```##```##``````##```##`````##` 
      `##``````###````##``````###``##`````````````##``##````````####```````##```##``````````##``###````##`````##````##`````## 
      ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````###``### 
      ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````##`` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
      ``````````````````````````Copyright``yutiansut``2017``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     
    

# 在这里我们演示一下 下单/交易/结算的整个流程

我们首先会建立一个账户类和一个回测类



```python
 # 初始化一个account
Account=QA.QA_Account()

# 初始化一个回测类
B = QA.QA_BacktestBroker()

```

在第一天的时候,全仓买入 000001


```python
# 全仓买入'000001'

Order=Account.send_order(code='000001',
                        price=11,
                        money=Account.cash_available,
                        time='2018-05-09',
                        towards=QA.ORDER_DIRECTION.BUY,
                        order_model=QA.ORDER_MODEL.MARKET,
                        amount_model=QA.AMOUNT_MODEL.BY_MONEY
                        )



```


```python

## 打印order的占用资金
print('ORDER的占用资金: {}'.format((Order.amount*Order.price)*(1+Account.commission_coeff)))
```

    ORDER的占用资金: 999049.7000000001
    


```python
# 账户剩余资金
print('账户剩余资金 :{}'.format(Account.cash_available))
```

    账户剩余资金 :950.2999999999302
    

此时的账户cash并未减少,因为此过程为申报订单(已委托 未成交状态)

回测类接受订单,并返回撮合结果


```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
print(rec_mes)
```

    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': None, 'strategy': None, 'account': 'Acc_b6DI7PfB'}, 'order_id': 'Order_kOhmiyR9', 'trade_id': 'Trade_7A4Y2wG6'}, 'body': {'order': {'price': 10.96, 'code': '000001', 'amount': 90800, 'date': '2018-05-09', 'datetime': '2018-05-09 09:30:00', 'towards': 1}, 'market': {'open': 10.98, 'high': 11.03, 'low': 10.88, 'close': 10.97, 'volume': 627656.0, 'code': '000001'}, 'fee': {'commission': 1492.071, 'tax': 0}}}
    

账户类接收到回测返回的回报信息,更新账户


```python
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_b6DI7PfB',
     'portfolio_cookie': None,
     'user_cookie': None,
     'broker': 'backtest',
     'market_type': 'stock_cn',
     'strategy_name': None,
     'current_time': None,
     'allow_sellopen': False,
     'allow_t0': False,
     'margin_level': False,
     'init_assets': 1000000,
     'cash': [1000000, 3339.9289999998837],
     'history': [['2018-05-09 09:30:00',
       '000001',
       10.96,
       90800.0,
       'Order_kOhmiyR9',
       'Trade_7A4Y2wG6',
       'Acc_b6DI7PfB',
       1492.071,
       0.0]],
     'trade_index': ['2018-05-09 09:30:00'],
     'running_time': datetime.datetime(2018, 5, 14, 23, 24, 46, 518098)}



此时我们可以打印一下现在的状态(现在的状态可以理解为在交易时 买入一只000001股票,但当天尚未收盘)


```python
print('账户的可用资金 {}'.format(Account.cash_available))
```

    账户的可用资金 3339.9289999998837
    

我们注意到 当最初申报订单的时候,可用资金只有950.2999999999302元,而买入成功后,可用资金有3339.9289999998837元,原因是下单的时候模式是市价单模式(QA.ORDER_MODEL.MARKET),故实际成交金额为10.96元

买入以后 账户的持仓为90800股 000001


```python
Account.hold
```




    code
    000001    90800.0
    Name: amount, dtype: float64



买入后账户现金表被扩展


```python
Account.cash
```




    [1000000, 3339.9289999998837]



因为是t+1的A股市场,故此时可卖数量为0


```python
Account.sell_available
```




    {}



# 执行结算


```python
Account.settle()
```

# 结算后


```python
Account.cash
```




    [1000000, 3339.9289999998837]




```python
Account.cash_available
```




    3339.9289999998837




```python
Account.sell_available
```




    code
    000001    90800.0
    Name: amount, dtype: float64




```python
Account.hold
```




    code
    000001    90800.0
    Name: amount, dtype: float64



# 执行卖出操作

现在的持仓为: 000001 90800股


```python
holdnum=Account.sell_available.get('000001',0)
```


```python
holdnum
```




    90800.0



申报一个卖出单,把可卖全部卖出


```python
Order=Account.send_order(code='000001',
                        price=11,
                        amount=holdnum,
                        time='2018-05-10',
                        towards=QA.ORDER_DIRECTION.SELL,
                        order_model=QA.ORDER_MODEL.MARKET,
                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )

```


```python
Order
```




    < QA_Order datetime:2018-05-10 09:31:00 code:000001 price:11 towards:-1 btype:stock_cn order_id:Order_4nV1lmEp account:Acc_b6DI7PfB status:100 >




```python
Account.cash_available  # 因为此时订单尚未申报成功 可用现金不变
```




    3339.9289999998837




```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
print(rec_mes)
```

    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': None, 'strategy': None, 'account': 'Acc_b6DI7PfB'}, 'order_id': 'Order_4nV1lmEp', 'trade_id': 'Trade_RZ7KDGbE'}, 'body': {'order': {'price': 11.0, 'code': '000001', 'amount': 90800, 'date': '2018-05-10', 'datetime': '2018-05-10 09:30:00', 'towards': -1}, 'market': {'open': 11.03, 'high': 11.09, 'low': 10.91, 'close': 11.01, 'volume': 552735.0, 'code': '000001'}, 'fee': {'commission': 1498.2, 'tax': 998.8}}}
    


```python
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_b6DI7PfB',
     'portfolio_cookie': None,
     'user_cookie': None,
     'broker': 'backtest',
     'market_type': 'stock_cn',
     'strategy_name': None,
     'current_time': None,
     'allow_sellopen': False,
     'allow_t0': False,
     'margin_level': False,
     'init_assets': 1000000,
     'cash': [1000000, 3339.9289999998837, 1000641.7289999999],
     'history': [['2018-05-09 09:30:00',
       '000001',
       10.96,
       90800.0,
       'Order_kOhmiyR9',
       'Trade_7A4Y2wG6',
       'Acc_b6DI7PfB',
       1492.071,
       0.0],
      ['2018-05-10 09:30:00',
       '000001',
       11.0,
       -90800.0,
       'Order_4nV1lmEp',
       'Trade_RZ7KDGbE',
       'Acc_b6DI7PfB',
       1498.2,
       998.8]],
     'trade_index': ['2018-05-09 09:30:00', '2018-05-10 09:30:00'],
     'running_time': datetime.datetime(2018, 5, 14, 23, 24, 46, 640769)}




```python
Account.cash_available # 此时订单已成交 cash_available立刻结转
```




    1000641.7289999999


