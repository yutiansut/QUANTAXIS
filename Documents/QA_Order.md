# 详解 QA_Order  --  QUANTAXIS中的标准订单类 


QA_Order是quantaxis的标准订单类, 产生于 QA_Account.send_order 这个接口


<!-- vscode-markdown-toc -->
* 1. [QA_Order的属性](#QA_Order)
* 2. [QA_Order 的状态判断机制](#QA_Order-1)
* 3. [QA_Order的成交回调机制](#QA_Order-1)
* 4. [QA_Order的事件](#QA_Order-1)
* 5. [QA_Order的多市场兼容/接口兼容](#QA_Order-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='QA_Order'></a>QA_Order的属性

```python
    def __init__(self, price=None, date=None, datetime=None, sending_time=None, trade_time=False, amount=0, market_type=None, frequence=None,
                 towards=None, code=None, user=None, account_cookie=None, strategy=None, order_model=None, money=None, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                 order_id=None, trade_id=False, _status=ORDER_STATUS.NEW, callback=False, commission_coeff=0.00025, tax_coeff=0.001, exchange_id=None, *args, **kwargs):
        '''



        QA_Order 对象表示一个委托业务， 有如下字段
        - price 委托价格 (限价单用)
        - date 委托日期 (一般日线级别回测用)
        - datetime 当前时间 (分钟线级别和实时用)
        - sending_time 委托时间 (分钟线级别和实时用)
        - trade_time 成交时间 [list] (分钟/日线/实盘时用, 一笔订单多次成交会不断append进去)
        - amount 委托数量
        - frequence 频率 (回测用 DAY/1min/5min/15min/30min/...)
        - towards 买卖方向
        - code  订单的品种
        - user  订单发起者
        - account_cookie 订单发起账户的标识
        - stratgy 策略号
        - order_model  委托方式(限价/市价/下一个bar/)  type str eg 'limit'
        - money  订单金额
        - amount_model 委托量模式(按量委托/按总成交额委托) type str 'by_amount'
        - order_id   委托单id
        - trade_id   成交单id
        - _status    内部维护的订单状态
        - callback   当订单状态改变的时候 主动回调的函数(可以理解为自动执行的OnOrderAction)
        - commission_coeff 手续费系数
        - tax_coeff  印花税系数(股票)
        - exchange_id  交易所id (一般用于实盘期货)

        :param args: type tuple
        :param kwargs: type dict
```

- price 委托价格 (限价单用)
- date 委托日期 (一般日线级别回测用)
- datetime 当前时间 (分钟线级别和实时用)
- sending_time 委托时间 (分钟线级别和实时用)
- trade_time 成交时间 [list] (分钟/日线/实盘时用, 一笔订单多次成交会不断append进去)
- amount 委托数量
- frequence 频率 (回测用 DAY/1min/5min/15min/30min/...)
- towards 买卖方向
- code  订单的品种
- user  订单发起者
- account_cookie 订单发起账户的标识
- stratgy 策略号
- order_model  委托方式(限价/市价/下一个bar/)  type str eg 'limit'
- money  订单金额
- amount_model 委托量模式(按量委托/按总成交额委托) type str 'by_amount'
- order_id   委托单id
- trade_id   成交单id
- _status    内部维护的订单状态
- callback   当订单状态改变的时候 主动回调的函数(可以理解为自动执行的OnOrderAction)
- commission_coeff 手续费系数
- tax_coeff  印花税系数(股票)
- exchange_id  交易所id (一般用于实盘期货)


##  2. <a name='QA_Order-1'></a>QA_Order 的状态判断机制

```python

    @property
    def status(self):
        if self._status in [ORDER_STATUS.FAILED, ORDER_STATUS.NEXT, ORDER_STATUS.SETTLED, ORDER_STATUS.CANCEL_ALL, ORDER_STATUS.CANCEL_PART]:
            return self._status

        if self.pending_amount <= 0:
            self._status = ORDER_STATUS.SUCCESS_ALL
            return self._status
        elif self.pending_amount > 0 and self.trade_amount > 0:
            self._status = ORDER_STATUS.SUCCESS_PART
            return self._status
        elif self.trade_amount == 0:
            self._status = ORDER_STATUS.QUEUED
            return self._status

```

在QA_Order中, 你想获取一个订单状态的时候, 会经历一个惰性计算的过程

当订单属于  [委托失败 | 继续委托| 已经结算| 全部撤单| 部分撤单]状态 ===> 直接返回状态结果

当订单的  待成交数量<=0  ===>  订单已经成交

当订单的待成交数量>0 且交易数量>0  ===>  订单部分成交

当订单的 成交数量==0   ===> 订单扔在队列中


##  3. <a name='QA_Order-1'></a>QA_Order的成交回调机制

在QA_Account生成一个订单(接口: QA_Account.send_order)的时候, 会将QA_Account.receive_deal的函数 作为回调句柄, 传给QA_Order的callback函数

因此, 当出现一笔交易的时候, QA_Order会通过Account.receive_deal的方式自动回调告知账户成交


```python

# QA_Account 生成QA_Order的代码
_order = QA_Order(user_cookie=self.user_cookie, strategy=self.strategy_name, frequence=self.frequence,
                    account_cookie=self.account_cookie, code=code, market_type=self.market_type,
                    date=date, datetime=time, sending_time=time, callback=self.receive_deal,
                    amount=amount, price=price, order_model=order_model, towards=towards, money=money,
                    amount_model=amount_model, commission_coeff=self.commission_coeff, tax_coeff=self.tax_coeff, *args, **kwargs)  # init

```

可以看到 ```  callback=self.receive_deal``` 该句中将 Account的成交回调函数句柄的内存地址赋给了QA_Order

```python
# QA_Order的成交函数
self.trade_id.append(trade_id)
self.trade_price = (self.trade_price*self.trade_amount +
                    trade_price*trade_amount)/(self.trade_amount+trade_amount)
self.trade_amount += trade_amount
self.trade_time.append(trade_time)
self.callback(self.code, trade_id, self.order_id, self.realorder_id,
                trade_price, trade_amount, self.towards, trade_time)
```
而QA_Order在成交了一笔订单以后, 则会调用self.callback




##  4. <a name='QA_Order-1'></a>QA_Order的事件


QA_Order 的事件有以下几种:


- create()   生成一个订单的时候调用

- queued(realorder_id)  订单进入委托队列时使用(及 创建成功)
- failed(reason=None)   订单创建失败时调用

- trade(trade_id, trade_price, trade_amount, trade_time) 出现一笔成交单的时候调用
- cancel()   撤单时调用

- settle()  订单被结算事件调用时使用

##  5. <a name='QA_Order-1'></a>QA_Order的多市场兼容/接口兼容

to_df
to_dict
to_otgformat
to_qatradegatway

from_otgformat
from_dict

