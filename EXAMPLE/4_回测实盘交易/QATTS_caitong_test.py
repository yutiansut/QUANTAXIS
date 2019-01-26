# coding: utf-8
import os
import QUANTAXIS as QA

if __name__ == '__main__':
    trade_server_ip = "127.0.0.1"
    trade_server_port = "19820"
    transport_enc_key = ""
    transport_enc_iv = ""
    tdx_server_ip = "60.191.116.36"
    tdx_server_port = 7708
    tdx_version = "6.44"
    user_name = ""
    user_pass = ""
    # 通讯密码
    user_tx_pass = ""

    print("测试代码")
    print("在运行前,请先运行tdxtradeserver的后缀名为 exe 文件")
    print("下面需要输入的 key/iv 在后缀名ini中自己查找")
    if len(transport_enc_key) == 0:
        transport_enc_key = input('env_key:   ')
    if len(transport_enc_iv) == 0:
        transport_enc_iv = input('env_iv:    ')

    api = QA.QA_TTSBroker(
        endpoint="http://%s:%s/api" % (trade_server_ip,
                                       trade_server_port),
        enc_key=bytes(transport_enc_key,
                      encoding='utf-8'),
        enc_iv=bytes(transport_enc_iv,
                     encoding='utf-8')
    )

    print("Check API Server, Ping...")
    result = api.ping()
    print("Check API Server, Result")
    print(result)

    print("account和password是自己的账户和交易密码")

    if len(user_name) == 0:
        user_name = input('account:    ')
    if len(user_pass) == 0:
        user_pass = input('password:   ')
    print("--登陆--")

    result = api.logon(
        tdx_server_ip,
        tdx_server_port,
        tdx_version,
        1,
        user_name,
        user_name,
        user_pass,
        user_tx_pass
    )

    if result["success"]:
        for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15):
            print("---查询信息 cate=%d--" % i)
            print(api.data_to_df(api.query_data(i)))

        print('==============================下面是下单部分========================')
        print('即将演示的是  下单000001  数量100股  价格9.8 的限价单模式')

        if str(input('我已知晓, 并下单 按y继续 n 退出'))[0] == 'y':

            # 市价单可能需要开通权限
            # order_model=QA.ORDER_MODEL.LIMIT 限价单
            print(
                api.send_order(
                    code='000001',
                    price=9.8,
                    amount=100,
                    towards=QA.ORDER_DIRECTION.BUY,
                    order_model=QA.ORDER_DIRECTION.BUY,
                )
            )

        print("---登出---")
        print(api.logoff())
