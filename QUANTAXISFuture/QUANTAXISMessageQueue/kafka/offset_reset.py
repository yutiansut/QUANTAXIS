# coding:utf-8

import logging
from kazoo.client import KazooClient
import urllib

logging.basicConfig(level = logging.INFO)

offset_check_logger = logging.getLogger('offset_reset')

zkclient = KazooClient('localhost:3000,localhost:3001,localhost:3002/kafka')
zkclient.start()

nodes = zkclient.get_children('/consumers/balance-consumer/nodes')

for node in nodes:
    try:
        handle = urllib.request.urlopen("http://" + node + "/reset-offset")
        code = handle.getcode()
        response = handle.read()
        if code == 200:
            print ("{} success".format(node))
            continue
    except:
        pass
    print ("{} failed".format(node))