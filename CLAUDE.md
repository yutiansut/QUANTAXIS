# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

QUANTAXIS is a quantitative financial framework written in Python that provides a comprehensive suite of tools for financial data analysis, backtesting, and trading strategy development. The project is organized into multiple modular components for different aspects of quantitative finance.

## Architecture

The codebase is structured into distinct modules under the `QUANTAXIS/` package:

- **QAFetch**: Multi-market data acquisition and storage (MongoDB/ClickHouse)
- **QAUtil**: Trading time utilities, calendars, market identification, and dataframe conversions
- **QIFI/QAMarket**: Unified multi-market, multi-language account system
  - `qifiaccount`: Standard account system consistent across languages (Python/Rust/C++)
  - `qifimanager`: Multi-account management system
  - `qaposition`: Single asset position management for precise long/short control
  - `marketpreset`: Market preset classes for futures/stocks/crypto metadata
- **QAFactor**: Factor research suite for factor analysis, management, and combination
- **QAData**: Multi-asset, multi-market data structures for real-time and backtesting
- **QAIndicator**: Custom indicator framework with batch market-wide application
- **QAEngine**: Custom thread/process base classes for async and distributed computing
- **QAPubSub**: MQ-based message queue supporting 1-1, 1-n, n-n message distribution
- **QAStrategy**: CTA/arbitrage backtesting suite with QIFI mode support
- **QAWebServer**: Tornado-based web server for microservice architecture
- **QASchedule**: Background task scheduling built on QAWebServer
- **QAAnalysis**: Analysis and reporting tools
- **QACmd**: Command-line interface and utilities
- **QASU**: System utilities and maintenance tools

## Development Commands

### Installation
```bash
pip install -e .
# Or install requirements first:
pip install -r requirements.txt
```

### Code Quality
```bash
# Linting (uses pylint with configuration in .pylintrc)
pylint QUANTAXIS/

# The project has a comprehensive .pylintrc configuration file
```

### Console Commands
The package provides several console entry points:
- `quantaxis` - Main CLI command
- `quantaxisq` - TDX data fetching
- `qarun` - Strategy runner
- `qawebserver` - Web server launcher

### Data Management
```bash
# Update market data (various scripts in config/)
python config/update_data.py
python config/update_all.py
python config/update_future.py
python config/update_fin.py
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

- **MongoDB**: Primary data storage for market data and account information
- **ClickHouse**: High-performance analytics database for large-scale data analysis
- Support for tick/L2 order/transaction data formats

## Configuration Files

- `.pylintrc`: Comprehensive linting configuration
- `requirements.txt`: Core dependencies
- `config/`: Directory containing data update and maintenance scripts
- `docker/`: Docker configurations for various deployment scenarios

## Examples and Usage

Check the `examples/` directory for:
- `qifiaccountexample.py`: QIFI account system usage
- `factoranalysis.py`: Factor analysis workflows
- `scheduleserver.py`: Task scheduling examples
- `featureanalysis.ipynb`: Jupyter notebook examples

## Version Support

Python 3.5-3.10 supported (see setup.py for version validation).