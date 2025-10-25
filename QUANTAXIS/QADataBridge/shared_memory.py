"""
共享内存数据传输 - 跨进程/跨语言零拷贝通信

基于QADataSwap实现高性能共享内存数据传输:
- 零拷贝数据传输 (5-10x faster)
- 跨进程通信
- 跨语言通信 (Python/Rust/C++)
- 支持Pandas/Polars DataFrame

@yutiansut @quantaxis
"""

from typing import Optional, Union
import pandas as pd

try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None

try:
    from qadataswap import SharedDataFrame as _SharedDataFrame
    HAS_DATASWAP = True
except ImportError:
    HAS_DATASWAP = False
    _SharedDataFrame = None


# ============================================================================
# 共享内存写入器
# ============================================================================

class SharedMemoryWriter:
    """
    共享内存数据写入器

    用于向共享内存写入DataFrame数据，实现跨进程零拷贝传输

    参数:
        name: 共享内存区域名称
        size_mb: 共享内存大小(MB)，默认100MB
        buffer_count: 缓冲区数量，默认3

    示例:
        >>> from QUANTAXIS.QADataBridge import SharedMemoryWriter
        >>> import polars as pl
        >>>
        >>> # 创建写入器
        >>> writer = SharedMemoryWriter("market_data", size_mb=100)
        >>>
        >>> # 写入数据
        >>> df = pl.DataFrame({'price': [10.5, 20.3], 'volume': [1000, 2000]})
        >>> writer.write(df)
        >>>
        >>> # 关闭
        >>> writer.close()
    """

    def __init__(self, name: str, size_mb: int = 100, buffer_count: int = 3):
        """
        初始化共享内存写入器

        参数:
            name: 共享内存名称
            size_mb: 大小(MB)
            buffer_count: 缓冲区数量
        """
        if not HAS_DATASWAP:
            raise RuntimeError(
                "SharedMemoryWriter需要QADataSwap支持\n"
                "请安装: pip install quantaxis[rust]"
            )

        self.name = name
        self.size_mb = size_mb
        self.buffer_count = buffer_count

        # 创建底层writer
        self._writer = _SharedDataFrame.create_writer(
            name=name,
            size_mb=size_mb,
            buffer_count=buffer_count
        )

    def write(self, df: Union[pd.DataFrame, 'pl.DataFrame']) -> bool:
        """
        写入DataFrame到共享内存

        参数:
            df: Pandas或Polars DataFrame

        返回:
            bool: 是否成功

        示例:
            >>> writer.write(df)
            True
        """
        # 转换为Polars (如果需要)
        if isinstance(df, pd.DataFrame):
            from .arrow_converter import convert_pandas_to_polars
            df = convert_pandas_to_polars(df)

        # 写入
        try:
            self._writer.write(df)
            return True
        except Exception as e:
            print(f"写入失败: {e}")
            return False

    def get_stats(self) -> dict:
        """
        获取统计信息

        返回:
            dict: 统计信息字典
        """
        return self._writer.get_stats()

    def close(self):
        """关闭写入器"""
        if hasattr(self._writer, 'close'):
            self._writer.close()

    def __enter__(self):
        """上下文管理器支持"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.close()

    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"SharedMemoryWriter(name='{self.name}', "
            f"size_mb={self.size_mb}, buffer_count={self.buffer_count})"
        )


# ============================================================================
# 共享内存读取器
# ============================================================================

class SharedMemoryReader:
    """
    共享内存数据读取器

    用于从共享内存读取DataFrame数据，实现跨进程零拷贝传输

    参数:
        name: 共享内存区域名称

    示例:
        >>> from QUANTAXIS.QADataBridge import SharedMemoryReader
        >>>
        >>> # 创建读取器
        >>> reader = SharedMemoryReader("market_data")
        >>>
        >>> # 读取数据
        >>> df = reader.read(timeout_ms=5000)
        >>> if df is not None:
        >>>     print(df.head())
        >>>
        >>> # 关闭
        >>> reader.close()
    """

    def __init__(self, name: str):
        """
        初始化共享内存读取器

        参数:
            name: 共享内存名称
        """
        if not HAS_DATASWAP:
            raise RuntimeError(
                "SharedMemoryReader需要QADataSwap支持\n"
                "请安装: pip install quantaxis[rust]"
            )

        self.name = name

        # 创建底层reader
        self._reader = _SharedDataFrame.create_reader(name=name)

    def read(self,
             timeout_ms: int = 5000,
             to_pandas: bool = False) -> Optional[Union[pd.DataFrame, 'pl.DataFrame']]:
        """
        从共享内存读取DataFrame

        参数:
            timeout_ms: 超时时间(毫秒)
            to_pandas: 是否转换为Pandas DataFrame

        返回:
            DataFrame或None (超时)

        示例:
            >>> # 读取为Polars
            >>> df_polars = reader.read()
            >>>
            >>> # 读取为Pandas
            >>> df_pandas = reader.read(to_pandas=True)
        """
        try:
            df = self._reader.read(timeout_ms=timeout_ms)

            if df is None:
                return None

            # 转换为Pandas (如果需要)
            if to_pandas:
                from .arrow_converter import convert_polars_to_pandas
                df = convert_polars_to_pandas(df)

            return df

        except Exception as e:
            print(f"读取失败: {e}")
            return None

    def get_stats(self) -> dict:
        """
        获取统计信息

        返回:
            dict: 统计信息字典
        """
        return self._reader.get_stats()

    def close(self):
        """关闭读取器"""
        if hasattr(self._reader, 'close'):
            self._reader.close()

    def __enter__(self):
        """上下文管理器支持"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.close()

    def __repr__(self) -> str:
        """字符串表示"""
        return f"SharedMemoryReader(name='{self.name}')"


# ============================================================================
# 便捷函数
# ============================================================================

def create_writer(name: str, size_mb: int = 100) -> SharedMemoryWriter:
    """
    便捷函数: 创建共享内存写入器

    参数:
        name: 共享内存名称
        size_mb: 大小(MB)

    返回:
        SharedMemoryWriter: 写入器实例

    示例:
        >>> writer = create_writer("my_data", size_mb=50)
    """
    return SharedMemoryWriter(name, size_mb=size_mb)


def create_reader(name: str) -> SharedMemoryReader:
    """
    便捷函数: 创建共享内存读取器

    参数:
        name: 共享内存名称

    返回:
        SharedMemoryReader: 读取器实例

    示例:
        >>> reader = create_reader("my_data")
    """
    return SharedMemoryReader(name)
