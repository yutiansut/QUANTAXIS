

import QUANTAXIS as QA


collection=QA.QA_Setting.client.quantaxis.backtest_history
collection.ensure_index('cookie')