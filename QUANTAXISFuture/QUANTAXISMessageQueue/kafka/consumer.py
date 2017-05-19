from kafka import KafkaClient, SimpleProducer, SimpleConsumer
kafka = KafkaClient("localhost:9092")
consumer = SimpleConsumer(kafka,"python","topic")

for msg in consumer:

    print(msg)
kafka.close()

