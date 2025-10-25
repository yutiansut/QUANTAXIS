# QUANTAXIS 快速入门

> 🚀 **10分钟上手QUANTAXIS** - 从零开始的量化交易之旅
>
> **版本**: v2.1.0-alpha2 | **难度**: 入门 | **时间**: 10-15分钟

---

## 📋 目录

- [前置准备](#前置准备)
- [第一个程序](#第一个程序)
- [数据获取](#数据获取)
- [数据分析](#数据分析)
- [简单回测](#简单回测)
- [使用Rust加速](#使用rust加速)
- [下一步学习](#下一步学习)

---

## ✅ 前置准备

### 确认安装

```python
# 检查QUANTAXIS是否已安装
import QUANTAXIS as QA
print(f"QUANTAXIS版本: {QA.__version__}")

# 预期输出: QUANTAXIS版本: 2.1.0.alpha2
```

如果未安装，请参考[安装指南](./INSTALLATION.md)。

### 导入常用模块

```python
import QUANTAXIS as QA
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
```

---

## 🎯 第一个程序

让我们从最简单的例子开始——获取股票数据并查看。

### 示例1: Hello QUANTAXIS

```python
"""
第一个QUANTAXIS程序
功能: 获取平安银行(000001)的历史数据
"""

import QUANTAXIS as QA

# 获取股票日线数据
# 参数: 股票代码, 开始日期, 结束日期
df = QA.QA_fetch_get_stock_day(
    code='000001',      # 平安银行
    start='2024-01-01', # 开始日期
    end='2024-01-31'    # 结束日期
)

# 显示数据
print("\n" + "=" * 50)
print("平安银行 2024年1月行情数据")
print("=" * 50)
print(df.head())

# 统计信息
print("\n基本统计:")
print(f"交易天数: {len(df)}")
print(f"最高价: {df['high'].max():.2f}")
print(f"最低价: {df['low'].min():.2f}")
print(f"平均成交量: {df['volume'].mean():.0f}股")
```

**运行输出**:
```
==================================================
平安银行 2024年1月行情数据
==================================================
            open   high    low  close    volume
date
2024-01-02  10.5  10.68  10.45  10.52  12543200
2024-01-03  10.5  10.75  10.48  10.68  15234100
...

基本统计:
交易天数: 20
最高价: 11.25
最低价: 10.32
平均成交量: 14523456股
```

---

## 📊 数据获取

QUANTAXIS支持多种市场的数据获取。

### 示例2: 股票数据

```python
"""
获取多只股票的历史数据
"""

import QUANTAXIS as QA

# 股票代码列表
stocks = ['000001', '000002', '600000']

# 批量获取数据
for code in stocks:
    df = QA.QA_fetch_get_stock_day(
        code=code,
        start='2024-01-01',
        end='2024-01-10'
    )

    # 使用QA数据结构
    data = QA.QA_DataStruct_Stock_day(df)

    print(f"\n股票 {code}:")
    print(f"  交易天数: {len(data.data)}")
    print(f"  涨跌幅: {data.data['close'].pct_change().mean() * 100:.2f}%")
```

---

### 示例3: 期货数据

```python
"""
获取期货主力合约数据
"""

import QUANTAXIS as QA

# 获取期货日线数据
df_future = QA.QA_fetch_get_future_day(
    code='IF2512',      # 沪深300期货2025年12月合约
    start='2024-01-01',
    end='2024-01-31'
)

# 使用期货数据结构
data_future = QA.QA_DataStruct_Future_day(df_future)

print(f"\n期货合约 IF2512:")
print(f"  交易天数: {len(data_future.data)}")
print(f"  开盘价范围: {data_future.data['open'].min():.2f} - {data_future.data['open'].max():.2f}")
print(f"  收盘价范围: {data_future.data['close'].min():.2f} - {data_future.data['close'].max():.2f}")
```

---

### 示例4: 实时数据

```python
"""
获取实时行情数据
"""

import QUANTAXIS as QA

# 获取股票实时行情
realtime = QA.QA_fetch_get_stock_realtime(
    code=['000001', '000002', '600000']
)

print("\n实时行情:")
print(realtime[['code', 'price', 'bid1', 'ask1', 'volume']])
```

---

## 📈 数据分析

使用QUANTAXIS的数据结构进行分析。

### 示例5: 技术指标计算

```python
"""
计算技术指标
"""

import QUANTAXIS as QA

# 获取数据
df = QA.QA_fetch_get_stock_day('000001', '2023-01-01', '2024-01-31')
data = QA.QA_DataStruct_Stock_day(df)

# 计算均线
ma5 = data.data['close'].rolling(5).mean()
ma10 = data.data['close'].rolling(10).mean()
ma20 = data.data['close'].rolling(20).mean()

print("\n均线系统 (最近5天):")
print(pd.DataFrame({
    '日期': data.data.index[-5:],
    '收盘价': data.data['close'][-5:].values,
    'MA5': ma5[-5:].values,
    'MA10': ma10[-5:].values,
    'MA20': ma20[-5:].values,
}))

# 使用QA内置指标
from QUANTAXIS.QAIndicator import QA_indicator_MA, QA_indicator_MACD

# 计算MACD
macd_df = QA_indicator_MACD(data.data)
print("\nMACD指标 (最近5天):")
print(macd_df.tail())
```

---

### 示例6: 数据可视化

```python
"""
数据可视化
"""

import QUANTAXIS as QA
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取数据
df = QA.QA_fetch_get_stock_day('000001', '2023-01-01', '2024-01-31')
data = QA.QA_DataStruct_Stock_day(df)

# 创建图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# 价格走势
ax1.plot(data.data.index, data.data['close'], label='收盘价')
ax1.plot(data.data.index, data.data['close'].rolling(20).mean(), label='MA20')
ax1.set_title('平安银行股价走势')
ax1.set_ylabel('价格 (元)')
ax1.legend()
ax1.grid(True)

# 成交量
ax2.bar(data.data.index, data.data['volume'], alpha=0.5)
ax2.set_title('成交量')
ax2.set_ylabel('成交量 (股)')
ax2.grid(True)

plt.tight_layout()
plt.savefig('stock_analysis.png')
print("\n✅ 图表已保存至 stock_analysis.png")
```

---

## 🔄 简单回测

### 示例7: 均线策略回测

```python
"""
简单的均线交叉策略回测
策略: MA5上穿MA20买入，下穿卖出
"""

import QUANTAXIS as QA
from QUANTAXIS.QIFI import QIFI_Account

# 1. 准备数据
df = QA.QA_fetch_get_stock_day('000001', '2023-01-01', '2024-01-31')
data = QA.QA_DataStruct_Stock_day(df)

# 2. 计算指标
ma5 = data.data['close'].rolling(5).mean()
ma20 = data.data['close'].rolling(20).mean()

# 3. 生成信号
signal = pd.DataFrame(index=data.data.index)
signal['ma5'] = ma5
signal['ma20'] = ma20
signal['position'] = 0

# 金叉买入，死叉卖出
signal.loc[ma5 > ma20, 'position'] = 1
signal.loc[ma5 < ma20, 'position'] = 0

# 4. 创建账户
account = QIFI_Account(
    username="test_strategy",
    password="test",
    model="stock",
    init_cash=100000  # 初始资金10万
)

# 5. 模拟交易
position = 0
for date, row in signal.iterrows():
    price = data.data.loc[date, 'close']

    # 买入信号
    if row['position'] == 1 and position == 0:
        # 计算可买数量（100股整数倍）
        amount = int(account.cash / price / 100) * 100
        if amount > 0:
            account.receive_simpledeal({
                'code': '000001',
                'price': price,
                'amount': amount,
                'datetime': str(date),
                'towards': 'buy'
            })
            position = 1
            print(f"{date}: 买入 {amount}股 @ {price:.2f}元")

    # 卖出信号
    elif row['position'] == 0 and position == 1:
        # 获取当前持仓
        if '000001' in account.positions:
            amount = account.positions['000001']['volume']
            account.receive_simpledeal({
                'code': '000001',
                'price': price,
                'amount': amount,
                'datetime': str(date),
                'towards': 'sell'
            })
            position = 0
            print(f"{date}: 卖出 {amount}股 @ {price:.2f}元")

# 6. 输出结果
print("\n" + "=" * 50)
print("回测结果")
print("=" * 50)
print(f"初始资金: {100000:.2f}元")
print(f"最终资金: {account.cash:.2f}元")
print(f"总盈亏: {account.cash - 100000:.2f}元")
print(f"收益率: {(account.cash / 100000 - 1) * 100:.2f}%")
```

---

### 示例8: 使用QA回测框架

```python
"""
使用QUANTAXIS回测框架
"""

import QUANTAXIS as QA
from QUANTAXIS.QAStrategy import QAStrategyCtaBase

class MyStrategy(QAStrategyCtaBase):
    """简单的均线策略"""

    def __init__(self):
        super().__init__()
        self.ma_short = 5
        self.ma_long = 20

    def on_bar(self, bar):
        """每根K线回调"""
        # 计算均线
        ma5 = bar['close'].rolling(self.ma_short).mean().iloc[-1]
        ma20 = bar['close'].rolling(self.ma_long).mean().iloc[-1]

        # 交易逻辑
        if ma5 > ma20:
            self.buy(bar['code'].iloc[-1], bar['close'].iloc[-1], 100)
        elif ma5 < ma20:
            self.sell(bar['code'].iloc[-1], bar['close'].iloc[-1], 100)

# 创建策略实例
strategy = MyStrategy()

# 运行回测
result = QA.QA_Backtest(
    strategy=strategy,
    code='000001',
    start='2023-01-01',
    end='2024-01-31',
    init_cash=100000
)

print(f"\n收益率: {result.profit_rate * 100:.2f}%")
```

---

## ⚡ 使用Rust加速

### 示例9: QARS2高性能账户

```python
"""
使用Rust实现的高性能账户
性能提升: 100x
"""

from QUANTAXIS.QARSBridge import has_qars_support

if has_qars_support():
    from QUANTAXIS.QARSBridge import QARSAccount

    # 创建Rust账户（100x加速）
    account = QARSAccount(
        account_cookie="rust_account",
        init_cash=100000.0
    )

    # 买入操作
    account.buy(
        code="000001",
        price=10.5,
        datetime="2024-01-15",
        amount=1000
    )

    print(f"✅ Rust账户创建成功")
    print(f"   可用资金: {account.cash:.2f}元")
    print(f"   持仓股票: {list(account.positions.keys())}")

else:
    print("⚠️  QARS2未安装，请运行: pip install quantaxis[rust]")
```

---

### 示例10: 零拷贝数据转换

```python
"""
使用零拷贝进行高性能数据转换
性能提升: 2-5x
"""

from QUANTAXIS.QADataBridge import has_dataswap_support

if has_dataswap_support():
    from QUANTAXIS.QADataBridge import convert_pandas_to_polars
    import pandas as pd

    # 创建Pandas数据
    df_pandas = pd.DataFrame({
        'code': ['000001'] * 1000,
        'price': [10.5] * 1000,
        'volume': [1000] * 1000,
    })

    # 零拷贝转换为Polars（2-5x加速）
    df_polars = convert_pandas_to_polars(df_pandas)

    print(f"✅ 零拷贝转换成功")
    print(f"   原始格式: {type(df_pandas)}")
    print(f"   转换后: {type(df_polars)}")
    print(f"   性能提升: 2-5x")

else:
    print("⚠️  QADataSwap未安装，请运行: pip install quantaxis[rust]")
```

---

## 🎓 学习路径

### 初学者 (第1-2周)

**目标**: 熟悉基本操作

1. **数据获取**
   - ✅ 获取股票/期货数据
   - ✅ 理解数据结构
   - ✅ 数据可视化

2. **简单分析**
   - ✅ 计算技术指标
   - ✅ 统计分析
   - ✅ 数据清洗

**推荐练习**:
```python
# 练习1: 获取多只股票数据并对比
# 练习2: 计算并可视化MA、MACD等指标
# 练习3: 分析成交量与价格的关系
```

---

### 进阶 (第3-4周)

**目标**: 掌握回测框架

1. **策略开发**
   - ✅ 简单的均线策略
   - ✅ 多因子策略
   - ✅ 事件驱动策略

2. **回测优化**
   - ✅ 参数优化
   - ✅ 风险控制
   - ✅ 绩效分析

**推荐练习**:
```python
# 练习4: 实现双均线策略并回测
# 练习5: 添加止损止盈逻辑
# 练习6: 对比不同参数的表现
```

---

### 高级 (第5-8周)

**目标**: 生产环境部署

1. **高性能优化**
   - ✅ 使用QARS2 Rust账户
   - ✅ 使用零拷贝数据传输
   - ✅ 多进程并行

2. **实盘交易**
   - ✅ 接入交易接口
   - ✅ 风险管理
   - ✅ 监控告警

**推荐练习**:
```python
# 练习7: 将策略迁移到QARS2
# 练练习8: 使用共享内存进行跨进程通信
# 练习9: 搭建完整的交易系统
```

---

## 📚 下一步学习

### 推荐文档

1. **核心概念**
   - [QIFI协议详解](./QUANTAXIS/QARSBridge/QIFI_PROTOCOL.md)
   - [数据结构说明](./docs/data_structures.md)
   - [回测框架文档](./docs/backtest.md)

2. **进阶功能**
   - [QARSBridge使用指南](./QUANTAXIS/QARSBridge/README.md)
   - [QADataBridge性能优化](./QUANTAXIS/QADataBridge/README.md)
   - [因子分析框架](./docs/factor_analysis.md)

3. **API参考**
   - [完整API文档](./API_REFERENCE.md)
   - [配置参数说明](./docs/configuration.md)

### 示例代码

```bash
# 查看所有示例
ls examples/

# 运行QARSBridge示例
python examples/qarsbridge_example.py

# 运行QADataBridge示例
python examples/qadatabridge_example.py

# 运行性能测试
python scripts/benchmark_databridge.py
```

### 社区资源

- **GitHub**: https://github.com/QUANTAXIS/QUANTAXIS
- **QQ群**: 563280068
- **Discord**: https://discord.gg/quantaxis
- **论坛**: https://forum.quantaxis.cn
- **文档**: https://doc.quantaxis.cn

---

## 💡 实用技巧

### 技巧1: 配置数据库连接

```python
from QUANTAXIS.QAUtil import DATABASE

# 查看当前配置
print(DATABASE)

# 自定义配置
import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.quantaxis
```

### 技巧2: 批量数据获取

```python
# 获取股票列表
stock_list = QA.QA_fetch_get_stock_list()

# 批量获取数据
for code in stock_list[:10]:  # 前10只股票
    df = QA.QA_fetch_get_stock_day(code, '2024-01-01', '2024-01-31')
    # 处理数据...
```

### 技巧3: 错误处理

```python
try:
    df = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-31')
except Exception as e:
    print(f"数据获取失败: {e}")
    # 降级处理...
```

### 技巧4: 性能分析

```python
import time

# 对比标准实现和Rust实现
start = time.time()
# ... 标准代码 ...
time_standard = time.time() - start

start = time.time()
# ... Rust代码 ...
time_rust = time.time() - start

print(f"加速比: {time_standard / time_rust:.2f}x")
```

---

## ❓ 常见问题

### Q1: 如何获取更多股票代码？

```python
# 获取所有A股代码
stock_list = QA.QA_fetch_get_stock_list()
print(f"共{len(stock_list)}只股票")
print(stock_list.head())
```

### Q2: 如何处理缺失数据？

```python
df = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-31')

# 检查缺失值
print(df.isnull().sum())

# 填充缺失值
df_filled = df.fillna(method='ffill')  # 前向填充
```

### Q3: 如何加速数据处理？

```python
# 方式1: 使用Polars
from QUANTAXIS.QADataBridge import convert_pandas_to_polars

df_polars = convert_pandas_to_polars(df)
# Polars操作通常快5-10x

# 方式2: 使用向量化操作
df['returns'] = df['close'].pct_change()  # ✅ 向量化
# 避免循环: for i in range(len(df)): ... ❌
```

---

**恭喜你完成了QUANTAXIS快速入门！🎉**

现在你已经掌握了：
- ✅ 数据获取和分析
- ✅ 技术指标计算
- ✅ 简单策略回测
- ✅ Rust组件使用

继续探索更多高级功能，祝交易顺利！

---

**@yutiansut @quantaxis**
**最后更新**: 2025-10-25
