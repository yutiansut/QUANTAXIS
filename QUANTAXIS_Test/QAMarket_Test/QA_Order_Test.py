import unittest

from QUANTAXIS.QAMarket import QA_Order;

from unittest.mock import MagicMock;
from unittest.mock import Mock;

class QA_OrderTest(unittest.TestCase):

    # 随机创建一批订单
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testQAOrder(self):

        aQaOrder = QA_Order();
        aQaOrder.get = Mock(return_value=None)
        self.assertEqual(aQaOrder.get(None), None)

        aQaOrder.get = Mock(return_value="1.0")
        self.assertEqual(aQaOrder.get('price'), '1.0')



        print(" test QAOrder !")
