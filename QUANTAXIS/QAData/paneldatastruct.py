from clickhouse_driver.util.helpers import column_chunks
import numpy as np
import pandas as pd
from dateutil import parser


class QAPanelDataStruct():

    """
    paneldata
    
    """
    def __init__(self, data, dtype) -> None:
        self.data = data
        self.type = dtype

    def get_loc(self, codelist, start, end):
        if 'min' in self.type:
            start = parser.parse(start)
            end = parser.parse(end)
        elif 'day' in self.type:
            start = parser.parse(start).date()
            end = parser.parse(end).date()

        return self.data.loc[slice(start, end), codelist]

    def get_date(self, codelist, date):
        if 'min' in self.type:
            date = parser.parse(date)
        elif 'day' in self.type:
            date = parser.parse(date).date()

        return self.data.loc[date, codelist]
