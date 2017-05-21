# coding:utf-8

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:1234')
for _ in range(100):
     future=producer.send('foobar', b'some_message_bytes')
     result = future.get(timeout=60)