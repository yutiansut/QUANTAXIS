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

import datetime

import pandas as pd

from QUANTAXIS.QAUtil import DATABASE, QA_util_log_info


def QA_data_calc_marketvalue(data, xdxr):
    '使用数据库数据计算复权'
    mv = xdxr.query('category!=6').loc[:,
                                       ['shares_after',
                                        'liquidity_after']].dropna()
    res = pd.concat([data, mv], axis=1)

    res = res.assign(
        shares=res.shares_after.fillna(method='ffill'),
        lshares=res.liquidity_after.fillna(method='ffill')
    )
    return res.assign(mv=res.close*res.shares*10000, liquidity_mv=res.close*res.lshares*10000).drop(['shares_after', 'liquidity_after'], axis=1)\
            .loc[(slice(data.index.remove_unused_levels().levels[0][0],data.index.remove_unused_levels().levels[0][-1]),slice(None)),:]


def QA_data_marketvalue(data):

    def __QA_fetch_stock_xdxr(
            code,
            format_='pd',
            collections=DATABASE.stock_xdxr
    ):
        '获取股票除权信息/数据库'
        try:
            data = pd.DataFrame(
                [item for item in collections.find({'code': code})]
            ).drop(['_id'],
                   axis=1)
            data['date'] = pd.to_datetime(data['date'])

            return data.drop_duplicates(
                'date',
                keep='last'
            ).set_index(['date',
                         'code'],
                        drop=False)
        except:
            return pd.DataFrame(
                data=[],
                columns=[
                    'category',
                    'category_meaning',
                    'code',
                    'date',
                    'fenhong',
                    'fenshu',
                    'liquidity_after',
                    'liquidity_before',
                    'name',
                    'peigu',
                    'peigujia',
                    'shares_after',
                    'shares_before',
                    'songzhuangu',
                    'suogu',
                    'xingquanjia'
                ]
            )

    code = data.index.remove_unused_levels().levels[1][0] if isinstance(
        data.index,
        pd.core.indexes.multi.MultiIndex
    ) else data['code'][0]
    return QA_data_calc_marketvalue(data, __QA_fetch_stock_xdxr(code))
