# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

QUANTAXIS is a quantitative financial framework written in Python that provides a comprehensive suite of tools for financial data analysis, backtesting, and trading strategy development. The project is organized into multiple modular components for different aspects of quantitative finance.

**Version**: 2.0.0 (incompatible upgrade from 1.x)
**Author**: @yutiansut (When making changes, attribute to @yutiansut @quantaxis, not Claude)

## Related Projects Ecosystem

- [QAUltra-cpp](https://github.com/QUANTAXIS/qaultra-cpp) - C++ implementation of QUANTAXIS
- [QAUltra-rs](https://github.com/QUANTAXIS/qautlra-rs) - Rust implementation (partially open source)
- [QADataSwap](https://github.com/QUANTAXIS/qadataswap) - Cross-language communication framework (Rust/C++/Python)
- [QAExchange-RS](https://github.com/yutiansut/qaexchange-rs) - Exchange implementation + self-developed HTAP hybrid database

## Core Concept: QIFI Protocol

**CRITICAL**: QIFI (Quantaxis Differential Information Flow for Finance Integration) is the unified account structure used throughout QUANTAXIS. All accounts, orders, positions, and trades exist within the QIFI structure stored in MongoDB.

### QIFI Structure
The QIFI protocol decouples strategy logic from account implementation. A QIFI account contains:
- `accounts`: Account balances, margins, risk metrics
- `orders`: Order book with status tracking
- `positions`: Position details (long/short, today/history, P&L)
- `trades`: Executed trades
- `events`: Time-stamped event log
- `broker_name`: Trading counter identifier

**Key principle**: Strategies request resources (backtest/simulation/live accounts) and read QIFI fields directly without knowing the underlying implementation. See `QUANTAXIS/QIFI/qifi.md` for the complete specification and `examples/qifiaccountexample.py` for usage.

## Architecture

The codebase is structured into distinct modules under the `QUANTAXIS/` package:

- **QAFetch**: Multi-market data acquisition and storage (MongoDB/ClickHouse)
  - Supports stocks (TDX, Tushare), futures (CTP), crypto (Binance, Huobi, OKEx)
  - Unified interface across multiple data sources with fallback support
- **QAUtil**: Trading time utilities, calendars, market identification, and dataframe conversions
- **QIFI/QAMarket**: Unified multi-market, multi-language account system
  - `QifiAccount`: Standard account system consistent across Python/Rust/C++
  - `qifimanager`: Multi-account management system
  - `qaposition`: Single asset position management for precise long/short control
  - `marketpreset`: Market preset classes for futures/stocks/crypto metadata (margins, fees, tick sizes)
- **QAFactor**: Factor research suite for factor analysis, management, and combination
- **QAData**: Multi-asset, multi-market data structures (QA_DataStruct_*) for real-time and backtesting
  - Supports Stock/Future/Index/Crypto for Day/Min/Tick data
  - Resampling capabilities (tick→1min→5min→day)
- **QAIndicator**: Custom indicator framework with batch market-wide application
- **QAEngine**: Custom thread/process base classes for async and distributed computing
  - `QA_Thread`, `QA_AsyncThread`, `QA_Worker` for parallel task execution
- **QAPubSub**: MQ-based message queue (RabbitMQ) supporting 1-1, 1-n, n-n message distribution
- **QAStrategy**: CTA/arbitrage backtesting suite with QIFI mode support
- **QAWebServer**: Tornado-based web server for microservice architecture
- **QASchedule**: Background task scheduling built on QAWebServer
  - Supports dynamic task assignment and DAG-based pipelines
- **QAAnalysis**: Analysis and reporting tools
- **QACmd**: Command-line interface and utilities
- **QASU**: System utilities and maintenance tools

## Development Commands

### Prerequisites

QUANTAXIS requires MongoDB, ClickHouse, and RabbitMQ. The easiest way to set up the stack is with Docker:

```bash
# Start all required services (MongoDB, ClickHouse, Redis, RabbitMQ)
cd docker
docker-compose -f just_database.yaml up -d

# Services will be available at:
# - MongoDB: localhost:27017
# - ClickHouse: localhost:9000 (native), localhost:8123 (HTTP)
# - Redis: localhost:6379
# - RabbitMQ: localhost:5672 (AMQP), localhost:15672 (management UI)
```

### Installation
```bash
pip install -e .
# Or install requirements first:
pip install -r requirements.txt
```

### Initial Data Setup
```bash
# Initialize and populate database with market data
python config/data_init.py

# Update various market data types
python config/update_all.py        # Update all markets
python config/update_data.py       # Update stock data
python config/update_future.py     # Update futures data
python config/update_fin.py        # Update financial data
```

### Code Quality
```bash
# Linting (uses pylint with configuration in .pylintrc)
pylint QUANTAXIS/

# The project has a comprehensive .pylintrc configuration file
# CI/CD runs on GitHub Actions (see .github/workflows/)
```

### Console Commands
After installation, the following commands are available system-wide:

```bash
# Main CLI interface
quantaxis

# TDX (TongDaXin) market data fetching
quantaxisq

# Run strategies
qarun

# Start QUANTAXIS web server (microservices)
qawebserver
```

### Docker Deployment

Multiple Docker images are available for different use cases:

```bash
# Full development environment with Jupyter
docker pull daocloud.io/quantaxis/qa-jupyter

# Base runtime environment
docker pull daocloud.io/quantaxis/qa-base

# Event message queue (RabbitMQ)
docker pull daocloud.io/quantaxis/qaeventmq

# For Kubernetes deployments, see docker/k8s_deploy_qaservice/
```

## Key Dependencies

- **Database**: MongoDB (pymongo 3.11.2), ClickHouse (clickhouse-driver)
- **Data Processing**: pandas ≥1.1.5, numpy ≥1.12.0, pyarrow ≥6.0.1
- **Web**: tornado ≥6.3.2, flask ≥0.12.2
- **Financial**: tushare, pytdx ≥1.67, empyrical, pyfolio, alphalens
- **Async/Messaging**: pika (RabbitMQ), motor (async MongoDB), gevent-websocket
- **Analysis**: matplotlib, seaborn ≥0.11.1, statsmodels ≥0.12.1, scipy

## Multi-Language Integration

The project supports integration with QUANTAXIS Rust version through:
- Apache Arrow format (pyarrow) for cross-language data exchange
- Consistent QIFI account structures across Python/Rust/C++
- Arrow-based communication with arrow-rs and datafusion-rs

## Database Architecture

QUANTAXIS uses a multi-database architecture for different use cases:

- **MongoDB**: Primary data storage
  - Market data (stocks, futures, crypto): day/min/tick OHLCV
  - QIFI account structures (accounts, orders, positions, trades)
  - Factor data and research results
  - Default database name: `quantaxis`

- **ClickHouse**: High-performance OLAP database
  - Large-scale historical data analysis
  - QIFI account storage with better compression
  - Tabular data and factor analysis
  - Supports tick/L2 order/transaction data formats

- **Redis**: Cache and real-time data
  - Session management
  - Real-time market data cache

- **RabbitMQ** (via QAPubSub): Message queue
  - Real-time order flow
  - Task distribution and collection
  - Event-driven architecture support

## What's New in 2.0

Version 2.0 is a **breaking upgrade** from 1.x with major architectural changes:

**Data Layer**:
- Added ClickHouse support for self-hosted data distribution
- Support for tabular data and factor-based data structures
- Native support for tick/L2 order/transaction formats

**Microservices**:
- New QAWebServer module (Tornado-based)
- Dynamic task scheduling via QASchedule
- DAG-based pipeline support
- QAPubSub module for RabbitMQ integration

**Account System**:
- Removed legacy QAARP account system (no longer maintained)
- Complete migration to QIFI protocol
- Multi-market/cross-market account models
- Support for margin trading (futures, stocks) and options (in development)

**Live/Simulation Trading**:
- Unified QIFI interface for all trading modes
- CTP interface support (futures and options)
- Stock trading via QMT integration
- Parent-child account order distribution and tracking (OMS)
- Order gateway with risk management rules

**Multi-Language Support**:
- Communication with QUANTAXIS Rust version via Apache Arrow
- Consistent QIFI account structures across Python/Rust/C++
- Factor computation using Rust job workers

## Configuration Files

- `.pylintrc`: Comprehensive linting configuration
- `requirements.txt`: Core dependencies
- `config/`: Directory containing data update and maintenance scripts
- `docker/`: Docker configurations for various deployment scenarios

## Examples and Usage

The `examples/` directory contains practical usage examples:

```bash
# QIFI account usage (backtest mode with ClickHouse)
python examples/qifiaccountexample.py

# Factor analysis workflow
python examples/factoranalysis.py

# Task scheduling server setup
python examples/scheduleserver.py

# ClickHouse QIFI integration
python examples/test_ckread_qifi.py

# Jupyter notebooks in examples/ for interactive analysis
```

### Basic QIFI Account Example
```python
from QUANTAXIS.QIFI.QifiAccount import QIFI_Account

# Create account (backtest mode, using ClickHouse)
account = QIFI_Account(
    username='testx',
    password='123456',
    model='BACKTEST',
    nodatabase=False,
    dbname='ck',
    clickhouse_port=9000
)

# Initialize and send order
account.initial()
order = account.send_order("000001", 200, 20, 1, datetime='2021-09-30')

# Execute trade
account.make_deal(order)

# Get positions
positions = list(account.position_qifimsg.values())

# Settle at day end
account.settle()
```

## Version Support

**Python**: 3.5-3.10 supported (see setup.py:40 for version validation)

## Community and Support

- **QQ Group**: 563280067 ([Join link](https://jq.qq.com/?_wv=1027&k=4CEKGzn))
- **Developer Group**: 773602202 (requires GitHub ID for code contributors)
- **Production Deployment Group**: 945822690 (for multi-account local deployment)
- **Discord**: https://discord.gg/mkk5RgN
- **Forum**: [QUANTAXIS Club](http://www.yutiansut.com:3000) (highest priority for support)
- **GitHub Issues**: [Report bugs and request features](https://github.com/QUANTAXIS/QUANTAXIS/issues)

## Documentation

- [QABook Release](https://github.com/QUANTAXIS/QUANTAXIS/releases/download/latest/quantaxis.pdf) - Comprehensive documentation (PDF)
- Project README (Chinese): `README.md`
- QIFI Protocol Specification: `QUANTAXIS/QIFI/qifi.md`