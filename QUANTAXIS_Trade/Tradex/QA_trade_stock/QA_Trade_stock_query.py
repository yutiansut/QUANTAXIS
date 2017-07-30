#coding:utf-8

import msvcrt
import sys
import configparser
import os
#print (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# input()
import TradeX

TradeX.OpenTdx()