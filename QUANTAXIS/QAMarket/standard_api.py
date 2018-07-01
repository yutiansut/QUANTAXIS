



def callback_message(cls):
    # 这是标准的return back message

    message = {
        'header': {
            'source': 'market',
            'status': cls.status,
            'code': cls.order.code,
            'session': {
                'user': cls.order.user,
                'strategy': cls.order.strategy,
                'account': cls.order.account_cookie
            },
            'order_id': cls.order.order_id,
            'trade_id': cls.order.trade_id
        },
        'body': {
            'order': {
                'price': float("%.2f" % float(cls.deal_price)),
                'code': cls.order.code,
                'amount': cls.deal_amount,
                'date': cls.order.date,
                'datetime': cls.order.datetime,
                'towards': cls.order.towards
            },
            'fee': {
                'commission': cls.commission_fee,
                'tax': cls.tax
            }
        }
    }
    return message