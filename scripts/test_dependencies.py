#!/usr/bin/env python3
"""
QUANTAXIS 2.1 依赖测试脚本

测试所有核心依赖是否正确安装并兼容
检测Rust组件(QARS2, QADataSwap)是否可用

@yutiansut @quantaxis
"""

import sys
import importlib.metadata as metadata
from typing import Tuple, List, Optional

# ANSI颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text: str):
    """打印节标题"""
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


def get_package_version(package_name: str) -> Optional[str]:
    """获取包版本"""
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return None


def test_import(module_name: str, package_name: Optional[str] = None,
                optional: bool = False) -> Tuple[bool, Optional[str]]:
    """
    测试模块导入

    Args:
        module_name: 模块名
        package_name: 包名(用于获取版本)
        optional: 是否为可选依赖

    Returns:
        (是否成功, 版本号)
    """
    try:
        module = __import__(module_name)

        # 获取版本
        if package_name:
            version = get_package_version(package_name)
        else:
            version = getattr(module, '__version__', 'unknown')

        return True, version
    except ImportError as e:
        if not optional:
            print_error(f"{module_name} 导入失败: {e}")
        return False, None


def test_python_version():
    """测试Python版本"""
    print_header("Python版本检查")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version < (3, 9):
        print_error(f"Python版本过低: {version_str}")
        print_error("QUANTAXIS 2.1+ 需要 Python 3.9-3.12")
        return False
    elif version >= (4, 0):
        print_error(f"Python版本过高: {version_str}")
        print_error("QUANTAXIS 2.1 仅支持 Python 3.9-3.12")
        return False
    else:
        print_success(f"Python {version_str}")

        # 推荐版本提示
        if version.minor == 11:
            print_success("✨ Python 3.11 - 最佳性能版本")
        elif version.minor == 12:
            print_success("✨ Python 3.12 - 最新版本")
        elif version.minor == 9:
            print_warning("建议升级到Python 3.11+以获得更好性能")

        return True


def test_core_dependencies():
    """测试核心依赖"""
    print_header("核心依赖检查")

    dependencies = {
        # (模块名, 包名, 是否可选)
        # 数据库层
        'pymongo': ('pymongo', 'pymongo', False),
        'motor': ('motor', 'motor', False),
        'clickhouse_driver': ('clickhouse_driver', 'clickhouse-driver', False),
        'redis': ('redis', 'redis', False),

        # 数据处理层
        'pandas': ('pandas', 'pandas', False),
        'numpy': ('numpy', 'numpy', False),
        'pyarrow': ('pyarrow', 'pyarrow', False),
        'scipy': ('scipy', 'scipy', False),
        'statsmodels': ('statsmodels', 'statsmodels', False),

        # Web框架
        'tornado': ('tornado', 'tornado', False),
        'flask': ('flask', 'flask', False),
        'pika': ('pika', 'pika', False),

        # 金融数据
        'tushare': ('tushare', 'tushare', False),
        'pytdx': ('pytdx', 'pytdx', False),

        # 量化分析
        'empyrical': ('empyrical', 'empyrical', False),
        'pyfolio': ('pyfolio', 'pyfolio', False),
        'alphalens': ('alphalens', 'alphalens', False),
    }

    all_success = True
    results = []

    for label, (module, package, optional) in dependencies.items():
        success, version = test_import(module, package, optional)

        if success:
            print_success(f"{label:20s} {version}")
            results.append((label, version, True))
        else:
            if not optional:
                all_success = False
                print_error(f"{label:20s} 未安装")
            results.append((label, None, False))

    return all_success, results


def test_rust_integration():
    """测试Rust集成组件"""
    print_header("Rust集成检查 (可选)")

    rust_components = {
        'qars3': ('qars3', 'qars3', True),
        'qadataswap': ('qadataswap', 'qadataswap', True),
    }

    results = {}

    for label, (module, package, optional) in rust_components.items():
        success, version = test_import(module, package, optional)

        if success:
            print_success(f"{label:20s} {version} (Rust核心可用)")
            results[label] = True
        else:
            print_warning(f"{label:20s} 未安装 (使用Python fallback)")
            results[label] = False

    # QARS2可用性检测
    if results.get('qars3'):
        try:
            import qars3
            # 尝试创建账户测试
            account = qars3.QAAccount(
                account_cookie="test_deps",
                init_cash=1000000.0,
                broker="QUANTAXIS"
            )
            print_success("  → QARS2账户系统可用")

            # 性能提示
            print(f"{GREEN}    性能提升: 账户操作100x, 回测10x{RESET}")
        except Exception as e:
            print_warning(f"  → QARS2账户测试失败: {e}")

    # QADataSwap可用性检测
    if results.get('qadataswap'):
        try:
            import qadataswap
            has_arrow = qadataswap.has_arrow_support()
            if has_arrow:
                print_success("  → QADataSwap零拷贝通信可用 (Arrow支持)")
            else:
                print_warning("  → QADataSwap可用，但Arrow支持缺失")
        except Exception as e:
            print_warning(f"  → QADataSwap测试失败: {e}")

    return results


def test_performance_packages():
    """测试性能优化包"""
    print_header("性能优化包 (可选)")

    performance_packages = {
        'polars': ('polars', 'polars', True),
        'orjson': ('orjson', 'orjson', True),
        'msgpack': ('msgpack', 'msgpack', True),
        'numba': ('numba', 'numba', False),  # numba在requirements中，非可选
    }

    results = {}

    for label, (module, package, optional) in performance_packages.items():
        success, version = test_import(module, package, optional)

        if success:
            print_success(f"{label:20s} {version}")
            results[label] = True

            # Polars特殊提示
            if label == 'polars':
                print(f"{GREEN}    数据处理性能: 比Pandas快5-10x{RESET}")
        else:
            if optional:
                print_warning(f"{label:20s} 未安装")
            else:
                print_error(f"{label:20s} 未安装")
            results[label] = False

    return results


def test_quantaxis_modules():
    """测试QUANTAXIS模块"""
    print_header("QUANTAXIS模块检查")

    try:
        import QUANTAXIS as QA
        print_success(f"QUANTAXIS {QA.__version__}")

        # 检测Rust集成状态
        if hasattr(QA, '__has_qars__'):
            if QA.__has_qars__:
                print_success(f"  → QARS集成: 已启用 (版本 {QA.__qars_version__})")
            else:
                print_warning("  → QARS集成: 未启用 (使用Python实现)")

        if hasattr(QA, '__has_dataswap__'):
            if QA.__has_dataswap__:
                print_success(f"  → DataSwap集成: 已启用 (版本 {QA.__dataswap_version__})")
            else:
                print_warning("  → DataSwap集成: 未启用")

        # 测试核心模块导入
        modules = [
            'QAFetch',
            'QAData',
            'QAUtil',
            'QIFI',
            'QAMarket',
            'QAEngine',
            'QAPubSub',
        ]

        for mod in modules:
            try:
                __import__(f'QUANTAXIS.{mod}')
                print_success(f"  → {mod}")
            except ImportError as e:
                print_error(f"  → {mod} 导入失败: {e}")
                return False

        return True

    except ImportError as e:
        print_error(f"QUANTAXIS导入失败: {e}")
        return False


def print_installation_guide():
    """打印安装指南"""
    print_header("安装指南")

    print("\n基础安装:")
    print(f"  {BLUE}pip install -e .{RESET}")

    print("\n包含性能优化:")
    print(f"  {BLUE}pip install -e .[performance]{RESET}")

    print("\n包含Rust组件:")
    print(f"  {BLUE}pip install -e .[rust]{RESET}")

    print("\n完整安装:")
    print(f"  {BLUE}pip install -e .[full]{RESET}")

    print("\n手动安装Rust组件:")
    print("  1. QARS2:")
    print(f"     {BLUE}cd /home/quantaxis/qars2{RESET}")
    print(f"     {BLUE}pip install -e .{RESET}")

    print("\n  2. QADataSwap:")
    print(f"     {BLUE}cd /home/quantaxis/qars2/libs/qadataswap{RESET}")
    print(f"     {BLUE}pip install -e .{RESET}")


def generate_report(results: dict):
    """生成测试报告"""
    print_header("测试报告")

    total = 0
    success = 0

    for category, result in results.items():
        if isinstance(result, bool):
            total += 1
            if result:
                success += 1
        elif isinstance(result, tuple):
            all_ok, deps = result
            total += 1
            if all_ok:
                success += 1
        elif isinstance(result, dict):
            for _, status in result.items():
                total += 1
                if status:
                    success += 1

    print(f"\n总计: {success}/{total} 通过")

    if success == total:
        print_success("✨ 所有依赖检查通过!")
        return True
    else:
        print_warning(f"⚠ {total - success} 项需要注意")
        return False


def main():
    """主函数"""
    print(f"{BLUE}")
    print("=" * 60)
    print("  QUANTAXIS 2.1 依赖测试")
    print("  @yutiansut @quantaxis")
    print("=" * 60)
    print(f"{RESET}")

    results = {}

    # 测试Python版本
    results['python'] = test_python_version()

    # 测试核心依赖
    results['core_deps'] = test_core_dependencies()

    # 测试Rust集成
    results['rust'] = test_rust_integration()

    # 测试性能包
    results['performance'] = test_performance_packages()

    # 测试QUANTAXIS模块
    results['quantaxis'] = test_quantaxis_modules()

    # 生成报告
    all_ok = generate_report(results)

    # 打印安装指南
    if not all_ok:
        print_installation_guide()

    # 返回退出码
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
