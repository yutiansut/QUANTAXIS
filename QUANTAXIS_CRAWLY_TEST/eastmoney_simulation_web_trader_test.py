from QUANTAXIS_CRAWLY.eastmoney_simulation_web_trader import EastMoneySimulationWebTrader
import unittest

class TestEastMoneySimTrader(unittest.TestCase):

    def testTrader(self):
        EMSimTrader = EastMoneySimulationWebTrader()
        EMSimTrader.startTrade()


