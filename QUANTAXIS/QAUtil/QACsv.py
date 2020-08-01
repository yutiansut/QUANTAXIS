# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

import csv


def QA_util_save_csv(data, name, column=None, location=None):
    # 重写了一下保存的模式
    # 增加了对于可迭代对象的判断 2017/8/10
    """
    explanation:
        将数据保存为csv
    
    params:
        * data->
            含义: 需要被保存的数据
            类型: List
            参数支持: []
        * name:
            含义: 要保存的名字
            类型: str
            参数支持: []
        * column:
            含义: 行的名称(可选)
            类型: str
            参数支持: [None]
        * location:
            含义: 保存位置(可选)
            类型: str
            参数支持: []
    """
    assert isinstance(data, list)
    if location is None:
        path = './' + str(name) + '.csv'
    else:
        path = location + str(name) + '.csv'
    with open(path, 'w', newline='') as f:
        csvwriter = csv.writer(f)
        if column is None:
            pass
        else:
            csvwriter.writerow(column)

        for item in data:

            if isinstance(item, list):
                csvwriter.writerow(item)
            else:
                csvwriter.writerow([item])


if __name__ == '__main__':
    QA_util_save_csv(['a', 'v', 2, 3], 'test')
    QA_util_save_csv([['a', 'v', 2, 3]], 'test2')
