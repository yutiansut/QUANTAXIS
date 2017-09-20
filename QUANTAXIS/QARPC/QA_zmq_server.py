from zmq import *
import zmq
import datetime
import time
import sys



class QA_RPC_Sever_push():
    def __init__(self, addr):
        self._ctx=zmq.Context()
        self._sock = self._ctx.socket(zmq.PUSH)
        self._sock.bind(addr)
    
    def push(self, datas):
        #assert isinstance(datas, list)
        #for data in datas:
        self._sock.send_string(datas)
        print ('push done')

class QA_RPC_Sever_pub():

    port = "5556"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print( "%d %d" % (topic, messagedata))
        socket.send("%d %d" % (topic, messagedata))
        time.sleep(1)




class QA_RPC_Sever_pubs():
    
    port = "5556"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print( "%d %d" % (topic, messagedata))
        socket.send("%d %d" % (topic, messagedata))
        time.sleep(1)



