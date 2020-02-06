# 下单说明:

## 全仓买入测试

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


# 打印剩余资金
Account.cash_available
Out[5]: 950.2999999999302

## 打印order的占用资金
(Order.amount*Order.price)*(1+Account.commission_coeff)
Out[6]: 999049.7000000001

## order占用的资金和account的资金相加等于总和
999049.7000000001+950.2999999999302
Out[7]: 1000000.0
```