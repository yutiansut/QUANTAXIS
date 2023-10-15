

import pika
from QUANTAXIS.QAPubSub.setting import qapubsub_ip, qapubsub_port, qapubsub_user, qapubsub_password


class base_ps():

    def __init__(self, host=qapubsub_ip, port=qapubsub_port, user=qapubsub_user, password=qapubsub_password, channel_number=1, queue_name='', routing_key='default',  exchange='', exchange_type='fanout', vhost='/'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.queue_name = queue_name
        self.exchange = exchange
        self.routing_key = routing_key
        self.vhost = vhost
        self.exchange_type = exchange_type
        self.channel_number = channel_number
        # fixed: login with other user, pass failure @zhongjy
        self.credentials = pika.PlainCredentials(
            self.user, self.password, erase_on_connect=True)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost,
                                      credentials=self.credentials, heartbeat=0, socket_timeout=5,
                                      )
        )

        self.channel = self.connection.channel(
            channel_number=self.channel_number)

    def reconnect(self):
        try:
            self.connection.close()
        except:
            pass

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port,credentials=self.credentials,
                                      heartbeat=0, virtual_host=self.vhost,
                                      socket_timeout=5,))

        self.channel = self.connection.channel(
            channel_number=self.channel_number)
        return self

    def close(self):
        self.connection.close()