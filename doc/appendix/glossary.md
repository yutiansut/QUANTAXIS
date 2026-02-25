# 术语表

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本文档包含QUANTAXIS及量化交易中常用术语的定义和解释。

---

## 📚 核心概念

### QUANTAXIS
全方位Python量化金融框架，提供数据获取、策略开发、回测和实盘交易的完整解决方案。

### QIFI (Quantitative Investment Framework Interface)
QUANTAXIS统一账户系统接口，支持Python/Rust/C++多语言，实现跨市场、跨语言的标准化账户管理。

### QARS2 (QUANTAXIS Rust)
QUANTAXIS的Rust实现，通过Rust语言实现100倍性能提升，提供高性能数据处理和指标计算。

### QADataFrame
QUANTAXIS自定义数据结构，基于pandas DataFrame扩展，提供金融数据特有的操作和方法。

---

## 💰 交易术语

### 多头 (Long Position)
买入持有某个资产，预期价格上涨获利。也称"做多"。

**示例**: 
```python
self.BuyOpen('rb2501', 1)  # 开多头仓位
```

### 空头 (Short Position)
卖出某个资产，预期价格下跌获利。也称"做空"。

**示例**:
```python
self.SellOpen('rb2501', 1)  # 开空头仓位
```

### 开仓 (Open Position)
建立新的交易头寸（多头或空头）。

### 平仓 (Close Position)
关闭现有的交易头寸。

**示例**:
```python
self.SellClose('rb2501', 1)  # 平多头仓位
self.BuyClose('rb2501', 1)   # 平空头仓位
```

### 持仓 (Position)
当前持有的资产数量和状态。

### 滑点 (Slippage)
实际成交价格与期望价格之间的差异。

**示例**:
```python
strategy = MyStrategy(slippage=0.0001)  # 设置滑点0.01%
```

### 手续费 (Commission)
交易时支付给券商的费用。

**示例**:
```python
strategy = MyStrategy(commission=0.0003)  # 手续费0.03%
```

### 保证金 (Margin)
期货交易时需要缴纳的履约保证金。

### 杠杆 (Leverage)
使用借入资金进行交易，放大收益和风险。

---

## 📊 技术指标

### MA (Moving Average)
移动平均线，计算一定周期内的平均价格。

**示例**:
```python
ma20 = QA.MA(data['close'], 20)  # 20日均线
```

### MACD (Moving Average Convergence Divergence)
指数平滑异同移动平均线，用于判断趋势和买卖时机。

**组成**: DIF（快线）、DEA（慢线）、MACD（柱状图）

**示例**:
```python
macd = QA.MACD(data['close'])
```

### KDJ
随机指标，用于判断超买超卖。

**组成**: K值、D值、J值

### RSI (Relative Strength Index)
相对强弱指标，测量价格动量。

**示例**:
```python
rsi = QA.RSI(data['close'], 14)  # 14日RSI
```

### ATR (Average True Range)
平均真实波幅，衡量市场波动性。

### Bollinger Bands
布林带，价格波动区间指标。

**组成**: 上轨、中轨（MA）、下轨

---

## 📈 策略术语

### CTA (Commodity Trading Advisor)
商品交易顾问策略，基于技术分析的趋势跟踪策略。

### Alpha策略
寻求与市场相关性低的绝对收益策略。

### Beta策略
获取市场整体收益的策略，与市场高度相关。

### 套利 (Arbitrage)
利用不同市场或合约间的价差获利。

**类型**:
- 跨期套利
- 跨品种套利
- 跨市场套利

### 对冲 (Hedging)
通过相反方向的交易降低风险敞口。

**示例**:
```python
self.BuyOpen('rb2501', 1)   # 买入现货
self.SellOpen('rb2502', 1)  # 卖出远月合约对冲
```

### 因子 (Factor)
影响资产收益的特征变量。

**常见因子**:
- 价值因子
- 动量因子
- 质量因子
- 低波动因子

---

## 📉 风险指标

### 最大回撤 (Maximum Drawdown)
从最高点到最低点的最大跌幅。

**计算**:
```python
max_drawdown = (peak - trough) / peak
```

### 夏普比率 (Sharpe Ratio)
单位风险的超额收益，衡量风险调整后的收益。

**公式**:
```
Sharpe = (Return - RiskFreeRate) / Volatility
```

**示例**:
```python
sharpe = strategy.acc.sharpe_ratio
```

### 卡尔玛比率 (Calmar Ratio)
年化收益率与最大回撤的比值。

### 索提诺比率 (Sortino Ratio)
类似夏普比率，但只考虑下行风险。

### 信息比率 (Information Ratio)
相对基准的超额收益与跟踪误差的比值。

### 胜率 (Win Rate)
盈利交易占总交易的比例。

**计算**:
```python
win_rate = win_trades / total_trades
```

### 盈亏比 (Profit/Loss Ratio)
平均盈利与平均亏损的比值。

**计算**:
```python
pl_ratio = avg_profit / avg_loss
```

---

## 🔄 回测术语

### 回测 (Backtesting)
使用历史数据测试交易策略的过程。

### 样本内测试 (In-Sample Testing)
使用训练数据测试策略。

### 样本外测试 (Out-of-Sample Testing)
使用未参与优化的数据测试策略。

### 向前分析 (Walk-Forward Analysis)
滚动优化和测试的方法。

### 过拟合 (Overfitting)
策略过度适应历史数据，实际表现不佳。

### 未来函数 (Look-Ahead Bias)
使用未来数据做决策，导致回测结果虚高。

**示例**:
```python
# ❌ 错误：使用当前bar数据
if bar.close > bar.open:
    self.BuyOpen(bar.code, 1, bar.close)

# ✅ 正确：使用历史数据
if self.last_close > self.last_open:
    self.BuyOpen(bar.code, 1)
```

---

## 🏛️ 市场术语

### A股
中国大陆证券市场人民币普通股票。

### 期货 (Futures)
标准化远期合约，约定未来某时间以特定价格交易。

**主要交易所**:
- 上期所 (SHFE)
- 大商所 (DCE)
- 郑商所 (CZCE)
- 中金所 (CFFEX)

### 期权 (Options)
买方有权在未来以约定价格买卖标的的合约。

**类型**:
- 看涨期权 (Call Option)
- 看跌期权 (Put Option)

### 数字货币 (Cryptocurrency)
基于区块链技术的数字资产。

### Tick数据
最小价格变动单位的逐笔成交数据。

### K线 (Candlestick)
显示一定时间内开盘价、收盘价、最高价、最低价的图形。

**类型**:
- 分钟线 (1min, 5min, 15min, 30min, 60min)
- 日线 (day)
- 周线 (week)
- 月线 (month)

---

## 💻 技术术语

### EventMQ
基于RabbitMQ的事件消息队列，用于实盘交易的异步通信。

### MongoDB
文档型NoSQL数据库，QUANTAXIS的主要数据存储。

### ClickHouse
列式存储数据库，用于大规模数据分析。

### PyO3
Python-Rust绑定库，QARS2使用PyO3实现Python接口。

### Apache Arrow
跨语言的列式内存数据格式，实现零拷贝数据交换。

### Docker
容器化技术，用于应用打包和部署。

### Kubernetes
容器编排平台，用于大规模容器化应用管理。

---

## 🔧 系统组件

### XServer
QUANTAXIS中间件服务器，处理GUI和交易系统间的通信。

### XMonitor
QUANTAXIS监控客户端（GUI），基于Qt开发。

### XMarketCenter
行情网关，连接各类数据源并分发行情数据。

### XTrader
交易网关，连接券商接口执行交易。

### XRiskJudge
风控引擎，实时监控和拦截高风险交易。

### XQuant
策略引擎，运行交易策略。

---

## 📊 数据频率

### 日线 (day/1day)
每个交易日一根K线。

### 周线 (week/1week)
每周一根K线。

### 月线 (month/1month)
每月一根K线。

### 分钟线
- 1min: 1分钟K线
- 5min: 5分钟K线
- 15min: 15分钟K线
- 30min: 30分钟K线
- 60min: 60分钟K线

### Tick
逐笔成交数据，最小时间粒度。

---

## 🎯 策略类型

### QAStrategyCtaBase
CTA策略基类，用于期货趋势跟踪策略。

### QAMultiBase
多标的策略基类，支持同时交易多个品种。

### QAHedgeBase
对冲策略基类，支持多空组合策略。

### QAFactorBase
因子策略基类，用于因子选股和轮动策略。

---

## 📝 账户术语

### account_cookie
账户唯一标识符。

### init_cash
初始资金。

### balance
当前账户权益（现金+持仓市值）。

### available
可用资金。

### margin
保证金占用。

### position_profit
持仓盈亏。

### float_profit
浮动盈亏。

### frozen
冻结资金（未成交订单）。

---

## 🔗 相关资源

- **快速开始**: [快速入门](../README.md)
- **用户指南**: [用户手册](../user-guide/README.md)
- **常见问题**: [FAQ](./faq.md)

---

## 📝 总结

术语分类：

✅ **核心概念**: QUANTAXIS、QIFI、QARS2  
✅ **交易术语**: 多空、开平仓、滑点、手续费  
✅ **技术指标**: MA、MACD、KDJ、RSI  
✅ **风险指标**: 夏普比率、最大回撤、胜率  
✅ **系统组件**: XServer、XTrader、XQuant  

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回文档中心](../README.md)
