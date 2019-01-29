#

from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
from QUANTAXIS.QAARP.QAUser import QA_User
import threading
from QUANTAXIS.QAUtil.QASetting import DATABASE

class QA_Model(QA_Thread):
    """
    运行中的策略被称为一个QAModel, QAModel是一个已经封装完整 可以直接运行的策略

    只需要指定其运行环境即可

     具备websocket能力/ 实例化为一个可以交易的websocket型账户

    Arguments:
        QA_Thread {[type]} -- [description]

    Raises:
        Exception -- [description]

    Returns:
        [type] -- [description]
    """

    def __init__(self, user: QA_User, wsuri: str, broker_name='simnow', sig=True):

        super().__init__(name='QAModel_{}'.format(account_cookie))
        
        self.account_cookie = user.generate_simpleaccount()
        self.password = password
        self.broker_name = broker_name
        self.account_client = DATABASE.model
        self.connection = True
        self.message = {'password': password, 'wsuri': wsuri, 'broker_name': broker_name, 'updatetime': str(
            datetime.datetime.now()), 'accounts': {}, 'orders': {}, 'positions': {}, 'trades': {}}
        self.last_update_time = datetime.datetime.now()
        self.sig = sig
        self.if_restart = False
        self.orders_client = DATABASE.orders



    def run(self):


        self.call_sub()
        while True:
            now = datetime.datetime.now()
            if not self.sig:
                raise RuntimeError
            if now.hour in [9, 10, 11, 13, 14, 21, 22]:

                if now.hour == 9 or (now.hour == 10 and (now.minute < 15 or now.minute > 30)) or (now.hour == 11 and now.minute < 30) or\
                        (now.hour == 13) or now.hour == 14 or now.hour == 21 or now.hour == 22:
                    if now - self.last_update_time > datetime.timedelta(seconds=30):
                        QA.QA_util_log_info(
                            'SOMETHING MAYBE WRONG {}'.format(self.account_cookie))
                        self.call_close()
                        self.last_update_time = datetime.datetime.now()
                        self.if_restart = True
            if now.hour in [8, 12, 20]:
                # 自动重启
                if now.minute == 59 and now.second in [0, 1, 2]:
                    QA.QA_util_log_info('RESTART')

                    self.call_close()
                    self.if_restart = True
                    time.sleep(3)  # 阻塞住

            QA.QA_util_log_info(datetime.datetime.now())
            QA.QA_util_log_info(self.last_update_time)
            QA.QA_util_log_info(threading.enumerate())

    def call_close(self):
        #self.ws.close()
        pass
    
    def call_sub(self):
        # threading.Thread(target=self.sub.start,
        #                  name='ORDER_HANDLER {}'.format(
        #                      self.account_cookie), daemon=True).start()
        # threading.Thread(target=self.ws.run_forever, name='sub_websock {}'.format(
        #     self.account_cookie), daemon=True).start()
        # time.sleep(2)
        pass


    def handle(self, message):
        if message['aid'] == "rtn_data":

            try:
                data = message['data'][0]['trade']
                QA.QA_util_log_info(data)
                account_cookie = str(list(data.keys())[0])

                #user_id = data[account_cookie]['user_id']
                self.last_update_time = datetime.datetime.now()
                self.message['updatetime'] = str(
                    self.last_update_time)
                self.message['accounts'] = data[account_cookie]['accounts']['CNY']

                self.message['positions'] = self.update(
                    self.message['positions'], data[account_cookie]['positions'])
                self.message['orders'] = self.update(
                    self.message['orders'], data[account_cookie]['orders'])
                self.message['trades'] = self.update(
                    self.message['trades'], data[account_cookie]['trades'])
                self.account_client.update_one({'account_cookie': account_cookie}, {
                                               '$set': self.message}, upsert=True)
                # QA.QA_util_log_info(self.message)
            except Exception as e:
                if 'notify' in message['data'][0]:
                    data = message['data'][0]['notify']
                QA.QA_util_log_info(message)



    def update(self, old, new):

        for item in new.keys():
            old[item] = new[item]
            # old.update(new[item])
        return old

    def callback(self, a, b, c, body):
        """
        格式为json的str/bytes
        字段:
        {
            account_cookie
            order_direction {str} -- [description] (default: {'BUY'})
            order_offset {str} -- [description] (default: {'OPEN'})
            volume {int} -- [description] (default: {1})
            order_id {bool} -- [description] (default: {False})
            code {str} -- [description] (default: {'rb1905'})
            exchange_id {str} -- [description] (default: {'SHFE'})
        }
        """
        def targs():
            z = json.loads(str(body, encoding='utf-8'))
            QA.QA_util_log_info('===================== \n RECEIVE')
            QA.QA_util_log_info(z)

            if z['topic'] == 'sendorder':
                self.orders_client.insert_one(z)
                self.ws.send(
                    send_order(
                        z.get('account_cookie'),
                        z.get('order_direction', 'BUY'),
                        z.get('order_offset', 'OPEN'),
                        z.get('volume', 1),
                        z.get('order_id', False),
                        z.get('code', 'rb1905'),
                        z.get('exchange_id', 'SHFE'),
                        z.get('price', 3925))
                )
            elif z['topic'] == 'peek':
                self.ws.send(peek())
            elif z['topic'] == 'subscribe':
                self.ws.send(
                    subscribe_quote())
            elif z['topic'] == 'cancel_order':
                self.ws.send(
                    cancel_order(z['account_cookie'], z['order_id']))
            elif z['topic'] == 'transfer':
                self.ws.send(
                    transfer(z['account_cookie'], z['password'],
                             z['bankid'], z['bankpassword'], z['amount'])
                )
        threading.Thread(target=targs, name='callback_handler',
                         daemon=True).start()
