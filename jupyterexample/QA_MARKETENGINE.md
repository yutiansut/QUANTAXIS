

```python
import QUANTAXIS as QA
import threading
```

    QUANTAXIS>> start QUANTAXIS
    QUANTAXIS>> ip:127.0.0.1,port:27017
    QUANTAXIS>> Selecting the Best Server IP of TDX
    QUANTAXIS>> === The BEST SERVER ===
     stock_ip 115.238.90.165 future_ip 61.152.107.141
    QUANTAXIS>> Welcome to QUANTAXIS, the Version is remake-version
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
      ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````##````## 
      ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````####` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
      ``````````````````````````Copyright``yutiansut``2017``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     
    


```python
user = QA.QA_Portfolio()
# 创建两个account
#这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
#然后返回的是这个账户的id
a_1 = user.new_account()
a_2 = user.new_account()

```


```python
a_1
```




    'Acc_DasXt8cC'




```python
"""
然后这里 是创建一个交易前置  你可以理解成 创建了一个无界面的通达信客户端
然后start()开启这个客户端
连接到backtest的broker上 这个broker可以更换
"""
# 创建一个交易前置
market = QA.QA_Market()
# 交易前置连接broker 
market.start()
market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)

# 打印market
print(market)


```

    < QA_MARKET with ['backtest'] Broker >
    


```python
#线程里面 开启了一个broker的线程 
threading.enumerate()
```




    [<_MainThread(MainThread, started 13012)>,
     <Thread(Thread-4, started daemon 21380)>,
     <Heartbeat(Thread-5, started daemon 15080)>,
     <HistorySavingThread(IPythonHistorySavingThread, started 3348)>,
     <ParentPollerWindows(Thread-3, started daemon 20444)>,
     <Thread(pymongo_server_monitor_thread, started daemon 21476)>,
     <Thread(pymongo_kill_cursors_thread, started daemon 8648)>,
      <QA_ENGINE with ['backtest'] kernals>,
     < QA_Thread backtest >]




```python
# 再连接一个模拟盘的BROKER
market.connect(QA.RUNNING_ENVIRONMENT.SIMULATION)
```




    True




```python
"""
然后我们假设又连进了模拟盘 看到这时候引擎里面有两个broker了
好比是通达信连了实盘又连了模拟盘
"""
threading.enumerate()
```




    [<_MainThread(MainThread, started 13012)>,
     <Thread(Thread-4, started daemon 21380)>,
     <Heartbeat(Thread-5, started daemon 15080)>,
     <HistorySavingThread(IPythonHistorySavingThread, started 3348)>,
     <ParentPollerWindows(Thread-3, started daemon 20444)>,
     <Thread(pymongo_server_monitor_thread, started daemon 21476)>,
     <Thread(pymongo_kill_cursors_thread, started daemon 8648)>,
      <QA_ENGINE with ['backtest', 'simulation'] kernals>,
     < QA_Thread backtest >,
     < QA_Thread simulation >]




```python
"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易
market.login(a_1,QA.BROKER_TYPE.BACKETEST)
market.login(a_2,QA.BROKER_TYPE.BACKETEST)
# 打印市场中的交易账户
print(market.get_account_id())


```

    ['Acc_DasXt8cC', 'Acc_GQ3hu9d5']
    


```python
#然后这里 往交易前置里面添加订单 这个操作是异步的
```


```python
#这两个是 每个账户都下了单
```


```python
market.insert_order(account_id=a_1, amount=100000,price=None, amount_model=QA.AMOUNT_MODEL.BY_PRICE,time='2017-12-14', code='000001', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_DAY,
                   data_type=QA.MARKETDATA_TYPE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)
```

    < QA_Order datetime:2017-12-14 09:31:00 code:000001 price:13.0 towards:1 btype:0x01 order_id:Order_L5gj0sUo account:Acc_DasXt8cC status:300 >
    


```python
market.insert_order(account_id=a_2, amount=100000,price=None, amount_model=QA.AMOUNT_MODEL.BY_PRICE,time='2017-12-14', code='000001', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_DAY,
                   data_type=QA.MARKETDATA_TYPE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)
```

    < QA_Order datetime:2017-12-14 09:31:00 code:000001 price:13.0 towards:1 btype:0x01 order_id:Order_26WY3Nmp account:Acc_GQ3hu9d5 status:300 >
    


```python
#
"""
下单以后 现金不会减少 但是可用现金会被扣除
因为如果是市价单 你的成交价未定
没法直接减少现金
可用现金减少 cash不减少 等到settle 等到成功交易的时候 才会扣cash

"""
```




    '\n下单以后 现金不会减少 但是可用现金会被扣除\n因为如果是市价单 你的成交价未定\n没法直接减少现金\n可用现金减少 cash不减少 等到settle 等到成功交易的时候 才会扣cash\n\n'




```python
market.session[a_1].cash_available
```




    900000




```python
market.session[a_1].cash
```




    [1000000]




```python
"""
这里是交易前置内部的订单队列
"""
market.order_handler.order_queue()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>account_cookie</th>
      <th>amount</th>
      <th>amount_model</th>
      <th>code</th>
      <th>data_type</th>
      <th>date</th>
      <th>datetime</th>
      <th>market_type</th>
      <th>order_id</th>
      <th>order_model</th>
      <th>price</th>
      <th>sending_time</th>
      <th>status</th>
      <th>strategy</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Order_L5gj0sUo</th>
      <td>Acc_DasXt8cC</td>
      <td>100000</td>
      <td>by_price</td>
      <td>000001</td>
      <td>day</td>
      <td>2017-12-14</td>
      <td>2017-12-14 09:31:00</td>
      <td>0x01</td>
      <td>Order_L5gj0sUo</td>
      <td>close</td>
      <td>13.0</td>
      <td>2017-12-14 09:31:00</td>
      <td>300</td>
      <td></td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>0x01</td>
      <td></td>
    </tr>
    <tr>
      <th>Order_26WY3Nmp</th>
      <td>Acc_GQ3hu9d5</td>
      <td>100000</td>
      <td>by_price</td>
      <td>000001</td>
      <td>day</td>
      <td>2017-12-14</td>
      <td>2017-12-14 09:31:00</td>
      <td>0x01</td>
      <td>Order_26WY3Nmp</td>
      <td>close</td>
      <td>13.0</td>
      <td>2017-12-14 09:31:00</td>
      <td>300</td>
      <td></td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>0x01</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
market.order_handler.order_queue.trade_list
```




    [< QA_Order datetime:2017-12-14 09:31:00 code:000001 price:13.0 towards:1 btype:0x01 order_id:Order_L5gj0sUo account:Acc_DasXt8cC status:100 >,
     < QA_Order datetime:2017-12-14 09:31:00 code:000001 price:13.0 towards:1 btype:0x01 order_id:Order_26WY3Nmp account:Acc_GQ3hu9d5 status:100 >]




```python
#pending 是指的待成交列表
market.order_handler.order_queue.pending
```




<div>


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>account_cookie</th>
      <th>amount</th>
      <th>amount_model</th>
      <th>code</th>
      <th>data_type</th>
      <th>date</th>
      <th>datetime</th>
      <th>market_type</th>
      <th>order_id</th>
      <th>order_model</th>
      <th>price</th>
      <th>sending_time</th>
      <th>status</th>
      <th>strategy</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Order_L5gj0sUo</th>
      <td>Acc_DasXt8cC</td>
      <td>100000</td>
      <td>by_price</td>
      <td>000001</td>
      <td>day</td>
      <td>2017-12-14</td>
      <td>2017-12-14 09:31:00</td>
      <td>0x01</td>
      <td>Order_L5gj0sUo</td>
      <td>close</td>
      <td>13.0</td>
      <td>2017-12-14 09:31:00</td>
      <td>300</td>
      <td></td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>0x01</td>
      <td></td>
    </tr>
    <tr>
      <th>Order_26WY3Nmp</th>
      <td>Acc_GQ3hu9d5</td>
      <td>100000</td>
      <td>by_price</td>
      <td>000001</td>
      <td>day</td>
      <td>2017-12-14</td>
      <td>2017-12-14 09:31:00</td>
      <td>0x01</td>
      <td>Order_26WY3Nmp</td>
      <td>close</td>
      <td>13.0</td>
      <td>2017-12-14 09:31:00</td>
      <td>300</td>
      <td></td>
      <td>1</td>
      <td>None</td>
      <td>None</td>
      <td>0x01</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
"""
这个_trade是一个私有方法 只有模拟盘和回测才会有 实盘就是真的交易了 
这个_trade是backtest类去调用的

"""
market._trade(QA.BROKER_TYPE.BACKETEST)
```

    QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 1 tasks to do
    

    ON TRADE
    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': '', 'strategy': '', 'account': 'Acc_DasXt8cC'}, 'order_id': 'Order_L5gj0sUo', 'trade_id': 'Trade_PyBjheit'}, 'body': {'order': {'price': 13.0, 'code': '000001', 'amount': 7600, 'date': '2017-12-14', 'datetime': '2017-12-14 09:31:00', 'towards': 1}, 'market': {'open': 13.15, 'high': 13.31, 'low': 12.91, 'close': 13.0, 'volume': 1001997.0, 'code': '000001'}, 'fee': {'commission': 148.2, 'tax': 0}}}
    ON TRADE
    {'header': {'source': 'market', 'status': 200, 'code': '000001', 'session': {'user': '', 'strategy': '', 'account': 'Acc_GQ3hu9d5'}, 'order_id': 'Order_26WY3Nmp', 'trade_id': 'Trade_nfQhzk5R'}, 'body': {'order': {'price': 13.0, 'code': '000001', 'amount': 7600, 'date': '2017-12-14', 'datetime': '2017-12-14 09:31:00', 'towards': 1}, 'market': {'open': 13.15, 'high': 13.31, 'low': 12.91, 'close': 13.0, 'volume': 1001997.0, 'code': '000001'}, 'fee': {'commission': 148.2, 'tax': 0}}}
    


```python
"""下面这两个是 查询  一个是异步查询 一个是同步的(no_wait)
异步不会阻塞当前线程 同步会阻塞"""
```




    '下面这两个是 查询  一个是异步查询 一个是同步的(no_wait)\n异步不会阻塞当前线程 同步会阻塞'




```python
market.query_data(broker_name=QA.BROKER_TYPE.BACKETEST,data_type=QA.MARKETDATA_TYPE.DAY,market_type=QA.MARKET_TYPE.STOCK_DAY,
                 code='000001',start='2017-12-14')
```

    QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 1 tasks to do
    

    ON QUERY
    [['000001' '13.15' '13.31' '12.91' '13.0' '1001997.0' '2017-12-14']]
    


```python
market.query_data_no_wait(broker_name=QA.BROKER_TYPE.BACKETEST,data_type=QA.MARKETDATA_TYPE.DAY,market_type=QA.MARKET_TYPE.STOCK_DAY,
                 code='000001',start='2017-12-14')
```




    array([['000001', '13.15', '13.31', '12.91', '13.0', '1001997.0',
            '2017-12-14']],
          dtype='<U10')




```python
"""成交了以后 你可以看到账户的资产变化了"""
market.session[a_1]
```




    <QA_Account Acc_DasXt8cC Assets:999851.8>




```python
"""待成交列表被清空"""
market.order_handler.order_queue.pending
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>account_cookie</th>
      <th>amount</th>
      <th>amount_model</th>
      <th>code</th>
      <th>data_type</th>
      <th>date</th>
      <th>datetime</th>
      <th>market_type</th>
      <th>order_id</th>
      <th>order_model</th>
      <th>price</th>
      <th>sending_time</th>
      <th>status</th>
      <th>strategy</th>
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
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python
"""待成交队列清空"""
market.order_handler.order_queue.trade_list
```




    []




```python
"""
cash 现金减少
"""
market.session[a_1].cash
```




    [1000000, 901051.8]




```python
"""
资产减少
"""
market.session[a_1].assets
```




    [1000000, 999851.8]




```python
"""
因为没有触发每日结算时间 在T+1的市场 即使买入了也没有可卖的
"""
market.session[a_1].sell_available
```




    [['datetime', 'code', 'price', 'amount', 'order_id', 'trade_id']]




```python
"""
持仓表增加
"""
market.session[a_1].hold
```




    [['2017-12-14 09:31:00',
      '000001',
      13.0,
      7600.0,
      'Order_L5gj0sUo',
      'Trade_PyBjheit']]




```python
import pandas as pd
"""用pandas打印的漂亮一点"""
pd.DataFrame(data=market.session[a_1].hold,columns=market.session[a_1]._hold_headers)
```




<div>

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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-12-14 09:31:00</td>
      <td>000001</td>
      <td>13.0</td>
      <td>7600.0</td>
      <td>Order_L5gj0sUo</td>
      <td>Trade_PyBjheit</td>
    </tr>
  </tbody>
</table>
</div>




```python
"""
账户信息

可以看到 减少的资产 主要是因为收了手续费
"""
market.session[a_1].message
```




    {'body': {'account': {'assets': [1000000, 999851.8],
       'cash': [1000000, 901051.8],
       'detail': [['2017-12-14 09:31:00',
         '000001',
         13.0,
         7600.0,
         'Order_L5gj0sUo',
         'Trade_PyBjheit',
         [],
         [],
         [],
         [],
         7600.0,
         148.2]],
       'history': [['2017-12-14 09:31:00',
         '000001',
         13.0,
         1,
         7600.0,
         'Order_L5gj0sUo',
         'Trade_PyBjheit',
         148.2]],
       'hold': [['2017-12-14 09:31:00',
         '000001',
         13.0,
         7600.0,
         'Order_L5gj0sUo',
         'Trade_PyBjheit']]},
      'date_stamp': 1514244662.029989,
      'time': '2017-12-26 07:31:02.029989'},
     'header': {'cookie': 'Acc_DasXt8cC',
      'session': {'code': '000001', 'strategy': '', 'user': ''},
      'source': 'account'}}




```python
"""结算事件"""
market._settle(QA.BROKER_TYPE.BACKETEST)
```

    QUANTAXIS>> From Engine  <QA_ENGINE with ['backtest', 'simulation'] kernals>: There are still 2 tasks to do
    QUANTAXIS>> From Engine  <QA_ENGINE with ['backtest', 'simulation'] kernals>: There are still 1 tasks to do
    QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 3 tasks to do
    QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 2 tasks to do
    QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 1 tasks to do
    


```python
"""
结算完以后 可卖数量就会变成和持仓数一样
"""
market.session[a_1].sell_available
```




    code
    000001    7600.0
    Name: amount, dtype: float64




```python
"""
结算完以后 待成交队列也被清空
"""

market.order_handler.order_queue()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>


