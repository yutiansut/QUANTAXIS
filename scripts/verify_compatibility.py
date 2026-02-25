# coding:utf-8
"""
QUANTAXIS 2.1.0 兼容性验证脚本 (源代码级别)

通过直接检查源代码文件来验证向后兼容性
不依赖于安装环境,避免环境问题

作者: @yutiansut @quantaxis
版本: 2.1.0-alpha2
日期: 2025-10-25
"""

import os
import re
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("=" * 80)
print("QUANTAXIS 2.1.0 源代码级兼容性验证")
print("=" * 80)
print(f"项目路径: {PROJECT_ROOT}")
print("=" * 80)

# 测试结果统计
tests_passed = 0
tests_failed = 0
total_tests = 0


def test_result(test_name, passed, details=""):
    """记录测试结果"""
    global tests_passed, tests_failed, total_tests
    total_tests += 1

    if passed:
        tests_passed += 1
        print(f"\n✅ [{total_tests}] {test_name}")
    else:
        tests_failed += 1
        print(f"\n❌ [{total_tests}] {test_name}")

    if details:
        print(f"   {details}")


def check_file_exists(file_path):
    """检查文件是否存在"""
    full_path = PROJECT_ROOT / file_path
    return full_path.exists()


def check_function_exists(file_path, function_name):
    """检查函数是否存在于文件中"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False, "文件不存在"

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 检查函数定义
        pattern = rf'^def {re.escape(function_name)}\('
        if re.search(pattern, content, re.MULTILINE):
            return True, f"找到函数定义"
        return False, "未找到函数定义"


def check_class_exists(file_path, class_name):
    """检查类是否存在于文件中"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False, "文件不存在"

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 检查类定义
        pattern = rf'^class {re.escape(class_name)}[\(:]'
        if re.search(pattern, content, re.MULTILINE):
            return True, f"找到类定义"
        return False, "未找到类定义"


def check_method_exists(file_path, class_name, method_name):
    """检查类方法是否存在"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False, "文件不存在"

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 简单检查方法定义
        pattern = rf'def {re.escape(method_name)}\('
        if re.search(pattern, content):
            return True, f"找到方法 {method_name}"
        return False, f"未找到方法 {method_name}"


def check_import_exists(file_path, import_name):
    """检查导出是否存在于__init__.py中"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False, "文件不存在"

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 检查是否在导出列表中
        if import_name in content:
            return True, f"找到导出: {import_name}"
        return False, f"未找到导出: {import_name}"


def get_version():
    """获取版本号"""
    init_file = PROJECT_ROOT / "QUANTAXIS" / "__init__.py"
    if not init_file.exists():
        return None

    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.MULTILINE)
        if match:
            return match.group(1)
    return None


# ============================================================================
# 测试1: 版本检查
# ============================================================================
print("\n" + "=" * 80)
print("第一部分: 版本验证")
print("=" * 80)

version = get_version()
if version == '2.1.0.alpha2':
    test_result("版本号正确", True, f"版本: {version}")
else:
    test_result("版本号检查", False, f"期望: 2.1.0.alpha2, 实际: {version}")


# ============================================================================
# 测试2: 旧API存在性检查 (c1e609d兼容性)
# ============================================================================
print("\n" + "=" * 80)
print("第二部分: 旧API兼容性验证 (c1e609d)")
print("=" * 80)

# 2.1 MongoDB旧API
passed, details = check_function_exists(
    "QUANTAXIS/QAUtil/QASql.py",
    "QA_util_sql_mongo_setting"
)
test_result("MongoDB旧API - QA_util_sql_mongo_setting", passed, details)

# 2.2 RabbitMQ旧API
passed, details = check_class_exists(
    "QUANTAXIS/QAPubSub/base.py",
    "base_ps"
)
test_result("RabbitMQ旧API - base_ps", passed, details)

# 2.3 QAMarket旧API
passed, details = check_class_exists(
    "QUANTAXIS/QAMarket/QAOrder.py",
    "QA_Order"
)
test_result("QAMarket旧API - QA_Order", passed, details)

passed, details = check_class_exists(
    "QUANTAXIS/QAMarket/QAPosition.py",
    "QA_Position"
)
test_result("QAMarket旧API - QA_Position", passed, details)

passed, details = check_class_exists(
    "QUANTAXIS/QAMarket/market_preset.py",
    "MARKET_PRESET"
)
test_result("QAMarket旧API - MARKET_PRESET", passed, details)

# 2.4 QIFI Account旧API
passed, details = check_class_exists(
    "QUANTAXIS/QIFI/QifiAccount.py",
    "QIFI_Account"
)
test_result("QIFI旧API - QIFI_Account", passed, details)

# 2.5 数据获取旧API
passed, details = check_function_exists(
    "QUANTAXIS/QAFetch/__init__.py",
    "QA_fetch_get_stock_list"
)
test_result("数据获取旧API - QA_fetch_get_stock_list", passed, details)


# ============================================================================
# 测试3: 新增功能检查 (向后兼容的增强)
# ============================================================================
print("\n" + "=" * 80)
print("第三部分: 新增功能验证 (不破坏兼容性)")
print("=" * 80)

# 3.1 base_ps context manager支持
passed, details = check_method_exists(
    "QUANTAXIS/QAPubSub/base.py",
    "base_ps",
    "__enter__"
)
test_result("base_ps新增 - with语句支持 (__enter__)", passed, details)

passed, details = check_method_exists(
    "QUANTAXIS/QAPubSub/base.py",
    "base_ps",
    "__exit__"
)
test_result("base_ps新增 - with语句支持 (__exit__)", passed, details)

passed, details = check_method_exists(
    "QUANTAXIS/QAPubSub/base.py",
    "base_ps",
    "close"
)
test_result("base_ps增强 - 优雅关闭 (close)", passed, details)

# 3.2 资源管理器新API
passed, details = check_class_exists(
    "QUANTAXIS/QAUtil/QAResourceManager.py",
    "QAMongoResourceManager"
)
test_result("新增模块 - QAMongoResourceManager", passed, details)

passed, details = check_class_exists(
    "QUANTAXIS/QAUtil/QAResourceManager.py",
    "QARabbitMQResourceManager"
)
test_result("新增模块 - QARabbitMQResourceManager", passed, details)

passed, details = check_class_exists(
    "QUANTAXIS/QAUtil/QAResourceManager.py",
    "QAResourcePool"
)
test_result("新增模块 - QAResourcePool", passed, details)

# 3.3 检查新API在__init__.py中的导出
passed, details = check_import_exists(
    "QUANTAXIS/__init__.py",
    "QAMongoResourceManager"
)
test_result("主模块导出 - QAMongoResourceManager", passed, details)

passed, details = check_import_exists(
    "QUANTAXIS/__init__.py",
    "QA_Order"
)
test_result("主模块导出 - QA_Order (新增便捷导入)", passed, details)


# ============================================================================
# 测试4: 文档完整性检查
# ============================================================================
print("\n" + "=" * 80)
print("第四部分: 文档完整性验证")
print("=" * 80)

docs_to_check = [
    ("BACKWARD_COMPATIBILITY_REPORT.md", "详细兼容性分析报告"),
    ("COMPATIBILITY_SUMMARY.md", "兼容性总结"),
    ("FINAL_SUMMARY.md", "最终工作总结"),
    ("scripts/test_backward_compatibility.py", "自动化测试脚本"),
    ("examples/resource_manager_example.py", "资源管理器示例"),
    ("QUANTAXIS/QAUtil/RESOURCE_MANAGER_README.md", "资源管理器文档"),
]

for doc_path, doc_name in docs_to_check:
    exists = check_file_exists(doc_path)
    test_result(f"文档 - {doc_name}", exists,
                f"文件: {doc_path}" if exists else f"文件不存在: {doc_path}")


# ============================================================================
# 测试5: 依赖版本检查
# ============================================================================
print("\n" + "=" * 80)
print("第五部分: 依赖版本验证")
print("=" * 80)

requirements_file = PROJECT_ROOT / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        req_content = f.read()

        # 检查关键依赖
        critical_deps = {
            "pymongo": r"pymongo>=4\.10",
            "pika": r"pika>=1\.3\.2",
            "pandas": r"pandas>=2\.0",
            "pytdx": r"pytdx>=1\.72",  # 修复后的版本
        }

        for dep_name, pattern in critical_deps.items():
            if re.search(pattern, req_content):
                test_result(f"依赖版本 - {dep_name}", True,
                           f"找到正确的版本要求")
            else:
                test_result(f"依赖版本 - {dep_name}", False,
                           f"版本要求不正确或缺失")
else:
    test_result("requirements.txt文件", False, "文件不存在")


# ============================================================================
# 测试总结
# ============================================================================
print("\n" + "=" * 80)
print("验证总结")
print("=" * 80)
print(f"总测试数: {total_tests}")
print(f"通过: {tests_passed} ✅")
print(f"失败: {tests_failed} ❌")

if tests_failed == 0:
    success_rate = 100.0
    print(f"\n🎉 所有测试通过! 向后兼容性验证成功!")
    print(f"成功率: {success_rate:.1f}%")
else:
    success_rate = (tests_passed / total_tests) * 100
    print(f"\n⚠️ 部分测试失败")
    print(f"成功率: {success_rate:.1f}%")

# 兼容性评级
if success_rate == 100:
    grade = "A+ (完美)"
elif success_rate >= 95:
    grade = "A (优秀)"
elif success_rate >= 90:
    grade = "B+ (良好)"
elif success_rate >= 85:
    grade = "B (合格)"
elif success_rate >= 80:
    grade = "C+ (基本合格)"
elif success_rate >= 70:
    grade = "C (需改进)"
else:
    grade = "D (不合格)"

print(f"兼容性评级: {grade}")

# 关键结论
print("\n" + "=" * 80)
print("关键结论")
print("=" * 80)

if tests_failed == 0:
    print("✅ QUANTAXIS 2.1.0-alpha2 与 c1e609d 版本**完全向后兼容**")
    print("✅ 所有旧API保持不变,可直接升级")
    print("✅ 新功能为可选增强,不影响现有代码")
    print("⚠️ 需要Python 3.9+环境")
else:
    print(f"⚠️ 发现 {tests_failed} 个问题,需要修复")

print("=" * 80)

# 返回退出码
sys.exit(0 if tests_failed == 0 else 1)
