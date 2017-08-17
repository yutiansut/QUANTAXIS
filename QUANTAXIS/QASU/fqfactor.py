# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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


from QUANTAXIS.QAData import QA_data_fq_factor
import json
from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info, QA_util_to_json_from_pandas, QA_util_date_stamp
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_list


def QA_save_fq_factor(client=QA_Setting.client):
    '保存复权因子'
    _coll = client.quantaxis.fq_factor

    _stock_list = QA_fetch_get_stock_list()

    for _item in _stock_list:
        data = QA_data_fq_factor(_item)
        data['date'] = data.index
        data['date'] = data['date'].apply(lambda x: str(x)[0:10])
        data['date_stamp'] = data['date'].apply(
            lambda x: QA_util_date_stamp(x))

        data['code'] = _item

        data_json = QA_util_to_json_from_pandas(data)
        _coll.insert_many(data_json)

def QA_update_fq_factor(client=QA_Setting.client):
    pass
if __name__ == '__main__':
    QA_save_fq_factor()
