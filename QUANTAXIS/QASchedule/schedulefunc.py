##

import os
import toml
def read_config(file):
    config =  toml.loads(file)

@read_config
def before_trading():
    pass



@read_config
def on_trading():

    """
    trading_day 
    
    """
    pass

@read_config
def after_1530():
    """
    start 15:31
    """
    pass

@read_config
def before_nighttrading():

    """
    start 8:30
    """
    pass


@read_config
def before_nighttrading():
    pass
