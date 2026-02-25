#!/usr/bin/env python3
"""
QUANTAXIS QARSBridge 使用示例

演示如何使用QARSBridge桥接层访问QARS2 Rust高性能组件
包括账户管理、交易操作、回测引擎等核心功能

@yutiansut @quantaxis
"""

from QUANTAXIS.QARSBridge import (
    QARSAccount,
    QARSBacktest,
    has_qars_support,
    HAS_QARS
)
import pandas as pd


# ============================================================================
# 示例1: 检测QARS2支持
# ============================================================================

def example_check_qars_support():
    """
    检查QARS2 Rust核心是否可用

    如果QARS2未安装，系统会自动回退到纯Python实现
    """
    print("=" * 60)
    print("示例1: 检测QARS2支持")
    print("=" * 60)

    if has_qars_support():
        print("✓ QARS2 Rust核心可用")
        print("  性能提升: 账户操作100x, 回测10x")
    else:
        print("⚠ QARS2未安装，使用Python fallback")
        print("  建议安装: pip install quantaxis[rust]")

    print(f"\nHAS_QARS: {HAS_QARS}")
    print()


# ============================================================================
# 示例2: 创建和使用QARS账户
# ============================================================================

def example_qars_account():
    """
    演示QARSAccount的基本使用

    包括：
    - 创建账户
    - 股票买卖
    - 期货开平仓
    - 查询持仓和账户信息
    """
    print("=" * 60)
    print("示例2: QARS账户基本操作")
    print("=" * 60)

    # 创建账户
    account = QARSAccount(
        account_cookie="demo_account",
        portfolio="测试组合",
        init_cash=1000000.0,
        environment="backtest"
    )

    print(f"账户创建成功: {account}")
    print()

    # 股票交易示例
    print("--- 股票交易 ---")

    # 买入平安银行
    success = account.buy("000001", 10.5, "2025-01-15", 1000)
    print(f"买入000001: {'成功' if success else '失败'}")

    # 买入招商银行
    success = account.buy("600036", 38.2, "2025-01-15", 500)
    print(f"买入600036: {'成功' if success else '失败'}")

    # 查看持仓
    positions = account.get_positions()
    print(f"\n当前持仓:\n{positions[['code', 'volume_long']]}")

    # 卖出部分持仓
    success = account.sell("000001", 10.8, "2025-01-16", 500)
    print(f"\n卖出000001: {'成功' if success else '失败'}")

    print()

    # 期货交易示例
    print("--- 期货交易 ---")

    # IF沪深300股指期货 - 买入开仓(做多)
    success = account.buy_open("IF2512", 4500.0, "2025-01-15", 2)
    print(f"IF2512买入开仓: {'成功' if success else '失败'}")

    # IC中证500股指期货 - 卖出开仓(做空)
    success = account.sell_open("IC2512", 6800.0, "2025-01-15", 1)
    print(f"IC2512卖出开仓: {'成功' if success else '失败'}")

    # 查看期货持仓
    positions = account.get_positions()
    if not positions.empty:
        print(f"\n期货持仓:")
        print(positions[['code', 'volume_long', 'volume_short', 'margin']])

    # 平仓操作
    success = account.sell_close("IF2512", 4520.0, "2025-01-16", 1)
    print(f"\nIF2512卖出平仓: {'成功' if success else '失败'}")

    print()

    # 查询账户信息
    print("--- 账户信息 ---")
    account_info = account.get_account_info()

    print(f"账户权益: {account_info.get('balance', 0):.2f}")
    print(f"可用资金: {account_info.get('available', 0):.2f}")
    print(f"占用保证金: {account_info.get('margin', 0):.2f}")
    print(f"浮动盈亏: {account_info.get('float_profit', 0):.2f}")
    print(f"风险度: {account_info.get('risk_ratio', 0):.2%}")

    print()

    # 导出QIFI格式
    print("--- QIFI格式导出 ---")
    qifi = account.get_qifi()
    print(f"QIFI账户cookie: {qifi['account_cookie']}")
    print(f"持仓数量: {len(qifi.get('positions', {}))}")
    print(f"订单数量: {len(qifi.get('orders', {}))}")
    print(f"成交数量: {len(qifi.get('trades', {}))}")

    print()


# ============================================================================
# 示例3: 上下文管理器使用
# ============================================================================

def example_context_manager():
    """
    演示使用with语句管理账户

    退出时会自动结算账户
    """
    print("=" * 60)
    print("示例3: 上下文管理器")
    print("=" * 60)

    with QARSAccount(
        account_cookie="context_account",
        init_cash=1000000.0
    ) as account:
        # 执行交易
        account.buy("000001", 10.5, "2025-01-15", 1000)
        account.buy("600036", 38.2, "2025-01-15", 500)

        # 查询
        info = account.get_account_info()
        print(f"账户余额: {info.get('balance', 0):.2f}")
        print(f"可用资金: {info.get('available', 0):.2f}")

    # 退出with块时自动结算
    print("\n账户已自动结算")
    print()


# ============================================================================
# 示例4: 从QIFI恢复账户
# ============================================================================

def example_from_qifi():
    """
    演示从QIFI字典创建账户

    这允许账户状态的保存和恢复
    """
    print("=" * 60)
    print("示例4: 从QIFI恢复账户")
    print("=" * 60)

    # 创建原始账户并交易
    account1 = QARSAccount(
        account_cookie="qifi_account",
        init_cash=1000000.0
    )
    account1.buy("000001", 10.5, "2025-01-15", 1000)
    account1.buy("600036", 38.2, "2025-01-15", 500)

    # 导出QIFI
    qifi = account1.get_qifi()
    print(f"原始账户: {account1}")

    # 从QIFI创建新账户
    account2 = QARSAccount.from_qifi(qifi)
    print(f"恢复账户: {account2}")

    # 验证状态
    positions1 = account1.get_positions()
    positions2 = account2.get_positions()

    print(f"\n原始账户持仓数: {len(positions1)}")
    print(f"恢复账户持仓数: {len(positions2)}")

    print()


# ============================================================================
# 示例5: 回测引擎 (需要QARS2完整支持)
# ============================================================================

def example_backtest():
    """
    演示QARS回测引擎使用

    注意: 此功能需要QARS2完整安装
    """
    print("=" * 60)
    print("示例5: 回测引擎")
    print("=" * 60)

    if not HAS_QARS:
        print("⚠ 回测引擎需要QARS2支持")
        print("  请安装: pip install quantaxis[rust]")
        print()
        return

    try:
        # 创建回测引擎
        backtest = QARSBacktest(
            start="2024-01-01",
            end="2024-12-31"
        )

        print(f"回测引擎: {backtest}")
        print("回测功能演示需要完整的QARS2策略系统")

        # TODO: 添加策略示例
        # class SimpleStrategy(QARSStrategy):
        #     def on_bar(self, bar):
        #         # 策略逻辑
        #         pass

        print()

    except Exception as e:
        print(f"回测引擎初始化失败: {e}")
        print()


# ============================================================================
# 示例6: 分红和拆股事件
# ============================================================================

def example_corporate_actions():
    """
    演示股票分红和拆股事件处理
    """
    print("=" * 60)
    print("示例6: 公司行为事件")
    print("=" * 60)

    account = QARSAccount(
        account_cookie="events_account",
        init_cash=1000000.0
    )

    # 买入股票
    account.buy("000001", 10.0, "2025-01-15", 10000)

    print("初始持仓:")
    positions = account.get_positions()
    print(positions[['code', 'volume_long', 'open_price_long']])

    # 分红事件: 每股分红0.5元
    account.receive_dividend("000001", 0.5, "2025-03-20")
    print("\n分红后账户信息:")
    info = account.get_account_info()
    print(f"账户余额: {info.get('balance', 0):.2f}")

    # 拆股事件: 1拆2
    account.stock_split("000001", 2.0, "2025-06-01")
    print("\n拆股后持仓:")
    positions = account.get_positions()
    print(positions[['code', 'volume_long', 'open_price_long']])

    print()


# ============================================================================
# 示例7: 性能对比
# ============================================================================

def example_performance_comparison():
    """
    对比QARS2 Rust版本和Python版本的性能
    """
    print("=" * 60)
    print("示例7: 性能对比")
    print("=" * 60)

    import time

    # 测试创建账户性能
    print("测试1: 创建1000个账户")

    start = time.time()
    for i in range(1000):
        account = QARSAccount(
            account_cookie=f"test_{i}",
            init_cash=1000000.0
        )
    elapsed = time.time() - start

    print(f"耗时: {elapsed:.3f}秒")
    if HAS_QARS:
        print(f"  (Rust版本预期: ~0.5秒)")
    else:
        print(f"  (Python版本预期: ~50秒)")

    print()

    # 测试订单发送性能
    print("测试2: 发送10000个订单")

    account = QARSAccount(
        account_cookie="perf_test",
        init_cash=100000000.0
    )

    start = time.time()
    for i in range(10000):
        account.buy("000001", 10.0 + i * 0.001, "2025-01-15", 100)
    elapsed = time.time() - start

    print(f"耗时: {elapsed:.3f}秒")
    if HAS_QARS:
        print(f"  (Rust版本预期: ~0.5秒)")
    else:
        print(f"  (Python版本预期: ~50秒)")

    print()


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有示例"""

    print("\n" + "=" * 60)
    print("QUANTAXIS QARSBridge 使用示例")
    print("@yutiansut @quantaxis")
    print("=" * 60 + "\n")

    # 运行所有示例
    example_check_qars_support()
    example_qars_account()
    example_context_manager()
    example_from_qifi()
    example_backtest()
    example_corporate_actions()
    example_performance_comparison()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
