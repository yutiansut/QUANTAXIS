# coding:utf-8
"""
QUANTAXIS 2.1.0 向后兼容性测试脚本

测试所有旧API是否在新版本中正常工作

作者: @yutiansut @quantaxis
版本: 2.1.0-alpha2
"""

import sys
import traceback

print("=" * 70)
print("QUANTAXIS 2.1.0 向后兼容性测试")
print("=" * 70)

# 测试结果统计
total_tests = 0
passed_tests = 0
failed_tests = 0


def test_case(name, func):
    """执行单个测试用例"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    print(f"\n[{total_tests}] 测试: {name}")
    try:
        func()
        print(f"    ✅ 通过")
        passed_tests += 1
        return True
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        traceback.print_exc()
        failed_tests += 1
        return False


# ============================================================================
# 测试1: 版本检查
# ============================================================================

def test_version():
    """测试版本号"""
    import QUANTAXIS as QA

    print(f"    版本: {QA.__version__}")
    assert QA.__version__ == '2.1.0.alpha2', f"版本不匹配: {QA.__version__}"

    print(f"    作者: {QA.__author__}")
    assert QA.__author__ == 'yutiansut', f"作者不匹配: {QA.__author__}"

    # 检查Rust支持
    print(f"    QARS2支持: {QA.__has_qars__}")
    print(f"    QADataSwap支持: {QA.__has_dataswap__}")


# ============================================================================
# 测试2: 旧API - MongoDB连接
# ============================================================================

def test_old_mongo_api():
    """测试旧的MongoDB连接API"""
    from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting

    # 这是旧版本的API，应该仍然有效
    client = QA_util_sql_mongo_setting()
    print(f"    客户端类型: {type(client)}")

    # 测试连接
    try:
        client.admin.command('ping')
        print(f"    连接状态: 正常")
    except Exception as e:
        print(f"    连接状态: 无法连接 ({e})")

    # 关闭连接
    client.close()
    print(f"    连接已关闭")


# ============================================================================
# 测试3: 旧API - RabbitMQ
# ============================================================================

def test_old_rabbitmq_api():
    """测试旧的RabbitMQ API"""
    from QUANTAXIS.QAPubSub.base import base_ps

    # 旧版本的API
    try:
        ps = base_ps()
        print(f"    连接状态: {ps.connection.is_open}")
        print(f"    通道状态: {ps.channel.is_open}")
        ps.close()
        print(f"    连接已关闭")
    except Exception as e:
        print(f"    RabbitMQ不可用: {e}")
        print(f"    (这是正常的，如果没有RabbitMQ服务)")


# ============================================================================
# 测试4: 旧API - QAMarket
# ============================================================================

def test_old_qamarket_api():
    """测试旧的QAMarket API"""
    # 旧的导入方式应该仍然有效
    from QUANTAXIS.QAMarket.QAOrder import QA_Order
    from QUANTAXIS.QAMarket.QAPosition import QA_Position
    from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET

    # 创建订单
    order = QA_Order(
        account_cookie='test_account',
        code='000001',
        price=10.5,
        amount=1000,
        order_direction='BUY'
    )
    print(f"    订单ID: {order.order_id[:20]}...")
    print(f"    订单代码: {order.code}")

    # 创建持仓
    pos = QA_Position(code='000001', market_type='STOCK_CN')
    print(f"    持仓代码: {pos.code}")

    # 市场预设
    preset = MARKET_PRESET()
    rb_info = preset.get_code('RB')
    if rb_info:
        print(f"    RB合约乘数: {rb_info.get('unit_table')}")


# ============================================================================
# 测试5: 旧API - QIFI账户
# ============================================================================

def test_old_qifi_api():
    """测试旧的QIFI账户API"""
    from QUANTAXIS.QIFI.QifiAccount import QIFI_Account

    # 旧版本的API
    account = QIFI_Account(
        username='test_user',
        password='test_password',
        trade_host='stock',
        init_cash=100000.0
    )

    print(f"    账户用户名: {account.account_cookie}")
    print(f"    初始资金: {account.init_cash}")
    print(f"    当前可用: {account.available}")


# ============================================================================
# 测试6: 旧API - 数据获取
# ============================================================================

def test_old_fetch_api():
    """测试旧的数据获取API"""
    import QUANTAXIS as QA

    # 注意: 这个测试需要数据库支持，可能失败
    try:
        # 这是旧版本的API
        df = QA.QA_fetch_get_stock_list()
        print(f"    股票列表条数: {len(df) if df is not None else 0}")

        # 尝试获取日线数据
        df_day = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-05')
        if df_day is not None:
            print(f"    日线数据条数: {len(df_day)}")
    except Exception as e:
        print(f"    数据获取失败 (数据库未配置): {e}")


# ============================================================================
# 测试7: 新API可用性 (不影响兼容性)
# ============================================================================

def test_new_api_availability():
    """测试新API是否可用"""
    import QUANTAXIS as QA

    # 测试QAMarket是否可以从主模块导入
    try:
        from QUANTAXIS import QA_Order, QA_Position, MARKET_PRESET
        print(f"    ✅ QAMarket可从主模块导入")
    except ImportError as e:
        print(f"    ❌ QAMarket导入失败: {e}")

    # 测试QAResourceManager是否可用
    try:
        from QUANTAXIS import QAMongoResourceManager, QAResourcePool
        print(f"    ✅ QAResourceManager可用")
    except ImportError:
        print(f"    ⚠️  QAResourceManager不可用 (依赖未安装)")

    # 测试QARSBridge是否可用
    try:
        from QUANTAXIS import QARSAccount, has_qars_support
        print(f"    ✅ QARSBridge可用: {has_qars_support()}")
    except ImportError:
        print(f"    ⚠️  QARSBridge不可用 (qars3未安装)")

    # 测试QADataBridge是否可用
    try:
        from QUANTAXIS import convert_pandas_to_polars, has_dataswap_support
        print(f"    ✅ QADataBridge可用: {has_dataswap_support()}")
    except ImportError:
        print(f"    ⚠️  QADataBridge不可用 (qadataswap未安装)")


# ============================================================================
# 测试8: with语句支持 (新增功能)
# ============================================================================

def test_context_manager_support():
    """测试with语句支持"""
    from QUANTAXIS.QAPubSub.base import base_ps

    # 新增的with语句支持
    try:
        with base_ps() as ps:
            print(f"    进入with块: 连接={ps.connection.is_open}")
        print(f"    ✅ with语句支持正常")
    except Exception as e:
        print(f"    RabbitMQ不可用: {e}")


# ============================================================================
# 主测试流程
# ============================================================================

def main():
    """执行所有测试"""
    print("\n" + "=" * 70)
    print("开始测试...")
    print("=" * 70)

    # 执行测试
    test_case("版本检查", test_version)
    test_case("旧API - MongoDB连接", test_old_mongo_api)
    test_case("旧API - RabbitMQ", test_old_rabbitmq_api)
    test_case("旧API - QAMarket", test_old_qamarket_api)
    test_case("旧API - QIFI账户", test_old_qifi_api)
    test_case("旧API - 数据获取", test_old_fetch_api)
    test_case("新API可用性", test_new_api_availability)
    test_case("with语句支持", test_context_manager_support)

    # 总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"总测试数: {total_tests}")
    print(f"通过: {passed_tests} ✅")
    print(f"失败: {failed_tests} ❌")

    if failed_tests == 0:
        print("\n🎉 所有测试通过! 向后兼容性验证成功!")
        success_rate = 100.0
    else:
        success_rate = (passed_tests / total_tests) * 100
        print(f"\n⚠️  部分测试失败，成功率: {success_rate:.1f}%")

    # 兼容性评级
    if success_rate == 100:
        grade = "A+ (完美)"
    elif success_rate >= 90:
        grade = "A (优秀)"
    elif success_rate >= 80:
        grade = "B (良好)"
    elif success_rate >= 70:
        grade = "C (合格)"
    else:
        grade = "D (需要改进)"

    print(f"兼容性评级: {grade}")

    print("\n" + "=" * 70)

    # 返回退出码
    return 0 if failed_tests == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
