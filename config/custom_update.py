#!/usr/local/bin/python
from QUANTAXIS.QASU.main import (
    QA_SU_save_long_freq,
    QA_SU_save_short_freq,
    QA_SU_save_list,
    QA_SU_save_stock_info,
    QA_SU_save_stock_xdxr,
    QA_SU_save_stock_block,
    QA_SU_save_financialfiles
)

update_list = []
min_freq = []

try:
    with open('update_list.txt', 'r') as f:
        update_list.extend([line.rstrip('\n') for line in f if line[0] != '#'])
except:
    pass

if len(update_list) > 0:
    min_freq.extend(x[10:].replace(' ', '') for x in update_list if '@' in x)
    min_freq = min_freq[0].split(',') if len(min_freq) else []
    update_list = update_list[:-1] if '@' in update_list[-1] else update_list
else:
    print('do not have the update list file: update_list.txt')


# update basic info
def info_update(update_list):
    for update in update_list:
        if update == 'stock_info':
            QA_SU_save_stock_info('tdx')
            update_list.remove(update)
        elif update == 'stock_xdxr':
            QA_SU_save_stock_xdxr('tdx')
            update_list.remove(update)
        elif update == 'stock_block':
            QA_SU_save_stock_block('tdx')
            update_list.remove(update)
        elif update == 'save_financialfiles':
            QA_SU_save_financialfiles()
            update_list.remove(update)
    return update_list


update_list = info_update(update_list)

for update in update_list:
    if 'min' in update:
        QA_SU_save_short_freq(engine='tdx', type_=update, min_list=min_freq)
    elif 'list' in update:
        QA_SU_save_list(engine='tdx', type_=update)
    else:
        QA_SU_save_long_freq(engine='tdx', type_=update)
