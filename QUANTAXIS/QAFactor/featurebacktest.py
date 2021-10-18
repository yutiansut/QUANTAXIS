#
from uuid import uuid4
from QUANTAXIS.QAUtil import QA_util_get_last_day, QA_util_get_trade_range, QA_util_code_change_format
from QUANTAXIS.QAFactor.featureView import QAFeatureView
from QUANTAXIS.QIFI.QifiAccount import QIFI_Account
from QUANTAXIS.QAFetch.QAClickhouse import QACKClient
from dateutil import parser
from qaenv import clickhouse_ip, clickhouse_password, clickhouse_user, clickhouse_port, mongo_ip

"""
backtest for feature data

"""


class QAFeatureBacktest():
    def __init__(self, feature, quantile=0.998, init_cash=50000000, rolling=5,portfolioname='feature', mongo_ip =mongo_ip,
                 clickhouse_host=clickhouse_ip, clickhouse_port=clickhouse_port, clickhouse_user=clickhouse_user, clickhouse_password=clickhouse_password) -> None:
        """
        feature --> standard QAFeature
        quantile -> prue long only   upper quantile can be selected

        init_cash --> account backtest initcash

        rolling --> dategap for rolling sell

        clickhouse should be save data first
        
        mongoip -->  use to save qifiaccount

        """
        self.feature = feature.reset_index().drop_duplicates(
            ['date', 'code']).set_index(['date', 'code']).sort_index().dropna()
        self.featurename = feature.columns[0]
        self.start = str(self.feature.index.levels[0][0])[0:10]
        self.end = str(self.feature.index.levels[0][-1])[0:10]
        self.codelist = self.feature.index.levels[1].tolist()

        self.client = QACKClient(
            host=clickhouse_host, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password)
        self.quantile = quantile
        self.preload = self.feature.groupby(
            level=0, as_index=False, group_keys=False).apply(lambda x: self.slice_feature(x))
        self.datacenter = self.client.get_stock_day_qfq_adv(
            self.codelist, self.start, self.end)
        self.closepanel = self.datacenter.closepanel.bfill() ## 向前复权 匹配股票停牌模式 使用复牌后第一个收盘价卖出
        self.account = QIFI_Account(init_cash=init_cash, username='QAFB_{}_{}'.format(self.featurename, uuid4()), broker_name='feature', portfolioname=portfolioname,
                                    password='1', nodatabase=False, model='BACKTEST', trade_host=mongo_ip)
        self.tradetable = {}
        self.rolling = rolling
        self.cashpre = init_cash/rolling
        
        self.account.initial()

    def slice_feature(self, data):
        res = data[data > data.quantile(self.quantile)].dropna()
        res.index = res.index.remove_unused_levels()
        return res

    def get_feature(self, start, end=None):
        start = parser.parse(start).date()

        end = start if end is None else parser.parse(end).date()

        return self.feature.loc[start:end, :, :]

    def get_buy_list(self, date):
        """
        date --> real date
        """
        signaldate = QA_util_get_last_day(date)
        try:
            buy = self.preload.loc[parser.parse(signaldate).date(), :, :]
            buy.index = buy.index.remove_unused_levels()
            return buy.index.levels[1].tolist()
        except:
            return []

    def get_sell_list(self, date):
        #signaldate = QA.QA_util_get_last_day(date, 5)
        try:
            sell = list(self.tradetable[QA_util_get_last_day(
                date, self.rolling-1)].keys())
            return sell
        except:
            return []

    def run(self,):
        """
        buy nextday open
        
        sell next Nday close
        """

        for date in QA_util_get_trade_range(self.start, self.end):
            buylist = self.get_buy_list(date)
            selllist = self.get_sell_list(date)
            self.tradetable[date] = {}

            if len(selllist) == 0:
                pass

            else:
                data = self.closepanel.loc[parser.parse(date).date(), selllist].map(lambda x: round(x,2)).to_dict()
                cashpre = self.cashpre/len(selllist)
                for code in selllist:

                    volume = self.tradetable[QA_util_get_last_day(
                        date, self.rolling-1)][code]
                    if volume < 100:
                        pass
                    else:
                        order = self.account.send_order(
                            code[0:6], volume, price=data[code], datetime=date+' 15:00:00', towards=-1)
                        self.account.make_deal(order)

            if len(buylist) != 0:

                d = self.datacenter.selects(
                    buylist, date, date).open.map(lambda x: round(x, 2))

                d.index = d.index.droplevel(0)

                data = d.to_dict()
                cashpre = self.cashpre/len(buylist)
                for code in buylist:
                    try:
                        volume = int(
                            0.01*cashpre/data[code])*100 if data[code] != 0 else 0
                        if volume < 100:
                            pass
                        else:
                            order = self.account.send_order(
                                code[0:6], volume, price=data[code], datetime=date+' 09:30:00', towards=1)
                            self.account.make_deal(order)
                            self.tradetable[date][code] = volume
                    except:
                        """
                        主要是停牌买不入 直接放弃
                        
                        此处买入未加入连续一字板的检测 rust 会增加此处的逻辑
                        
                        """
                        pass
            else:
                pass

            holdinglist = [QA_util_code_change_format(code)
                           for code in list(self.account.positions.keys())]
            pricepanel = self.closepanel.loc[parser.parse(date).date(), holdinglist].map(lambda x: round(x,2))
            #pricepanel.index = pricepanel.index.droplevel(0)
            pricepanel =pricepanel.to_dict()
            for code in holdinglist:

                self.account.on_price_change(code[0:6], pricepanel[code])
            self.account.settle()


if __name__ == "__main__":
    from QUANTAXIS.QAFactor import QAFeatureView
    featurepreview = QAFeatureView()
    feature = featurepreview.get_single_factor('Factor')

    print(feature)
    QAFB = QAFeatureBacktest(feature)
    QAFB.run()
