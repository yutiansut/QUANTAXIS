from kafka import KafkaClient, SimpleProducer, SimpleConsumer
kafka = KafkaClient("localhost:9093")
producer = SimpleProducer(kafka)
producer.send_messages("test",b"Hello world!")