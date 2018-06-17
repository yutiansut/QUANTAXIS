# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
import os
import sys
import pymongo
from QUANTAXIS.QAFetch.QAfinancial import parse_all, download_financialzip,parse_filelist

from QUANTAXIS.QAUtil.QALocalize import (cache_path, download_path, qa_path,
                                         setting_path)
from QUANTAXIS.QAUtil.QASql import ASCENDING, DESCENDING
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
from QUANTAXIS.QAUtil import DATABASE


def QA_SU_save_financial_files():
    """本地存储financialdata
    """
    filename=download_financialzip()
    if len(filename)>0:
        data = QA_util_to_json_from_pandas(parse_filelist(filename).reset_index(
        ).drop_duplicates(subset=['code', 'report_date']).sort_index())

        coll = DATABASE.financial
        coll.create_index(
            [("code", ASCENDING), ("report_date", ASCENDING)], unique=True)
        try:
            coll.insert_many(data, ordered=True)

        except pymongo.bulk.BulkWriteError:
            pass
    else:
        print('SUCCESSFULLY SAVE/UPDATE FINANCIAL DATA')