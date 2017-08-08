#coding:utf-8



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
            
if __name__=='__main__':
    from pytdx.hq import TdxHq_API
    api=TdxHq_API()
    print(get_stock_1_min(api,'000001'))