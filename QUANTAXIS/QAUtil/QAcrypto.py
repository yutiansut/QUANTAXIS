from QUANTAXIS.QAUtil import (QASETTING, QA_util_log_info)

def QA_SU_save_symbols(fetch_symnol_func, exchange):
    """
    explanation:
        保存获取的代码列表
    
    params:
        * fetch_symnol_func->
            含义: 获取代码列表的函数对象,注意这是一个函数对象,而不是函数运行的实体
            类型: func
            参数支持: []
        * exchange:
            含义: 交易所代码
            类型: str
            参数支持: []
    """
    symbols = fetch_symnol_func()
    col = QASETTING.client[exchange].symbols
    if col.find().count() == len(symbols):
        QA_util_log_info(
            "{} SYMBOLS are already existed and no more to update".format(exchange))
    else:
        QA_util_log_info(
            "Delete the original {} symbols collections".format(exchange))
        QASETTING.client.exchange.drop_collection("symbols")
        QA_util_log_info("Downloading the new symbols")
        col.insert_many(symbols)
        QA_util_log_info(
            "{} Symbols download is done! Thank you man!".format(exchange))
