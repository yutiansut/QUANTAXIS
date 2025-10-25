# QAStrategy 模块文档

## 概述

QAStrategy 是 QUANTAXIS 的策略框架模块，提供了完整的量化交易策略开发、回测和执行环境。支持 CTA、套利、多因子等多种策略类型，集成 QIFI 账户系统进行风险管理。

## 模块架构

### 核心组件

1. **qactabase.py**: CTA策略基类
2. **qahedgebase.py**: 套利策略基类
3. **qafactorbase.py**: 因子策略基类
4. **qamultibase.py**: 多策略管理基类
5. **syncoms.py**: 策略同步通信
6. **util.py**: 策略工具函数

## 策略类型

### 1. CTA策略 (qactabase.py)

```python
from QUANTAXIS.QAStrategy.qactabase import QACTABase

class MyTrendStrategy(QACTABase):
    def __init__(self):
        super().__init__()
        self.period = 20

    def on_bar(self, bar):
        # 计算技术指标
        ma = self.data.ma(self.period)

        # 交易信号
        if bar.close > ma.iloc[-1]:
            self.buy(bar.code, 100, bar.close)
        elif bar.close < ma.iloc[-1]:
            self.sell(bar.code, 100, bar.close)

    def on_trade(self, trade):
        print(f"交易执行: {trade}")
```

### 2. 套利策略 (qahedgebase.py)

```python
from QUANTAXIS.QAStrategy.qahedgebase import QAHedgeBase

class SpreadStrategy(QAHedgeBase):
    def __init__(self):
        super().__init__()
        self.code1 = 'IF2012'
        self.code2 = 'IC2012'

    def on_bar(self, bar):
        # 计算价差
        spread = bar[self.code1].close - bar[self.code2].close

        # 套利信号
        if spread > self.upper_threshold:
            self.sell(self.code1, 1)  # 卖出IF
            self.buy(self.code2, 1)   # 买入IC
        elif spread < self.lower_threshold:
            self.buy(self.code1, 1)   # 买入IF
            self.sell(self.code2, 1)  # 卖出IC
```

### 3. 因子策略 (qafactorbase.py)

```python
from QUANTAXIS.QAStrategy.qafactorbase import QAFactorBase

class MultiFactorStrategy(QAFactorBase):
    def __init__(self):
        super().__init__()

    def calculate_factors(self, data):
        # 计算多个因子
        factors = {}
        factors['momentum'] = self.calc_momentum(data)
        factors['mean_reversion'] = self.calc_mean_reversion(data)
        factors['volatility'] = self.calc_volatility(data)
        return factors

    def factor_signal(self, factors):
        # 因子合成信号
        signal = (factors['momentum'] * 0.4 +
                 factors['mean_reversion'] * 0.3 +
                 factors['volatility'] * 0.3)
        return signal
```

## 策略生命周期

### 1. 初始化阶段

```python
def initialize(self):
    # 策略参数设置
    self.universe = ['000001', '000002', '000858']
    self.lookback = 20
    self.rebalance_frequency = 'D'

    # 初始化指标
    self.indicators = {}

    # 设置手续费
    self.set_commission(0.0003)
```

### 2. 数据处理阶段

```python
def handle_data(self, data):
    # 数据预处理
    clean_data = self.clean_data(data)

    # 计算技术指标
    self.indicators['ma20'] = clean_data.ma(20)
    self.indicators['rsi'] = clean_data.rsi(14)

    # 生成交易信号
    signals = self.generate_signals(clean_data)

    # 执行交易
    self.execute_trades(signals)
```

### 3. 风险管理

```python
def risk_management(self, position):
    # 止损检查
    if position.unrealized_pnl < -self.max_loss:
        self.close_position(position.code)

    # 持仓检查
    if position.volume > self.max_position:
        excess = position.volume - self.max_position
        self.sell(position.code, excess)

    # 集中度检查
    total_value = self.account.total_value
    if position.market_value / total_value > 0.1:
        self.reduce_position(position.code)
```

## 回测框架

### 1. 回测配置

```python
# 回测参数设置
backtest_config = {
    'start_date': '2020-01-01',
    'end_date': '2020-12-31',
    'initial_cash': 1000000,
    'universe': ['000001', '000002', '000858'],
    'frequency': 'D',
    'commission': 0.0003,
    'slippage': 0.001
}
```

### 2. 回测执行

```python
from QUANTAXIS import QA_Backtest

# 创建回测实例
backtest = QA_Backtest()

# 设置策略
backtest.set_strategy(MyTrendStrategy)

# 设置参数
backtest.set_config(backtest_config)

# 运行回测
results = backtest.run()

# 分析结果
performance = backtest.analyze_performance(results)
```

## 实盘交易

### 1. 实盘配置

```python
# 实盘交易配置
live_config = {
    'broker': 'CTP',
    'account': 'your_account',
    'password': 'your_password',
    'strategy_id': 'trend_strategy_v1'
}
```

### 2. 实盘执行

```python
from QUANTAXIS import QA_LiveTrading

# 创建实盘交易实例
live_trading = QA_LiveTrading()

# 设置策略和配置
live_trading.set_strategy(MyTrendStrategy)
live_trading.set_config(live_config)

# 启动实盘交易
live_trading.start()
```

## 多策略管理

```python
from QUANTAXIS.QAStrategy.qamultibase import QAMultiBase

class PortfolioManager(QAMultiBase):
    def __init__(self):
        super().__init__()
        self.strategies = []

    def add_strategy(self, strategy, weight):
        self.strategies.append({
            'strategy': strategy,
            'weight': weight
        })

    def allocate_capital(self, total_capital):
        for item in self.strategies:
            allocated = total_capital * item['weight']
            item['strategy'].set_capital(allocated)

    def run_strategies(self, data):
        results = []
        for item in self.strategies:
            result = item['strategy'].handle_data(data)
            results.append(result)
        return self.combine_results(results)
```

## 策略同步 (syncoms.py)

```python
from QUANTAXIS.QAStrategy.syncoms import QASyncCommunicator

# 策略间通信
communicator = QASyncCommunicator()

# 发送信号
communicator.send_signal('strategy_a', 'buy_signal', {'code': '000001'})

# 接收信号
def on_signal_received(sender, signal_type, data):
    if signal_type == 'buy_signal':
        self.handle_buy_signal(data)

communicator.subscribe('strategy_b', on_signal_received)
```

## 性能评估

### 1. 收益指标

```python
# 计算策略收益指标
def calculate_returns(strategy_results):
    returns = strategy_results['returns']

    metrics = {
        'total_return': returns.sum(),
        'annual_return': returns.mean() * 252,
        'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252),
        'max_drawdown': calculate_max_drawdown(returns),
        'win_rate': (returns > 0).sum() / len(returns)
    }

    return metrics
```

### 2. 风险指标

```python
# 计算风险指标
def calculate_risk_metrics(returns):
    return {
        'volatility': returns.std() * np.sqrt(252),
        'skewness': returns.skew(),
        'kurtosis': returns.kurtosis(),
        'var_95': returns.quantile(0.05),
        'cvar_95': returns[returns <= returns.quantile(0.05)].mean()
    }
```

## 最佳实践

1. **策略开发**:
   - 先在回测环境验证策略逻辑
   - 进行充分的历史数据测试
   - 考虑交易成本和滑点影响

2. **风险控制**:
   - 设置合理的止损和止盈条件
   - 控制单笔交易和总持仓规模
   - 实施适当的仓位管理

3. **实盘部署**:
   - 从小资金开始实盘验证
   - 监控策略表现和系统稳定性
   - 建立异常情况处理机制

## 相关模块

- **QIFI**: 账户管理和风险控制
- **QAData**: 数据结构和技术指标
- **QAEngine**: 策略并行执行
- **QAMarket**: 订单和持仓管理