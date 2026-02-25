#!/bin/bash
# QUANTAXIS 文档本地构建脚本
#
# 功能说明:
# - 安装mdbook (如果未安装)
# - 构建mdbook文档
# - 可选: 启动本地预览服务器
#
# 使用方法:
#   bash scripts/build_docs.sh          # 仅构建
#   bash scripts/build_docs.sh --serve  # 构建并启动预览服务器
#
# 作者: @yutiansut @quantaxis
# 更新日期: 2025-10-25

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  QUANTAXIS 文档构建脚本${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 检查mdbook是否已安装
if ! command -v mdbook &> /dev/null; then
    echo -e "${YELLOW}❌ mdbook未安装，正在安装...${NC}"

    # 检测操作系统
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     MACHINE=linux;;
        Darwin*)    MACHINE=macos;;
        *)          MACHINE="UNKNOWN:${OS}"
    esac

    if [ "$MACHINE" = "linux" ] || [ "$MACHINE" = "macos" ]; then
        # 下载并安装mdbook
        MDBOOK_VERSION="0.4.40"
        TEMP_DIR=$(mktemp -d)

        if [ "$MACHINE" = "linux" ]; then
            MDBOOK_URL="https://github.com/rust-lang/mdBook/releases/download/v${MDBOOK_VERSION}/mdbook-v${MDBOOK_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
        else
            MDBOOK_URL="https://github.com/rust-lang/mdBook/releases/download/v${MDBOOK_VERSION}/mdbook-v${MDBOOK_VERSION}-x86_64-apple-darwin.tar.gz"
        fi

        echo -e "${YELLOW}📥 下载mdbook ${MDBOOK_VERSION}...${NC}"
        curl -sSL "$MDBOOK_URL" | tar -xz -C "$TEMP_DIR"

        # 移动到用户bin目录
        mkdir -p "$HOME/bin"
        mv "$TEMP_DIR/mdbook" "$HOME/bin/"
        rm -rf "$TEMP_DIR"

        # 添加到PATH (如果未添加)
        if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
            export PATH="$HOME/bin:$PATH"
            echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
            echo -e "${YELLOW}✅ 已添加 $HOME/bin 到PATH${NC}"
        fi

        echo -e "${GREEN}✅ mdbook安装成功!${NC}"
    else
        echo -e "${RED}❌ 不支持的操作系统: ${MACHINE}${NC}"
        echo -e "${YELLOW}请手动安装mdbook: https://rust-lang.github.io/mdBook/guide/installation.html${NC}"
        exit 1
    fi
else
    MDBOOK_VERSION=$(mdbook --version | awk '{print $2}')
    echo -e "${GREEN}✅ mdbook已安装 (版本: ${MDBOOK_VERSION})${NC}"
fi

echo ""
echo -e "${YELLOW}📚 正在构建文档...${NC}"

# 进入项目根目录
cd "$(dirname "$0")/.."

# 构建文档
if mdbook build; then
    echo ""
    echo -e "${GREEN}✅ 文档构建成功!${NC}"
    echo -e "${GREEN}   输出目录: ./book/${NC}"
    echo ""

    # 检查是否需要启动预览服务器
    if [ "$1" = "--serve" ] || [ "$1" = "-s" ]; then
        echo -e "${YELLOW}🌐 启动预览服务器...${NC}"
        echo -e "${GREEN}   访问地址: http://localhost:3000${NC}"
        echo -e "${YELLOW}   按 Ctrl+C 停止服务器${NC}"
        echo ""
        mdbook serve --open
    else
        echo -e "${YELLOW}💡 提示: 使用以下命令启动预览服务器:${NC}"
        echo -e "${GREEN}   bash scripts/build_docs.sh --serve${NC}"
        echo -e "${GREEN}   或者:${NC}"
        echo -e "${GREEN}   mdbook serve --open${NC}"
    fi
else
    echo ""
    echo -e "${RED}❌ 文档构建失败!${NC}"
    exit 1
fi
