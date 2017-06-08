# coding:utf-8


def QA_SU_save_account_message(message, client):
    #header = message['header']
    #body = message['body']
    coll = client.quantaxis.backtest_history
    # print(message)
    coll.insert({
        #'time': message['body']['time'],
        
        'time_stamp': message['body']['date_stamp'],
        "cookie": message['header']['cookie'],
        'user': message['header']['session']['user'],
        'strategy': message['header']['session']['strategy'],
        'cash': message['body']['account']['cash'],
        'hold': message['body']['account']['hold'],
        'history': message['body']['account']['history'],
        'assets': message['body']['account']['assets']
    })


def QA_SU_save_backtest_message(message, client):
    coll = client.quantaxis.backtest_info
    coll.insert(message)
    