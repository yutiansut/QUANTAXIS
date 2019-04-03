import QUANTAXIS as QA

if __name__ == '__main__':
    api = QA.QA_TTSBroker()

    print("Check API Server, Ping...")
    result = api.ping()
    print("Check API Server, Result")
    print(result)

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
                    price=1.0,
                    amount=100,
                    towards=QA.ORDER_DIRECTION.BUY,
                    order_model=QA.ORDER_MODEL.LIMIT
                )
            )

        print("---登出---")
        print(api.logoff())
