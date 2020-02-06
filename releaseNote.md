# release Note

QUANTAXIS 1.3.0


此版本相较于之前的版本有了较多的修正

## QAARP

- 几乎重写了 QAUSER, 大量修改 QAPORTFOLIO部分代码


1. 从此 创建一个QAAccout的推荐方式是  从QAUSER创建

```python

import QUANTAXIS as QA

user = QA.QA_User(username = 'quantaxis', password = 'quantaxis')

# 然后创建一个组合 如果该组合存在 返回该组合
portfolio =  user.new_portfolio('qatestportfolio')

# 基于组合创建你想要的QA_Account

account = portfolio.new_account(account_cookie='test_a', init_cash= 200000, ....)

```
2. 在你退出这个程序的时候 如果你想保存这个过程, 使用 ```account.save()```

```python
###

account.save()
```

3. 从组合中删除一个 QA_Account的过程:

```

portfolio.drop_account(account_coookie)
```

4. 往组合中添加一个新的已经实例化的 QA_Account:

```python

acc = QA_Account(usercookie = xxxx, portfolio_cookie=xxxx, account_cookie=xxxx)

portfolio.add_account(account_cookie, acc)
```

## QAMAKET


QA_Market 在1.3.0 版本也经历的较多修改

1. 删除了 QABroker的独立线程
2. 保留QAEvent, 但是实际上删除了QATask的任务提交过程
3. 主要任务都放在主线程中进行


QA_BacktestBroker 也进行了相应的更新



