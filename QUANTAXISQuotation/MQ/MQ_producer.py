import pika

# 建立一个实例
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost',5672)  # 默认端口5672，可不写
    )
# 声明一个管道，在管道里发消息
channel = connection.channel()
# 在管道里声明queue
channel.queue_declare(queue='hello')
# RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello',  # queue名字
                      body='Hello World!')  # 消息内容
print(" [x] Sent 'Hello World!'")
connection.close()  # 队列关闭