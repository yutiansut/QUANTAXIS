
import time
import datetime
import socket

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
from QUANTAXIS.QAUtil import DATABASE


from QUANTAXIS.QAUtil import (DATABASE,QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info, QA_util_code_tolist, QA_util_date_str2int, QA_util_date_int2str,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse, QADate_trade,QADate)


from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
from QUANTAXIS.QAUtil.QADate_trade import *

import pandas as pd
import numpy as np

from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_RootClass import *


class QThread_Fetch_Eastmoney_WebPageData(QThread_RootClass):

    lastTimeCheckPointStart = 0
    stockCodeList = []

    #每次修改数据库记录更新时间戳， 防止线程没有反应， 为实现？？？
    lastTimeThreadActivateTimeStamp = datetime.datetime.now()

    connectAddress = ""
    connectPortInt = 0
    processIndex = -1

    '''
            emit the string to the UI log table
    '''
    pyqtSignalToLogOpInfoTable = None
    pyqtSignalToLogErrorTable = None

    chrome_start_ok = False
    bThreadTobeOver = False

    def send_msg_to_server(self, sock, strMsg0):
        bytes_content = strMsg0.encode()
        bytes_content = bytes_content.zfill(128)
        assert (len(bytes_content) == 128)
        # 🛠todo fix 128 个byte 很傻
        sock.sendall(bytes_content)

    def unpack_cmd_string(self, data):
        cmdString = data.decode();
        cmdArry = cmdString.split('@')
        cmdArry[0] = cmdArry[0].strip('0')
        return cmdArry

    def get_connect_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.connectAddress, self.connectPortInt)
        sock.connect(server_address)
        return sock



    def run(self):

        try:
            sock = self.get_connect_sock()
            strMsg0 = "start_chrome_driver@start_chrome_driver"
            self.send_msg_to_server(sock, strMsg0)

            data = sock.recv(128)
            if len(data) == 128:
                cmd = self.unpack_cmd_string(data)
                if (cmd[0] == 'state' and cmd[1] == 'start_chrome_driver_ok'):
                    chrome_start_ok = True

                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅启动ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                elif (cmd == 'state'):
                    errorMessage = cmd[2]
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "❌启动ChromeDriver程序失败1❌"
                    strErroInfo = errorMessage;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)

            sock.close()
            #############################################################
            #############################################################
            # 循环获取股票列表，获取一个股，连接一次，然后 释放连接
            for iCodeIndex in range(self.lastTimeCheckPointStart, len(self.stockCodeList)):

                # 进程收到关闭请求
                if self.bThreadTobeOver == True:
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅收到退出线程停止命令✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                    break;


                strProcessIndex = str(self.processIndex)
                strCode = self.stockCodeList[iCodeIndex]
                sock = self.get_connect_sock()

                ##send command
                #############################################################
                strMsg0 = "fetch_a_stock_data_to_mongodb@%s" % strCode
                self.send_msg_to_server(sock,strMsg0)

                data = sock.recv(128)
                if len(data) == 128:
                    cmd = self.unpack_cmd_string(data)
                    if (cmd[0] == 'state' and cmd[1] == 'fetch_a_stock_data_to_mongodb_open_web_page_ok'):
                        strProcessIndex = str(self.processIndex)
                        strOp = "✅成功打开网页✅"
                        strInfo = "OK";
                        self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)


                        while True:
                            data = sock.recv(128)
                            if len(data) == 128:
                                cmd = self.unpack_cmd_string(data)

                                if (cmd[0] == 'state' and cmd[1] == 'progress'):
                                    prasePageProgress = cmd[2]

                                    strOp = "✅解析网页中🐞进度条报告"
                                    strInfo = prasePageProgress;
                                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                                    ###################################################################################
                                    # 进程收到关闭请求
                                    if self.bThreadTobeOver == True:
                                        strProcessIndex = str(self.processIndex)
                                        strCode = "None"
                                        strOp = "✅收到退出线程停止命令✅"
                                        strInfo = "OK";
                                        self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                        break;

                                    continue

                                elif (cmd[0] == 'state' and cmd[1]  == 'hearbeat'):
                                    prasePageDateStr = cmd[2]

                                    strOp = "✅解析网页中🕷进度日期报告"
                                    strInfo = prasePageDateStr;

                                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                                    ###################################################################################
                                    # 进程收到关闭请求
                                    if self.bThreadTobeOver == True:
                                        strProcessIndex = str(self.processIndex)
                                        strCode = "None"
                                        strOp = "✅收到退出线程停止命令✅"
                                        strInfo = "OK";
                                        self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                        break;

                                    continue

                                elif (cmd[0]  == 'state' and cmd[1] == 'fetch_a_stock_data_to_mongodb_prase_web_page_ok'):
                                    successPraseWebPageRecord = cmd[2]
                                    iRecNewCount = int(successPraseWebPageRecord)
                                    strOp = "✅写入🐜数据库OK"
                                    strInfo = "📋新增%d条记录" % iRecNewCount;
                                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                    break

                                elif (cmd[0]  == 'state' and cmd[1] == 'fetch_a_stock_data_to_mongodb_prase_web_page_failed'):
                                    generalMessage = cmd[2]
                                    strProcessIndex = str(self.processIndex)
                                    strOp = "❌解析网页失败❌"
                                    strErroInfo = generalMessage;
                                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                                    break
                                else:
                                    # 不应该执行到这里
                                    generalMessage = ""
                                    if len(cmd)>=1 and cmd[0] is not None:
                                        generalMessage = generalMessage + " " +  cmd[0]
                                    if len(cmd)>=2 and cmd[1] is not None:
                                        generalMessage = generalMessage + " " +  cmd[1]
                                    if len(cmd)>=3 and cmd[2] is not None:
                                        generalMessage = generalMessage + " " +  cmd[2]

                                    strProcessIndex = str(self.processIndex)
                                    strOp = "❌解析网页未知错误❌"
                                    strErroInfo = generalMessage;
                                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)

                                    break

                    elif (cmd[0] == 'state' and cmd[1] == 'fetch_a_stock_data_to_mongodb_open_web_page_failed'):
                        errorMessage = cmd[2]
                        strProcessIndex = str(self.processIndex)
                        strCode = strCode
                        strOp = "❌打开网页错误❌"
                        strErroInfo = errorMessage
                        self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                        pass


                sock.close()


            #############################################################
            #############################################################
            sock = self.get_connect_sock()
            strMsg0 = "shutdown_chrome_driver@shutdown_chrome_driver"
            self.send_msg_to_server(sock,strMsg0)

            data = sock.recv(128)
            if len(data) == 128:
                cmd = self.unpack_cmd_string(data)
                if( cmd[0] == 'state' and cmd[1] == 'shutdown_chrome_driver_ok'):
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅关闭ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                elif (cmd[0] == 'state'):
                    errorMessage = cmd[1]
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "❌关闭ChromeDriver程序失败1❌"
                    strErroInfo = errorMessage ;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)


            sock.close()
        except Exception as ee:
            errMsg = ee.__str__()
            print(errMsg)

        finally:
            pass

'''

 def run33(self):
 
  ##send command
            #############################################################
            strMsg0 = "start_chrome_driver@start_chrome_driver"
            bytes_content = strMsg0.encode()
            bytes_content = bytes_content.zfill(128)
            assert (len(bytes_content) == 128)
            # 🛠todo fix 128 个byte 很傻
            sock.sendall(bytes_content)
            #############################################################
            #############################################################
            data = sock.recv(128)
            if len(data) == 128:
                cmdString = data.decode();
                cmdArry = cmdString.split('@')
                cmd = cmdArry[0].strip('0')
                parame = cmdArry[1]
                if (cmd == 'state' and parame == 'start_chrome_driver_ok'):
                    chrome_start_ok = True

                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅启动ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                elif (cmd == 'state'):
                    errorMessage = cmdArry[2]
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "❌启动ChromeDriver程序失败1❌"
                    strErroInfo = errorMessage + " " + parame;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
            #############################################################


           
            #############################################################
            #############################################################
            data = sock.recv(128)
            if len(data) == 128:
                cmdString = data.decode();
                cmdArry = cmdString.split('@')
                cmd = cmdArry[0].strip('0')
                parame = cmdArry[1]
                if (cmd == 'state' and parame == 'shutdown_chrome_driver_ok'):
                    chrome_shutdown_ok = True
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅关闭ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)


                else:
                    chrome_shutdown_ok = False
            #############################################################

        except Exception as ee:
            print(ee)
            errorMessage = ee.__str__()

            strProcessIndex = str(self.processIndex)
            strCode = "None"
            strOp = "❌线程错误❌"
            strErroInfo = errorMessage;
            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)

        finally:
            sock.close()



        # 命令进程 开启 chromedriver

            ##connect to the process
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.connectAddress, self.connectPortInt)
            sock.connect(server_address)

            ##send command
            #############################################################
            strMsg0 = "start_chrome_driver@start_chrome_driver"
            bytes_content = strMsg0.encode()
            bytes_content = bytes_content.zfill(128)
            assert (len(bytes_content) == 128)
            # 🛠todo fix 128 个byte 很傻
            sock.sendall(bytes_content)
            #############################################################



                    ##send command
                    #############################################################
                    strMsg0 = "fetch_a_stock_data_to_mongodb@%s" % strCode
                    bytes_content = strMsg0.encode()
                    bytes_content = bytes_content.zfill(128)
                    assert (len(bytes_content) == 128)
                    # 🛠todo fix 128 个byte 很傻
                    sock.sendall(bytes_content)
                    #############################################################

                    ##wait command execute result
                    #############################################################

                    while True:

                        data = sock.recv(128)
                        if len(data) == 128:
                            cmdString = data.decode();
                            cmdArry = cmdString.split('@')
                            cmd = cmdArry[0].strip('0')
                            parame = cmdArry[1]
                            if (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_open_web_page_ok'):
                                strProcessIndex = str(self.processIndex)
                                strOp = "✅成功打开网页✅"
                                strInfo = "OK";
                                self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                                ##wait command execute result
                                #############################################################
                                continue

                            if (cmd == 'state' and parame == 'progress'):
                                prasePageProgress = cmdArry[2]

                                strOp = "✅解析网页中🐞进度条报告"
                                strInfo = prasePageProgress;
                                self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                continue
                            elif (cmd == 'state' and parame == 'hearbeat'):
                                prasePageDateStr = cmdArry[2]

                                strOp = "✅解析网页中🕷进度日期报告"
                                strInfo = prasePageDateStr;

                                self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                continue

                            elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_prase_web_page_ok'):
                                successPraseWebPageRecord = cmdArry[2]
                                iRecNewCount = int(successPraseWebPageRecord)
                                strOp = "✅写入🐜数据库OK"
                                strInfo = "📋新增%d条记录" % iRecNewCount;
                                self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                                break

                            elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_prase_web_page_failed'):
                                generalMessage = cmdArry[2]
                                strProcessIndex = str(self.processIndex)
                                strOp = "❌解析网页失败4❌"
                                strErroInfo = generalMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp,strErroInfo)
                                break

                            elif (cmd == 'state' and parame == 'error_general_1'):
                                generalMessage = cmdArry[2]
                                strProcessIndex = str(self.processIndex)
                                strOp = "❌解析网页失败5❌"
                                strErroInfo = generalMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp,strErroInfo)
                                break


                            elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_open_web_page_failed'):
                                errorMessage = cmdArry[2]

                                strProcessIndex = str(self.processIndex)
                                strOp = "❌打开网页失败7❌"
                                strErroInfo = errorMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                                break;

                            elif (cmd == 'state' and parame == 'error_general_2'):
                                generalMessage = cmdArry[2]
                                strProcessIndex = str(self.processIndex)
                                strOp = "❌打开网页失败8❌"
                                strErroInfo = generalMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                                break

                            elif (cmd == 'state' and parame == 'error_general_1'):
                                generalMessage = cmdArry[2]
                                strProcessIndex = str(self.processIndex)
                                strOp = "❌打开网页失败9❌"
                                strErroInfo = generalMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                                break

                            elif (cmd == 'state'):
                                generalMessage = cmdArry[2]
                                if len(cmdArry) >= 3:
                                    generalMessage = generalMessage + cmdArry[3]

                                strProcessIndex = str(self.processIndex)
                                strOp = "❌解析网页失败10❌"
                                strErroInfo = generalMessage;
                                self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                                break、、
'''

'''
    def run00000(self):
        #############################################################

        #命令进程 开启 chromedriver
        try:

            ##connect to the process
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.connectAddress, self.connectPortInt)
            sock.connect(server_address)

            ##send command
            #############################################################
            strMsg0 = "start_chrome_driver@start_chrome_driver"
            bytes_content = strMsg0.encode()
            bytes_content = bytes_content.zfill(128)
            assert (len(bytes_content) == 128)
            # 🛠todo fix 128 个byte 很傻
            sock.sendall(bytes_content)
            #############################################################


            ##wait command execute result
            #############################################################
            data = sock.recv(128)
            if len(data) == 128:

                cmdString = data.decode();
                cmdArry = cmdString.split('@')
                cmd = cmdArry[0].strip('0')
                parame = cmdArry[1]
                if (cmd == 'state' and parame == 'start_chrome_driver_ok'):
                    chrome_start_ok = True

                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅启动ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)


                elif( cmd == 'state' and parame == 'start_chrome_driver_failed'):
                    errorMessage = cmdArry[2]
                    chrome_start_ok = False

                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "❌启动ChromeDriver程序失败1❌"
                    strErroInfo = errorMessage;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)

                elif( cmd == 'state' and parame == 'error_general'):
                    generalMessage = cmdArry[2]
                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "❌启动ChromeDriver程序失败2❌"
                    strErroInfo = generalMessage;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)


            #############################################################

            else:
                chrome_start_ok = False
        except Exception as ee:
            print(ee)
            errorMessage = ee.__str__()

            strProcessIndex = str(self.processIndex)
            strCode = "None"
            strOp = "❌启动ChromeDriver程序3❌"
            strErroInfo = errorMessage;
            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)


        finally:
            sock.close()
        ###########################################
        ############################################
        ###############获取 记录 循环################
        ############################################

        if chrome_start_ok:

            #############################################################
            # 循环获取股票列表，获取一个股，连接一次，然后 释放连接
            for iCodeIndex in range(self.lastTimeCheckPointStart, len(self.stockCodeList)):


                strProcessIndex = str(self.processIndex)
                strCode = self.stockCodeList[iCodeIndex]


                try:
                    ##connect to the process
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_address = (self.connectAddress, self.connectPortInt)
                    sock.connect(server_address)

                    ##send command
                    #############################################################
                    strMsg0 = "fetch_a_stock_data_to_mongodb@%s"%strCode
                    bytes_content = strMsg0.encode()
                    bytes_content = bytes_content.zfill(128)
                    assert (len(bytes_content) == 128)
                    # 🛠todo fix 128 个byte 很傻
                    sock.sendall(bytes_content)
                    #############################################################

                    ##wait command execute result
                    #############################################################
                    data = sock.recv(128)
                    if len(data) == 128:

                        cmdString = data.decode();
                        cmdArry = cmdString.split('@')
                        cmd = cmdArry[0].strip('0')
                        parame = cmdArry[1]
                        if (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_open_web_page_ok'):

                            strProcessIndex = str(self.processIndex)
                            strOp = "✅成功打开网页✅"
                            strInfo = "OK";
                            self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                            ##wait command execute result
                            #############################################################
                            continue


                        if (cmd == 'state' and parame == 'progress'):
                            prasePageProgress = cmdArry[2]

                            strOp = "✅解析网页中🐞进度条报告"
                            strInfo = prasePageProgress;
                            self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                            continue
                        elif (cmd == 'state' and parame == 'hearbeat'):
                            prasePageDateStr = cmdArry[2]

                            strOp = "✅解析网页中🕷进度日期报告"
                            strInfo = prasePageDateStr;

                            self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                            continue

                        elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_prase_web_page_ok'):
                            successPraseWebPageRecord = cmdArry[2]
                            iRecNewCount = int(successPraseWebPageRecord)
                            strOp = "✅写入🐜数据库OK"
                            strInfo = "📋新增%d条记录" % iRecNewCount;
                            self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)
                            break

                        elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_prase_web_page_failed'):
                            generalMessage = cmdArry[2]
                            strProcessIndex = str(self.processIndex)
                            strOp = "❌解析网页失败4❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp,
                                                                strErroInfo)
                            break

                        elif (cmd == 'state' and parame == 'error_general_1'):
                            generalMessage = cmdArry[2]
                            strProcessIndex = str(self.processIndex)
                            strOp = "❌解析网页失败5❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp,
                                                                strErroInfo)
                            break


                        elif (cmd == 'state'):
                            generalMessage= "_"
                            if len(cmdArry) >= 3:
                                generalMessage = cmdArry[2]

                            strProcessIndex = str(self.processIndex)
                            strOp = "❌解析网页失败56❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp,strErroInfo)
                            break;

                        elif (cmd == 'state' and parame == 'fetch_a_stock_data_to_mongodb_open_web_page_failed'):
                            errorMessage = cmdArry[2]

                            strProcessIndex = str(self.processIndex)
                            strOp = "❌打开网页失败7❌"
                            strErroInfo = errorMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                            break;

                        elif (cmd == 'state' and parame == 'error_general_2'):
                            generalMessage = cmdArry[2]
                            strProcessIndex = str(self.processIndex)
                            strOp = "❌打开网页失败8❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                            break

                        elif (cmd == 'state' and parame == 'error_general_1'):
                            generalMessage = cmdArry[2]
                            strProcessIndex = str(self.processIndex)
                            strOp = "❌打开网页失败9❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                            break

                        elif (cmd == 'state'):
                            generalMessage = cmdArry[2]
                            if len(cmdArry) >= 3:
                                generalMessage = generalMessage + cmdArry[3]

                            strProcessIndex = str(self.processIndex)
                            strOp = "❌解析网页失败10❌"
                            strErroInfo = generalMessage;
                            self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)
                            break;

                    #############################################################



                except Exception as ee:
                    print(ee)
                    errorMessage = ee.__str__()

                    strProcessIndex = str(self.processIndex)
                    strCode = strCode
                    strOp = "❌获取股票%s❌"%strCode
                    strErroInfo = errorMessage;
                    self.pyqtSignalToLogErrorTable.emit(strProcessIndex, strCode, strOp, strErroInfo)


                finally:
                    sock.close()

                #############################################################
                #进程收到关闭请求
                if self.bThreadTobeOver == True:


                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅收到退出线程停止命令✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)

                    break;

            pass

        #############################################################
        ######################  所有记录 获取完毕 结束################################
        #############################################################
        # 命令进程 关闭 chromedriver
        try:
            ##connect to the process
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.connectAddress, self.connectPortInt)
            sock.connect(server_address)

            data = sock.recv(128)
            if len(data) == 128:

                cmdString = data.decode();
                cmdArry = cmdString.split('@')
                cmd = cmdArry[0].strip('0')
                parame = cmdArry[1]
                if (cmd == 'state' and parame == 'shutdown_chrome_driver_ok'):
                    chrome_shutdown_ok = True

                    strProcessIndex = str(self.processIndex)
                    strCode = "None"
                    strOp = "✅关闭ChromeDriver程序✅"
                    strInfo = "OK";
                    self.pyqtSignalToLogOpInfoTable.emit(strProcessIndex, strCode, strOp, strInfo)


                else:
                    chrome_shutdown_ok = False
            else:
                chrome_shutdown_ok = False
        except Exception as ee:
            print(ee)
        finally:
            sock.close()
        #############################################################

'''
