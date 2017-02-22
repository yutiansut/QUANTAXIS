# coding: utf-8
import jieba.analyse 
import pymongo
import jieba
import jieba.posseg
import jieba.analyse

print('='*40)


client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['wsc']
coll=db['articles']
strings =""
for content in coll.find({"poster":"王维丹"}):
    urlx=content['content']
    strings=strings+urlx     
text= strings.replace(" ","").replace("\u66f4\u591a","").replace("\u7cbe\u5f69","").replace("\u8d22\u7ecf","").replace("\u89c1\u95fb","").replace("App","")
text=text.replace("\u8d44\u8baf","").replace("\u70b9\u51fb","").replace("\u8fd9\u91cc","").replace("\u4e0b\u8f7d","").replace("\u534e\u5c14\u8857","")
for x, w in jieba.analyse.extract_tags(text, withWeight=True):
    print('%s %s' % (x, w))

print('-'*40)
print(' TextRank')
print('-'*40)
for x, w in jieba.analyse.textrank(text, withWeight=True):
    print('%s %s' % (x, w))

print('='*40)
jieba.analyse.textrank(text, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))

