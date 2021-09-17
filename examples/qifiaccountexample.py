from QUANTAXIS.QIFI.QifiAccount import QIFI_Account

if __name__ == '__main__':

    account =  QIFI_Account(username='testx', password='123456', model='BACKTEST', nodatabase=True)

    """
    sendorder
    
    """
    order = account.send_order()


    """
    cancel order
    
    """
    cancel = account.cancel_order(order.order_id)


    """
    make deal
    
    """
    account.make_deal(order)


    account.settle()

    """
    next day
    """

    account.send_order()