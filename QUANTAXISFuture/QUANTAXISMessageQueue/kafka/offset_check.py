# coding:utf-8

from pykafka.client import KafkaClient
import logging
import pykafka
from pykafka.protocol import PartitionOffsetFetchRequest

logging.basicConfig(level = logging.INFO)

offset_check_logger = logging.getLogger('offset_check')

client = KafkaClient('localhost:8990,localhost:8991,localhost:8992')

nmq = client.topics['nmq']

offsets = nmq.latest_available_offsets()

offset_check_logger.info('消息总量如下:')

for partition, item in offsets.iteritems():
    offset_check_logger.info('[partition={} offset={}]'.format(partition, item.offset[0]))
    
partitions = offsets.keys()
    
offset_check_logger.info('消息读取量如下:')

offset_manager = client.cluster.get_offset_manager('balance-consumer')

requests = [PartitionOffsetFetchRequest(topic_name = 'nmq', partition_id = part_id) for part_id in partitions]

response = offset_manager.fetch_consumer_group_offsets('balance-consumer', requests)

for partition, item in response.topics['nmq'].iteritems():
    offset_check_logger.info('[partition={} offset={}]'.format(partition, item.offset))
