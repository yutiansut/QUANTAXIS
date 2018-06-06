

```python
import QUANTAXIS as QA
```

    QUANTAXIS>> start QUANTAXIS
    QUANTAXIS>> Welcome to QUANTAXIS, the Version is 1.0.46
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
      ``````````````````````````Copyright``yutiansut``2018``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` 
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

    账户剩余资金 :0
    

此时的账户cash并未减少,因为此过程为申报订单(已委托 未成交状态)

回测类接受订单,并返回撮合结果


```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
print(rec_mes)
```

    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': None, 'strategy': None, 'account': 'Acc_fSyZbDFk'}, 'order_id': 'Order_aVQ0MYie', 'trade_id': 'Trade_iGenJ6wM'}, 'body': {'order': {'price': 10.96, 'code': '000001', 'amount': 90800, 'date': '2018-05-09', 'datetime': '2018-05-09 09:30:00', 'towards': 1}, 'fee': {'commission': 248.67849999999999, 'tax': 0}}}
    

账户类接收到回测返回的回报信息,更新账户


```python
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_fSyZbDFk',
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
     'commission_coeff': 0.00025,
     'tax_coeff': 0.0015,
     'cash': [1000000, 4583.321499999845],
     'history': [['2018-05-09 09:30:00',
       '000001',
       10.96,
       90800.0,
       'Order_aVQ0MYie',
       'Trade_iGenJ6wM',
       'Acc_fSyZbDFk',
       248.67849999999999,
       0.0]],
     'trade_index': ['2018-05-09 09:30:00'],
     'running_time': datetime.datetime(2018, 6, 6, 13, 52, 16, 692993)}



此时我们可以打印一下现在的状态(现在的状态可以理解为在交易时 买入一只000001股票,但当天尚未收盘)


```python
print('账户的可用资金 {}'.format(Account.cash_available))
```

    账户的可用资金 4583.321499999845
    

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




    [1000000, 4583.321499999845]



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




    [1000000, 4583.321499999845]




```python
Account.cash_available
```




    4583.321499999845




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




    < QA_Order datetime:2018-05-10 09:31:00 code:000001 amount:90800.0 price:11 towards:-1 btype:stock_cn order_id:Order_YPtDn4sI account:Acc_fSyZbDFk status:300 >




```python
Account.cash_available  # 因为此时订单尚未申报成功 可用现金不变
```




    4583.321499999845




```python
rec_mes=B.receive_order(QA.QA_Event(order=Order))
print(rec_mes)
```

    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': None, 'strategy': None, 'account': 'Acc_fSyZbDFk'}, 'order_id': 'Order_YPtDn4sI', 'trade_id': 'Trade_CfR4JzXB'}, 'body': {'order': {'price': 11.0, 'code': '000001', 'amount': 90800.0, 'date': '2018-05-10', 'datetime': '2018-05-10 09:30:00', 'towards': -1}, 'fee': {'commission': 249.7, 'tax': 1498.2}}}
    


```python
Account.receive_deal(rec_mes)
```




    {'source': 'account',
     'account_cookie': 'Acc_fSyZbDFk',
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
     'commission_coeff': 0.00025,
     'tax_coeff': 0.0015,
     'cash': [1000000, 4583.321499999845, 1001635.4214999999],
     'history': [['2018-05-09 09:30:00',
       '000001',
       10.96,
       90800.0,
       'Order_aVQ0MYie',
       'Trade_iGenJ6wM',
       'Acc_fSyZbDFk',
       248.67849999999999,
       0.0],
      ['2018-05-10 09:30:00',
       '000001',
       11.0,
       -90800.0,
       'Order_YPtDn4sI',
       'Trade_CfR4JzXB',
       'Acc_fSyZbDFk',
       249.7,
       1498.2]],
     'trade_index': ['2018-05-09 09:30:00', '2018-05-10 09:30:00'],
     'running_time': datetime.datetime(2018, 6, 6, 13, 52, 16, 856556)}




```python
Account.cash_available # 此时订单已成交 cash_available立刻结转
```




    1001635.4214999999




```python
Account.history_table
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
      <th>order_id</th>
      <th>trade_id</th>
      <th>account_cookie</th>
      <th>commission</th>
      <th>tax</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-05-09 09:30:00</td>
      <td>000001</td>
      <td>10.96</td>
      <td>90800.0</td>
      <td>Order_aVQ0MYie</td>
      <td>Trade_iGenJ6wM</td>
      <td>Acc_fSyZbDFk</td>
      <td>248.6785</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-05-10 09:30:00</td>
      <td>000001</td>
      <td>11.00</td>
      <td>-90800.0</td>
      <td>Order_YPtDn4sI</td>
      <td>Trade_CfR4JzXB</td>
      <td>Acc_fSyZbDFk</td>
      <td>249.7000</td>
      <td>1498.2</td>
    </tr>
  </tbody>
</table>
</div>




```python
Account.orders
```




    < QA_OrderQueue AMOUNT 2 WAITING TRADE 2 >




```python
Account.orders.queue_df.query('date=="2018-05-09"')
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
      <th>account_cookie</th>
      <th>amount</th>
      <th>amount_model</th>
      <th>callback</th>
      <th>code</th>
      <th>commission_coeff</th>
      <th>date</th>
      <th>datetime</th>
      <th>frequence</th>
      <th>market_type</th>
      <th>...</th>
      <th>price</th>
      <th>sending_time</th>
      <th>status</th>
      <th>strategy</th>
      <th>tax_coeff</th>
      <th>towards</th>
      <th>trade_id</th>
      <th>transact_time</th>
      <th>type</th>
      <th>user</th>
    </tr>
    <tr>
      <th>order_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Order_aVQ0MYie</th>
      <td>Acc_fSyZbDFk</td>
      <td>90800.0</td>
      <td>by_money</td>
      <td>&lt;bound method QA_Account.receive_deal of &lt; QA_...</td>
      <td>000001</td>
      <td>0.00025</td>
      <td>2018-05-09</td>
      <td>2018-05-09 09:31:00</td>
      <td>day</td>
      <td>stock_cn</td>
      <td>...</td>
      <td>11</td>
      <td>2018-05-09 09:31:00</td>
      <td>300</td>
      <td>None</td>
      <td>0.0015</td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>stock_cn</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 23 columns</p>
</div>


