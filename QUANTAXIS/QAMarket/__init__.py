# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2025 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
QAMarket - 市场预设和订单/持仓管理模块

本模块提供QUANTAXIS核心的市场交易相关功能:

1. **市场预设 (market_preset)**:
   - MARKET_PRESET: 期货/股票市场合约参数预设
   - 提供: 合约乘数、最小跳价、保证金系数、手续费系数等

2. **订单管理 (QAOrder)**:
   - QA_Order: 单个订单对象 (QIFI协议兼容)
   - QA_OrderQueue: 订单队列管理器

3. **持仓管理 (QAPosition)**:
   - QA_Position: 单标的精准仓位管理 (多空分离/今昨分离)
   - QA_PMS: 多标的持仓管理系统 (Portfolio Management System)

## 快速开始

### 1. 使用市场预设获取合约参数
```python
from QUANTAXIS.QAMarket import MARKET_PRESET

# 获取螺纹钢合约信息
preset = MARKET_PRESET()
rb_info = preset.get_code('RB')
print(f"合约乘数: {rb_info['unit_table']}")  # 10
print(f"最小跳价: {rb_info['price_tick']}")   # 1.0
print(f"保证金率: {rb_info['buy_frozen_coeff']}")  # 0.12
```

### 2. 创建订单对象
```python
from QUANTAXIS.QAMarket import QA_Order

order = QA_Order(
    account_cookie='account_001',
    code='000001',
    price=10.5,
    amount=1000,
    order_direction='BUY',  # 买入
    market_type='STOCK_CN'
)
print(order.order_id)  # 自动生成的订单ID
```

### 3. 管理持仓
```python
from QUANTAXIS.QAMarket import QA_Position

# 创建期货持仓 (多空分离/今昨分离)
position = QA_Position(
    code='RB2512',
    market_type='FUTURE_CN'
)

# 开多仓
position.open_long(price=3500, volume=10, datetime='2024-01-15')
print(f"多头持仓: {position.volume_long}")  # 10
print(f"保证金: {position.margin_long}")    # 42000.0 (3500*10*10*0.12)

# 平仓
position.close_long(price=3550, volume=5, datetime='2024-01-16')
print(f"浮动盈亏: {position.float_profit_long}")  # 2500.0 ((3550-3500)*5*10)
```

### 4. 多标的持仓管理
```python
from QUANTAXIS.QAMarket import QA_PMS

# 创建持仓管理系统
pms = QA_PMS(account_cookie='account_001')

# 管理多个持仓
pms.update_pos('RB2512', volume_long=10, price=3500)
pms.update_pos('CU2512', volume_long=5, price=72500)

# 查询总体风险
total_margin = sum([pos.margin for pos in pms.positions.values()])
print(f"总保证金: {total_margin}")
```

## 模块结构

- **market_preset.py**: 市场参数预设表 (期货/股票/期权)
- **QAOrder.py**: 订单类和订单队列
- **QAPosition.py**: 持仓类和持仓管理系统

## QIFI协议兼容

QAMarket模块的订单/持仓结构完全兼容QIFI (QuantAxis Interoperable Financial Interface)协议,
支持跨语言(Python/Rust/C++)和跨系统的数据交换。

## 作者

@yutiansut @quantaxis

## 版本

v2.1.0+ (2025)
"""

# 市场预设
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET

# 订单管理
from QUANTAXIS.QAMarket.QAOrder import (
    QA_Order,
    QA_OrderQueue
)

# 持仓管理
from QUANTAXIS.QAMarket.QAPosition import (
    QA_Position,
    QA_PMS
)

__all__ = [
    # 市场预设
    'MARKET_PRESET',

    # 订单
    'QA_Order',
    'QA_OrderQueue',

    # 持仓
    'QA_Position',
    'QA_PMS',
]

__version__ = '2.1.0'
__author__ = 'yutiansut/quantaxis'
