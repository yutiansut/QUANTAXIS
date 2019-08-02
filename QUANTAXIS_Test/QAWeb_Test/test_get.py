import requests
import datetime
import threading
from time import ctime,sleep
 
 
 
def t1(func):
  for i in range(50):
    starttime = datetime.datetime.now()
    url = "http://localhost:8010/marketdata/stock/day?code=000005"
    f=requests.get(url)
    endtime = datetime.datetime.now()
    print( "round:%s, tread number:%s,len : %s,time:%f" % (i, func,len(f.text), (endtime - starttime).microseconds / 1000))

 
 
if __name__ == '__main__':
  threads=[]
  for i in range(300):
    name = "t%s" % (i)
    name = threading.Thread(target=t1,args=(i,))
    threads.append(name)
 
 
  for t in threads:
    t.setDaemon(True)
    t.start()
  t.join()