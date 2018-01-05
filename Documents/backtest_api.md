# QABacktest 的 api


```python
from QUANTAXIS import QA_Backtest as QB
#常量:
QB.backtest_type #回测类型 day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
QB.account.message  #当前账户消息
QB.account.cash  #当前可用资金
QB.account.hold # 当前账户持仓
QB.account.history #当前账户的历史交易记录
QB.account.assets #当前账户总资产
QB.account.detail #当前账户的交易对账单
QB.account.init_assest #账户的最初资金
QB.strategy_gap #前推日期
QB.strategy_name #策略名称

QB.strategy_stock_list #回测初始化的时候  输入的一个回测标的
QB.strategy_start_date #回测的开始时间
QB.strategy_end_date  #回测的结束时间


QB.today  #在策略里面代表策略执行时的日期
QB.now  #在策略里面代表策略执行时的时间
QB.benchmark_code  #策略业绩评价的对照行情

QB.backtest_print_log = True  # 是否在屏幕上输出结果


QB.setting.QA_setting_user_name = str('admin') #回测账户
QB.setting.QA_setting_user_password = str('admin') #回测密码


#函数:
#获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today/QB.now)
- 可选项: gap_ 
- 可选项: type_ 'lt','lte' 默认是lt
#获取单个bar
QB.QA_backtest_get_market_data_bar(QB,code,QB.today/QB.now)

#拿到开高收低量
Open,High,Low,Close,Volume=QB.QA_backtest_get_OHLCV(QB,QB.QA_backtest_get_market_data(QB,item,QB.today))

#获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)

#一键平仓:
QB.QA_backtest_sell_all(QB)

#报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)
"""
order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market  [其实是以bar的开盘价成交]
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C
"""
#查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)
#查询当前一只股票的可卖数量
QB.QA_backtest_sell_available(QB,code)
#查询当前一只股票的持仓平均成本
QB.QA_backtest_hold_price(QB,code)

```


