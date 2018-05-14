

```python
import QUANTAXIS as QA
```

    QUANTAXIS>> start QUANTAXIS
    QUANTAXIS>> Selecting the Best Server IP of TDX
    

    Bad REPSONSE 60.28.29.69
    Bad REPSONSE 180.153.18.17
    Bad REPSONSE 59.173.18.69
    Bad REPSONSE 61.153.144.179
    Bad REPSONSE 112.74.214.43
    

    QUANTAXIS>> === The BEST SERVER ===
     stock_ip 60.191.117.167 future_ip 58.246.109.27
    QUANTAXIS>> Welcome to QUANTAXIS, the Version is 1.0.29
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
     
    


```python
 # 初始化一个account
Account=QA.QA_Account()

# 全仓买入'000001'

Order=Account.send_order(code='000001',
                        price=11,
                        money=Account.cash_available,
                        time='2018-05-09',
                        towards=QA.ORDER_DIRECTION.BUY,
                        order_model=QA.ORDER_MODEL.MARKET,
                        amount_model=QA.AMOUNT_MODEL.BY_MONEY
                        )

B = QA.QA_BacktestBroker()
# 打印剩余资金
Account.cash_available


```




    950.2999999999302




```python

## 打印order的占用资金
(Order.amount*Order.price)*(1+Account.commission_coeff)


```




    999049.7000000001




```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
print(rec_mes)
```

    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': None, 'strategy': None, 'account': 'Acc_752ProBV'}, 'order_id': 'Order_92MKxE3r', 'trade_id': 'Trade_ueLUNTrP'}, 'body': {'order': {'price': 10.96, 'code': '000001', 'amount': 90800, 'date': '2018-05-09', 'datetime': '2018-05-09 09:30:00', 'towards': 1}, 'market': {'open': 10.98, 'high': 11.03, 'low': 10.88, 'close': 10.97, 'volume': 627656.0, 'code': '000001'}, 'fee': {'commission': 1492.071, 'tax': 0}}}
    


```python
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_752ProBV',
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
       'Order_92MKxE3r',
       'Trade_ueLUNTrP',
       'Acc_752ProBV',
       1492.071,
       0.0]],
     'trade_index': ['2018-05-09 09:30:00'],
     'running_time': datetime.datetime(2018, 5, 14, 22, 47, 1, 389009)}




```python
Account.cash_available
```




    3339.9289999998837




```python
Account.hold
```




    code
    000001    90800.0
    Name: amount, dtype: float64




```python
Account.cash
```




    [1000000, 3339.9289999998837]




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


```python
holdnum=Account.sell_available.get('000001',0)
```


```python
holdnum
```




    90800.0




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




    < QA_Order datetime:2018-05-10 09:31:00 code:000001 price:11 towards:-1 btype:stock_cn order_id:Order_IPhjq294 account:Acc_752ProBV status:100 >




```python
Account.cash_available  # 因为此时订单尚未申报成功 可用现金不变
```




    3339.9289999998837




```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_752ProBV',
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
       'Order_92MKxE3r',
       'Trade_ueLUNTrP',
       'Acc_752ProBV',
       1492.071,
       0.0],
      ['2018-05-10 09:30:00',
       '000001',
       11.0,
       -90800.0,
       'Order_IPhjq294',
       'Trade_sQxT2qcB',
       'Acc_752ProBV',
       1498.2,
       998.8]],
     'trade_index': ['2018-05-09 09:30:00', '2018-05-10 09:30:00'],
     'running_time': datetime.datetime(2018, 5, 14, 22, 47, 1, 515670)}




```python
Account.cash_available # 此时订单已成交 cash_available立刻结转
```




    1000641.7289999999


