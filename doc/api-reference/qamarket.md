# QAMarket 模块文档

## 概述

QAMarket 是 QUANTAXIS 的市场交易核心模块，提供了完整的交易相关功能，包括市场预设参数、订单管理、持仓管理等。该模块为不同市场（股票、期货、期权）提供统一的交易接口和风险控制机制。

## 模块架构

### 核心组件

1. **market_preset.py**: 市场预设参数管理
   - 合约基础信息配置
   - 保证金系数设置
   - 手续费率配置
   - 价格最小变动单位

2. **QAOrder.py**: 订单管理系统
   - 订单创建和管理
   - 订单状态跟踪
   - 订单撮合逻辑

3. **QAPosition.py**: 持仓管理系统
   - 持仓计算和管理
   - 盈亏计算
   - 风险控制

## 市场预设 (MARKET_PRESET)

### 功能特性

MARKET_PRESET 类提供了各种金融品种的标准化配置信息：

#### 合约参数配置

```python
class MARKET_PRESET:
    def __init__(self):
        self.table = {
            'AG': {  # 白银
                'name': '白银',
                'unit_table': 15,                    # 合约乘数
                'price_tick': 1.0,                   # 最小变动价位
                'buy_frozen_coeff': 0.1,             # 多头保证金系数
                'sell_frozen_coeff': 0.1,            # 空头保证金系数
                'exchange': EXCHANGE_ID.SHFE,        # 交易所
                'commission_coeff_peramount': 0.00005,    # 按金额收费系数
                'commission_coeff_pervol': 0,             # 按手数收费
                'commission_coeff_today_peramount': 0.00005,  # 平今按金额收费
                'commission_coeff_today_pervol': 0        # 平今按手数收费
            }
        }
```

#### 支持的金融品种

**期货品种**:
- **贵金属**: AG(白银), AU(黄金)
- **有色金属**: AL(铝), CU(铜), ZN(锌), PB(铅), SN(锡), NI(镍)
- **黑色金属**: RB(螺纹钢), HC(热轧卷板), I(铁矿石), J(焦炭), JM(焦煤)
- **能源化工**: CU(原油), PTA(精对苯二甲酸), MA(甲醇), PP(聚丙烯)
- **农产品**: C(玉米), CS(玉米淀粉), M(豆粕), RM(菜粕), CF(棉花)

#### 主要参数说明

1. **unit_table**: 合约乘数
   - 定义每手合约对应的标的数量
   - 例: 黄金期货每手1000克

2. **price_tick**: 最小变动价位
   - 价格变动的最小单位
   - 例: 黄金期货最小变动0.02元

3. **保证金系数**:
   - **buy_frozen_coeff**: 多头开仓保证金系数
   - **sell_frozen_coeff**: 空头开仓保证金系数

4. **手续费系数**:
   - **commission_coeff_peramount**: 按成交金额收取
   - **commission_coeff_pervol**: 按成交手数收取
   - **commission_coeff_today_***: 平今仓手续费

### 使用示例

```python
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET

# 初始化市场预设
market = MARKET_PRESET()

# 获取合约信息
contract_info = market.table['AU']  # 黄金期货
print(f"合约名称: {contract_info['name']}")
print(f"合约乘数: {contract_info['unit_table']}")
print(f"最小变动价位: {contract_info['price_tick']}")
print(f"保证金系数: {contract_info['buy_frozen_coeff']}")

# 计算保证金需求
price = 400.0  # 黄金价格
volume = 1     # 手数
margin_required = price * contract_info['unit_table'] * contract_info['buy_frozen_coeff']
print(f"开仓保证金: {margin_required}")

# 计算手续费
commission = price * contract_info['unit_table'] * contract_info['commission_coeff_peramount']
print(f"手续费: {commission}")
```

## 订单管理 (QAOrder)

### 订单系统特性

1. **多市场支持**: 支持股票、期货、期权等不同市场
2. **订单状态管理**: 完整的订单生命周期跟踪
3. **风险控制**: 内置风险检查机制
4. **线程安全**: 支持多线程并发交易

### 订单方向定义

```python
from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION

# 订单方向常量
ORDER_DIRECTION.BUY          # 买入
ORDER_DIRECTION.SELL         # 卖出
ORDER_DIRECTION.BUY_OPEN     # 买开（期货）
ORDER_DIRECTION.BUY_CLOSE    # 买平（期货）
ORDER_DIRECTION.SELL_OPEN    # 卖开（期货）
ORDER_DIRECTION.SELL_CLOSE   # 卖平（期货）
```

### 订单状态管理

```python
from QUANTAXIS.QAUtil.QAParameter import ORDER_STATUS

# 订单状态
ORDER_STATUS.NEW             # 新订单
ORDER_STATUS.PENDING         # 待成交
ORDER_STATUS.PARTIALLY_FILLED # 部分成交
ORDER_STATUS.FILLED          # 已成交
ORDER_STATUS.CANCELED        # 已撤销
ORDER_STATUS.REJECTED        # 已拒绝
```

### 订单创建示例

```python
from QUANTAXIS.QAMarket.QAOrder import QA_Order

# 创建股票订单
stock_order = QA_Order(
    code='000001',
    price=10.50,
    volume=1000,
    direction=ORDER_DIRECTION.BUY,
    market_type=MARKET_TYPE.STOCK_CN
)

# 创建期货订单
future_order = QA_Order(
    code='AU2012',
    price=400.0,
    volume=1,
    direction=ORDER_DIRECTION.BUY_OPEN,
    market_type=MARKET_TYPE.FUTURE_CN
)
```

## 持仓管理 (QAPosition)

### 持仓计算功能

QA_Position 类提供了精确的持仓管理：

1. **多空持仓分离**: 分别管理多头和空头持仓
2. **成本计算**: 动态计算持仓成本
3. **盈亏计算**: 实时计算浮动盈亏和实现盈亏
4. **风险监控**: 持仓风险指标计算

### 主要功能方法

```python
from QUANTAXIS.QAMarket.QAPosition import QA_Position

# 创建持仓对象
position = QA_Position()

# 更新持仓
position.update_pos(
    code='AU2012',
    direction='BUY',
    volume=1,
    price=400.0
)

# 获取持仓信息
pos_info = position.get_position('AU2012')
print(f"持仓量: {pos_info['volume']}")
print(f"持仓成本: {pos_info['cost_price']}")
print(f"浮动盈亏: {pos_info['float_pnl']}")

# 平仓操作
position.close_position(
    code='AU2012',
    volume=1,
    price=405.0
)
```

### 持仓风险指标

```python
# 计算持仓价值
position_value = position.get_position_value()

# 计算保证金占用
margin_used = position.get_margin_used()

# 计算风险度
risk_ratio = margin_used / total_balance

# 获取盈亏统计
pnl_stats = position.get_pnl_statistics()
```

## 交易所配置

### 支持的交易所

```python
from QUANTAXIS.QAUtil.QAParameter import EXCHANGE_ID

# 中国期货交易所
EXCHANGE_ID.SHFE    # 上海期货交易所
EXCHANGE_ID.DCE     # 大连商品交易所
EXCHANGE_ID.CZCE    # 郑州商品交易所
EXCHANGE_ID.CFFEX   # 中国金融期货交易所
EXCHANGE_ID.INE     # 上海国际能源交易中心

# 股票交易所
EXCHANGE_ID.SSE     # 上海证券交易所
EXCHANGE_ID.SZSE    # 深圳证券交易所
```

## 风险控制机制

### 1. 保证金控制

```python
def check_margin_requirement(account, order):
    """检查保证金是否充足"""
    required_margin = calculate_margin(order)
    available_balance = account.get_available_balance()

    if required_margin > available_balance:
        raise InsufficientMarginError("保证金不足")

    return True
```

### 2. 持仓限制

```python
def check_position_limit(account, order):
    """检查持仓限制"""
    current_position = account.get_position(order.code)
    position_limit = get_position_limit(order.code)

    new_position = current_position + order.volume
    if new_position > position_limit:
        raise PositionLimitExceeded("超出持仓限制")

    return True
```

### 3. 价格检查

```python
def check_price_limit(order):
    """检查价格限制"""
    limit_up, limit_down = get_price_limits(order.code)

    if order.price > limit_up or order.price < limit_down:
        raise PriceLimitExceeded("价格超出涨跌停限制")

    return True
```

## 实际应用场景

### 1. 期货套利交易

```python
# 跨期套利示例
def cross_month_arbitrage():
    # 买入近月合约
    near_order = QA_Order(
        code='AU2012',
        price=400.0,
        volume=1,
        direction=ORDER_DIRECTION.BUY_OPEN
    )

    # 卖出远月合约
    far_order = QA_Order(
        code='AU2103',
        price=405.0,
        volume=1,
        direction=ORDER_DIRECTION.SELL_OPEN
    )

    return [near_order, far_order]
```

### 2. 股票量化交易

```python
# 股票买卖示例
def stock_trading_strategy():
    # 买入信号
    buy_order = QA_Order(
        code='000001',
        price=10.50,
        volume=1000,
        direction=ORDER_DIRECTION.BUY,
        market_type=MARKET_TYPE.STOCK_CN
    )

    # 设置止损单
    stop_loss_order = QA_Order(
        code='000001',
        price=9.50,
        volume=1000,
        direction=ORDER_DIRECTION.SELL,
        order_type='STOP_LOSS'
    )

    return [buy_order, stop_loss_order]
```

## 最佳实践

1. **合约配置维护**:
   - 定期更新合约参数
   - 关注交易所规则变化
   - 及时调整保证金和手续费率

2. **风险管理**:
   - 设置合理的持仓限制
   - 实施严格的保证金控制
   - 建立完善的风险监控体系

3. **性能优化**:
   - 使用缓存机制提高查询效率
   - 批量处理订单减少系统开销
   - 合理设计持仓数据结构

## 相关模块

- **QIFI**: 账户管理，使用QAMarket的订单和持仓功能
- **QAStrategy**: 策略模块，基于QAMarket进行交易决策
- **QAUtil**: 提供基础参数和工具函数支持