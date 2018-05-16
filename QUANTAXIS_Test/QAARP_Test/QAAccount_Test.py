import unittest;

#from QUANTAXIS.QAARP import ( QAAccount )
from QUANTAXIS import *;
import QUANTAXIS as QA


class Test_QAAccount(unittest.TestCase):

    def test_QAAccount_class(self):

        Account = QA.QA_Account()
        B = QA.QA_BacktestBroker()

        Order = Account.send_order(code='000001',
                                   price=11,
                                   money=Account.cash_available,
                                   time='2018-01-09',
                                   towards=QA.ORDER_DIRECTION.BUY,
                                   order_model=QA.ORDER_MODEL.MARKET,
                                   amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                   )

        print('ORDER的占用资金: {}'.format((Order.amount * Order.price) * (1 + Account.commission_coeff)))
        print('账户剩余资金 :{}'.format(Account.cash_available))
        rec_mes=B.receive_order(QA.QA_Event(order=Order))
        print(rec_mes)
        Account.receive_deal(rec_mes)
        print('账户的可用资金 {}'.format(Account.cash_available))



        