from QUANTAXIS.QIFI.QifiAccount import QIFI_Account

if __name__ == '__main__':

    account =  QIFI_Account(username='testx', password='123456', model='BACKTEST', nodatabase=False, dbname='ck', 
        clickhouse_port=9000, clickhouse_user='default', clickhouse_password='')

    """
    sendorder
    
    """
    account.initial()
    order = account.send_order("000001", 200, 20, 1, datetime='2021-09-30')


    """
    cancel order
    
    """
    #cancel = account.cancel_order(order['order_id'])


    """
    make deal
    
    """
    account.make_deal(order)
    res = list(account.position_qifimsg.values())
    
    print(res[0])

    account.settle()

    """
    next day
    """

    