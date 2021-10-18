
from qaenv import mongo_ip
from QUANTAXIS.QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAUtil import QA_util_to_json_from_pandas
from QUANTAXIS.QIFI.QifiManager import QA_QIFIMANAGER, QA_QIFISMANAGER
class QAQIFI_Handler(QABaseHandler):
    #manager = QA_QIFIMANAGER(mongo_ip)
    manager = QA_QIFISMANAGER(mongo_ip)

    def get(self):
        action = self.get_argument('action', 'acchistory')

        acc = self.get_argument('account_cookie', 'KTKS_t01_au2012_5min')
        manage_acc = QA_QIFIMANAGER(acc, mongo_ip)
        if action == 'acchistory':
            """
            GET http://127.0.0.1:8019/qifi?action=monthprofit
            {
            "res": {
                "2020-02-03 00:00:00": 51212,
                "2020-02-04 00:00:00": 50602,
                "2020-02-05 00:00:00": 50922,
                "2020-02-06 00:00:00": 50522,
                "2020-02-07 00:00:00": 50442,
                "2020-02-10 00:00:00": 51233,
                "2020-02-11 00:00:00": 51103,
                "2020-02-12 00:00:00": 51123,
                "2020-02-13 00:00:00": 51023,
                "2020-02-14 00:00:00": 50923,
                "2020-02-17 00:00:00": 51073,
                "2020-02-18 00:00:00": 50993,
                "2020-02-19 00:00:00": 51443,
                "2020-02-20 00:00:00": 50573,
                "2020-02-21 00:00:00": 50893,
                "2020-02-24 00:00:00": 50723,
                "2020-02-25 00:00:00": 50843,
                }
            }
            """
            history_assets = manage_acc.assets
            history_assets.index = history_assets.index.map(str)
            self.write({'res': history_assets.to_dict()})
        elif action == 'monthprofit':
            """
            GET http://127.0.0.1:8019/qifi?action=monthprofit
            {
                "res": {
                    "2020-02-29 00:00:00": -899.0,
                    "2020-03-31 00:00:00": 4024.0,
                    "2020-04-30 00:00:00": -7704.0,
                    "2020-05-31 00:00:00": 136.0,
                    "2020-06-30 00:00:00": -1847.0,
                    "2020-07-31 00:00:00": 60.0
                }
            }
            """
            self.write({'res': manage_acc.month_assets_profit.to_dict()})
        elif action == 'historytrade':
            """
            GET http://127.0.0.1:8019/qifi?action=historytrade
            {
                "res": [
                    {
                        "commission": 2.0,
                        "direction": "SELL",
                        "offset": "OPEN",
                        "price": 4084.1736,
                        "trade_date_time": 1579141800000000000,
                        "volume": 1.0,
                        "code": "a2009",
                        "datetime": "2020-01-16 10:30:00"
                    },
                    {
                        "commission": 2.0,
                        "direction": "BUY",
                        "offset": "CLOSE",
                        "price": 4065.4436,
                        "trade_date_time": 1581297600000000000,
                        "volume": 1.0,
                        "code": "a2009",
                        "datetime": "2020-02-10 09:20:00"
                    },
                ]
            }
            """

            res = manage_acc.trade.loc[:, ['commission', 'direction',
                                           'instrument_id', 'offset', 'price', 'trade_date_time', 'volume']].reset_index()
            res = res.assign(datetime=res.tradetime.map(str)).loc[:, ['commission', 'direction',
                                                                      'offset', 'price', 'trade_date_time', 'volume', 'code', 'datetime']]

            self.write({'res': QA_util_to_json_from_pandas(res)})

        elif action == 'holdingpanel':
            trading_day = self.get_argument('trading_day')
            res = self.manager.get_holding_panel(acc, trading_day)
            self.write({'res': QA_util_to_json_from_pandas(res)})


class QAQIFIS_Handler(QABaseHandler):
    #manager = QA_QIFIMANAGER(mongo_ip)
    manager = QA_QIFISMANAGER(mongo_ip)

    def get(self):
        action = self.get_argument('action', 'acchistory')

        if action == 'accountlist':
            res = self.manager.get_allaccountname()
            self.write({'res': res})
        elif action == 'portfoliolist':
            res = self.manager.get_allportfolio()
            self.write({'res': res})
        elif action == 'accountinportfolio':
            portfolio = self.get_argument('portfolio', 't12')
            res = self.manager.get_portfolio_panel(portfolio)

            self.write({'res': QA_util_to_json_from_pandas(res)})

    def post(self):
        action = self.get_argument('action', 'change_name')
        if action == 'drop_account':

            account_cookie = self.get_argument('account_cookie')
            res = self.manager.drop_account(account_cookie)
            self.write({
                'res': res,
                'status': 200
            })
        elif action == 'drop_many':
            account_cookies = self.get_argument('account_cookies')
            res = self.manager.drop_many(account_cookies)
            self.write({
                'res': res,
                'status': 200
            })

