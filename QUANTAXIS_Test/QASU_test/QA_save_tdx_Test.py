import unittest
import pprint

from QUANTAXIS import QUANTAXIS as QA
from QUANTAXIS.QAUtil.QADate import *
from QUANTAXIS.QAUtil.QADate_trade import *

#from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_option_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_M_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_SR_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_CU_contract_time_to_market)

from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_C_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_CF_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_RU_contract_time_to_market)

from QUANTAXIS.QASU.save_tdx import  (_save_option_commodity_au_day)
from QUANTAXIS.QASU.save_tdx import  (_save_option_commodity_au_min)




class TestSaveOptionData(unittest.TestCase):

    def testQA_save_option_commodity_au_day(self):
        _save_option_commodity_au_day()

    def testQA_save_option_commodity_au_min(self):
        _save_option_commodity_au_min()

if __name__ == '__main__':
    unittest.main()