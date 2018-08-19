# coding:utf-8

import QUANTAXIS as QA
import datetime
import pandas as pd


class Runtime():
    def __init__(self):
        self.quotation=[]

    @property
    def now(self):
        return datetime.datetime.now()


    def get_quotations(self):
        
        pass