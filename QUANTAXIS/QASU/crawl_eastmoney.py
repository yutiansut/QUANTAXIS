
import os
from QUANTAXIS.QAUtil import QALocalize
from QUANTAXIS_CRAWLY.run_selenium_alone import read_east_money_page_zjlx_to_sqllite


def QA_read_eastmoney_zjlx_web_page_to_sqllite(stockCode = None):

    # todo 🛠 check stockCode 是否存在有效合法
    # todo 🛠 QALocalize 从QALocalize 目录中读取 固定位置存放驱动文件

    print("📨当前工作路径文件位置 : ",os.getcwd())
    path_check = os.getcwd()+"/selenium_driver"
    if os.path.exists(path_check) == False:
        print("😵 确认当前路径是否包含selenium_driver目录 😰 ")
        return
    else:
        print(os.getcwd()+"/selenium_drive"," 目录存在 😁")
    print("")

    path_for_save_data = QALocalize.download_path + "/eastmoney_stock_zjlx"
    isExists = os.path.exists(path_for_save_data)
    if isExists == False:
        os.mkdir(path_for_save_data)
        isExists = os.path.exists(path_for_save_data)
        if isExists == True:
            print(path_for_save_data,"目录不存在！ 成功建立目录 😢")
        else:
            print(path_for_save_data,"目录不存在！ 失败建立目录 🤮, 可能没有权限 🈲")
            return
    else:
        print(path_for_save_data,"目录存在！准备读取数据 😋")

    full_path_name = path_for_save_data + "/" + stockCode + "_zjlx.sqlite.db"

    read_east_money_page_zjlx_to_sqllite(stockCode,full_path_name)

    #创建目录
    #启动线程读取网页，写入数据库
    #等待完成