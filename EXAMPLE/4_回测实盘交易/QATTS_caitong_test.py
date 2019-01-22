
import os
import QUANTAXIS as QA
print('在运行前 请先运行tdxtradeserver的 exe文件')
print('这是测试代码, 下面需要输入的 key/iv在ini中自己查找, account 和password是自己的账户密码 ')
api = QA.QA_TTSBroker(endpoint="http://127.0.0.1:19820/api",
                    enc_key=bytes(input('env_key:   '), encoding='utf-8'), enc_iv=bytes(input('env_iv:    '), encoding='utf-8'))

print("---Ping---")
result = api.ping()
print(result)

print("---登入---")
acc = input('account:    ')
password = input('password:   ')
result = api.logon("60.191.116.36", 7708,
                    "6.44", 1,
                    acc, acc, password, "")

if result["success"]:
    for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15):
        print("---查询信息 cate=%d--" % i)
        print(api.data_to_df(api.query_data(i)))


    print('==============================下面是下单部分========================')
    print('即将演示的是  下单000001  数量100股  价格9.8 的限价单模式')
    
    if str(input('我已知晓, 并下单 按y继续 n 退出'))[0] == 'y':
    
        print(api.send_order(code='000001', price=9.8, amount=100,
                            towards=QA.ORDER_DIRECTION.BUY, order_model=QA.ORDER_DIRECTION.BUY))
    print("---登出---")
    print(api.logoff())
