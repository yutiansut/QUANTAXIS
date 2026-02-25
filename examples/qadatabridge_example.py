#!/usr/bin/env python3
"""
QADataBridge使用示例 - 零拷贝数据转换和共享内存通信

展示如何使用QADataBridge进行高效的数据转换和跨进程通信:
- Pandas ↔ Polars零拷贝转换
- 共享内存跨进程数据传输
- 性能对比示例

@yutiansut @quantaxis
"""

import time
import numpy as np
import pandas as pd

try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    print("⚠️  Polars未安装，部分示例将跳过")
    print("   安装: pip install polars>=0.20.0")

from QUANTAXIS.QADataBridge import (
    has_dataswap_support,
    convert_pandas_to_polars,
    convert_polars_to_pandas,
)

try:
    from QUANTAXIS.QADataBridge import (
        SharedMemoryWriter,
        SharedMemoryReader,
    )
    HAS_SHARED_MEMORY = True
except ImportError:
    HAS_SHARED_MEMORY = False
    print("⚠️  SharedMemory未安装（需要QADataSwap）")


# ============================================================================
# 示例1: 检查QADataSwap支持
# ============================================================================

def example_01_check_support():
    """
    示例1: 检查QADataSwap支持状态

    功能:
        - 检测QADataSwap是否安装
        - 显示零拷贝通信可用性
    """
    print("\n" + "=" * 60)
    print("示例1: 检查QADataSwap支持")
    print("=" * 60)

    if has_dataswap_support():
        print("✅ QADataSwap已安装，零拷贝通信可用")
        print("   性能提升: 数据传输速度提升5-10倍")
    else:
        print("⚠️  QADataSwap未安装，使用Python fallback")
        print("   建议安装: pip install quantaxis[rust]")
        print("   或者: cd /home/quantaxis/qadataswap && pip install -e .")


# ============================================================================
# 示例2: Pandas转Polars (零拷贝)
# ============================================================================

def example_02_pandas_to_polars():
    """
    示例2: Pandas DataFrame转换为Polars DataFrame

    功能:
        - 通过Arrow实现零拷贝转换
        - 相比标准转换快2-3倍

    性能:
        - 大数据集(100万行): 2-3x加速
        - 内存占用: 降低50-80%
    """
    if not HAS_POLARS:
        print("\n⚠️  示例2跳过: Polars未安装")
        return

    print("\n" + "=" * 60)
    print("示例2: Pandas → Polars零拷贝转换")
    print("=" * 60)

    # 创建示例数据（股票行情）
    df_pandas = pd.DataFrame({
        'code': ['000001', '000002', '000003'],
        'price': [10.5, 20.3, 15.8],
        'volume': [1000, 2000, 1500],
        'datetime': pd.date_range('2025-01-15', periods=3, freq='D')
    })

    print("\n📊 原始Pandas DataFrame:")
    print(df_pandas)
    print(f"   类型: {type(df_pandas)}")
    print(f"   内存: {df_pandas.memory_usage(deep=True).sum() / 1024:.2f} KB")

    # 转换为Polars
    start_time = time.time()
    df_polars = convert_pandas_to_polars(df_pandas)
    elapsed = (time.time() - start_time) * 1000

    print(f"\n✅ 转换为Polars DataFrame (耗时: {elapsed:.4f}ms):")
    print(df_polars)
    print(f"   类型: {type(df_polars)}")

    print("\n💡 使用场景:")
    print("   - QUANTAXIS数据转换为Polars进行高性能分析")
    print("   - 与Rust QARS2组件交换数据")
    print("   - 大数据集快速处理")


# ============================================================================
# 示例3: Polars转Pandas
# ============================================================================

def example_03_polars_to_pandas():
    """
    示例3: Polars DataFrame转换为Pandas DataFrame

    功能:
        - 通过Arrow实现零拷贝转换
        - 保持数据类型和精度
    """
    if not HAS_POLARS:
        print("\n⚠️  示例3跳过: Polars未安装")
        return

    print("\n" + "=" * 60)
    print("示例3: Polars → Pandas零拷贝转换")
    print("=" * 60)

    # 创建Polars DataFrame（期货持仓）
    df_polars = pl.DataFrame({
        'contract': ['IF2512', 'IC2512', 'IH2512'],
        'direction': ['LONG', 'LONG', 'SHORT'],
        'volume': [10, 15, 8],
        'open_price': [4500.0, 7000.0, 3000.0],
        'last_price': [4550.0, 7100.0, 2980.0],
    })

    print("\n📊 原始Polars DataFrame:")
    print(df_polars)
    print(f"   类型: {type(df_polars)}")

    # 转换为Pandas
    start_time = time.time()
    df_pandas = convert_polars_to_pandas(df_polars)
    elapsed = (time.time() - start_time) * 1000

    print(f"\n✅ 转换为Pandas DataFrame (耗时: {elapsed:.4f}ms):")
    print(df_pandas)
    print(f"   类型: {type(df_pandas)}")

    # 计算盈亏
    df_pandas['profit'] = (df_pandas['last_price'] - df_pandas['open_price']) * df_pandas['volume']

    print("\n📈 计算盈亏:")
    print(df_pandas[['contract', 'direction', 'volume', 'profit']])
    print(f"   总盈亏: {df_pandas['profit'].sum():.2f}")


# ============================================================================
# 示例4: 批量数据转换
# ============================================================================

def example_04_batch_conversion():
    """
    示例4: 批量数据转换

    功能:
        - 同时转换多个DataFrame
        - 适用于多品种数据处理
    """
    if not HAS_POLARS:
        print("\n⚠️  示例4跳过: Polars未安装")
        return

    print("\n" + "=" * 60)
    print("示例4: 批量数据转换")
    print("=" * 60)

    # 创建多个股票的数据
    stock_codes = ['000001', '000002', '000003']
    dfs_pandas = []

    for code in stock_codes:
        df = pd.DataFrame({
            'code': [code] * 5,
            'datetime': pd.date_range('2025-01-15', periods=5, freq='D'),
            'price': np.random.uniform(10, 20, 5),
            'volume': np.random.randint(1000, 5000, 5)
        })
        dfs_pandas.append(df)

    print(f"\n📊 原始数据: {len(dfs_pandas)}个Pandas DataFrame")
    for i, df in enumerate(dfs_pandas):
        print(f"   股票{i+1} ({stock_codes[i]}): {len(df)}行")

    # 批量转换
    start_time = time.time()
    dfs_polars = [convert_pandas_to_polars(df) for df in dfs_pandas]
    elapsed = (time.time() - start_time) * 1000

    print(f"\n✅ 批量转换完成 (耗时: {elapsed:.4f}ms)")
    print(f"   转换了{len(dfs_polars)}个DataFrame")
    print(f"   平均每个: {elapsed/len(dfs_polars):.4f}ms")

    # 合并所有数据
    df_combined = pl.concat(dfs_polars)
    print(f"\n📊 合并后的Polars DataFrame: {len(df_combined)}行")
    print(df_combined.head(10))


# ============================================================================
# 示例5: 共享内存写入器 (跨进程通信)
# ============================================================================

def example_05_shared_memory_writer():
    """
    示例5: 共享内存写入器

    功能:
        - 将DataFrame写入共享内存
        - 实现跨进程零拷贝传输

    性能:
        - 传输速度: 比pickle快5-10倍
        - 零内存拷贝
    """
    if not HAS_SHARED_MEMORY:
        print("\n⚠️  示例5跳过: SharedMemory需要QADataSwap")
        return

    if not HAS_POLARS:
        print("\n⚠️  示例5跳过: Polars未安装")
        return

    print("\n" + "=" * 60)
    print("示例5: 共享内存写入器")
    print("=" * 60)

    # 创建市场数据
    df = pl.DataFrame({
        'code': ['IF2512'] * 100,
        'datetime': pd.date_range('2025-01-15 09:30:00', periods=100, freq='1min'),
        'price': np.random.uniform(4500, 4600, 100),
        'volume': np.random.randint(100, 1000, 100),
    })

    print(f"\n📊 准备写入的数据: {len(df)}行")
    print(df.head())

    # 创建共享内存写入器
    print("\n✅ 创建共享内存写入器...")
    writer = SharedMemoryWriter(
        name="quantaxis_market_data",
        size_mb=50  # 50MB共享内存
    )

    print(f"   名称: quantaxis_market_data")
    print(f"   大小: 50MB")

    # 写入数据
    print("\n📤 写入数据到共享内存...")
    start_time = time.time()
    success = writer.write(df)
    elapsed = (time.time() - start_time) * 1000

    if success:
        print(f"   ✅ 写入成功 (耗时: {elapsed:.4f}ms)")
        print(f"   数据大小: {len(df)}行")
    else:
        print(f"   ❌ 写入失败")

    # 获取统计信息
    stats = writer.get_stats()
    print(f"\n📊 统计信息:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # 关闭写入器
    writer.close()
    print("\n✅ 写入器已关闭")

    print("\n💡 使用场景:")
    print("   - 行情数据实时推送")
    print("   - 策略进程间数据共享")
    print("   - Python ↔ Rust数据交换")


# ============================================================================
# 示例6: 共享内存读取器
# ============================================================================

def example_06_shared_memory_reader():
    """
    示例6: 共享内存读取器

    功能:
        - 从共享内存读取DataFrame
        - 支持超时和格式转换
    """
    if not HAS_SHARED_MEMORY:
        print("\n⚠️  示例6跳过: SharedMemory需要QADataSwap")
        return

    print("\n" + "=" * 60)
    print("示例6: 共享内存读取器")
    print("=" * 60)

    # 创建读取器
    print("\n✅ 创建共享内存读取器...")
    reader = SharedMemoryReader(name="quantaxis_market_data")
    print(f"   名称: quantaxis_market_data")

    # 读取数据（Polars格式）
    print("\n📥 从共享内存读取数据 (Polars格式)...")
    start_time = time.time()
    df_polars = reader.read(timeout_ms=5000, to_pandas=False)
    elapsed = (time.time() - start_time) * 1000

    if df_polars is not None:
        print(f"   ✅ 读取成功 (耗时: {elapsed:.4f}ms)")
        print(f"\n📊 读取的Polars DataFrame:")
        print(df_polars.head())
    else:
        print(f"   ⏱️  读取超时 (没有新数据)")

    # 读取数据（Pandas格式）
    print("\n📥 从共享内存读取数据 (Pandas格式)...")
    start_time = time.time()
    df_pandas = reader.read(timeout_ms=5000, to_pandas=True)
    elapsed = (time.time() - start_time) * 1000

    if df_pandas is not None:
        print(f"   ✅ 读取成功 (耗时: {elapsed:.4f}ms)")
        print(f"\n📊 读取的Pandas DataFrame:")
        print(df_pandas.head())
    else:
        print(f"   ⏱️  读取超时")

    # 关闭读取器
    reader.close()
    print("\n✅ 读取器已关闭")


# ============================================================================
# 示例7: 性能对比 - 零拷贝 vs 标准转换
# ============================================================================

def example_07_performance_comparison():
    """
    示例7: 性能对比 - 零拷贝 vs 标准转换

    对比:
        - Arrow零拷贝转换 vs 标准转换
        - 不同数据规模的性能差异
    """
    if not HAS_POLARS:
        print("\n⚠️  示例7跳过: Polars未安装")
        return

    print("\n" + "=" * 60)
    print("示例7: 性能对比 - 零拷贝 vs 标准转换")
    print("=" * 60)

    # 测试不同规模的数据
    test_sizes = [1000, 10000, 100000]

    print("\n📊 测试配置:")
    print(f"   数据规模: {test_sizes}")
    print(f"   列数: 10列")

    for num_rows in test_sizes:
        print(f"\n{'=' * 40}")
        print(f"测试规模: {num_rows:,}行")
        print(f"{'=' * 40}")

        # 创建测试数据
        data = {
            f'col_{i}': np.random.rand(num_rows)
            for i in range(10)
        }
        df_pandas = pd.DataFrame(data)

        # 零拷贝转换（Arrow）
        start = time.time()
        df_polars_arrow = convert_pandas_to_polars(df_pandas)
        time_arrow = (time.time() - start) * 1000

        # 标准转换
        start = time.time()
        df_polars_standard = pl.from_pandas(df_pandas)
        time_standard = (time.time() - start) * 1000

        # 计算加速比
        speedup = time_standard / time_arrow if time_arrow > 0 else 1.0

        print(f"Arrow零拷贝: {time_arrow:.4f}ms")
        print(f"标准转换:   {time_standard:.4f}ms")
        print(f"加速比:     {speedup:.2f}x")

        if speedup > 1.5:
            print("✅ 零拷贝显著更快")
        elif speedup > 1.0:
            print("⚡ 零拷贝稍快")
        else:
            print("➡️  性能相近")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("🚀 QADataBridge使用示例")
    print("   高性能零拷贝数据转换和跨进程通信")
    print("=" * 60)

    # 运行所有示例
    example_01_check_support()
    example_02_pandas_to_polars()
    example_03_polars_to_pandas()
    example_04_batch_conversion()
    example_05_shared_memory_writer()
    example_06_shared_memory_reader()
    example_07_performance_comparison()

    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成")
    print("=" * 60)

    print("\n📚 更多信息:")
    print("   - QADataSwap文档: /home/quantaxis/qadataswap/README.md")
    print("   - QUANTAXIS文档: https://github.com/QUANTAXIS/QUANTAXIS")
    print("   - 性能测试: python scripts/benchmark_databridge.py")


if __name__ == '__main__':
    main()
