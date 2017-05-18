import pika
import time

# 建立实例
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
# 声明管道
channel = connection.channel()

# 为什么又声明了一个‘hello’队列？
# 如果确定已经声明了，可以不声明。但是你不知道那个机器先运行，所以要声明两次。
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):  # 四个参数为标准格式
    print(ch, method, properties)  # 打印看一下是什么
    # 管道内存对象  内容相关信息  后面讲
    print(" [x] Received %r" % body)
    time.sleep(15)
    ch.basic_ack(delivery_tag = method.delivery_tag)  # 告诉生成者，消息处理完成

channel.basic_consume(  # 消费消息
        callback,  # 如果收到消息，就调用callback函数来处理消息
        queue='hello',  # 你要从那个队列里收消息
        # no_ack=True  # 写的话，如果接收消息，机器宕机消息就丢了
        # 一般不写。宕机则生产者检测到发给其他消费者
        )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # 开始消费消息