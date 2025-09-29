# QUANTAXIS 模块文档索引

## 文档概述

本目录包含 QUANTAXIS 量化金融框架的完整模块文档，每个文档详细介绍了相应模块的功能、架构、API和使用示例。

## 核心模块文档

### 1. [QAFetch - 数据获取模块](./QAFetch.md)
- **功能**: 多数据源统一接口，支持股票、期货、数字货币等市场数据获取
- **特点**: 多数据源适配、统一API、实时和历史数据支持
- **适用场景**: 数据获取、数据源切换、实时行情接收

### 2. [QAUtil - 工具模块](./QAUtil.md)
- **功能**: 时间处理、数据转换、配置管理等基础工具
- **特点**: 交易日历、格式转换、系统配置、性能监控
- **适用场景**: 基础工具支持、系统配置、数据预处理

### 3. [QIFI - 账户系统](./QIFI.md)
- **功能**: 统一账户管理、跨市场持仓、多语言一致性
- **特点**: 实盘/模拟支持、动态权益计算、风险控制
- **适用场景**: 账户管理、资金管理、风险控制

### 4. [QAMarket - 市场交易](./QAMarket.md)
- **功能**: 市场预设、订单管理、持仓管理
- **特点**: 多市场支持、风险控制、保证金计算
- **适用场景**: 交易执行、风险管理、市场参数配置

### 5. [QAData - 数据结构](./QAData.md)
- **功能**: 标准化数据容器、数据处理、技术指标集成
- **特点**: 多市场数据结构、数据重采样、复权处理
- **适用场景**: 数据存储、数据分析、技术指标计算

### 6. [QAStrategy - 策略框架](./QAStrategy.md)
- **功能**: 策略开发、回测、实盘交易
- **特点**: CTA/套利/因子策略、完整回测框架、实盘部署
- **适用场景**: 策略开发、策略回测、实盘交易

## 扩展模块文档

### 7. [QAEngine - 任务引擎](./QAEngine.md)
- **功能**: 多线程/异步任务处理、分布式计算
- **适用场景**: 高性能计算、并行处理、任务调度

### 8. [QAPubSub - 消息系统](./QAPubSub.md)
- **功能**: 发布订阅消息队列、异步通信
- **适用场景**: 微服务通信、实时消息、任务分发

### 9. [其他模块综述](./RemainingModules.md)
- **QAFactor**: 因子研究和分析
- **QAIndicator**: 技术指标计算
- **QAWebServer**: Web服务和API
- **QASchedule**: 任务调度
- **QAAnalysis**: 数据分析工具
- **QASU**: 数据存储更新
- **QASetting**: 配置管理
- **QACmd**: 命令行工具

## 模块依赖关系

```
数据层: QAFetch → QASU → QAData
工具层: QAUtil → QASetting → QACmd
分析层: QAIndicator → QAFactor → QAAnalysis
交易层: QAMarket → QIFI → QAStrategy
服务层: QAEngine → QAPubSub → QAWebServer → QASchedule
```

## 学习路径建议

### 初学者路径
1. **QAUtil** - 掌握基础工具和概念
2. **QAFetch** - 学习数据获取方法
3. **QAData** - 理解数据结构和处理
4. **QAStrategy** - 开发简单策略

### 进阶开发者路径
1. **QAIndicator** + **QAFactor** - 深入技术分析和因子研究
2. **QIFI** + **QAMarket** - 掌握账户和交易管理
3. **QAEngine** + **QAPubSub** - 学习高性能和分布式架构

### 生产部署路径
1. **QASU** + **QASetting** - 数据管理和系统配置
2. **QAWebServer** + **QASchedule** - 服务化和任务调度
3. **QAAnalysis** - 监控和分析工具

## 快速参考

### 常用导入
```python
import QUANTAXIS as QA

# 数据获取
from QUANTAXIS.QAFetch import QA_fetch_stock_day_adv

# 数据结构
from QUANTAXIS.QAData import QA_DataStruct_Stock_day

# 技术指标
from QUANTAXIS.QAIndicator import MA, RSI, MACD

# 策略基类
from QUANTAXIS.QAStrategy import QACTABase

# 账户管理
from QUANTAXIS.QIFI import QIFI_Account
```

### 典型工作流
```python
# 1. 获取数据
data = QA.QA_fetch_stock_day_adv('000001', '2020-01-01', '2020-12-31')

# 2. 创建数据结构
stock_data = QA.QA_DataStruct_Stock_day(data)

# 3. 计算技术指标
ma20 = QA.MA(stock_data.close, 20)

# 4. 策略开发
class MyStrategy(QA.QACTABase):
    def on_bar(self, bar):
        if bar.close > ma20.iloc[-1]:
            self.buy(bar.code, 100)

# 5. 回测执行
result = QA.QA_backtest(MyStrategy, stock_data)
```

## 技术支持

- **官方文档**: [QUANTAXIS Documentation](https://github.com/QUANTAXIS/QUANTAXIS)
- **社区论坛**: [QUANTAXIS Club](http://www.yutiansut.com:3000)
- **问题反馈**: [GitHub Issues](https://github.com/QUANTAXIS/QUANTAXIS/issues)
- **QQ群**: 563280067

## 更新说明

本文档基于 QUANTAXIS 2.0.0 版本编写，涵盖了所有主要模块的功能和使用方法。随着框架的更新，文档将持续维护和完善。

最后更新: 2025-09-29