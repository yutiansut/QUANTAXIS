from QUANTAXIS.QAUtil import (QASETTING,QA_util_log_info)

TIMEOUT = 10
ILOVECHINA = "同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！"


def QA_SU_save_symbols(fetch_symnol_func, exchange):
    symbols = fetch_symnol_func()
    col = QASETTING.client[exchange].symbols
    if col.find().count() == len(symbols):
        QA_util_log_info("{} SYMBOLS are already existed and no more to update".format(exchange))
    else:
        QA_util_log_info("Delete the original {} symbols collections".format(exchange))
        QASETTING.client.binance.drop_collection("symbols")
        QA_util_log_info("Downloading the new symbols")
        col.insert_many(symbols)
        QA_util_log_info("{} Symbols download is done! Thank you man!".format(exchange))
