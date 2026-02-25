#!/usr/bin/env python3
"""
文档验证脚本

验证QUANTAXIS 2.1.0文档更新的完整性和一致性

@yutiansut @quantaxis
"""

import os
import sys
import re
from pathlib import Path


# ANSI颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text: str):
    """打印标题"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")


def print_success(text: str):
    """打印成功信息"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_warning(text: str):
    """打印警告信息"""
    print(f"{YELLOW}⚠ {text}{RESET}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{RED}✗ {text}{RESET}")


def check_version_consistency():
    """检查版本号一致性"""
    print_header("版本号一致性检查")

    versions = {}

    # 检查__init__.py
    init_file = Path("QUANTAXIS/__init__.py")
    if init_file.exists():
        content = init_file.read_text()
        match = re.search(r"__version__ = ['\"]([^'\"]+)['\"]", content)
        if match:
            versions['__init__.py'] = match.group(1)
            print_success(f"__init__.py: {versions['__init__.py']}")
        else:
            print_error("__init__.py: 未找到版本号")
    else:
        print_error("__init__.py: 文件不存在")

    # 检查README.md
    readme_file = Path("README.md")
    if readme_file.exists():
        content = readme_file.read_text()
        match = re.search(r"# QUANTAXIS ([\d.]+(?:-[a-z]+\d+)?)", content)
        if match:
            versions['README.md'] = match.group(1)
            print_success(f"README.md: {versions['README.md']}")
        else:
            print_error("README.md: 未找到版本号")
    else:
        print_error("README.md: 文件不存在")

    # 检查一致性 (支持点号和连字符格式)
    # 将所有版本号标准化为使用点号
    normalized = {
        k: v.replace('-', '.')
        for k, v in versions.items()
    }

    if len(set(normalized.values())) == 1:
        print_success(f"所有文件版本号一致: {list(versions.values())[0]}")
        return True
    else:
        print_error(f"版本号不一致: {versions}")
        return False


def check_required_files():
    """检查必需文件是否存在"""
    print_header("必需文件检查")

    required_files = [
        ("README.md", "主文档"),
        ("CLAUDE.md", "开发指南"),
        ("UPGRADE_PLAN.md", "升级计划"),
        ("PHASE1_COMPLETE.md", "Phase 1报告"),
        ("PHASE2_COMPLETE.md", "Phase 2报告"),
        ("DOCUMENTATION_UPDATE.md", "文档更新总结"),
        ("QUANTAXIS/__init__.py", "主模块"),
        ("QUANTAXIS/QARSBridge/__init__.py", "QARSBridge模块"),
        ("QUANTAXIS/QARSBridge/qars_account.py", "账户包装器"),
        ("QUANTAXIS/QARSBridge/qars_backtest.py", "回测引擎"),
        ("QUANTAXIS/QARSBridge/QIFI_PROTOCOL.md", "QIFI协议"),
        ("examples/qarsbridge_example.py", "使用示例"),
        ("scripts/test_dependencies.py", "依赖测试"),
    ]

    all_exist = True
    for file_path, description in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print_success(f"{description:20s} {file_path:50s} ({size:>6d} bytes)")
        else:
            print_error(f"{description:20s} {file_path:50s} [不存在]")
            all_exist = False

    return all_exist


def check_documentation_links():
    """检查文档内部链接"""
    print_header("文档链接检查")

    readme_file = Path("README.md")
    if not readme_file.exists():
        print_error("README.md不存在")
        return False

    content = readme_file.read_text()

    # 查找Markdown链接
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    links = re.findall(link_pattern, content)

    internal_links = [
        (text, url) for text, url in links
        if url.startswith('./') or not url.startswith('http')
    ]

    all_valid = True
    for text, url in internal_links:
        # 移除锚点
        file_path = url.split('#')[0]
        path = Path(file_path)

        if path.exists():
            print_success(f"[{text}] → {url}")
        else:
            print_error(f"[{text}] → {url} [不存在]")
            all_valid = False

    if all_valid:
        print_success(f"所有内部链接有效 (共{len(internal_links)}个)")

    return all_valid


def check_code_examples():
    """检查代码示例语法"""
    print_header("代码示例检查")

    example_file = Path("examples/qarsbridge_example.py")
    if not example_file.exists():
        print_error("示例文件不存在")
        return False

    try:
        # 尝试编译代码
        with open(example_file, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, str(example_file), 'exec')
        print_success("示例代码语法正确")
        return True
    except SyntaxError as e:
        print_error(f"示例代码语法错误: {e}")
        return False


def check_qifi_protocol():
    """检查QIFI协议文档"""
    print_header("QIFI协议文档检查")

    protocol_file = Path("QUANTAXIS/QARSBridge/QIFI_PROTOCOL.md")
    if not protocol_file.exists():
        print_error("QIFI协议文档不存在")
        return False

    content = protocol_file.read_text()

    # 检查必需章节
    required_sections = [
        "概述",
        "核心数据结构",
        "QIFI主结构",
        "Account",
        "Position",
        "Order",
        "Trade",
        "跨语言兼容性",
    ]

    all_found = True
    for section in required_sections:
        if section in content:
            print_success(f"章节存在: {section}")
        else:
            print_error(f"章节缺失: {section}")
            all_found = False

    return all_found


def check_chinese_documentation():
    """检查中文文档规范"""
    print_header("中文文档规范检查")

    files_to_check = [
        "QUANTAXIS/QARSBridge/qars_account.py",
        "QUANTAXIS/QARSBridge/qars_backtest.py",
        "examples/qarsbridge_example.py",
    ]

    all_chinese = True
    for file_path in files_to_check:
        path = Path(file_path)
        if not path.exists():
            print_error(f"{file_path}: 文件不存在")
            all_chinese = False
            continue

        content = path.read_text(encoding='utf-8')

        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))

        # 查找docstring
        docstrings = re.findall(r'"""([^"]+)"""', content, re.DOTALL)

        if chinese_chars > 100:
            print_success(f"{file_path}: 包含{chinese_chars}个中文字符")
        else:
            print_warning(f"{file_path}: 仅包含{chinese_chars}个中文字符")
            all_chinese = False

        if docstrings:
            # 检查docstring是否包含中文
            chinese_in_docs = sum(
                len(re.findall(r'[\u4e00-\u9fff]', doc))
                for doc in docstrings
            )
            if chinese_in_docs > 50:
                print_success(f"{file_path}: 文档字符串使用中文")
            else:
                print_warning(f"{file_path}: 文档字符串缺少中文")

    return all_chinese


def generate_summary():
    """生成总结报告"""
    print_header("文档验证总结")

    results = {
        "版本号一致性": check_version_consistency(),
        "必需文件": check_required_files(),
        "文档链接": check_documentation_links(),
        "代码示例": check_code_examples(),
        "QIFI协议": check_qifi_protocol(),
        "中文文档": check_chinese_documentation(),
    }

    print("\n" + "=" * 60)
    print("验证结果:")
    print("=" * 60)

    for check, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        color = GREEN if passed else RED
        print(f"{color}{status}{RESET} - {check}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print_success("✨ 所有检查通过！文档更新完整。")
        return 0
    else:
        failed_count = sum(1 for v in results.values() if not v)
        print_error(f"⚠ {failed_count}/{len(results)} 项检查失败")
        return 1


def main():
    """主函数"""
    print(f"{BLUE}")
    print("=" * 60)
    print("  QUANTAXIS 2.1.0 文档验证")
    print("  @yutiansut @quantaxis")
    print("=" * 60)
    print(f"{RESET}")

    # 切换到项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    # 运行检查
    exit_code = generate_summary()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
