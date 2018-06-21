# coding:utf-8


import QUANTAXIS as QA
import pandas as pd
import re



def get_block(block):
    block_tdx = QA.DATABASE.stock_block
    block_ths = QA.DATABASE.stock_block_ths
    codelist = QA.QA_fetch_stock_list_adv()
    block = [block] if isinstance(block, str) else block

    code_tdx = pd.DataFrame(
        [item for item in block_tdx.find({'blockname': {'$in': block}})])
    code_ths = pd.DataFrame(
        [item for item in block_ths.find({'blockname': {'$in': block}})])

    return pd.concat([code_tdx, code_ths], axis=0).code.drop_duplicates().tolist()


def get_name(code):
    codelist = QA.QA_fetch_stock_list_adv()
    return QA.QA_util_to_json_from_pandas(codelist.set_index('code', drop=False).loc[code].loc[:, ['code', 'name']])


if __name__ == '__main__':
    print(get_block(['上海国资改革', '阿里巴巴概念']))
