from QUANTAXIS.QAEngine.asyncexec import QA_AsyncExec



"""这里展示了如何超级简便的使用QA异步执行线程

我们实例化两个 继承 QA_AsyncExec, 让他们监听

然后你可以从外部传入 ==> 直接传入 QA_AsyncExec的任务队列即可


你的典型场景:

监听多个股票(单独)
监听多个事件
监听订单
监听账户事件

CEP的基础

"""
class job1(QA_AsyncExec):
    def do(self):
        try:
            x=self.queue.get()
            print('job1 do {}'.format(x))
        except:
            pass

class job2(QA_AsyncExec):
    def do(self):
        try:
            x=self.queue.get()
            print('job2 do {}'.format(x))
        except:
            pass

j1 = job1()
j2 = job2()

j1.start()
j2.start()


for i in range(100):
    j1.put(i)
    j2.put(i)

"""
λ  python .\QUANTAXIS\Exp\test_async.py   
job2 do 0                                 
job1 do 0                                 
job1 do 1                                 
job1 do 2                                 
job2 do 1                                 
job2 do 2
job1 do 3                                 
job2 do 3                                 
job1 do 4                                 
job2 do 4                                 
job1 do 5                                 
job1 do 6                                 
job2 do 5                                 
job1 do 7                                 
job1 do 8                                 
job2 do 6                                 
job1 do 9                                 
job2 do 7                                 
job1 do 10                                
job2 do 8                                 
job2 do 9                                 
job1 do 11                                
job1 do 12                                
job2 do 10                                
job1 do 13                                
job2 do 11                                
job1 do 14                                
job1 do 15                                
job2 do 12                                
job1 do 16                                
job2 do 13                                
job1 do 17                                
job2 do 14                                
job1 do 18                                
job2 do 15                                
job1 do 19                                
job1 do 20                                
job2 do 16                                
job1 do 21                                
job2 do 17                                
job1 do 22                                
job2 do 18                                
job2 do 19                                
job1 do 23                                
job2 do 20                                
job2 do 21                                
.........
"""