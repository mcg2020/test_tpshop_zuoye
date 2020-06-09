# 导包
import os
import time
import unittest
from HTMLTestRunner_PY3 import HTMLTestRunner
from script.tpshop_test_parameterized import TpshopTest

# 实例化测试套件
suite = unittest.TestSuite()
# 添加测试用例
suite.addTest(unittest.makeSuite(TpshopTest))
# 设置测试报告的路径和名称
report_path = os.path.dirname(os.path.abspath(__file__)) + \
              "/report/ihrm{}.html".format(time.strftime('%Y%m%d %H%M%S'))
with open(report_path, mode='wb') as f:
    # 实例化HTMLTestRunner
    runner = HTMLTestRunner.HTMLTestRunner(f, verbosity=1, title="IHRM人力资源管理 系统接口测试报告",
                                           description="测试登陆接口和员工管理模块")
    # 使用Runner运行测试套件生成测试报告
    runner.run(suite)