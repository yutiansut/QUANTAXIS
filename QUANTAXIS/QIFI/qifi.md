# QIFI
Quantaxis Differential Information Flow for Finance Intergration


QIFI 协议 作为qatrader/ qapms的标准协议, 支持股票/期货市场

- 名称 QIFI   为 Quantaxis Differential Information Flow for Finance Intergration

- 核心字段
	-  'accounts'

	-  'events'

	-  'trades'

	-  'orders'

	-  'positions'

	-  'broker_name'
		

交易的协议参见[交易协议](trade_protocol.md)


### 关联项目


- [QUANTAXIS](https://github.com/quantaxis/quantaxis)
- [QATrader](https://github.com/yutiansut/qatrader)
- [QIFIAccount](https://github.com/yutiansut/QIFIAccount)
- [QAStrategy](https://github.com/yutiansut/QAStrategy)


- [QAPMS](https://github.com/yutiansut/QAPMS)
- [QACEPEngine](https://github.com/yutiansut/QACEPEngine)
- [QARiskPro](https://github.com/yutiansut/QARiskPro)
- [QAPBSystem](https://github.com/yutiansut/QAPBSystem)






###  为什么要有这个协议:

主要目的是把 策略  /  背后的账户实现解耦

策略无需关心背后的账户情况, 仅需相应的申请资源即可(如 申请模拟账户/ 申请回测账户/ 申请实盘账户/)
策略在申请完毕后, 可以直接去读取相应字段,  如 策略想获取持仓的时候 即可直接get('positions') 即为持仓字段




### 协议实例概览

```json
{
    "account_cookie" : "100010",  // 账户号(兼容QUANTAXIS QAAccount)
    "password" : "100010",
    "ping_gap" : 5,
    "portfolio" : "default",
    "broker_name" : "QUANTAXIS",  // 接入商名称
    "capital_password" : null,   // 资金密码 (实盘用)
    "bank_password" : null,   // 银行密码(实盘用)
    "bankid" : "SIM",         // 银行id
    "investor_name" : "",   // 开户人名称
    "money" : 0.0,          // 当前可用现金
    "pub_host" : "localhost",
    "settlement" : {},
    "taskid" : null,
    
    "qifi_id": String,
    "trade_host" : "127.0.0.1",
    "updatetime" : "2019-09-06 21:19:48.346640",
    "wsuri" : "ws://www.yutiansut.com:7988",
    "bankname" : "模拟银行",
    "trading_day" : "20190909",
    "status" : 200
    "accounts" : {
        "user_id" : "100010",  // 用户号 兼容diff协议, ==> 实盘则为具体账户号
        "currency" : "CNY",    // 货币属性 兼容diff协议
        "pre_balance" : 0.0,   // 上一个交易日的结算权益
        "deposit" : 1000000.0, // 今日转入资金
        "withdraw" : 0.0,      // 今日转出资金
        "WithdrawQuota" : 3.95252516672997e-322, // 当前可取字段(QIFI 独有)
        "close_profit" : 0.0,  // 平仓盈亏
        "commission" : 6.84,   // 手续费
        "premium" : 0.0,       // 附加费
        "static_balance" : 1000000.0,   // 静态权益(一般= pre_balance)
        "position_profit" : -80.0,  // 持仓盈亏
        "float_profit" : -80.0,   // 浮动盈亏
        "balance" : 999913.16,    // 当前权益
        "margin" : 5472.0,        // 保证金
        "frozen_margin" : 5472.0,  // 冻结保证金
        "frozen_commission" : 0.0, // 冻结手续费
        "frozen_premium" : 0.0,    // 冻结附加费用
        "available" : 988969.16,   // 可用资金
        "risk_ratio" : 0.00547247522974895   // 风险度
    },
    "banks" : {               // 银行内容(支持多银行 id识别)
        "SIM" : {
            "id" : "SIM",
            "name" : "模拟银行",
            "bank_account" : "",
            "fetch_amount" : 0.0,
            "qry_count" : 0
        }
    },
    "event" : {                   // 事件 time+ 内容
        "2019-09-06 21:01:36" : "登录成功",
        "2019-09-06 21:12:53" : "下单成功",
        "2019-09-06 21:14:25" : "下单成功",
        "2019-09-06 21:14:37" : "下单成功",
        "2019-09-06 21:14:57" : "成交通知,合约:SHFE.rb2001,手数:1",
        "2019-09-06 21:16:50" : "成交通知,合约:SHFE.rb2001,手数:1"
    },
    "orders" : {            // 多段order 订单
        "QAOTG_5oAYRUI3" : {
            "seqno" : 8,
            "user_id" : "100010",
            "order_id" : "QAOTG_5oAYRUI3",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "direction" : "SELL",
            "offset" : "OPEN",
            "volume_orign" : 1,
            "price_type" : "LIMIT",
            "limit_price" : 3426.0,
            "time_condition" : "GFD",
            "volume_condition" : "ANY",
            "insert_date_time" : NumberLong(1567775573528050636),
            "exchange_order_id" : "QAOTG_5oAYRUI3",
            "status" : "FINISHED",
            "volume_left" : 0,
            "last_msg" : ""
        },
        "QAOTG_xyVXjgcZ" : {
            "seqno" : 3,
            "user_id" : "100010",
            "order_id" : "QAOTG_xyVXjgcZ",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "direction" : "SELL",
            "offset" : "OPEN",
            "volume_orign" : 1,
            "price_type" : "LIMIT",
            "limit_price" : 3480.0,
            "time_condition" : "GFD",
            "volume_condition" : "ANY",
            "insert_date_time" : NumberLong(1567775665377198042),
            "exchange_order_id" : "QAOTG_xyVXjgcZ",
            "status" : "ALIVE",
            "volume_left" : 1,
            "last_msg" : ""
        },
        "QAOTG_BIn7hPtG" : {
            "seqno" : 5,
            "user_id" : "100010",
            "order_id" : "QAOTG_BIn7hPtG",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "direction" : "SELL",
            "offset" : "OPEN",
            "volume_orign" : 1,
            "price_type" : "LIMIT",
            "limit_price" : 3480.0,
            "time_condition" : "GFD",
            "volume_condition" : "ANY",
            "insert_date_time" : NumberLong(1567775677891881150),
            "exchange_order_id" : "QAOTG_BIn7hPtG",
            "status" : "ALIVE",
            "volume_left" : 1,
            "last_msg" : ""
        },
        "QAOTG_P4kEw2FJ" : {
            "seqno" : 13,
            "user_id" : "100010",
            "order_id" : "QAOTG_P4kEw2FJ",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "direction" : "BUY",
            "offset" : "OPEN",
            "volume_orign" : 1,
            "price_type" : "LIMIT",
            "limit_price" : 3480.0,
            "time_condition" : "GFD",
            "volume_condition" : "ANY",
            "insert_date_time" : NumberLong(1567775810195686542),
            "exchange_order_id" : "QAOTG_P4kEw2FJ",
            "status" : "FINISHED",
            "volume_left" : 0,
            "last_msg" : ""
        }
    },
    "positions" : {
        "SHFE_rb2001" : {
            "user_id" : "100010",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "volume_long_today" : 1,
            "volume_long_his" : 0,
            "volume_long" : 1,
            "volume_long_frozen_today" : 0,
            "volume_long_frozen_his" : 0,
            "volume_long_frozen" : 0,
            "volume_short_today" : 1,
            "volume_short_his" : 0,
            "volume_short" : 1,
            "volume_short_frozen_today" : 0,
            "volume_short_frozen_his" : 0,
            "volume_short_frozen" : 0,
            "volume_long_yd" : 0,
            "volume_short_yd" : 0,
            "pos_long_his" : 0,
            "pos_long_today" : 1,
            "pos_short_his" : 0,
            "pos_short_today" : 1,
            "open_price_long" : 3434.0,
            "open_price_short" : 3426.0,
            "open_cost_long" : 34340.0,
            "open_cost_short" : 34260.0,
            "position_price_long" : 3434.0,
            "position_price_short" : 3426.0,
            "position_cost_long" : 34340.0,
            "position_cost_short" : 34260.0,
            "last_price" : 3432.0,
            "float_profit_long" : -20.0,
            "float_profit_short" : -60.0,
            "float_profit" : -80.0,
            "position_profit_long" : -20.0,
            "position_profit_short" : -60.0,
            "position_profit" : -80.0,
            "margin_long" : 2736.0,
            "margin_short" : 2736.0,
            "margin" : 5472.0
        }
    },
    "trades" : {
        "6" : {
            "seqno" : 7,
            "user_id" : "100010",
            "trade_id" : "6",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "order_id" : "QAOTG_5oAYRUI3",
            "exchange_trade_id" : "6",
            "direction" : "SELL",
            "offset" : "OPEN",
            "volume" : 1,
            "price" : 3426.0,
            "trade_date_time" : NumberLong(1567775697237747424),
            "commission" : 3.42
        },
        "11" : {
            "seqno" : 12,
            "user_id" : "100010",
            "trade_id" : "11",
            "exchange_id" : "SHFE",
            "instrument_id" : "rb2001",
            "order_id" : "QAOTG_P4kEw2FJ",
            "exchange_trade_id" : "11",
            "direction" : "BUY",
            "offset" : "OPEN",
            "volume" : 1,
            "price" : 3434.0,
            "trade_date_time" : NumberLong(1567775810195972480),
            "commission" : 3.42
        }
    },
    "transfers" : {},
 }
