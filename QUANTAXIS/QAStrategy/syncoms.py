
from QUANTAXIS.QAPubSub.consumer import subscriber_routing
from QUANTAXIS.QAPubSub.producer import publisher_routing
from qaenv import eventmq_ip
import json


class QAStrategySyncOrders():
    """
    订单同步器
    如何挂实盘账户请看 QATrader
    http://www.yutiansut.com:3000/topic/5dc865e8c466af76e9e3bdd1
    你可以理解成这是一个流处理的过程
    simid  被跟单的策略的id
    realid 实盘账户id
    realamount  实盘账户的订单数量
    """

    def __init__(self, simid, realid, realamount=1):
        self.sub = subscriber_routing(
            exchange='QAORDER_ROUTER', host=eventmq_ip, routing_key=simid)
        self.pub = publisher_routing(
            exchange='QAORDER_ROUTER', host=eventmq_ip, routing_key=realid)
        self.realamount = realamount
        self.realid = realid
        self.simid = simid

    def add_subscriber(self, simid):
        self.sub.add_sub('QAORDER_ROUTER', simid)

    def callback(self, a, b, c, data):
        d = json.loads(data, encoding='utf-8')

        if d['topic'] == 'send_order':

            self.on_order(d)

    def on_order(self, order):
        """在此处理你的订单逻辑
        如果你订阅了多个策略账户 则order['account_cookie']不相同

        Arguments:
            order {[type]} -- [description]
        """
        self.send_order(order)

    def send_order(self, order):

        order['topic'] = 'sendorder'
        order['code'] = order['instrument_id']
        order['account_cookie'] = self.realid
        order['user_id'] = self.realid
        order['volume'] = self.realamount
        order['order_direction'] = order['direction']
        order['order_offset'] = order['offset']
        self.pub.pub(json.dumps(order), routing_key=self.realid)

    def start(self):
        self.sub.callback = self.callback
        self.sub.start()
