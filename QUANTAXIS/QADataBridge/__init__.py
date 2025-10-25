"""
QUANTAXIS/QADataBridge - 跨语言零拷贝数据交换桥接层

基于QADataSwap提供Python/Rust/C++之间的高效数据交换:
- Arrow格式零拷贝转换
- Pandas ↔ Polars ↔ Arrow无缝切换
- 共享内存高性能通信
- 5-10x数据传输加速

示例:
    >>> from QUANTAXIS.QADataBridge import convert_pandas_to_polars, has_dataswap_support
    >>>
    >>> if has_dataswap_support():
    >>>     # Pandas转Polars (零拷贝)
    >>>     import pandas as pd
    >>>     df_pandas = pd.DataFrame({'a': [1, 2, 3]})
    >>>     df_polars = convert_pandas_to_polars(df_pandas)
    >>>
    >>>     # 共享内存通信
    >>>     from QUANTAXIS.QADataBridge import SharedMemoryWriter
    >>>     writer = SharedMemoryWriter("my_data")
    >>>     writer.write(df_polars)

@yutiansut @quantaxis
"""

__version__ = "2.1.0.alpha2"
__all__ = [
    'has_dataswap_support',
    'HAS_DATASWAP',
    'convert_pandas_to_polars',
    'convert_polars_to_pandas',
    'convert_pandas_to_arrow',
    'convert_arrow_to_pandas',
    'SharedMemoryWriter',
    'SharedMemoryReader',
]

# ============================================================================
# 检测QADataSwap是否可用
# ============================================================================
try:
    import qadataswap
    HAS_DATASWAP = True
    DATASWAP_VERSION = getattr(qadataswap, 'get_version', lambda: 'unknown')()
    HAS_ARROW = qadataswap.has_arrow_support()
except ImportError:
    HAS_DATASWAP = False
    DATASWAP_VERSION = None
    HAS_ARROW = False
    import warnings
    warnings.warn(
        "QADataSwap未安装，跨语言零拷贝通信功能不可用。\n"
        "安装方法:\n"
        "  pip install quantaxis[rust]\n"
        "或者:\n"
        "  cd /home/quantaxis/qars2/libs/qadataswap && pip install -e .\n"
        "\n"
        "性能对比: 零拷贝传输比传统序列化快5-10倍",
        ImportWarning,
        stacklevel=2
    )


def has_dataswap_support() -> bool:
    """
    检查是否有QADataSwap支持

    返回:
        bool: True如果QADataSwap可用

    示例:
        >>> if has_dataswap_support():
        >>>     print("零拷贝通信可用")
        >>> else:
        >>>     print("使用传统数据传输")
    """
    return HAS_DATASWAP


# ============================================================================
# 导入转换函数和共享内存类
# ============================================================================
if HAS_DATASWAP:
    # 使用QADataSwap实现
    from .arrow_converter import (
        convert_pandas_to_polars,
        convert_polars_to_pandas,
        convert_pandas_to_arrow,
        convert_arrow_to_pandas,
        convert_polars_to_arrow,
        convert_arrow_to_polars,
    )
    from .shared_memory import (
        SharedMemoryWriter,
        SharedMemoryReader,
    )

    # 打印提示
    import sys
    if not sys.flags.quiet:
        print(f"✨ QADataSwap已启用 (版本 {DATASWAP_VERSION})")
        print(f"   零拷贝数据传输: Pandas ↔ Polars ↔ Arrow")
        print(f"   Arrow支持: {'是' if HAS_ARROW else '否'}")

else:
    # 提供Python fallback (使用标准序列化)
    import warnings

    def convert_pandas_to_polars(df):
        """Pandas to Polars转换 (fallback - 使用复制)"""
        try:
            import polars as pl
            return pl.from_pandas(df)
        except ImportError:
            raise ImportError("需要安装polars: pip install polars")

    def convert_polars_to_pandas(df):
        """Polars to Pandas转换 (fallback - 使用复制)"""
        return df.to_pandas()

    def convert_pandas_to_arrow(df):
        """Pandas to Arrow转换 (fallback)"""
        try:
            import pyarrow as pa
            return pa.Table.from_pandas(df)
        except ImportError:
            raise ImportError("需要安装pyarrow: pip install pyarrow")

    def convert_arrow_to_pandas(table):
        """Arrow to Pandas转换 (fallback)"""
        return table.to_pandas()

    def convert_polars_to_arrow(df):
        """Polars to Arrow转换 (fallback)"""
        return df.to_arrow()

    def convert_arrow_to_polars(table):
        """Arrow to Polars转换 (fallback)"""
        try:
            import polars as pl
            return pl.from_arrow(table)
        except ImportError:
            raise ImportError("需要安装polars: pip install polars")

    class SharedMemoryWriter:
        """共享内存写入器 (fallback - 抛出错误)"""
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "SharedMemoryWriter需要QADataSwap支持\n"
                "请安装: pip install quantaxis[rust]"
            )

    class SharedMemoryReader:
        """共享内存读取器 (fallback - 抛出错误)"""
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "SharedMemoryReader需要QADataSwap支持\n"
                "请安装: pip install quantaxis[rust]"
            )

    import sys
    if not sys.flags.quiet:
        print("⚠ 使用Python fallback (未检测到QADataSwap)")
        print("  建议: pip install quantaxis[rust] 获得5-10x数据传输加速")


# ============================================================================
# 版本信息
# ============================================================================
def get_version_info() -> dict:
    """
    获取QADataBridge版本信息

    返回:
        dict: 版本信息字典

    示例:
        >>> info = get_version_info()
        >>> print(f"QADataSwap支持: {info['has_dataswap']}")
    """
    return {
        'bridge_version': __version__,
        'has_dataswap': HAS_DATASWAP,
        'dataswap_version': DATASWAP_VERSION,
        'has_arrow': HAS_ARROW,
        'backend': 'QADataSwap' if HAS_DATASWAP else 'Python',
    }
