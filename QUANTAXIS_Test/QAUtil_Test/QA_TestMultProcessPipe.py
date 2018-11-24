from multiprocessing import Process,Pipe

import time,os
def consumer(p,name):

    left,right=p
    left.close()
    while True:
        try:
            baozi=right.recv()
            print('%s 收到包子:%s' %(name,baozi))
            print("A", os.getpid(), os.getppid())

        except EOFError:
            right.close()
            break


def producer(seq,p):

    print("B", os.getpid(), os.getppid())

    left,right=p
    right.close()
    for i in seq:
        left.send(i)
        print(' FA包子:%d' %  i)
        print("B", os.getpid(), os.getppid())

        # time.sleep(1)
    else:
        left.close()

if __name__ == '__main__':


    left,right=Pipe()
    c1=Process(target=consumer,args=((left,right),'c1'))
    c1.start()
    seq=(i for i in range(10))
    producer(seq,(left,right))
    right.close()
    left.close()
    c1.join()
    print('主进程')
