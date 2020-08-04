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


import json
import os

from pytdx.reader import TdxMinBarReader

from QUANTAXIS.QAUtil import (DATABASE, QA_util_date_stamp, QA_util_log_info,
                              QA_util_time_stamp)


def QA_save_tdx_to_mongo(file_dir, client=DATABASE):
    """save file
    
    Arguments:
        file_dir {str:direction} -- 文件的地址
    
    Keyword Arguments:
        client {Mongodb:Connection} -- Mongo Connection (default: {DATABASE})
    """

    reader = TdxMinBarReader()
    __coll = client.stock_min_five
    for a, v, files in os.walk(file_dir):

        for file in files:

            if (str(file)[0:2] == 'sh' and int(str(file)[2]) == 6) or \
                (str(file)[0:2] == 'sz' and int(str(file)[2]) == 0) or \
                    (str(file)[0:2] == 'sz' and int(str(file)[2]) == 3):

                QA_util_log_info('Now_saving ' + str(file)
                                 [2:8] + '\'s 5 min tick')
                fname = file_dir + os.sep + file
                df = reader.get_df(fname)
                df['code'] = str(file)[2:8]
                df['market'] = str(file)[0:2]
                df['datetime'] = [str(x) for x in list(df.index)]
                df['date'] = [str(x)[0:10] for x in list(df.index)]
                df['time_stamp'] = df['datetime'].apply(
                    lambda x: QA_util_time_stamp(x))
                df['date_stamp'] = df['date'].apply(
                    lambda x: QA_util_date_stamp(x))
                data_json = json.loads(df.to_json(orient='records'))
                __coll.insert_many(data_json)


if __name__ == '__main__':
    file_dir = ['C:\\users\\yutiansut\\desktop\\sh5fz',
                'C:\\users\\yutiansut\\desktop\\sz5fz']
    for item in file_dir:
        QA_save_tdx_to_mongo(item)
