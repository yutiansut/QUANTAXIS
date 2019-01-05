# 详解 QA_Order  --  QUANTAXIS中的标准订单类 


QA_Order是quantaxis的标准订单类, 产生于 QA_Account.send_order 这个接口


## QA_Order的属性

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
