# QUANTAXIS 其他模块文档

## QAFactor - 因子研究模块

### 概述
QAFactor 提供完整的因子研究工具链，包括因子计算、回测、管理和分析功能。

### 核心组件
- **feature.py**: 因子定义和计算
- **featureAnalysis.py**: 因子分析工具
- **featurebacktest.py**: 因子回测框架
- **featurepool.py**: 因子池管理
- **featureView.py**: 因子可视化

### 主要功能

```python
from QUANTAXIS.QAFactor import QAFactor

# 因子计算
factor = QAFactor()
factor.add_factor('momentum', lambda x: x.pct_change(20))
factor.add_factor('mean_reversion', lambda x: -x.rolling(20).mean())

# 因子分析
analysis = factor.analyze_factors(data)
ic_values = analysis['ic']  # 信息系数
turnover = analysis['turnover']  # 换手率

# 因子回测
backtest_result = factor.backtest(
    start_date='2020-01-01',
    end_date='2020-12-31'
)
```

---

## QAIndicator - 技术指标模块

### 概述
QAIndicator 提供丰富的技术指标计算功能，支持自定义指标和批量计算。

### 核心组件
- **indicators.py**: 基础技术指标
- **talib_indicators.py**: TA-Lib指标封装
- **base.py**: 指标基类和框架

### 主要功能

```python
from QUANTAXIS.QAIndicator import MA, RSI, MACD, BOLL

# 移动平均
ma5 = MA(close_prices, 5)
ma20 = MA(close_prices, 20)

# RSI指标
rsi = RSI(close_prices, 14)

# MACD指标
dif, dea, macd = MACD(close_prices)

# 布林带
upper, middle, lower = BOLL(close_prices, 20)

# 批量计算
indicators = QAIndicator.batch_calculate(data, ['MA', 'RSI', 'MACD'])
```

---

## QAWebServer - Web服务模块

### 概述
基于 Tornado 的 Web 服务框架，提供 API 接口和微服务架构支持。

### 核心组件
- **server.py**: 主服务器
- **basehandles.py**: 基础请求处理器
- **qifiserver.py**: QIFI账户服务
- **schedulehandler.py**: 调度处理器

### 主要功能

```python
from QUANTAXIS.QAWebServer import QAWebServer

# 创建Web服务
app = QAWebServer()

# 添加路由
@app.route('/api/data')
def get_data(request):
    return {'data': 'sample_data'}

# 启动服务
app.run(port=8888)
```

---

## QASchedule - 任务调度模块

### 概述
提供任务调度功能，支持定时任务、事件触发任务和远程任务调度。

### 核心组件
- **schedulefunc.py**: 调度函数和工具

### 主要功能

```python
from QUANTAXIS.QASchedule import QAScheduler

# 创建调度器
scheduler = QAScheduler()

# 添加定时任务
@scheduler.schedule('09:30:00')
def market_open_task():
    print("市场开盘任务")

# 添加周期任务
@scheduler.interval(minutes=5)
def data_update_task():
    print("数据更新任务")

# 启动调度器
scheduler.start()
```

---

## QAAnalysis - 分析工具模块

### 概述
提供数据分析和信号处理工具，包括统计分析和技术分析功能。

### 核心组件
- **QAAnalysis_block.py**: 板块分析
- **QAAnalysis_signal.py**: 信号分析

### 主要功能

```python
from QUANTAXIS.QAAnalysis import QAAnalysis

# 板块分析
block_analysis = QAAnalysis.analyze_blocks(stock_data)
sector_performance = block_analysis.get_sector_performance()

# 信号分析
signal_analysis = QAAnalysis.analyze_signals(signals)
signal_quality = signal_analysis.evaluate_quality()
```

---

## QACmd - 命令行模块

### 概述
提供命令行接口和工具，便于批量操作和自动化脚本。

### 主要功能

```bash
# 命令行工具
quantaxis --help                    # 查看帮助
quantaxis fetch --code 000001       # 获取数据
quantaxis backtest --strategy trend # 运行回测
```

---

## QASU - 数据存储更新模块

### 概述
QASU (QUANTAXIS Storage Update) 负责数据的存储、更新和维护。

### 核心组件
- **save_*.py**: 各种数据源的保存模块
- **main.py**: 主要存储逻辑
- **user.py**: 用户数据管理

### 主要功能

```python
from QUANTAXIS.QASU import save_stock_day, save_stock_min

# 保存股票日线数据
save_stock_day(['000001', '000002'], '2020-01-01', '2020-12-31')

# 保存股票分钟数据
save_stock_min(['000001'], '2020-01-01', '2020-01-31', '1min')

# 增量更新
from QUANTAXIS.QASU import update_stock_day
update_stock_day()  # 更新到最新日期
```

---

## QASetting - 配置管理模块

### 概述
统一的配置管理系统，管理数据库连接、系统参数等配置信息。

### 核心组件
- **QALocalize.py**: 本地化配置
- **cache.py**: 缓存管理
- **executor.py**: 执行器配置

### 主要功能

```python
from QUANTAXIS.QASetting import QASetting

# 获取配置
config = QASetting()
database_config = config.get_config('DATABASE')
mongodb_uri = config.get_config('MONGODB_URI')

# 设置配置
config.set_config('CUSTOM_SETTING', 'value')

# 保存配置
config.save_config()
```

---

## 模块间关系图

```
QAFetch ──→ QAData ──→ QAIndicator ──→ QAStrategy
   │           │           │             │
   ↓           ↓           ↓             ↓
 QASU ──→ QAAnalysis ──→ QAFactor ──→ QIFI/QAMarket
   │           │           │             │
   ↓           ↓           ↓             ↓
QASetting ──→ QAUtil ──→ QAEngine ──→ QAPubSub
   │                       │             │
   ↓                       ↓             ↓
QACmd ←── QAWebServer ←── QASchedule ←───┘
```

## 使用建议

1. **新手入门**: 从 QAFetch → QAData → QAStrategy 的路径开始学习
2. **数据管理**: 重点关注 QASU 和 QASetting 模块
3. **策略开发**: 深入学习 QAStrategy、QAFactor、QAIndicator
4. **生产部署**: 关注 QAWebServer、QASchedule、QAPubSub
5. **高级功能**: 学习 QAEngine 进行性能优化

## 最佳实践

1. **模块化开发**: 每个模块专注特定功能，避免耦合
2. **配置管理**: 使用 QASetting 统一管理配置
3. **数据流**: 遵循 数据获取→处理→分析→策略→交易 的流程
4. **性能优化**: 合理使用 QAEngine 和 QAPubSub 提升性能
5. **监控运维**: 利用 QAWebServer 和 QASchedule 建立监控体系