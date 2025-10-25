

import pika
from QUANTAXIS.QAPubSub.setting import qapubsub_ip, qapubsub_port, qapubsub_user, qapubsub_password

# v2.1.0+: 引入统一资源管理器
try:
    from QUANTAXIS.QAUtil.QAResourceManager import QARabbitMQResourceManager
    HAS_RESOURCE_MANAGER = True
except ImportError:
    HAS_RESOURCE_MANAGER = False


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
        """
        优雅关闭连接 (v2.1.0升级)

        关闭顺序:
        1. 先关闭通道 (channel)
        2. 再关闭连接 (connection)

        这样可以避免资源泄漏和异常
        """
        # 1. 关闭通道
        if hasattr(self, 'channel') and self.channel is not None:
            try:
                if self.channel.is_open:
                    self.channel.close()
            except Exception as e:
                import logging
                logging.warning(f"关闭RabbitMQ通道失败: {e}")

        # 2. 关闭连接
        if hasattr(self, 'connection') and self.connection is not None:
            try:
                if self.connection.is_open:
                    self.connection.close()
            except Exception as e:
                import logging
                logging.warning(f"关闭RabbitMQ连接失败: {e}")

    def __enter__(self):
        """支持with语句 (v2.1.0新增)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持with语句自动关闭 (v2.1.0新增)"""
        self.close()
        return False