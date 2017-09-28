 

from .QA_zmq_client import QA_RPC_client
import datetime
import random
from concurrent.futures import ThreadPoolExecutor
def ports(item):
    QA_RPC_client('tcp://*:%s'%item,5).pull()
executor = ThreadPoolExecutor(max_workers=150)

res = {executor.submit(
    ports, i_) for i_ in range(90001,92000)}