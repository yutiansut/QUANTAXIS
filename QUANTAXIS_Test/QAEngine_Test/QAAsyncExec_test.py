from QUANTAXIS.QAEngine.QAAsyncExec import QA_AsyncExec

class job1(QA_AsyncExec):
    def do(self):
        try:
            event = self.get()
            print('job1 do {}'.format(event))
        except:
            pass


class job2(QA_AsyncExec):
    def do(self):
        try:
            event = self.get()
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
