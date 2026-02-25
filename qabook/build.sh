#!/bin/bash
# QUANTAXIS QABook LaTeX编译脚本
#
# 功能说明:
# - 检查LaTeX环境
# - 编译quantaxis.tex生成PDF
# - 支持清理临时文件
# - 支持持续监控模式
#
# 使用方法:
#   bash build.sh              # 编译PDF
#   bash build.sh clean        # 清理临时文件
#   bash build.sh watch        # 监控模式（文件变更自动重新编译）
#
# 作者: @yutiansut @quantaxis
# 更新日期: 2025-10-25

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  QUANTAXIS QABook PDF编译脚本${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 进入qabook目录
cd "$(dirname "$0")"

# 检查xelatex是否已安装
if ! command -v xelatex &> /dev/null; then
    echo -e "${RED}❌ xelatex未安装${NC}"
    echo -e "${YELLOW}请安装TeX Live:${NC}"
    echo -e "${BLUE}  Ubuntu/Debian: sudo apt-get install texlive-full${NC}"
    echo -e "${BLUE}  macOS: brew install --cask mactex${NC}"
    echo -e "${BLUE}  或访问: https://www.tug.org/texlive/${NC}"
    exit 1
fi

XELATEX_VERSION=$(xelatex --version | head -1)
echo -e "${GREEN}✅ XeLaTeX已安装${NC}"
echo -e "${BLUE}   版本: ${XELATEX_VERSION}${NC}"
echo ""

# 清理函数
clean_temp_files() {
    echo -e "${YELLOW}🧹 清理临时文件...${NC}"
    rm -f *.aux *.log *.out *.toc *.pdf *.gz *.fdb_latexmk *.fls *.synctex.gz 2>/dev/null || true
    echo -e "${GREEN}✅ 清理完成${NC}"
}

# 编译函数
build_pdf() {
    echo -e "${YELLOW}📄 开始编译 quantaxis.tex...${NC}"
    echo ""

    # 第一次编译（生成目录）
    echo -e "${BLUE}[1/3] 第一次编译...${NC}"
    xelatex -interaction=nonstopmode quantaxis.tex > /dev/null 2>&1 || {
        echo -e "${RED}❌ 编译失败！${NC}"
        echo -e "${YELLOW}查看日志: quantaxis.log${NC}"
        tail -50 quantaxis.log
        exit 1
    }

    # 第二次编译（生成交叉引用）
    echo -e "${BLUE}[2/3] 第二次编译...${NC}"
    xelatex -interaction=nonstopmode quantaxis.tex > /dev/null 2>&1 || {
        echo -e "${RED}❌ 编译失败！${NC}"
        exit 1
    }

    # 第三次编译（确保所有引用正确）
    echo -e "${BLUE}[3/3] 第三次编译...${NC}"
    xelatex -interaction=nonstopmode quantaxis.tex > /dev/null 2>&1 || {
        echo -e "${RED}❌ 编译失败！${NC}"
        exit 1
    }

    echo ""

    if [ -f "quantaxis.pdf" ]; then
        FILE_SIZE=$(du -h quantaxis.pdf | cut -f1)
        echo -e "${GREEN}✅ 编译成功！${NC}"
        echo -e "${GREEN}   输出文件: quantaxis.pdf${NC}"
        echo -e "${GREEN}   文件大小: ${FILE_SIZE}${NC}"
        echo ""

        # 清理临时文件（保留PDF）
        echo -e "${YELLOW}🧹 清理临时文件...${NC}"
        rm -f *.aux *.log *.out *.toc *.gz *.fdb_latexmk *.fls *.synctex.gz 2>/dev/null || true

        echo -e "${GREEN}✅ 完成！${NC}"
        return 0
    else
        echo -e "${RED}❌ PDF生成失败！${NC}"
        return 1
    fi
}

# 监控模式
watch_mode() {
    echo -e "${YELLOW}👀 监控模式已启动${NC}"
    echo -e "${YELLOW}   监控文件: quantaxis.tex${NC}"
    echo -e "${YELLOW}   按 Ctrl+C 停止${NC}"
    echo ""

    # 安装inotify-tools (如果未安装)
    if ! command -v inotifywait &> /dev/null; then
        echo -e "${RED}❌ inotifywait未安装${NC}"
        echo -e "${YELLOW}安装方法:${NC}"
        echo -e "${BLUE}  sudo apt-get install inotify-tools${NC}"
        exit 1
    fi

    # 初始编译
    build_pdf

    # 监控文件变化
    while inotifywait -e modify quantaxis.tex 2>/dev/null; do
        echo ""
        echo -e "${BLUE}检测到文件变更，重新编译...${NC}"
        echo ""
        build_pdf
    done
}

# 主逻辑
case "${1:-build}" in
    clean)
        clean_temp_files
        ;;
    watch)
        watch_mode
        ;;
    build|*)
        build_pdf
        ;;
esac
