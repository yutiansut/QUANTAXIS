# python-Kafka教程
by yutiansut


## api KafkaConsumer
```python
class kafka.KafkaConsumer(*topics, **configs)[source]
#Consume records from a Kafka cluster.

#The consumer will transparently handle the failure of servers in the Kafka cluster, and adapt as topic-partitions are created or migrate between brokers. It also interacts with the assigned kafka Group Coordinator node to allow multiple consumers to load balance consumption of topics (requires kafka >= 0.9.0.0).
```

```python
import kafka.kafkaConsumer
```
