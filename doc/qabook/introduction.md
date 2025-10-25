# QABook - QUANTAXIS技术文档PDF

**版本**: 2.1.0-alpha2
**格式**: PDF (LaTeX编译)
**作者**: @yutiansut @quantaxis

---

## 📚 简介

QABook是QUANTAXIS的完整技术文档，以PDF格式提供。文档使用LaTeX编写，包含完整的量化交易理论基础、数学推导、系统架构和实践应用。

### 为什么需要PDF文档？

- **📄 完整性**: 包含完整的数学公式和理论推导
- **🎨 专业排版**: LaTeX高质量排版，适合打印和阅读
- **📱 离线阅读**: 可下载到本地，随时随地查阅
- **🔖 系统化**: 按照教科书方式组织，便于系统学习

---

## 📖 内容概览

QABook包含以下主要章节：

### 1. 前言
- QUANTAXIS发展历程
- 设计思想和理念
- 适用人群和场景

### 2. 环境准备
- 开发环境配置
- 依赖安装

### 3. 核心功能
- **数据**: 数据获取和管理
- **分析**: 数据分析方法
- **交易**: 交易系统实现
- **可视化**: 数据可视化技术

### 4. 基础知识 (重点)
- **凸优化**
  - KT条件 (Kuhn-Tucker condition)
- **矩阵理论**
  - 相似矩阵
  - 对称矩阵
  - 正定矩阵
  - Cholesky分解
  - EVD特征值分解
  - SVD奇异值分解
  - 矩阵的二次型
- **随机矩阵理论**
  - Marcenko–Pastur律
  - 协方差特征值分布
- **统计学基础**
  - 波动率、方差与协方差
  - 协方差矩阵
  - 协方差矩阵降噪
  - 参数估计
  - 常见分布

### 5. 现代资产管理理论
- 投资组合理论
- 风险收益权衡
- 最优化方法

### 6. 组合管理优化
- 优化策略
- 注意事项和陷阱

### 7. 主动组合管理
- 主动投资管理方法
- Alpha策略

### 8. 风险补偿与期权定价
- 衍生品定价理论
- Black-Scholes模型

### 9. 过拟合问题
- 机器学习中的过拟合
- 处理方法

---

## 📥 获取PDF

### 方法1: 下载预编译版本 (推荐)

访问[GitHub Releases](https://github.com/QUANTAXIS/QUANTAXIS/releases)页面，下载最新编译的PDF文档。

每次更新qabook目录时，GitHub Actions会自动编译并发布新版本。

### 方法2: 自行编译

如果您需要最新版本或想进行修改：

1. 克隆仓库
   ```bash
   git clone https://github.com/QUANTAXIS/QUANTAXIS.git
   cd QUANTAXIS/qabook
   ```

2. 使用编译脚本
   ```bash
   bash build.sh
   ```

3. 查看生成的PDF
   ```bash
   open quantaxis.pdf  # macOS
   xdg-open quantaxis.pdf  # Linux
   ```

详细编译说明请参考[编译指南](./build-guide.md)。

---

## 📊 文档特点

### 高质量排版

- ✅ 使用XeLaTeX编译，支持完美的中文排版
- ✅ 数学公式清晰美观
- ✅ 代码高亮显示
- ✅ 专业的版式设计

### 内容丰富

- ✅ 完整的数学推导过程
- ✅ 详细的理论说明
- ✅ 实际代码示例
- ✅ 图表和可视化

### 持续更新

- ✅ GitHub Actions自动编译
- ✅ 每次更新自动发布新版本
- ✅ Release页面可查看历史版本

---

## 🎯 适用人群

QABook适合以下读者：

### 初学者
- 想系统学习量化交易的理论基础
- 需要了解数学和统计学知识
- 希望理解QUANTAXIS的设计思想

### 进阶用户
- 需要深入理解算法原理
- 想要优化交易策略
- 研究投资组合管理理论

### 专业用户
- 量化研究员
- 算法交易工程师
- 金融数学研究者

---

## 💡 使用建议

### 学习路径

**基础阶段** (1-2周):
1. 阅读前言，了解QUANTAXIS
2. 学习环境准备章节
3. 浏览核心功能部分

**深入阶段** (2-4周):
1. 系统学习基础知识章节
2. 重点理解矩阵理论和统计学
3. 掌握协方差矩阵的计算和降噪

**应用阶段** (4-8周):
1. 学习现代资产管理理论
2. 理解组合优化方法
3. 实践主动组合管理策略

### 配合使用

QABook与在线文档配合使用效果最佳：

- **理论学习**: 使用QABook PDF
- **代码实践**: 参考[在线文档](../README.md)
- **API查询**: 查看[API参考](../api-reference/overview.md)

---

## 🔗 相关资源

- **在线文档**: [doc/README.md](../README.md)
- **GitHub仓库**: https://github.com/QUANTAXIS/QUANTAXIS
- **LaTeX源文件**: [qabook/quantaxis.tex](../../qabook/quantaxis.tex)
- **编译指南**: [build-guide.md](./build-guide.md)
- **下载PDF**: [GitHub Releases](https://github.com/QUANTAXIS/QUANTAXIS/releases)

---

## 📝 参与贡献

欢迎改进QABook！

如果您发现错误或有改进建议：

1. 提交[Issue](https://github.com/QUANTAXIS/QUANTAXIS/issues)
2. 或直接编辑[quantaxis.tex](../../qabook/quantaxis.tex)
3. 提交Pull Request

贡献指南请参考[贡献指南](../development/contributing.md)。

---

**维护者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[下一页：编译指南 →](./build-guide.md)
