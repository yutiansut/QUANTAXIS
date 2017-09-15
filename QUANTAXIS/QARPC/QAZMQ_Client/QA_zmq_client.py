from zmq import *
import zmq

class MyPull():
    def __init__(self, content, addr, num):
        assert num > 0 and num < 256
        self._socks = {}
        self._poller = zmq.Poller()
        for i in range(num):
            sock = content.socket(zmq.PULL)
            sock.connect(addr)
            self._poller.register(sock, zmq.POLLIN)
            self._socks[sock] = i
        
    def close(self):
        for sock in self._socks.keys():
            self._poller.unregister(sock)
            sock.close()
    
    def pull(self):
        flag = False
        socks = dict(self._poller.poll(1)) # 如果不设超时，阻塞
        for sock in socks.keys():
            if socks[sock] == zmq.POLLIN:
                print (self._socks[sock], ' - ', sock.recv())
                flag = True
        
        if flag: self.pull() or None
    
    
ctx = zmq.Context()

pl = MyPull(ctx, 'tcp://127.0.0.1:8002', 5)
 
pl.pull()