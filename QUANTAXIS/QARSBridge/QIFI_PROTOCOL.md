# QIFI协议规范

> QIFI: **Q**uantaxis **D**ifferential **I**nformation **F**low for **F**inance **I**ntegration
> QUANTAXIS统一多市场、多语言账户系统协议

**作者**: @yutiansut @quantaxis
**版本**: v2.1.0
**最后更新**: 2025-10-25

---

## 概述

QIFI协议是QUANTAXIS生态系统中的核心账户协议，提供跨语言（Python/Rust/C++）、跨市场（股票/期货/期权）的统一账户表示。

### 协议特点

1. **跨语言兼容**: Python/Rust/C++完全一致的数据结构
2. **完整账户状态**: 包含账户、持仓、订单、成交、转账的完整信息
3. **增量更新支持**: 通过Diff机制支持高效的状态同步
4. **MongoDB友好**: 直接映射到MongoDB文档结构
5. **JSON序列化**: 标准JSON格式，便于跨系统传输

---

## 核心数据结构

### 1. QIFI主结构

QIFI是账户的顶层数据结构，包含账户的所有信息：

```rust
pub struct QIFI {
    // === 基础信息 ===
    pub databaseip: String,           // 数据库IP
    pub account_cookie: String,       // 账户ID/Cookie
    pub password: String,             // 密码
    pub portfolio: String,            // 投资组合名称
    pub broker_name: String,          // 券商名称
    pub capital_password: String,     // 资金密码
    pub bank_password: String,        // 银行密码
    pub bankid: String,               // 银行ID
    pub investor_name: String,        // 投资者姓名
    pub money: f64,                   // 资金

    // === 连接信息 ===
    pub pub_host: String,             // 发布主机
    pub trade_host: String,           // 交易主机
    pub wsuri: String,                // WebSocket URI
    pub eventmq_ip: String,           // 事件MQ地址

    // === 状态信息 ===
    pub trading_day: String,          // 交易日
    pub updatetime: String,           // 更新时间
    pub status: i32,                  // 状态码
    pub taskid: String,               // 任务ID
    pub ping_gap: i32,                // Ping间隔

    // === 银行信息 ===
    pub bankname: String,             // 银行名称
    pub banks: HashMap<String, BankDetail>,  // 银行详情

    // === 核心数据 ===
    pub accounts: Account,                      // 账户信息
    pub positions: HashMap<String, Position>,   // 持仓 {code: Position}
    pub orders: BTreeMap<String, Order>,        // 订单 {order_id: Order}
    pub trades: BTreeMap<String, Trade>,        // 成交 {trade_id: Trade}
    pub transfers: BTreeMap<String, Transfer>,  // 转账记录
    pub frozen: HashMap<String, Frozen>,        // 冻结信息

    // === 事件日志 ===
    pub event: HashMap<String, String>,    // 事件日志 {timestamp: event}
    pub settlement: HashMap<String, String>, // 结算记录
}
```

### 2. Account - 账户信息

```rust
pub struct Account {
    pub user_id: String,              // 用户ID

    // === 资金信息 ===
    pub currency: String,             // 币种 (CNY/USD等)
    pub pre_balance: f64,             // 昨日权益
    pub deposit: f64,                 // 入金
    pub withdraw: f64,                // 出金
    pub WithdrawQuota: f64,           // 可取资金
    pub static_balance: f64,          // 静态权益
    pub balance: f64,                 // 动态权益 (当前权益)
    pub available: f64,               // 可用资金

    // === 盈亏信息 ===
    pub close_profit: f64,            // 平仓盈亏
    pub position_profit: f64,         // 持仓盈亏
    pub float_profit: f64,            // 浮动盈亏

    // === 费用信息 ===
    pub commission: f64,              // 手续费
    pub premium: f64,                 // 权利金 (期权)

    // === 保证金信息 ===
    pub margin: f64,                  // 占用保证金
    pub frozen_margin: f64,           // 冻结保证金
    pub frozen_commission: f64,       // 冻结手续费
    pub frozen_premium: f64,          // 冻结权利金

    // === 风险指标 ===
    pub risk_ratio: f64,              // 风险度 = margin/balance
}
```

**关键公式**:
- `balance` = `pre_balance` + `deposit` - `withdraw` + `close_profit` + `position_profit` - `commission`
- `available` = `balance` - `margin` - `frozen_margin`
- `risk_ratio` = `margin` / `balance`

### 3. Position - 持仓信息

```rust
pub struct Position {
    pub user_id: String,              // 用户ID
    pub exchange_id: String,          // 交易所 (SSE/SZSE/SHFE/DCE等)
    pub instrument_id: String,        // 合约代码

    // === 多头持仓 ===
    pub volume_long: f64,             // 多头总量
    pub volume_long_today: f64,       // 多头今仓
    pub volume_long_his: f64,         // 多头昨仓
    pub volume_long_yd: f64,          // 多头昨日
    pub pos_long_his: f64,            // 多头历史
    pub pos_long_today: f64,          // 多头今日

    // === 空头持仓 ===
    pub volume_short: f64,            // 空头总量
    pub volume_short_today: f64,      // 空头今仓
    pub volume_short_his: f64,        // 空头昨仓
    pub volume_short_yd: f64,         // 空头昨日
    pub pos_short_his: f64,           // 空头历史
    pub pos_short_today: f64,         // 空头今日

    // === 冻结持仓 ===
    pub volume_long_frozen: f64,      // 多头冻结总量
    pub volume_long_frozen_today: f64,// 多头今仓冻结
    pub volume_long_frozen_his: f64,  // 多头昨仓冻结
    pub volume_short_frozen: f64,     // 空头冻结总量
    pub volume_short_frozen_today: f64,// 空头今仓冻结
    pub volume_short_frozen_his: f64, // 空头昨仓冻结

    // === 成本和价格 ===
    pub open_price_long: f64,         // 多头开仓均价
    pub open_price_short: f64,        // 空头开仓均价
    pub open_cost_long: f64,          // 多头开仓成本
    pub open_cost_short: f64,         // 空头开仓成本
    pub position_price_long: f64,     // 多头持仓均价
    pub position_price_short: f64,    // 空头持仓均价
    pub position_cost_long: f64,      // 多头持仓成本
    pub position_cost_short: f64,     // 空头持仓成本
    pub last_price: f64,              // 最新价

    // === 盈亏 ===
    pub float_profit_long: f64,       // 多头浮动盈亏
    pub float_profit_short: f64,      // 空头浮动盈亏
    pub float_profit: f64,            // 总浮动盈亏
    pub position_profit_long: f64,    // 多头持仓盈亏
    pub position_profit_short: f64,   // 空头持仓盈亏
    pub position_profit: f64,         // 总持仓盈亏

    // === 保证金 ===
    pub margin_long: f64,             // 多头保证金
    pub margin_short: f64,            // 空头保证金
    pub margin: f64,                  // 总保证金
}
```

**关键说明**:
- **股票**: 只使用多头字段 (`volume_long`, `open_price_long`等)
- **期货**: 同时支持多空双向持仓
- **今昨仓**: 区分今仓和昨仓用于上期所平今/平昨规则

### 4. Order - 订单信息

```rust
pub struct Order {
    pub seqno: i32,                   // 序号
    pub user_id: String,              // 用户ID
    pub order_id: String,             // 订单ID
    pub exchange_id: String,          // 交易所
    pub instrument_id: String,        // 合约代码

    // === 订单参数 ===
    pub direction: String,            // 方向: BUY/SELL
    pub offset: String,               // 开平: OPEN/CLOSE/CLOSETODAY
    pub volume_orign: f64,            // 原始数量
    pub volume_left: f64,             // 剩余数量
    pub limit_price: f64,             // 限价

    // === 订单类型 ===
    pub price_type: String,           // 价格类型: LIMIT/MARKET/FAK/FOK
    pub time_condition: String,       // 时间条件: GFD/IOC/GTC
    pub volume_condition: String,     // 数量条件: ANY/MIN/ALL

    // === 状态信息 ===
    pub status: String,               // 状态: ALIVE/FINISHED/CANCELLED
    pub insert_date_time: i64,        // 插入时间 (纳秒时间戳)
    pub exchange_order_id: String,    // 交易所订单ID
    pub last_msg: String,             // 最后消息
}
```

**订单状态**:
- `ALIVE`: 活跃订单
- `FINISHED`: 完成 (全部成交或撤单)
- `CANCELLED`: 已撤销

**订单方向**:
- `BUY`: 买入
- `SELL`: 卖出

**开平标志**:
- `OPEN`: 开仓
- `CLOSE`: 平仓
- `CLOSETODAY`: 平今
- `CLOSEYESTERDAY`: 平昨

### 5. Trade - 成交信息

```rust
pub struct Trade {
    pub seqno: i32,                   // 序号
    pub user_id: String,              // 用户ID
    pub trade_id: String,             // 成交ID (唯一标识)
    pub exchange_id: String,          // 交易所
    pub instrument_id: String,        // 合约代码
    pub order_id: String,             // 关联订单ID
    pub exchange_trade_id: String,    // 交易所成交ID

    // === 成交信息 ===
    pub direction: String,            // 方向: BUY/SELL
    pub offset: String,               // 开平: OPEN/CLOSE
    pub volume: f64,                  // 成交数量
    pub price: f64,                   // 成交价格
    pub trade_date_time: i64,         // 成交时间 (纳秒时间戳)

    // === 费用 ===
    pub commission: f64,              // 手续费
}
```

### 6. Transfer - 转账记录

```rust
pub struct Transfer {
    pub datetime: i64,                // 时间戳
    pub currency: String,             // 币种
    pub amount: f64,                  // 金额 (正数=入金，负数=出金)
    pub error_id: i32,                // 错误码
    pub error_msg: String,            // 错误消息
}
```

### 7. BankDetail - 银行详情

```rust
pub struct BankDetail {
    pub id: String,                   // 银行ID
    pub name: String,                 // 银行名称
    pub bank_account: String,         // 银行账户
    pub fetch_amount: f64,            // 可取金额
    pub qry_count: i64,               // 查询次数
}
```

### 8. Frozen - 冻结信息

```rust
pub struct Frozen {
    pub amount: f64,                  // 冻结数量
    pub coeff: f64,                   // 系数
    pub money: f64,                   // 冻结资金
}
```

---

## QIFI协议使用规范

### 1. 数据存储

#### MongoDB存储

QIFI结构直接对应MongoDB文档：

```python
# MongoDB集合结构
db.account_{portfolio}.insert_one(qifi_dict)

# 查询示例
qifi = db.account_default.find_one({"account_cookie": "my_account"})
```

#### 字段命名约定

- 使用snake_case命名 (`account_cookie`, `trading_day`)
- 时间戳使用纳秒级Unix时间戳 (`insert_date_time`, `trade_date_time`)
- HashMap的key使用字符串 (`positions`, `orders`, `trades`)

### 2. 跨语言兼容性

#### Python实现

```python
from QUANTAXIS.QARSBridge import QARSAccount

# 创建账户
account = QARSAccount(
    account_cookie="test",
    portfolio="default",
    init_cash=1000000.0
)

# 导出QIFI
qifi_dict = account.get_qifi()

# 从QIFI恢复
account2 = QARSAccount.from_qifi(qifi_dict)
```

#### Rust实现

```rust
use qars3::QA_QIFIAccount;

// 创建账户
let account = QA_QIFIAccount::new(
    "test",
    "default",
    1000000.0,
    "backtest"
);

// 获取QIFI
let qifi = account.get_qifi();
```

#### C++实现

```cpp
// C++通过PyO3绑定或直接使用Rust库
// 保持数据结构一致性
```

### 3. 增量更新机制

QIFI支持通过`Diff`枚举进行增量更新：

```rust
pub enum Diff {
    Accounts(Account),                    // 账户更新
    Positions(String, Option<Position>),  // 持仓更新
    Orders(String, Option<Order>),        // 订单更新
    Trades(String, Option<Trade>),        // 成交更新
    // ... 其他字段
}

// 计算两个QIFI的差异
let diffs = qifi1.diff(&qifi2);
```

**用途**:
- WebSocket实时推送
- 数据库增量更新
- 前后端状态同步

### 4. MiniAccount/MiniPosition

为了减少传输数据量，QIFI提供简化版本：

```rust
pub struct MiniAccount {
    pub user_id: String,
    pub balance: f64,
    pub available: f64,
    pub margin: f64,
    pub float_profit: f64,
    // ... 核心字段
    pub portfolio: String,
    pub user_cookie: String,
    pub date: String,
    pub datetime: String,
}

// 转换
let mini_account = qifi.to_mini();
let mini_position = position.to_mini(date);
```

---

## 实现要点

### 1. Python包装器要求

在实现Python包装器时，必须：

1. **保持字段名一致**: 与Rust结构体字段名完全一致
2. **保持类型一致**: `f64`→`float`, `String`→`str`, `HashMap`→`dict`
3. **保持嵌套结构**: `positions`, `orders`, `trades`使用字典
4. **时间戳格式**: 使用纳秒级Unix时间戳

```python
# 正确示例
qifi = {
    "account_cookie": "test",
    "accounts": {
        "balance": 1000000.0,
        "available": 950000.0,
        # ... 所有Account字段
    },
    "positions": {
        "000001": {
            "volume_long": 1000.0,
            "open_price_long": 10.5,
            # ... 所有Position字段
        }
    },
    "orders": {
        "order_123": {
            "order_id": "order_123",
            "status": "FINISHED",
            # ... 所有Order字段
        }
    }
}
```

### 2. 数据验证

实现时应验证：

```python
def validate_qifi(qifi: dict) -> bool:
    """验证QIFI数据完整性"""
    required_fields = [
        'account_cookie', 'accounts', 'positions',
        'orders', 'trades', 'portfolio'
    ]

    for field in required_fields:
        if field not in qifi:
            raise ValueError(f"Missing required field: {field}")

    # 验证accounts结构
    account_fields = [
        'balance', 'available', 'margin',
        'float_profit', 'position_profit'
    ]
    for field in account_fields:
        if field not in qifi['accounts']:
            raise ValueError(f"Missing account field: {field}")

    return True
```

### 3. 序列化/反序列化

```python
import json

# 序列化
qifi_json = json.dumps(qifi_dict, ensure_ascii=False, indent=2)

# 反序列化
qifi_dict = json.loads(qifi_json)

# MongoDB存储
from pymongo import MongoClient
db = MongoClient()['quantaxis']
db.accounts.insert_one(qifi_dict)
```

---

## MIFI协议

MIFI (Market Information Flow Interface) 是QIFI的市场数据对应协议，目前在qars2中定义较少，主要包括：

- `mifi/future.rs`: 期货市场信息
- `mifi/stock.rs`: 股票市场信息
- `mifi/union.rs`: 联合市场信息

**注**: MIFI协议仍在开发中，未来版本将补充完整定义。

---

## 版本兼容性

| QUANTAXIS版本 | QIFI版本 | QARS2版本 | 兼容性 |
|--------------|---------|----------|-------|
| 2.0.x        | v2.0    | -        | ✓     |
| 2.1.x        | v2.1    | 0.0.45+  | ✓     |

---

## 参考资源

- QARS2源码: `/home/quantaxis/qars2/src/qaprotocol/qifi/`
- Python实现: `QUANTAXIS/QIFI/`
- Rust实现: `qars3::qaprotocol::qifi`
- 示例代码: `examples/qarsbridge_example.py`

---

**文档维护**: @yutiansut @quantaxis
**最后审核**: 2025-10-25
