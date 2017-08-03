print('import successfully')

def before_backtest():
    print('from strategy: befor_backtest')
def before_trading():
    print('from strategy: befor_trading')
    
def handle_bar():
    print('from strategy: handle_bar')


def end_trading():
    print('from strategy: end_trading')

def end_backtest():
    print('from strategy: end_bar')
    
