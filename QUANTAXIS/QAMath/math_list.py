# coding:utf-8

"""
QUANTAXIS 数学模组
"""

def QA_math_diff(data):
    y=[]
    for i in range(0,len(data)-1,1):
        y.append(float(data[i+1][0])-float(data[i][0]))
    return y

def QA_math_max_min(data):
    return max(data)-min(data)


