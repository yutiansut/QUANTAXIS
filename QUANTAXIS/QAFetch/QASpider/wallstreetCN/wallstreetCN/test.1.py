from .spiders import mongodbQuery
import multiprocessing
import threading
query=mongodbQuery.querylist()
new_url = 'http://wallstreetcn.com/node/287070'
count = query.queryMongodbSame('title','news_url',new_url)
if count == 0:
    print ('no url in database')
else:
    print ('already in')
print (count)
#query.checkDifferentDatabase('title','articles','news_url','url',0)
#query.checkDifferentDatabase('articles','articles','url','url',1)