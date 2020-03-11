# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import scipy.signal as signal
import numpy as np


def Timeline_Integral_with_lambda(Tm,):
    """
    explanation:
       计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)		

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """
    T = [Tm[0]]
    #Ti = list(map(lambda x: reduce(lambda z,y: y * (z + y), Tm[0:x]), Tm))
    #Ti = list(map(lambda x,y: x * (y + x), Ti[1:], Tm))
    # print(Ti)
    #list(map(lambda x,y: x * (y + x), Tm[1:], T))
    return np.array(T)


def Timeline_Integral(Tm,):
    """
    explanation:
        计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快	

    params:
        * Tm ->:
            meaning:
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """
    T = [Tm[0]]
    for i in range(1, len(Tm)):
        T.append(Tm[i] * (T[i - 1] + Tm[i]))
    return np.array(T)


def Timeline_Integral_with_reduce(Tm,):
    """
    explanation:
        计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快		

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """

    """
    
    """
    T = []
    for i in range(1, len(Tm)):
        T.append(reduce(lambda x, y: y * (y + x), Tm[0:i]))
    return np.array(T)


# 经测试for最快，比reduce快
def Timeline_Integral_with_cross_before(Tm,):
    """
    explanation:
         计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零)		

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array
	
    demonstrate:
        Not described
	
    output:
        Not described
    """
    T = [Tm[0]]
    for i in range(1, len(Tm)):
        T.append(T[i - 1] + 1) if (Tm[i] != 1) else T.append(0)
    return np.array(T)


def LIS(X):
    """
    explanation:
        计算最长递增子序列		

    params:
        * X ->:
            meaning: 序列
            type: null
            optional: [null]

    return:
        (子序列开始位置, 子序列结束位置)

    demonstrate:
        Not described

    output:
        Not described
    """

    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] < X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]


def LDS(X):
    """
    explanation:
        计算最长递减子序列		

    params:
        * X ->:
            meaning: 序列
            type: null
            optional: [null]

    return:
         (子序列开始位置, 子序列结束位置)


    demonstrate:
        Not described

    output:
        Not described
    """
    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] > X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]
