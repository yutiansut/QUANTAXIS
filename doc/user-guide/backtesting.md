# 回测系统

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本章节介绍QUANTAXIS的回测系统，包括回测引擎、参数配置、性能分析和风险评估。QUANTAXIS提供了完整的回测框架，支持股票、期货、期权等多市场回测。

---

## 📚 回测系统概览

QUANTAXIS回测系统基于事件驱动架构，采用QIFI统一账户系统，支持策略回测和实盘无缝切换。

### ✨ 核心特性

- **事件驱动**: 基于Bar/Tick事件驱动
- **QIFI账户**: 统一的多市场账户管理
- **多市场支持**: 股票、期货、期权、加密货币
- **性能分析**: 完整的收益风险指标
- **可视化**: 内置多种图表展示
- **回测实盘一体化**: 同一代码切换模式

---

## 🚀 快速开始

### 1. 基础回测示例

```python
import QUANTAXIS as QA
from QUANTAXIS.QAStrategy import QAStrategyCtaBase


class SimpleMAStrategy(QAStrategyCtaBase):
    """简单均线策略"""

    def user_init(self):
        self.ma_period = 20

    def on_bar(self, bar):
        data = self.get_code_marketdata(bar.code)
        if len(data) < self.ma_period:
            return

        close_prices = [x['close'] for x in data]
        ma = sum(close_prices[-self.ma_period:]) / self.ma_period

        # 简单的均线策略
        positions = self.acc.positions
        if bar.close > ma and (bar.code not in positions or positions[bar.code].volume_long == 0):
            self.BuyOpen(bar.code, 1)
        elif bar.close < ma and bar.code in positions and positions[bar.code].volume_long > 0:
            self.SellClose(bar.code, 1)


# 运行回测
strategy = SimpleMAStrategy(
    code='rb2501',
    frequence='15min',
    strategy_id='simple_ma',
    start='2024-01-01',
    end='2024-12-31',
    init_cash=1000000
)

strategy.run_backtest()

# 查看结果
print(f"最终权益: {strategy.acc.balance:.2f}")
print(f"收益率: {(strategy.acc.balance / strategy.acc.init_cash - 1) * 100:.2f}%")
```

---

## ⚙️ 回测参数配置

### 1. 基础参数

```python
strategy = MyStrategy(
    # 交易标的
    code='rb2501',                    # 单个合约
    # code=['rb2501', 'hc2501'],    # 或多个合约

    # 时间周期
    frequence='5min',                 # '1min', '5min', '15min', '30min', '60min', 'day'

    # 回测时间范围
    start='2024-01-01',
    end='2024-12-31',

    # 初始资金
    init_cash=1000000,

    # 策略标识
    strategy_id='my_strategy',
    portfolio='default',

    # 数据源配置（可选）
    data_host='127.0.0.1',
    data_port=5672,

    # 其他参数
    send_wx=False,                    # 微信通知
    taskid=None,                      # 任务ID
)
```

### 2. 高级参数

```python
class MyStrategy(QAStrategyCtaBase):

    def user_init(self):
        # 滑点设置
        self.slippage = 0.0002        # 0.02%滑点

        # 手续费设置
        self.commission = 0.0003      # 0.03%手续费

        # 风险控制间隔
        self.risk_check_gap = 1       # 每1分钟检查一次

        # 最大持仓
        self.max_position = 5         # 最大5手

        # 止损止盈
        self.stop_loss = 0.02         # 2%止损
        self.take_profit = 0.05       # 5%止盈
```

---

## 📊 性能分析

### 1. 基本指标

回测完成后，可以获取以下性能指标：

```python
# 运行回测
strategy.run_backtest()

# 获取账户信息
acc = strategy.acc

# ==== 收益指标 ====
init_cash = acc.init_cash
final_balance = acc.balance
total_return = (final_balance / init_cash - 1) * 100
print(f"初始资金: {init_cash:,.2f}")
print(f"最终权益: {final_balance:,.2f}")
print(f"总收益: {final_balance - init_cash:,.2f}")
print(f"收益率: {total_return:.2f}%")

# ==== 交易统计 ====
trades = list(acc.trades.values())
orders = list(acc.orders.values())
print(f"总订单数: {len(orders)}")
print(f"总成交次数: {len(trades)}")

# ==== 持仓信息 ====
positions = acc.positions
print(f"当前持仓: {len(positions)}")
```

### 2. 详细分析

```python
import pandas as pd
import numpy as np


def analyze_backtest(acc):
    """完整的回测分析"""

    # 1. 收益分析
    init_cash = acc.init_cash
    final_balance = acc.balance
    total_return_pct = (final_balance / init_cash - 1) * 100

    # 2. 交易分析
    trades = list(acc.trades.values())
    if not trades:
        print("无交易记录")
        return

    # 盈利交易统计
    profits = [t.profit for t in trades if hasattr(t, 'profit')]
    win_trades = [p for p in profits if p > 0]
    lose_trades = [p for p in profits if p < 0]

    win_rate = len(win_trades) / len(profits) * 100 if profits else 0
    avg_win = np.mean(win_trades) if win_trades else 0
    avg_loss = abs(np.mean(lose_trades)) if lose_trades else 0
    profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    # 3. 风险指标（需要权益曲线）
    # balance_series = ...  # 从历史记录获取权益序列
    # max_drawdown = calculate_max_drawdown(balance_series)

    # 打印结果
    print("=" * 50)
    print("回测分析报告")
    print("=" * 50)

    print(f"\n【收益指标】")
    print(f"  初始资金: {init_cash:,.2f}")
    print(f"  最终权益: {final_balance:,.2f}")
    print(f"  总收益: {final_balance - init_cash:,.2f}")
    print(f"  收益率: {total_return_pct:.2f}%")

    print(f"\n【交易统计】")
    print(f"  总交易次数: {len(profits)}")
    print(f"  盈利次数: {len(win_trades)}")
    print(f"  亏损次数: {len(lose_trades)}")
    print(f"  胜率: {win_rate:.2f}%")

    print(f"\n【盈亏分析】")
    print(f"  平均盈利: {avg_win:,.2f}")
    print(f"  平均亏损: {avg_loss:,.2f}")
    print(f"  盈亏比: {profit_loss_ratio:.2f}")

    if profits:
        total_profit = sum(win_trades)
        total_loss = abs(sum(lose_trades))
        net_profit = total_profit - total_loss
        print(f"  总盈利: {total_profit:,.2f}")
        print(f"  总亏损: {total_loss:,.2f}")
        print(f"  净利润: {net_profit:,.2f}")


# 使用
analyze_backtest(strategy.acc)
```

### 3. 使用QAAnalysis模块

QUANTAXIS提供了内置的分析工具：

```python
from QUANTAXIS.QAAnalysis import QA_Performance


# 创建性能分析对象
perf = QA_Performance(acc)

# 获取各项指标
annual_return = perf.annual_return      # 年化收益率
sharpe_ratio = perf.sharpe_ratio        # 夏普比率
max_drawdown = perf.max_drawdown        # 最大回撤
win_rate = perf.win_rate                # 胜率

print(f"年化收益率: {annual_return:.2f}%")
print(f"夏普比率: {sharpe_ratio:.2f}")
print(f"最大回撤: {max_drawdown:.2f}%")
print(f"胜率: {win_rate:.2f}%")

# 生成报告
perf.generate_report()
```

---

## 📈 可视化分析

### 1. 权益曲线

```python
import matplotlib.pyplot as plt


def plot_equity_curve(acc):
    """绘制权益曲线"""

    # 获取历史权益记录
    history = acc.history  # 需要策略记录历史权益

    dates = [h['datetime'] for h in history]
    balances = [h['balance'] for h in history]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, balances, label='账户权益')
    plt.axhline(y=acc.init_cash, color='r', linestyle='--', label='初始资金')
    plt.title('账户权益曲线')
    plt.xlabel('日期')
    plt.ylabel('权益')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


plot_equity_curve(strategy.acc)
```

### 2. 回撤分析

```python
def plot_drawdown(balance_series):
    """绘制回撤曲线"""

    cummax = pd.Series(balance_series).cummax()
    drawdown = (balance_series - cummax) / cummax * 100

    plt.figure(figsize=(12, 6))
    plt.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
    plt.plot(drawdown, color='red', label='回撤')
    plt.title('回撤分析')
    plt.ylabel('回撤 (%)')
    plt.xlabel('时间')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```

### 3. 收益分布

```python
def plot_returns_distribution(trades):
    """绘制收益分布"""

    profits = [t.profit for t in trades if hasattr(t, 'profit')]

    plt.figure(figsize=(10, 6))
    plt.hist(profits, bins=50, alpha=0.7, edgecolor='black')
    plt.axvline(x=0, color='r', linestyle='--', label='盈亏平衡线')
    plt.title('收益分布')
    plt.xlabel('收益')
    plt.ylabel('频数')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


plot_returns_distribution(list(strategy.acc.trades.values()))
```

---

## 🔍 回测优化

### 1. 参数优化

```python
def optimize_strategy(code, start, end):
    """参数优化示例"""

    results = []

    # 遍历参数组合
    for fast in range(5, 21, 5):
        for slow in range(20, 61, 10):
            if fast >= slow:
                continue

            # 运行回测
            strategy = MyStrategy(
                code=code,
                frequence='15min',
                start=start,
                end=end,
                init_cash=1000000
            )

            # 设置参数
            strategy.fast_period = fast
            strategy.slow_period = slow

            # 运行
            strategy.run_backtest()

            # 记录结果
            final_balance = strategy.acc.balance
            return_pct = (final_balance / strategy.acc.init_cash - 1) * 100

            results.append({
                'fast': fast,
                'slow': slow,
                'return': return_pct,
                'balance': final_balance
            })

            print(f"快线{fast} 慢线{slow}: 收益率{return_pct:.2f}%")

    # 找出最优参数
    best = max(results, key=lambda x: x['return'])
    print(f"\n最优参数: 快线{best['fast']}, 慢线{best['slow']}, 收益率{best['return']:.2f}%")

    return results


# 运行优化
results = optimize_strategy('rb2501', '2024-01-01', '2024-12-31')
```

### 2. 走势期优化

为避免过拟合，使用走势期和样本外测试：

```python
# 训练期
train_start = '2024-01-01'
train_end = '2024-06-30'

# 测试期
test_start = '2024-07-01'
test_end = '2024-12-31'

# 在训练期优化参数
train_results = optimize_strategy('rb2501', train_start, train_end)
best_params = max(train_results, key=lambda x: x['return'])

# 在测试期验证
strategy = MyStrategy(
    code='rb2501',
    frequence='15min',
    start=test_start,
    end=test_end,
    init_cash=1000000
)
strategy.fast_period = best_params['fast']
strategy.slow_period = best_params['slow']
strategy.run_backtest()

test_return = (strategy.acc.balance / strategy.acc.init_cash - 1) * 100
print(f"样本外收益率: {test_return:.2f}%")
```

---

## ⚠️ 回测注意事项

### 1. 避免未来函数

```python
# ❌ 错误：使用当前bar的close
def on_bar(self, bar):
    if bar.close > self.ma:
        self.BuyOpen(bar.code, 1)

# ✅ 正确：使用上一根bar的数据
def on_bar(self, bar):
    data = self.get_code_marketdata(bar.code)
    if len(data) >= 2:
        last_close = data[-2]['close']
        if last_close > self.ma:
            self.BuyOpen(bar.code, 1)
```

### 2. 考虑交易成本

```python
def user_init(self):
    # 设置滑点
    self.slippage = 0.0002  # 双边0.04%

    # 设置手续费
    self.commission = 0.0003  # 双边0.06%

    # 总成本约0.1%
```

### 3. 考虑市场容量

```python
# 大资金策略需要考虑成交量限制
def on_bar(self, bar):
    # 检查成交量
    if bar.volume < 1000:  # 成交量太小
        return

    # 按成交量比例下单
    max_volume = int(bar.volume * 0.01)  # 不超过1%成交量
    volume = min(self.target_volume, max_volume)
```

### 4. 数据质量检查

```python
def validate_data(data):
    """验证数据质量"""

    # 检查缺失值
    if data.isnull().any().any():
        print("⚠️ 数据存在缺失值")
        return False

    # 检查异常值
    if (data['high'] < data['low']).any():
        print("⚠️ 存在high < low的异常数据")
        return False

    if (data['close'] > data['high']).any() or (data['close'] < data['low']).any():
        print("⚠️ close超出high/low范围")
        return False

    return True
```

---

## 📝 常见问题

### Q1: 回测结果不稳定？

**A**: 可能原因：

1. **样本量不足**: 增加回测时间范围
2. **参数过拟合**: 使用交叉验证
3. **数据质量问题**: 检查数据完整性
4. **策略逻辑缺陷**: 简化策略，增强鲁棒性

### Q2: 回测收益高但实盘差？

**A**: 常见原因：

1. **未考虑交易成本**: 设置真实的滑点和手续费
2. **使用了未来函数**: 检查信号生成逻辑
3. **数据偏差**: 回测数据和实盘数据不一致
4. **市场环境变化**: 策略不适应新市场

### Q3: 如何评估策略质量？

**A**: 综合评估指标：

```python
# 1. 收益指标
#    - 年化收益率 > 15%（中等）
#    - 收益率/最大回撤 > 2（良好）

# 2. 风险指标
#    - 夏普比率 > 1.5（良好）
#    - 最大回撤 < 20%（可接受）

# 3. 交易指标
#    - 胜率 > 50%（趋势策略）
#    - 盈亏比 > 1.5（均值回归策略）

# 4. 稳定性
#    - 样本内外收益差异 < 30%
#    - 月度胜率 > 60%
```

---

## 🔗 相关资源

- **策略开发**: [策略开发指南](./strategy-development.md)
- **数据获取**: [数据获取指南](./data-fetching.md)
- **实盘交易**: [实盘交易指南](./live-trading.md)

---

## 📝 总结

QUANTAXIS回测系统提供了：

✅ **事件驱动架构**: 高效的回测引擎
✅ **完整指标**: 收益、风险、交易统计
✅ **可视化分析**: 多种图表展示
✅ **参数优化**: 支持参数寻优
✅ **回测实盘一体化**: 无缝切换

**下一步**: 学习如何进行[实盘交易](./live-trading.md)

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[← 上一页：策略开发](./strategy-development.md) | [下一页：实盘交易 →](./live-trading.md)
