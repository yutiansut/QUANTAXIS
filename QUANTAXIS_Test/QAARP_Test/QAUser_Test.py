import unittest

import QUANTAXIS as QA


class Test_QAUser(unittest.TestCase):
    def testQAUser(self):

        user = QA.QA_User()
        portfolio1 = user.new_portfolio()

        print(user)
        print(portfolio1)

        try:
            p = user.get_portfolio(portfolio1)
            print(p)
            ac1 = user.get_portfolio(portfolio1).new_account()
            print(ac1)

            print(user)
            p2 = user.get_portfolio(portfolio1)
            ac2 = user.get_portfolio(portfolio1).get_account(ac1)

            self.assertEqual(p2, p)
            self.assertEqual(ac1, ac2)

        except:
            print("Error")
