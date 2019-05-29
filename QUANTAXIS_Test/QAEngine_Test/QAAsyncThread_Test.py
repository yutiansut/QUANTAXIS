#from QUANTAXIS.QAEngine.asyncexec import QA_AsyncExec
from QUANTAXIS.QAEngine.QAAsyncThread import QA_AsyncThread

"""这里展示了如何超级简便的使用QA异步执行线程

我们实例化两个 继承 QA_AsyncThread 让他们监听事件



你的典型场景:

监听多个股票(单独)
监听多个事件
监听订单
监听账户事件

CEP的基础

"""


class job1(QA_AsyncThread):
    def do(self, event):
        try:
            print('job1 do {}'.format(event))
        except:
            pass


class job2(QA_AsyncThread):
    def do(self, event):
        try:
            print('job2 do {}'.format(event))
        except:
            pass


j1 = job1()
j2 = job2()
print(j1)
print(j2)
j1.start()
j2.start()


for i in range(100):

    j1.put(i)
    j2.put(i)

"""
λ  python .\QUANTAXIS\Exp\test_async.py   
<QA_AsyncThread: QA_AsyncThread_SRq  id=1872684598216 ident None>           
<QA_AsyncThread: QA_AsyncThread_2tf  id=1872684555904 ident None>           
start                                                                       
start                                                                       
job1 do < QA_Event None None False , id = 1872759171784 >                   
job2 do < QA_Event None None False , id = 1872759172848 >                   
job1 do < QA_Event None None False , id = 1872759243216 >                   
job2 do < QA_Event None None False , id = 1872759243944 >                   
job1 do < QA_Event None None False , id = 1872759244896 >                   
job2 do < QA_Event None None False , id = 1872759245512 >                   
job1 do < QA_Event None None False , id = 1872759245176 >                   
job2 do < QA_Event None None False , id = 1872759246240 >                   
job1 do < QA_Event None None False , id = 1872759244056 >                   
job2 do < QA_Event None None False , id = 1872759244952 >                   
job1 do < QA_Event None None False , id = 1872759301736 >                   
job2 do < QA_Event None None False , id = 1872759172904 >                   
job1 do < QA_Event None None False , id = 1872759171784 >                   
job2 do < QA_Event None None False , id = 1872759303696 >                   
job1 do < QA_Event None None False , id = 1872759244224 >                   
job2 do < QA_Event None None False , id = 1872759370528 >                   
job1 do < QA_Event None None False , id = 1872759371032 >                   
job2 do < QA_Event None None False , id = 1872759172848 >                   
job1 do < QA_Event None None False , id = 1872759373496 >                   
job2 do < QA_Event None None False , id = 1872759373048 >                   
job1 do < QA_Event None None False , id = 1872759243944 >                   
job2 do < QA_Event None None False , id = 1872759371592 >                   
job1 do < QA_Event None None False , id = 1872759246240 >                   
job2 do < QA_Event None None False , id = 1872759244056 >                   
job1 do < QA_Event None None False , id = 1872759438360 >                   
job2 do < QA_Event None None False , id = 1872759244952 >                   
job1 do < QA_Event None None False , id = 1872760546640 >                   
job2 do < QA_Event None None False , id = 1872759438976 >                   
job1 do < QA_Event None None False , id = 1872759172904 >                   
job2 do < QA_Event None None False , id = 1872759171784 >                   
job1 do < QA_Event None None False , id = 1872759303696 >                   
job2 do < QA_Event None None False , id = 1872759244224 >                   
.........
"""
