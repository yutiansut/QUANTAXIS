import unittest


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
http://pandas.pydata.org/pandas-docs/stable/10min.html
'''
class TestPandas_10_Minutes(unittest.TestCase):


    def test_10_minutes_tutorial(self):
        #Object Creation
        #Creating a Series by passing a list of values, letting pandas create a default integer index:
        print("Creating a Series by passing a list of values, letting pandas create a default integer index:")
        print("pd.Series([ conent of data... ]")
        s = pd.Series([1,2,3,4,5,np.nan, 0, 9,100])
        print(s)
        print(" output have the default index 0,1,2,3,4 for the data serial")
        print("😇")

        print(" let's try the datatime serial,  pd have function called the date_range to do that")
        dates = pd.date_range('2013-11-11', periods=8)
        print(dates)
        print(" you can see the DatetimeIndex type, have three part in it, one is the date serials, and dtype is the type, and fequency is the day type.")
        print(" this is kind of index type can be used for dataframe!")

        df = pd.DataFrame(np.random.randn(8,8), index=dates, columns=list('ABCDEFGH'))
        print(df)
        print(" now we can konw that dataframe date like a table have three part in it, row the table, colums of table header, and index, index for each row")
        print("😇")

        print("conclution,  dataframe have two kind of data type , Serial and DataFrame type.")
        print(" DataFrame and Serials should use the index for fast retrieve the data row")
        print(" index can use DatetimeIndex type")

        print("😇")
        print(" pass the dict also can construct a dictionary to a dataframe")
        df2 = pd.DataFrame( {'A': 1.,
                            'B': [pd.Timestamp("20110111"), pd.Timestamp('20111212'), pd.Timestamp('20111214'),pd.Timestamp('20110202')],
                            'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                            'D': np.array( [3]*4, dtype='int32'),
                            'E': pd.Categorical(['test','train',"check","plan"])})
        print(df2)
        print(" note that , dict key as table header , value menas each column data")
        print(" check out the column of datetype list can use dtypes in dataframe property")
        print( df2.dtypes )
        print(" or just use the Column name to access types and value")
        print(df2.A)
        print(df2.B)
        print(df2.C)
        print(df2.D)
        print(df2.E)

        print("😇")
        print(df.head(2))
        print(df.tail(3))
        print("print the head and tail of N records")


        print("😇")
        print("index, dtypes, values, column, of dataframe ")
        print("dtypes")
        print(df.dtypes)
        print("columns")
        print(df.columns)
        print("values")
        print(df.values)

        print("😇")
        print(df.describe())

        print(df)
        print(" T and transpose() is the same")
        print(" first time transpose")
        df.transpose()
        print(" second time transpose")
        print(df.T)

        print("😇")
        print(" sort_index can sort just the index for axis = 0 or colum for axis = 1")
        print(df.sort_index(axis=0, ascending=False))
        print(" sort axis = 1")
        print(df.sort_index(axis=1, ascending=False))

        print("sort column by it's value")
        print(df.sort_values("A"))

        print("😇")
        print("getting the data, select the single column yeids a Serail data")


class TestDataFrameUsing(unittest.TestCase):

    def test_Ch05_Getting_Start_with_pandas(self):
        print(" chpter 05 Getting Start With Pandas ")
