from kafka import SimpleProducer, SimpleClient,SimpleConsumer

# To consume messages
client = SimpleClient('localhost:9092')
consumer = SimpleConsumer(client, "my-group", "my-topic")
for message in consumer:
    # message is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.decode('utf-8')`
    print(message)


# Use multiprocessing for parallel consumers
from kafka import MultiProcessConsumer

# This will split the number of partitions among two processes
consumer = MultiProcessConsumer(client, "my-group", "my-topic", num_procs=2)

# This will spawn processes such that each handles 2 partitions max
consumer = MultiProcessConsumer(client, "my-group", "my-topic",
                                partitions_per_proc=2)

for message in consumer:
    print(message)

for message in consumer.get_messages(count=5, block=True, timeout=4):
    print(message)

client.close()