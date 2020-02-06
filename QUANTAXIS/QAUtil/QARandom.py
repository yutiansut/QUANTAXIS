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

import random


def QA_util_random_with_zh_stock_code(stockNumber=10):
    '''
    随机生成股票代码
    :param stockNumber: 生成个数
    :return:  ['60XXXX', '00XXXX', '300XXX']
    '''
    codeList = []
    pt = 0
    for i in range(stockNumber):
        if pt == 0:
            #print("random 60XXXX")
            iCode = random.randint(600000, 609999)
            aCode = "%06d" % iCode

        elif pt == 1:
            #print("random 00XXXX")
            iCode = random.randint(600000, 600999)
            aCode = "%06d" % iCode

        elif pt == 2:
            #print("random 00XXXX")
            iCode = random.randint(2000, 9999)
            aCode = "%06d" % iCode

        elif pt == 3:
            #print("random 300XXX")
            iCode = random.randint(300000, 300999)
            aCode = "%06d" % iCode

        else:
            #print("random 00XXXX")
            iCode = random.randint(2000, 2999)
            aCode = "%06d" % iCode
        pt = (pt + 1) % 5
        codeList.append(aCode)
    return codeList


def QA_util_random_with_topic(topic='Acc', lens=8):
    """
    生成account随机值

    Acc+4数字id+4位大小写随机

    """
    _list = [chr(i) for i in range(65,
                                   91)] + [chr(i) for i in range(97,
                                                                 123)
                                          ] + [str(i) for i in range(10)]

    num = random.sample(_list, lens)
    return '{}_{}'.format(topic, ''.join(num))


if __name__ == '__main__':
    print(QA_util_random_with_topic(input()))
