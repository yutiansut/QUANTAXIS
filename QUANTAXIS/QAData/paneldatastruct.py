import pandas as pd

import numpy as np
from dateutil import parser


class QAPanelDataStruct():
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
