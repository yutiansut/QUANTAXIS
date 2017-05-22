#coding:utf-8

from kafka import SimpleProducer, SimpleClient
import logging

# 需要保留几个字段 9092端口

# To send messages asynchronously
client = SimpleClient('localhost:9092')
producer = SimpleProducer(client, async=True)
producer.send_messages('my-topic', b'async message')
input()
# To send messages in batch. You can use any of the available
# producers for doing this. The following producer will collect
# messages in batch and send them to Kafka after 20 messages are
# collected or every 60 seconds
# Notes:
# * If the producer dies before the messages are sent, there will be losses
# * Call producer.stop() to send the messages and cleanup
producer = SimpleProducer(client,
                          async=True,
                          batch_send_every_n=20,
                          batch_send_every_t=60)
# To send messages synchronously
client = SimpleClient('localhost:9092')
producer = SimpleProducer(client, async=False)

# Note that the application is responsible for encoding messages to type bytes
producer.send_messages('my-topic', b'some message')
producer.send_messages('my-topic', b'this method', b'is variadic')

# Send unicode message
producer.send_messages('my-topic', u'你怎么样?'.encode('utf-8'))

# To wait for acknowledgements
# ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
#                         a local log before sending response
# ACK_AFTER_CLUSTER_COMMIT : server will block until the message is committed
#                            by all in sync replicas before sending a response
producer = SimpleProducer(client,
                          async=False,
                          req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                          ack_timeout=2000,
                          sync_fail_on_error=False)

responses = producer.send_messages('my-topic', b'another message')
for r in responses:
    logging.info(r.offset)



from kafka import (
    SimpleClient, KeyedProducer,
    Murmur2Partitioner, RoundRobinPartitioner)

kafka = SimpleClient('localhost:9092')

# HashedPartitioner is default (currently uses python hash())
producer = KeyedProducer(kafka)
producer.send_messages('my-topic', b'key1', b'some message')
producer.send_messages('my-topic', b'key2', b'this methode')

# Murmur2Partitioner attempts to mirror the java client hashing
producer = KeyedProducer(kafka, partitioner=Murmur2Partitioner)

# Or just produce round-robin (or just use SimpleProducer)
producer = KeyedProducer(kafka, partitioner=RoundRobinPartitioner)