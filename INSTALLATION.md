# QUANTAXIS 安装指南

> 🚀 **QUANTAXIS 2.1.0** - 完整安装教程和依赖配置
>
> **版本**: v2.1.0-alpha2 | **Python**: 3.9-3.12 | **更新**: 2025-10-25

---

## 📋 目录

- [系统要求](#系统要求)
- [安装方式](#安装方式)
- [依赖说明](#依赖说明)
- [Rust组件安装](#rust组件安装)
- [数据库配置](#数据库配置)
- [验证安装](#验证安装)
- [常见问题](#常见问题)
- [升级指南](#升级指南)

---

## 🖥️ 系统要求

### 操作系统

| 系统 | 版本 | 支持状态 |
|------|------|---------|
| **Linux** | Ubuntu 18.04+, CentOS 7+ | ✅ 完全支持 |
| **macOS** | 10.14+ (Mojave) | ✅ 完全支持 |
| **Windows** | 10/11 | ⚠️ 部分支持 |

**推荐**: Linux (Ubuntu 20.04/22.04) 用于生产环境

### Python版本

| Python版本 | 支持状态 | 说明 |
|-----------|---------|------|
| **3.9** | ✅ 推荐 | 稳定版本 |
| **3.10** | ✅ 推荐 | 稳定版本 |
| **3.11** | ✅ 推荐 | 最新稳定版 |
| **3.12** | ✅ 支持 | 最新版本 |
| 3.8及以下 | ❌ 不支持 | - |

### 硬件要求

| 用途 | CPU | 内存 | 硬盘 |
|------|-----|------|------|
| **开发/学习** | 2核+ | 4GB+ | 20GB+ |
| **回测/研究** | 4核+ | 8GB+ | 100GB+ |
| **生产交易** | 8核+ | 16GB+ | 500GB+ SSD |

---

## 📦 安装方式

### 方式1: 基础安装（最简单）

适合初学者和基础使用场景。

```bash
# 使用pip安装
pip install quantaxis

# 或从源码安装
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS
pip install -e .
```

**包含功能**:
- ✅ 核心数据结构
- ✅ 数据获取和存储
- ✅ 回测框架
- ✅ 因子分析
- ❌ Rust高性能组件
- ❌ 零拷贝数据传输

---

### 方式2: 完整安装 with Rust（推荐）

推荐给追求性能的用户，包含所有高性能组件。

```bash
# 安装完整版（包含Rust组件）
pip install quantaxis[rust]

# 或从源码安装
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS
pip install -e .[rust]
```

**包含功能**:
- ✅ 所有基础功能
- ✅ QARS2 Rust高性能账户（100x加速）
- ✅ QADataSwap零拷贝传输（5-10x加速）
- ✅ Polars高性能DataFrame

**性能提升**:
- 账户操作: 100x加速
- 回测速度: 10x加速
- 数据传输: 5-10x加速

---

### 方式3: 开发者安装

适合需要修改源码或贡献代码的开发者。

```bash
# 克隆主仓库
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS

# 安装开发依赖
pip install -e .[dev]

# 安装完整依赖（包括Rust组件）
pip install -e .[rust,dev]
```

**额外包含**:
- ✅ pytest测试框架
- ✅ pylint代码检查
- ✅ black代码格式化
- ✅ mypy类型检查

---

### 方式4: Docker安装

适合快速部署和隔离环境。

```bash
# 拉取Docker镜像
docker pull quantaxis/quantaxis:latest

# 运行容器
docker run -it --name quantaxis \
  -p 8888:8888 \
  -v ~/quantaxis_data:/data \
  quantaxis/quantaxis:latest

# 或使用docker-compose
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS/docker
docker-compose up -d
```

**包含服务**:
- ✅ QUANTAXIS完整环境
- ✅ MongoDB数据库
- ✅ Jupyter Notebook
- ✅ WebServer服务

---

## 📚 依赖说明

### 核心依赖（必需）

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| **pandas** | ≥1.1.5 | 数据处理 |
| **numpy** | ≥1.12.0 | 数值计算 |
| **pymongo** | 3.11.2 | MongoDB连接 |
| **requests** | ≥2.14.2 | HTTP请求 |
| **lxml** | ≥3.8.0 | XML解析 |
| **tornado** | ≥6.3.2 | Web服务器 |

安装命令：
```bash
pip install pandas numpy pymongo requests lxml tornado
```

---

### 数据源依赖

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| **tushare** | ≥1.2.10 | 股票数据获取 |
| **pytdx** | ≥1.67 | 通达信数据 |
| **akshare** | latest | 多源数据获取 |

安装命令：
```bash
pip install tushare pytdx akshare
```

---

### 可选依赖（推荐）

#### 高性能组件

| 包名 | 版本要求 | 用途 | 性能提升 |
|------|---------|------|---------|
| **qars3** | latest | Rust账户引擎 | 100x |
| **qadataswap** | ≥0.1.0 | 零拷贝传输 | 5-10x |
| **polars** | ≥0.20.0 | 高性能DataFrame | 5-10x |
| **pyarrow** | ≥15.0.0 | Arrow数据格式 | 2-5x |

安装命令：
```bash
# 方式1: 通过quantaxis[rust]
pip install quantaxis[rust]

# 方式2: 单独安装
pip install polars pyarrow
cd /home/quantaxis/qars2 && pip install -e .
cd /home/quantaxis/qadataswap && pip install -e .
```

#### 可视化和分析

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| **matplotlib** | ≥3.0.0 | 图表绘制 |
| **seaborn** | ≥0.11.1 | 统计可视化 |
| **plotly** | ≥5.0.0 | 交互式图表 |
| **empyrical** | ≥0.5.0 | 绩效分析 |

安装命令：
```bash
pip install matplotlib seaborn plotly empyrical
```

#### 机器学习

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| **scikit-learn** | ≥0.24.0 | 机器学习 |
| **statsmodels** | ≥0.12.1 | 统计模型 |
| **alphalens** | latest | 因子分析 |

安装命令：
```bash
pip install scikit-learn statsmodels alphalens
```

---

## 🦀 Rust组件安装

### QARS2 (Rust账户引擎)

**性能**: 100x账户操作加速

#### 方式1: 从PyPI安装（推荐）

```bash
pip install qars3
```

#### 方式2: 从源码编译

```bash
# 克隆QARS2仓库
cd /home/quantaxis
git clone https://github.com/yutiansut/qars2.git
cd qars2

# 安装Rust（如果未安装）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# 编译安装
pip install -e .
```

**验证安装**:
```python
from QUANTAXIS.QARSBridge import has_qars_support

if has_qars_support():
    print("✅ QARS2已安装")
else:
    print("❌ QARS2未安装")
```

---

### QADataSwap (零拷贝数据传输)

**性能**: 5-10x数据传输加速

#### 方式1: 从PyPI安装（即将支持）

```bash
pip install qadataswap
```

#### 方式2: 从源码编译

```bash
# 克隆QADataSwap仓库
cd /home/quantaxis
git clone https://github.com/yutiansut/qadataswap.git
cd qadataswap

# 确保Rust已安装
rustc --version

# 编译安装
pip install -e .
```

**验证安装**:
```python
from QUANTAXIS.QADataBridge import has_dataswap_support

if has_dataswap_support():
    print("✅ QADataSwap已安装")
else:
    print("❌ QADataSwap未安装")
```

---

## 💾 数据库配置

### MongoDB安装

QUANTAXIS使用MongoDB作为主要数据存储。

#### Linux (Ubuntu/Debian)

```bash
# 导入MongoDB公钥
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# 添加MongoDB源
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# 安装MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# 启动MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# 验证安装
mongo --version
```

#### macOS

```bash
# 使用Homebrew安装
brew tap mongodb/brew
brew install mongodb-community@6.0

# 启动MongoDB
brew services start mongodb-community@6.0

# 验证安装
mongosh --version
```

#### Windows

1. 下载MongoDB安装包: https://www.mongodb.com/try/download/community
2. 运行安装程序，选择"Complete"安装
3. 配置MongoDB为Windows服务
4. 验证: 打开命令提示符，输入`mongod --version`

---

### MongoDB配置

创建QUANTAXIS数据库配置：

```bash
# 连接MongoDB
mongosh

# 创建数据库和用户
use quantaxis
db.createUser({
  user: "quantaxis",
  pwd: "your_password",
  roles: [{role: "readWrite", db: "quantaxis"}]
})

# 退出
exit
```

配置QUANTAXIS连接：

```python
# 在Python中配置
from QUANTAXIS.QAUtil import DATABASE

# 查看当前配置
print(DATABASE)

# 或修改配置文件
# ~/.quantaxis/setting/config.ini
```

---

### ClickHouse安装（可选）

用于大规模数据分析和查询加速。

```bash
# Ubuntu/Debian
sudo apt-get install -y apt-transport-https ca-certificates dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt-get update
sudo apt-get install -y clickhouse-server clickhouse-client

# 启动服务
sudo systemctl start clickhouse-server
sudo systemctl enable clickhouse-server
```

---

## ✅ 验证安装

### 基础验证

```python
# test_installation.py
import sys
print(f"Python版本: {sys.version}")

# 导入QUANTAXIS
import QUANTAXIS as QA
print(f"QUANTAXIS版本: {QA.__version__}")

# 检查核心模块
from QUANTAXIS import (
    QA_fetch_get_stock_day,
    QA_DataStruct_Stock_day,
    QIFI_Account,
)
print("✅ 核心模块导入成功")

# 检查数据库连接
from QUANTAXIS.QAUtil import DATABASE
try:
    DATABASE.stock_day.find_one()
    print("✅ MongoDB连接成功")
except Exception as e:
    print(f"⚠️  MongoDB连接失败: {e}")
```

运行验证：
```bash
python test_installation.py
```

---

### Rust组件验证

```python
# test_rust_components.py
from QUANTAXIS.QARSBridge import has_qars_support
from QUANTAXIS.QADataBridge import has_dataswap_support

print("\n" + "=" * 50)
print("Rust组件检查")
print("=" * 50)

# QARS2检查
if has_qars_support():
    from QUANTAXIS.QARSBridge import QARSAccount
    print("✅ QARS2 (Rust账户引擎) 已安装")
    print("   性能提升: 100x账户操作加速")
else:
    print("⚠️  QARS2未安装，使用Python实现")
    print("   建议: pip install quantaxis[rust]")

# QADataSwap检查
if has_dataswap_support():
    from QUANTAXIS.QADataBridge import (
        convert_pandas_to_polars,
        SharedMemoryWriter,
    )
    print("✅ QADataSwap (零拷贝传输) 已安装")
    print("   性能提升: 5-10x数据传输加速")
else:
    print("⚠️  QADataSwap未安装，使用标准传输")
    print("   建议: pip install quantaxis[rust]")

print("=" * 50)
```

运行验证：
```bash
python test_rust_components.py
```

**预期输出**:
```
==================================================
Rust组件检查
==================================================
✅ QARS2 (Rust账户引擎) 已安装
   性能提升: 100x账户操作加速
✅ QADataSwap (零拷贝传输) 已安装
   性能提升: 5-10x数据传输加速
==================================================
```

---

### 完整功能验证

```python
# test_full_features.py
import QUANTAXIS as QA
import pandas as pd

print("\n" + "=" * 50)
print("QUANTAXIS完整功能验证")
print("=" * 50)

# 1. 数据获取测试
print("\n1. 测试数据获取...")
try:
    df = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-10')
    print(f"   ✅ 获取数据成功: {len(df)}条记录")
except Exception as e:
    print(f"   ⚠️  数据获取失败: {e}")

# 2. 数据结构测试
print("\n2. 测试数据结构...")
try:
    data = QA.QA_DataStruct_Stock_day(df)
    print(f"   ✅ 数据结构创建成功")
    print(f"   数据范围: {data.data.index[0]} 至 {data.data.index[-1]}")
except Exception as e:
    print(f"   ⚠️  数据结构创建失败: {e}")

# 3. QIFI账户测试
print("\n3. 测试QIFI账户...")
try:
    account = QA.QIFI_Account(
        username="test",
        password="test",
        model="future",
        init_cash=100000
    )
    print(f"   ✅ QIFI账户创建成功")
    print(f"   初始资金: {account.init_cash}")
except Exception as e:
    print(f"   ⚠️  QIFI账户创建失败: {e}")

# 4. Rust组件测试（如果可用）
from QUANTAXIS.QARSBridge import has_qars_support
if has_qars_support():
    print("\n4. 测试QARS2 Rust账户...")
    try:
        from QUANTAXIS.QARSBridge import QARSAccount
        rust_account = QARSAccount("test", init_cash=100000)
        print(f"   ✅ Rust账户创建成功")
        print(f"   初始资金: {rust_account.init_cash}")
    except Exception as e:
        print(f"   ⚠️  Rust账户创建失败: {e}")

print("\n" + "=" * 50)
print("✅ 验证完成")
print("=" * 50)
```

运行验证：
```bash
python test_full_features.py
```

---

## ❓ 常见问题

### Q1: ImportError: No module named 'QUANTAXIS'

**原因**: QUANTAXIS未正确安装

**解决方案**:
```bash
# 重新安装
pip uninstall quantaxis
pip install quantaxis

# 或从源码安装
cd QUANTAXIS
pip install -e .
```

---

### Q2: MongoDB连接失败

**原因**: MongoDB未启动或配置错误

**解决方案**:
```bash
# 检查MongoDB状态
sudo systemctl status mongod

# 启动MongoDB
sudo systemctl start mongod

# 测试连接
mongosh
```

---

### Q3: Rust组件安装失败

**原因**: 缺少Rust工具链或编译失败

**解决方案**:
```bash
# 安装Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# 更新Rust
rustup update

# 重新安装
pip install --force-reinstall quantaxis[rust]
```

---

### Q4: pandas版本冲突

**原因**: pandas版本过低或过高

**解决方案**:
```bash
# 升级pandas
pip install --upgrade pandas>=1.1.5

# 或指定版本
pip install pandas==2.0.0
```

---

### Q5: Python版本不兼容

**错误**: `wrong version, should be 3.9/3.10/3.11 version`

**解决方案**:
```bash
# 检查Python版本
python --version

# 安装Python 3.9+
# Ubuntu/Debian
sudo apt-get install python3.9

# macOS
brew install python@3.9

# 创建虚拟环境
python3.9 -m venv quantaxis_env
source quantaxis_env/bin/activate
```

---

## 🔄 升级指南

### 从v1.x升级到v2.1.0

#### 1. 备份数据

```bash
# 备份MongoDB数据
mongodump --db quantaxis --out ~/quantaxis_backup

# 备份配置文件
cp -r ~/.quantaxis ~/quantaxis_config_backup
```

#### 2. 卸载旧版本

```bash
pip uninstall quantaxis
```

#### 3. 安装新版本

```bash
# 安装完整版
pip install quantaxis[rust]
```

#### 4. 迁移数据（如需要）

```python
# migration_script.py
import QUANTAXIS as QA

# 检查数据兼容性
# 执行必要的数据转换
# ...

print("✅ 数据迁移完成")
```

#### 5. 更新配置

```python
# 更新配置文件格式（如有变化）
from QUANTAXIS.QAUtil import QA_util_cfg_initial

QA_util_cfg_initial()
```

---

### 主要变更

#### v2.1.0新特性

- ✅ Python 3.9+支持
- ✅ QARS2 Rust账户引擎集成（100x加速）
- ✅ QADataSwap零拷贝传输（5-10x加速）
- ✅ QARSBridge桥接层
- ✅ QADataBridge数据交换层
- ✅ Polars高性能DataFrame支持

#### 不兼容变更

- ❌ 不再支持Python 3.8及以下
- ⚠️ 部分API接口调整（向后兼容）

---

## 📝 安装检查清单

完成安装后，请确认以下项目：

### 基础安装
- [ ] Python 3.9+已安装
- [ ] QUANTAXIS已安装
- [ ] MongoDB已安装并运行
- [ ] 可以导入QUANTAXIS模块
- [ ] 数据库连接正常

### Rust组件（可选但推荐）
- [ ] Rust工具链已安装
- [ ] QARS2已安装
- [ ] QADataSwap已安装
- [ ] Polars已安装
- [ ] PyArrow已安装

### 数据源配置
- [ ] Tushare已配置（如使用）
- [ ] AkShare已安装（如使用）
- [ ] pytdx已安装

### 功能验证
- [ ] 数据获取功能正常
- [ ] 账户创建功能正常
- [ ] 回测功能正常
- [ ] Rust组件功能正常（如已安装）

---

## 🆘 获取帮助

如果遇到安装问题，可以通过以下方式获取帮助：

### 官方渠道

- **GitHub Issues**: https://github.com/QUANTAXIS/QUANTAXIS/issues
- **QQ群**: 563280068
- **Discord**: https://discord.gg/quantaxis
- **论坛**: https://forum.quantaxis.cn

### 提问建议

提问时请提供以下信息：
1. 操作系统和版本
2. Python版本
3. QUANTAXIS版本
4. 完整的错误信息
5. 已尝试的解决方案

---

## 📚 下一步

安装完成后，建议：

1. **阅读快速入门**: [QUICKSTART.md](./QUICKSTART.md)
2. **查看示例代码**: [examples/](./examples/)
3. **运行基准测试**: 验证性能提升
4. **配置数据源**: 开始获取市场数据

---

**@yutiansut @quantaxis**
**最后更新**: 2025-10-25
