from zmq import *
import zmq
import datetime
import time



class MyPush():
    def __init__(self, content, addr):
        self._sock = content.socket(zmq.PUSH)
        self._sock.bind(addr)
    
    def push(self, datas):
        assert isinstance(datas, list)
        for data in datas:
            self._sock.send_string(data)
        print ('push done')



ctx = zmq.Context()
ps = MyPush(ctx, 'tcp://*:8002')




