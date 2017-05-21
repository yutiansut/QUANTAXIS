from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


class Kafka_producer():
    '''
    使用kafka的生产模块
    '''

    def __init__(self, kafkahost,kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
            ))

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print (e)

class Kafka_consumer():
    '''
    使用Kafka—python的消费模块
    '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
                                      bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort ))

    def consume_data(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except :
            print('error')


def produce():
    '''
    测试consumer和producer
    :return:
    '''
    ##测试生产模块
    
    producer = Kafka_producer("127.0.0.1", 9091, "ranktest")
    for id in range(10):
        params = '{abetst}:{null}---'+str(id)
        producer.sendjsondata(params)
    
def consume():
    ##测试消费模块
    #消费模块的返回格式为ConsumerRecord(topic=u'ranktest', partition=0, offset=202, timestamp=None, 
    #\timestamp_type=None, key=None, value='"{abetst}:{null}---0"', checksum=-1868164195, 
    #\serialized_key_size=-1, serialized_value_size=21)
    consumer = Kafka_consumer('127.0.0.1', 9091, "ranktest", 'test-python-ranktest')
    message = consumer.consume_data()
    for i in message:
        print (i.value)


if __name__ == '__main__':
    produce()
   # consume()