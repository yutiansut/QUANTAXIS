"""
QUANTAXIS/QARSBridge - QARS2 Rust核心桥接层

提供Python友好的接口访问QARS2 Rust高性能组件:
- QARSAccount: Rust高性能QIFI账户 (100x加速)
- QARSBacktest: Rust回测引擎 (10x加速)
- QARSData: Polars高性能数据结构
- has_qars_support(): 检测QARS2是否可用

示例:
    >>> from QUANTAXIS.QARSBridge import QARSAccount, has_qars_support
    >>>
    >>> if has_qars_support():
    >>>     # 使用Rust高性能账户
    >>>     account = QARSAccount("test", init_cash=1000000)
    >>> else:
    >>>     # 使用Python回退实现
    >>>     from QUANTAXIS.QIFI import QIFI_Account
    >>>     account = QIFI_Account("test")

@yutiansut @quantaxis
"""

__version__ = "2.1.0.alpha1"
__all__ = [
    'QARSAccount',
    'QARSBacktest',
    'has_qars_support',
    'HAS_QARS',
]

# ============================================================================
# 检测QARS2是否可用
# ============================================================================
try:
    import qars3
    from qars3 import QA_QIFIAccount as _RustQIFIAccount
    HAS_QARS = True
    QARS_VERSION = getattr(qars3, '__version__', 'unknown')
except ImportError:
    HAS_QARS = False
    QARS_VERSION = None
    _RustQIFIAccount = None
    import warnings
    warnings.warn(
        "QARS2 Rust核心未安装，将使用纯Python实现。\n"
        "安装方法:\n"
        "  pip install quantaxis[rust]\n"
        "或者:\n"
        "  cd /home/quantaxis/qars2 && pip install -e .\n"
        "\n"
        "性能对比: Rust版本比Python版本快10-100倍",
        ImportWarning,
        stacklevel=2
    )


def has_qars_support() -> bool:
    """
    检查是否有QARS2 Rust核心支持

    返回:
        bool: True如果QARS2可用

    示例:
        >>> if has_qars_support():
        >>>     print("Rust核心可用，将获得极致性能")
        >>> else:
        >>>     print("使用Python实现，建议安装QARS2")
    """
    return HAS_QARS


# ============================================================================
# 导入桥接类
# ============================================================================
if HAS_QARS:
    # 使用Rust实现
    from .qars_account import QARSAccount
    from .qars_backtest import QARSBacktest

    # 打印性能提示
    import sys
    if not sys.flags.quiet:
        print(f"✨ QARS2 Rust核心已启用 (版本 {QARS_VERSION})")
        print(f"   性能提升: 账户操作100x, 回测10x, 数据处理5-10x")

else:
    # 提供Python fallback
    from ..QIFI.QifiAccount import QIFI_Account as QARSAccount
    from ..QABacktest import QA_Backtest as QARSBacktest

    import sys
    if not sys.flags.quiet:
        print("⚠ 使用Python实现 (未检测到QARS2)")
        print("  建议: pip install quantaxis[rust] 获得100x性能提升")


# ============================================================================
# 版本信息
# ============================================================================
def get_version_info() -> dict:
    """
    获取QARS桥接层版本信息

    返回:
        dict: 版本信息字典

    示例:
        >>> info = get_version_info()
        >>> print(f"QARS支持: {info['has_qars']}")
    """
    return {
        'bridge_version': __version__,
        'has_qars': HAS_QARS,
        'qars_version': QARS_VERSION,
        'backend': 'Rust' if HAS_QARS else 'Python',
    }
