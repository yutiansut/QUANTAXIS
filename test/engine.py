import QUANTAXIS as QA
import time

x=QA.QA_Engine('job')
x.start()
time.sleep(2)
x.pause()
time.sleep(3)
x.resume()
x.Task.stop()