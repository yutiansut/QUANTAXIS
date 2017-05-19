from kafka import KafkaClient, SimpleProducer, SimpleConsumer
kafka = KafkaClient("localhost:2181")
producer = SimpleProducer(kafka)
producer.send_messages("test1",b"Hello world!")