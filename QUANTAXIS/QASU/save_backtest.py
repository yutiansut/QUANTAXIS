# coding:utf-8


def QA_SU_save_account_message(message, client):
    #header = message['header']
    #body = message['body']
    coll = client.quantaxis.backtest_history
    # print(message)
    coll.insert({
        #'time': message['body']['time'],
        'total_date': message['body']['account']['total_date'],
        'time_stamp': message['body']['date_stamp'],
        "cookie": message['header']['cookie'],
        'user': message['header']['session']['user'],
        'strategy': message['header']['session']['strategy'],
        'init_assest': message['body']['account']['init_assest'],
        'portfolio': message['body']['account']['portfolio'],
        'history': message['body']['account']['history'],
        'assest_now': message['body']['account']['assest_now'],
        'assest_history': message['body']['account']['assest_history'],
        'account_date': message['body']['account']['account_date'],
        'assest_free': message['body']['account']['assest_free'],
        'assest_fix': message['body']['account']['assest_fix'],
        'profit': message['body']['account']['profit'],
        'total_profit': message['body']['account']['total_profit'],
        'cur_profit_present': message['body']['account']['cur_profit_present'],
        'cur_profit_present_total': message['body']['account']['cur_profit_present_total'],
        'hold': message['body']['account']['hold'],
        'bid': message['body']['bid'],
        'market': message['body']['market']
    })


def QA_SU_save_backtest_message(message, client):
    coll = client.quantaxis.backtest_info
    coll.insert(message)


def QA_SU_save_account_message_many(message, client):
    # print(message)
    messages = []
    for item in message:
        try:
            # print(item['body']['account']['total_date'])
            messages.append({
                #'time': item['body']['time'],
                #'code':item['header']['session']['code'],
                'total_date': item['body']['account']['total_date'],
                'time_stamp': item['body']['date_stamp'],
                "cookie": item['header']['cookie'],
                'user': item['header']['session']['user'],
                'strategy': item['header']['session']['strategy'],
                'init_assest': item['body']['account']['init_assest'],
                'portfolio': item['body']['account']['portfolio'],
                'history': item['body']['account']['history'],
                'assest_now': item['body']['account']['assest_now'],
                'assest_history': item['body']['account']['assest_history'],
                'account_date': item['body']['account']['account_date'],
                'assest_free': item['body']['account']['assest_free'],
                'assest_fix': item['body']['account']['assest_fix'],
                'profit': item['body']['account']['profit'],
                'total_profit': item['body']['account']['total_profit'],
                'cur_profit_present': item['body']['account']['cur_profit_present'],
                'cur_profit_present_total': item['body']['account']['cur_profit_present_total'],
                'hold': item['body']['account']['hold'],
                'bid': item['body']['bid'],
                'market': item['body']['market']
            })
        except:
            print (item['body'])
            input()
    # print(messages)
    coll = client.quantaxis.backtest_history
    coll.insert_many(messages)
