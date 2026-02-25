# QUANTAXIS QABook - LaTeX文档系统

**版本**: 2.1.0-alpha2
**更新日期**: 2025-10-25
**作者**: @yutiansut @quantaxis

---

## 📚 简介

QABook是QUANTAXIS的完整LaTeX技术文档，涵盖量化交易的理论基础、实践应用和系统架构。使用XeLaTeX编译器生成高质量PDF文档，支持中文排版和数学公式。

### 文档内容

QABook包含以下主要章节：

1. **前言** - QUANTAXIS发展历程和设计思想
2. **环境准备** - 开发环境配置
3. **数据** - 数据获取和管理
4. **分析** - 数据分析方法
5. **交易** - 交易系统实现
6. **可视化** - 数据可视化技术
7. **基础知识** - 数学和统计学基础
   - 凸优化
   - 矩阵理论
   - 随机矩阵理论
   - 协方差矩阵
   - 参数估计
   - 常见分布
8. **现代资产管理理论** - 投资组合理论
9. **组合管理优化** - 优化策略和注意事项
10. **主动组合管理** - 主动投资管理方法
11. **风险补偿与期权定价** - 衍生品定价理论
12. **过拟合问题** - 机器学习中的过拟合处理

---

## 🚀 快速开始

### 方法1: 使用编译脚本 (推荐)

```bash
# 进入qabook目录
cd qabook/

# 编译PDF
bash build.sh

# 清理临时文件
bash build.sh clean

# 监控模式（文件变更自动重新编译）
bash build.sh watch
```

### 方法2: 手动编译

```bash
cd qabook/

# 编译三次以生成完整的目录和交叉引用
xelatex quantaxis.tex
xelatex quantaxis.tex
xelatex quantaxis.tex
```

---

## 📦 环境准备

### LaTeX发行版安装

QABook需要完整的TeX Live发行版，包含中文字体和各种宏包。

#### Linux (Ubuntu/Debian)

```bash
# 安装完整的TeX Live
sudo apt-get update
sudo apt-get install texlive-full

# 或者安装基础版本 + 中文支持
sudo apt-get install texlive-base texlive-latex-extra \
    texlive-xetex texlive-lang-chinese texlive-fonts-recommended
```

#### macOS

```bash
# 使用Homebrew安装MacTeX
brew install --cask mactex

# 或下载完整安装包
# https://www.tug.org/mactex/
```

#### Windows

1. 下载TeX Live ISO: https://www.tug.org/texlive/acquire-iso.html
2. 或使用MiKTeX: https://miktex.org/download
3. 安装时选择"完整安装"以包含所有宏包

### 验证安装

```bash
# 检查XeLaTeX版本
xelatex --version

# 应该输出类似：
# XeTeX 3.141592653-2.6-0.999995 (TeX Live 2024)
```

---

## 📁 文件结构

```
qabook/
├── quantaxis.tex      # 主LaTeX文档
├── qalogo.png         # QUANTAXIS Logo
├── build.sh           # 编译脚本
├── README.md          # 本文档
└── quantaxis.pdf      # 生成的PDF（编译后）
```

---

## ✍️ 编辑文档

### LaTeX编辑器推荐

**跨平台编辑器**:
- **VS Code** + LaTeX Workshop插件 (推荐)
- **TeXstudio** - 功能完整的LaTeX IDE
- **Overleaf** - 在线LaTeX编辑器

**VS Code配置**:
```json
{
  "latex-workshop.latex.recipes": [
    {
      "name": "XeLaTeX",
      "tools": ["xelatex", "xelatex", "xelatex"]
    }
  ],
  "latex-workshop.latex.tools": [
    {
      "name": "xelatex",
      "command": "xelatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "%DOC%"
      ]
    }
  ]
}
```

### 文档结构

#### 导言区 (Preamble)

```latex
\documentclass{scrartcl}        % 文档类
\usepackage[UTF8]{ctex}        % 中文支持
\usepackage{amsmath, amssymb}  % 数学公式
\usepackage{graphicx}          % 图片支持
\usepackage{pythonhighlight}   % Python代码高亮
\usepackage{hyperref}          % 超链接
```

#### 章节组织

```latex
\section{章节标题}
\subsection{小节标题}
\subsubsection{子小节标题}
```

#### 数学公式

```latex
% 行内公式
$E = mc^2$

% 行间公式
\begin{equation}
    \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\end{equation}

% 矩阵
\begin{bmatrix}
    a & b \\
    c & d
\end{bmatrix}
```

#### Python代码

```latex
\begin{python}
import QUANTAXIS as QA

account = QA.QA_Account()
account.receive_simpledeal(...)
\end{python}
```

#### 图片插入

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{image.png}
    \caption{图片标题}
    \label{fig:label}
\end{figure}
```

---

## 🔧 常见问题

### Q1: 编译失败 "! LaTeX Error: File 'xxx.sty' not found"

**原因**: 缺少LaTeX宏包

**解决**:
```bash
# Linux
sudo apt-get install texlive-latex-extra

# macOS
sudo tlmgr install <package-name>

# Windows (MiKTeX)
# 使用MiKTeX Package Manager安装缺失的包
```

### Q2: 中文显示为方框或乱码

**原因**: 缺少中文字体或ctex配置问题

**解决**:
```bash
# Linux - 安装中文字体支持
sudo apt-get install texlive-lang-chinese
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei

# 或在文档中指定字体
\setCJKmainfont{WenQuanYi Micro Hei}
```

### Q3: 编译速度很慢

**原因**: 文档较大，多次编译耗时

**优化**:
1. 使用`build.sh`脚本，自动处理多次编译
2. 开发时注释掉部分章节加快编译
3. 使用`latexmk`自动化工具

### Q4: 如何只编译部分章节？

**方法1**: 注释掉不需要的章节
```latex
% \section{不需要的章节}
% ...
```

**方法2**: 使用`\include`和`\includeonly`
```latex
% 导言区
\includeonly{chapter1,chapter3}

% 正文
\include{chapter1}
\include{chapter2}  % 不会被编译
\include{chapter3}
```

### Q5: PDF中的超链接不工作

**检查**: hyperref包的配置
```latex
\usepackage[colorlinks, linkcolor=black,
            anchorcolor=black, citecolor=black]{hyperref}
```

---

## 📊 文档规范

### 命名规范

- **章节标签**: `\label{sec:section-name}`
- **图片标签**: `\label{fig:figure-name}`
- **公式标签**: `\label{eq:equation-name}`
- **表格标签**: `\label{tab:table-name}`

### 引用规范

```latex
如\ref{sec:intro}所示...
参见图\ref{fig:architecture}...
根据公式\ref{eq:variance}...
```

### 代码规范

- Python代码使用`pythonhighlight`环境
- 添加注释说明代码功能
- 保持代码简洁，避免过长的代码块

### 数学公式规范

- 重要公式使用`equation`环境并编号
- 简单公式可使用`$...$`行内公式
- 矩阵、向量使用粗体表示

---

## 🌐 GitHub Actions自动编译

项目已配置GitHub Actions自动编译PDF：

### 触发条件

- 推送到`master`分支
- `qabook/`目录有更新
- 手动触发

### 工作流程

1. ✅ 安装TeX Live
2. ✅ 编译`quantaxis.tex`
3. ✅ 上传PDF到Release
4. ✅ 自动标记版本

### 下载编译好的PDF

访问项目的[Releases页面](https://github.com/QUANTAXIS/QUANTAXIS/releases)下载最新编译的PDF。

---

## 🛠️ 高级技巧

### 使用latexmk自动化编译

```bash
# 安装latexmk
sudo apt-get install latexmk

# 创建.latexmkrc配置文件
cat > .latexmkrc << 'EOF'
$pdf_mode = 5;  # XeLaTeX模式
$xelatex = 'xelatex -interaction=nonstopmode -synctex=1 %O %S';
$out_dir = 'build';
EOF

# 编译
latexmk quantaxis.tex

# 持续监控模式
latexmk -pvc quantaxis.tex
```

### PDF优化

```bash
# 压缩PDF大小
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=quantaxis_compressed.pdf quantaxis.pdf
```

### 转换为Word格式

```bash
# 使用pandoc转换
sudo apt-get install pandoc
pandoc quantaxis.tex -o quantaxis.docx
```

---

## 📚 LaTeX参考资源

### 官方文档

- [LaTeX Project](https://www.latex-project.org/)
- [CTAN - Comprehensive TeX Archive Network](https://www.ctan.org/)
- [TeX Live](https://www.tug.org/texlive/)

### 中文资源

- [一份不太简短的LaTeX2e介绍](http://www.ctan.org/tex-archive/info/lshort/chinese/)
- [LaTeX中文文档](https://github.com/huangxg/lshort-zh-cn)
- [CTeX社区](http://www.ctex.org/)

### 在线工具

- [Overleaf](https://www.overleaf.com/) - 在线LaTeX编辑器
- [Detexify](http://detexify.kirelabs.org/) - 手写识别LaTeX符号
- [Tables Generator](https://www.tablesgenerator.com/) - 表格生成器

### 常用宏包文档

- [amsmath](http://texdoc.net/texmf-dist/doc/latex/amsmath/amsldoc.pdf) - 数学公式
- [graphicx](http://texdoc.net/texmf-dist/doc/latex/graphics/graphicx.pdf) - 图片处理
- [hyperref](http://texdoc.net/texmf-dist/doc/latex/hyperref/hyperref-doc.pdf) - 超链接
- [ctex](http://texdoc.net/texmf-dist/doc/latex/ctex/ctex.pdf) - 中文支持

---

## 🤝 贡献指南

欢迎改进QABook文档！

### 贡献步骤

1. Fork本仓库
2. 创建分支: `git checkout -b docs/improve-qabook`
3. 编辑`quantaxis.tex`
4. 本地编译测试: `bash build.sh`
5. 提交PR

### 注意事项

- 保持现有的文档结构和风格
- 添加必要的数学推导和公式
- 提供代码示例和实际应用场景
- 确保编译无错误和警告

---

## 📝 版本历史

### v2.1.0 (2025-10-25)

- ✅ 优化LaTeX文档配置
- ✅ 添加自动编译脚本
- ✅ 创建完整使用指南
- ✅ 配置GitHub Actions自动发布
- ✅ 整合到文档系统

### v2.0.0

- 初始LaTeX文档
- 包含量化交易理论基础
- 数学和统计学基础知识

---

**维护者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回文档中心](../doc/README.md) | [查看PDF](./quantaxis.pdf)
