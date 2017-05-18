#coding:utf-8
#---- Condition
#---- 捉迷藏的游戏
import threading, time

class Hider(threading.Thread):
    def __init__(self, cond, name):
        super(Hider, self).__init__()
        self.cond = cond
        self.name = name
    
    def run(self):
        time.sleep(1) #确保先运行Seeker中的方法   
        
        self.cond.acquire() #b    
        print (self.name + ': 我已经把眼睛蒙上了')
        self.cond.notify()
        self.cond.wait() #c    
                         #f 
        print( self.name + ': 我找到你了 ~_~')
        self.cond.notify()
        self.cond.release()
                            #g
        print (self.name + ': 我赢了'   #h)
        
        
class Seeker(threading.Thread):
    def __init__(self, cond, name):
        super(Seeker, self).__init__()
        self.cond = cond
        self.name = name
    def run(self):
        self.cond.acquire()
        self.cond.wait()    #a    #释放对琐的占用，同时线程挂起在这里，直到被notify并重新占有琐。
                            #d
        print self.name + ': 我已经藏好了，你快来找我吧'
        self.cond.notify()
        self.cond.wait()    #e
                            #h
        self.cond.release() 
        print self.name + ': 被你找到了，哎~~~'
        
cond = threading.Condition()
seeker = Seeker(cond, 'seeker')
hider = Hider(cond, 'hider')
seeker.start()
hider.start()