# QIFI 模块文档

## 概述

QIFI (QUANTAXIS Isolated Financial Interface) 是 QUANTAXIS 的统一账户系统，提供了跨市场、跨语言的标准化账户管理接口。QIFI 设计用于支持多市场交易（股票、期货、期权等），并保持与 Rust/C++ 版本的账户结构一致性。

## 模块架构

### 核心组件

1. **QifiAccount.py**: QIFI 账户核心实现
   - 统一的账户管理接口
   - 支持实盘和模拟交易
   - 跨市场持仓管理
   - 动态权益计算

2. **QifiManager.py**: QIFI 账户管理器
   - 多账户管理系统
   - 账户组合管理
   - 账户状态监控

3. **qifisql.py**: QIFI 数据持久化
   - 账户数据存储
   - 交易记录管理
   - 数据查询接口

## 核心特性

### 1. 跨市场支持

QIFI 不区分持仓的具体市场类型，支持：
- 股票市场
- 期货市场
- 期权市场
- 数字货币市场

### 2. 多语言一致性

与 QUANTAXIS Rust/C++ 版本保持账户结构一致：
- 相同的数据格式
- 统一的接口设计
- 跨语言数据交换

### 3. 灵活部署模式

支持多种运行模式：
- **SIM**: 模拟交易模式
- **REAL**: 实盘交易模式
- **nodatabase**: 离线模式

## QIFI_Account 类

### 初始化参数

```python
class QIFI_Account:
    def __init__(self,
                 username,           # 用户名
                 password,           # 密码
                 model="SIM",        # 模式：SIM/REAL
                 broker_name="QAPaperTrading",  # 券商名称
                 portfolioname='QAPaperTrade',  # 组合名称
                 trade_host=mongo_ip,           # 交易主机
                 init_cash=1000000,             # 初始资金
                 taskid=str(uuid.uuid4()),      # 任务ID
                 nodatabase=False,              # 是否离线模式
                 dbname='mongodb',              # 数据库名称
                 clickhouse_ip=clickhouse_ip,   # ClickHouse配置
                 clickhouse_port=clickhouse_port,
                 clickhouse_user=clickhouse_user,
                 clickhouse_password=clickhouse_password)
```

### 主要属性

```python
# 基础信息
self.user_id           # 用户ID
self.qifi_id          # QIFI唯一标识
self.source_id        # 数据源标识
self.portfolio        # 所属组合
self.model            # 运行模式

# 券商信息
self.broker_name      # 券商名称
self.investor_name    # 开户人姓名
self.bank_id          # 银行代码
self.bankname         # 银行名称

# 交易参数
self.commission_fee   # 手续费率
self.trade_host       # 交易主机
self.status           # 账户状态
```

### 核心功能

#### 1. 订单处理

```python
# 订单方向解析
def parse_orderdirection(od):
    """
    解析订单方向和开平仓标志

    参数:
        od: 订单方向代码
            1,2,3,4: BUY 方向
            -1,-2,-3,-4: SELL 方向

    返回:
        direction: 'BUY' 或 'SELL'
        offset: 'OPEN', 'CLOSE', 'CLOSETODAY'
    """
    direction = 'BUY' if od in [1,2,3,4] else 'SELL'

    if abs(od) == 2 or od == 1:
        offset = 'OPEN'
    elif abs(od) == 3 or od == -1:
        offset = 'CLOSE'
    elif abs(od) == 4:
        offset = 'CLOSETODAY'

    return direction, offset
```

#### 2. 持仓管理

```python
# 使用 QAPosition 进行持仓管理
from QUANTAXIS.QAMarket.QAPosition import QA_Position

# 持仓计算和风险控制
position = QA_Position()
position.update_pos(code, direction, volume, price)
```

#### 3. 权益计算

QIFI 支持动态权益计算：
- 实时价格更新
- 浮动盈亏计算
- 保证金占用计算
- 可用资金计算

## QifiManager 管理器

### QA_QIFIMANAGER

```python
from QUANTAXIS.QIFI import QA_QIFIMANAGER

# 创建账户管理器
manager = QA_QIFIMANAGER()

# 添加账户
manager.add_account(account)

# 获取账户
account = manager.get_account(user_id)

# 账户组管理
manager.create_group(group_name)
manager.add_to_group(group_name, account_id)
```

### QA_QIFISMANAGER

多账户批量管理：
```python
from QUANTAXIS.QIFI import QA_QIFISMANAGER

# 批量管理
multi_manager = QA_QIFISMANAGER()

# 批量操作
multi_manager.update_all_accounts()
multi_manager.calculate_portfolio_pnl()
```

## 数据库支持

### MongoDB 存储

```python
# 账户数据存储
account_data = {
    'user_id': self.user_id,
    'qifi_id': self.qifi_id,
    'positions': positions_dict,
    'balance': balance_info,
    'trades': trade_records,
    'timestamp': datetime.now()
}
```

### ClickHouse 分析

支持高性能数据分析：
- 交易记录分析
- 性能统计
- 风险指标计算

## 使用示例

### 基础用法

```python
from QUANTAXIS.QIFI import QIFI_Account

# 创建模拟账户
account = QIFI_Account(
    username='test_user',
    password='password',
    model='SIM',
    init_cash=1000000
)

# 获取账户信息
print(f"用户ID: {account.user_id}")
print(f"账户模式: {account.model}")
print(f"初始资金: {account.init_cash}")
```

### 实盘账户

```python
# 创建实盘账户
real_account = QIFI_Account(
    username='real_user',
    password='real_password',
    model='REAL',
    broker_name='某期货公司',
    trade_host='192.168.1.100'
)
```

### 离线模式

```python
# 离线账户（不连接数据库）
offline_account = QIFI_Account(
    username='offline_user',
    password='password',
    nodatabase=True
)
```

### 多账户管理

```python
from QUANTAXIS.QIFI import QA_QIFIMANAGER

# 创建管理器
manager = QA_QIFIMANAGER()

# 创建多个账户
accounts = []
for i in range(5):
    account = QIFI_Account(
        username=f'user_{i}',
        password='password',
        portfolio=f'portfolio_{i}'
    )
    accounts.append(account)
    manager.add_account(account)

# 批量管理
manager.update_all_positions()
manager.calculate_total_pnl()
```

## 市场预设支持

```python
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET

# 获取市场信息
market_preset = MARKET_PRESET()

# 获取合约信息
contract_info = market_preset.get_contract_info('SHFE', 'cu2012')
print(f"合约乘数: {contract_info['volume_multiple']}")
print(f"最小变动价位: {contract_info['price_tick']}")
```

## 配置说明

### 环境变量配置

需要在 qaenv 中配置：
```python
# MongoDB 配置
mongo_ip = 'localhost'

# ClickHouse 配置
clickhouse_ip = 'localhost'
clickhouse_port = 9000
clickhouse_user = 'default'
clickhouse_password = ''
```

### 模式配置

1. **SIM 模式**:
   - 模拟交易
   - 虚拟资金
   - 用于策略测试

2. **REAL 模式**:
   - 实盘交易
   - 真实资金
   - 连接实际券商

## 最佳实践

1. **账户隔离**: 不同策略使用不同的账户或组合
2. **风险控制**: 设置合理的持仓限制和止损规则
3. **数据备份**: 定期备份账户数据和交易记录
4. **监控告警**: 设置账户异常状态的监控告警

## 注意事项

1. **线程安全**: 多线程环境下需要注意账户操作的线程安全
2. **数据一致性**: 确保账户数据在各个组件间的一致性
3. **异常处理**: 网络中断或数据库异常的处理机制
4. **权限管理**: 实盘环境下的账户权限和安全控制

## 相关模块

- **QAMarket**: 提供市场预设和订单、持仓管理
- **QAUtil**: 提供基础工具和数据库连接
- **QAStrategy**: 策略回测和实盘交易中使用QIFI账户