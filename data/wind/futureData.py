# -*- coding:utf-8 -*-
from WindPy import *

from datetime import datetime
import pymongo
import re

client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.futureList
w.start()
for item in coll.find("Code":re.compile('SHF')):
    print item