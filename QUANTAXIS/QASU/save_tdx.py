#coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pytdx.hq import TdxHq_API
api=TdxHq_API()

def get_stock_day(api,code):
    
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0

    with api.connect():
        for i in range(11):
            data+=api.get_security_bars(9,index_code,code,(10-i)*800+1,800)
    return api.to_df(data)

def get_stock_1_min(api,code):
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0
    with api.connect():
        for i in range(51):
            data+=api.get_security_bars(8,index_code,code,(50-i)*800+1,800)
            print(len(data))
    return api.to_df(data)
            



def get_stock_5_min(api,code):
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0
    with api.connect():
        for i in range(51):
            data+=api.get_security_bars(0,index_code,code,(50-i)*800+1,800)
            print(len(data))
    return api.to_df(data)

def get_stock_15_min(api,code):
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0
    with api.connect():
        for i in range(51):
            data+=api.get_security_bars(1,index_code,code,(50-i)*800+1,800)
            print(len(data))
    return api.to_df(data)
def get_stock_30_min(api,code):
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0
    with api.connect():
        for i in range(51):
            data+=api.get_security_bars(2,index_code,code,(50-i)*800+1,800)
            print(len(data))
    return api.to_df(data)
            
def get_stock_1_hour(api,code):           
    data=[]
    if str(code)[0]=='6':
        index_code=1
    else:
        index_code=0
    with api.connect():
        for i in range(51):
            data+=api.get_security_bars(2,index_code,code,(50-i)*800+1,800)
            print(len(data))
    return api.to_df(data)







if __name__=='__main__':
    from pytdx.hq import TdxHq_API
    api=TdxHq_API()
    print(get_stock_1_min(api,'000001'))