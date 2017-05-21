from kafka import KafkaClient, SimpleProducer, SimpleConsumer
kafka = KafkaClient("localhost:2181")
consumer = SimpleConsumer(kafka,"python","test")

for msg in consumer:

    print(msg)
kafka.close()

