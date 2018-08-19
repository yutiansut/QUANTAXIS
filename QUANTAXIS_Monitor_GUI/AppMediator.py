'''
https://sourcemaking.com/design_patterns/mediator/python/1
'''
import sys
import os
import threading
import subprocess
import time
import socket

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from datetime import datetime

from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab02_WebpageEastMoneyZJLX import processNumber
from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab02_WebpageEastMoneyZJLX import portNumberStart


from QUANTAXIS_Monitor_GUI.ProgressDlgs.ProgressDlg_Timeout import *
from QUANTAXIS_Monitor_GUI.ProgressDlgs.ProgressDlg_WithThreading import *


from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_GetStockList_Partition import *
from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_CheckZJLX_DB_Task import *
from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_FetchWebPage import *


from QUANTAXIS_Monitor_GUI.TasksByThreading.QA_Gui_DateFetch_Task import *



from QUANTAXIS.QAUtil.QASetting import *

#enum 有坑，容易造成第三方名字冲突
#https://blog.csdn.net/appleyk/article/details/77934767
#https://www.cnblogs.com/fyqx/p/6985902.html


class Mediator:
    """
    Implement cooperative behavior by coordinating Colleague objects.
    Know and maintains its colleagues.
    """
    ########################################################################################################
    processList = [] # process object
    strProcessStateTerminated = "ProcessTerminated"
    strProcessStateStartupFailed = "ProcessStartupFailed"
    strProcessStateRunning = "ProcessRunning"
    strProcessStateNoResponse = "ProcessNoResponse"
    strProcessStateError= "ProcessStateError"
    strCurrentProcessState = [] # = strProcessStateTerminated

    ########################################################################################################
    threadList =[] # thread objecg
    strThreadStateTerminated= "ThreadTerminated"
    strThreadStateRunning = "ThreadRunning"
    strCurrentThreadState = []

    ########################################################################################################
    currentNeedUpdateStockCodeList = []
    cuurentNeedUpdateCodeSegmentCountLists = []
    currentNeedUpdateCodeSegemenStockList = [] #list in list

    #每个线程上一次成功完成获取的点
    lastTimeProgressCheckPoint = []

    ########################################################################################################

    def __init__(self):

        for iIndex in range(processNumber):
            self.processList.append(None)
            self.threadList.append(None)
            self.strCurrentProcessState.append(self.strProcessStateTerminated)
            self.strCurrentThreadState.append(self.strThreadStateTerminated)
            self.lastTimeProgressCheckPoint.append(0)

            self.currentNeedUpdateCodeSegemenStockList.append(None)
            self.currentNeedUpdateStockCodeList.append(None)
            self.cuurentNeedUpdateCodeSegmentCountLists.append(0)

            pass

    def try_connect_server(self, strAddress, strPort):
        connectedOk = False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (strAddress, int(strPort))
            sock.settimeout(5.0)
            sock.connect(server_address)

            # data = sock.recv(128)
            # if len(data) == 128:
            #
            #     cmdString = data.decode();
            #     cmdArry = cmdString.split('@')
            #     cmd = cmdArry[0].strip('0')
            #     parame = cmdArry[1]
            #     if (cmd == 'state' and parame == 'process_start_ok'):
            #         connectedOk = True
            #     else:
            #         connectedOk = False
            # else:
            #     connectedOk = False
            connectedOk = True
        except  Exception as ee:
            strError = ee.__str__()
            print(strError)
        finally:
            sock.close()

        return connectedOk


    def try_connect_server_and_shutdown_process(self,strAddress, strPort):
        shutdownOk = False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (strAddress, int(strPort))
            sock.connect(server_address)

            #############################################################
            strMsg0 = "shutdown_process@shutdown_process"
            bytes_content = strMsg0.encode()
            bytes_content = bytes_content.zfill(128)
            assert (len(bytes_content) == 128)
            # 🛠todo fix 128 个byte 很傻
            sock.sendall(bytes_content)
            #############################################################
            #
            #
            # data = sock.recv(128)
            # if len(data) == 128:
            #
            #     cmdString = data.decode();
            #     cmdArry = cmdString.split('@')
            #     cmd = cmdArry[0].strip('0')
            #     parame = cmdArry[1]
            #     if (cmd == 'state' and parame == 'shutdown_procceed'):
            #         shutdownOk = True
            # else:
            #     shutdownOk = False
            shutdownOk = True
        except  Exception as ee:
            strError = ee.__str__()
            print(strError)
        finally:
            sock.close()

        return shutdownOk

    def startUpEastMoneyZjlxProcess(self, parentWnd, iProcessIndex, strAddress, strPort):
        print(strAddress,' ', strPort)

        if self.getCurrentProcessState(iProcessIndex) == self.strProcessStateRunning:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("已经启动了，正在工作中！😹  ")
            msg.setInformativeText("已经启动了，正在工作中😹 ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("已经启动了，正在工作中")
            retval = msg.exec()
            return;


        ui_log = parentWnd.trigger_sub_process_operation_log_by_index(iProcessIndex)

        try:

            #self.try_connect_server_and_shutdown_process(strAddress, strPort)

            # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI/MainTables/__file__
            realPath = os.path.realpath(__file__)  # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI/__file__
            realDir1 = os.path.dirname(realPath);  # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI
            realDir2 = os.path.dirname(realDir1);

            p = subprocess.Popen(
               ['python', './QUANTAXIS_Monitor_GUI/TasksByProcess/SubProcessFetchZJLX.py', (strPort)],
               cwd=realDir2)
            #stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            #第一次尝试30次
            tryCount = 0
            while True:
                boolConnectOk = self.try_connect_server(strAddress, strPort)
                if boolConnectOk == False:
                    strMsg = " 🐢正在subprocess启动未完成， #{}进程 地址{}, 端口{} ，⌛️耐心等待️⌛ 第%d次尝试 ".format(iProcessIndex, strAddress, strPort,tryCount)
                    ui_log.emit(strMsg)
                    dlg = ProgressDlg_Timeout(parent=None, timeOut=2, userHint=strMsg)
                    dlg.exec()

                    tryCount = tryCount + 1
                    if tryCount > 30:
                        break
                else:
                    break


            if boolConnectOk == False:
                msg = QMessageBox()
                #msg.setWindowFlags(Qt)
                strMsg = " 🐢正在subprocess启动失败 \n #{}进程 地址{}, 端口{} \n ❌启动失败，无法连接 startUpEastMoneyZjlxProcess❌".format(iProcessIndex, strAddress, strPort)
                ui_log.emit(strMsg)
                msg.setText(strMsg)
                msg.exec()

                # p.terminate()
                # print('强制退出进程')

                ui_log.emit('❌启动失败，无法连接 startUpEastMoneyZjlxProcess❌')

                self.strCurrentProcessState[iProcessIndex] = self.strProcessStateStartupFailed
                return False
            else:
                self.strCurrentProcessState[iProcessIndex] = self.strProcessStateRunning



            if self.processList[iProcessIndex] is None:
                self.processList[iProcessIndex] = p
                ui_log.emit('✅启动成功，开始等待命令✅')

            else:
                # 不应该执行到这里
                self.strCurrentProcessState[iProcessIndex] = self.strProcessStateError

                # p = self.processList[iProcessIndex]
                # p.terminate()
                # print('强制退出进程')
                # p = None
                # ui_log.emit('❌系统错误，退出进程！startUpEastMoneyZjlxProcess 强制退出进程 ❌')
                # dlg = ProgressDlg_Timeout(parent=None, timeOut=10, userHint=" ❌系统错误，退出进程！❌")
                # dlg.exec()
                #self.processList[iProcessIndex] = p

                return False

            print(p)
            #等待返回OK  尝试连接socket 服务程序
            #查询就绪命令
            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateRunning
            return True

        except Exception as ee:
            strError = ee.__str__()
            print(strError)

            #self.shutdownEastMoneyZjlxProcess(self,iProcessIndex,strAddress,strPort)
            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateStartupFailed
            return False



    def shutdownEastMoneyZjlxProcess(self, parentWnd, iProcessIndex, strAddress, strPort):
        print(strAddress, ' ', strPort)


        # if self.getCurrentProcessState(iProcessIndex) != self.strProcessStateRunning:
        #     msg = QMessageBox()
        #     msg.setIcon(QMessageBox.Information)
        #     msg.setText("进程已经停止了！😹  ")
        #     msg.setInformativeText("进程已经停止了😹 ")
        #     msg.setWindowTitle("操作提示：")
        #     msg.setDetailedText("进程已经停止了")
        #     retval = msg.exec()
        #     return;

        if self.getCurrentThreadState(iProcessIndex) != self.strThreadStateTerminated:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("线程没有停止，请先停止线程！😹  ")
            msg.setInformativeText("线程没有停止，请先停止线程😹 ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("线程没有停止，请先停止线程")
            retval = msg.exec()
            return

        ui_log = parentWnd.trigger_sub_process_operation_log_by_index(iProcessIndex)

        # 等待返回OK  尝试连接socket 服务程序
        # 发送关闭命令
        p = self.processList[iProcessIndex]

        # 第一次尝试30次
        tryCount = 0
        while True:

            tryCount = tryCount + 1

            bCanConnect = self.try_connect_server_and_shutdown_process(strAddress,strPort)
            if bCanConnect == True:
                strMsg = " ☄️正在关闭 #{}进程 地址{}, 端口{} ⌛️耐心等待️⌛ ".format(iProcessIndex, strAddress, strPort)
                ui_log.emit(strMsg)
                dlg = ProgressDlg_Timeout(parent=None, timeOut=5, userHint=strMsg)
                dlg.exec()
            else:
                break

            if tryCount > 30:
                break




        bCoonectOk = self.try_connect_server(strAddress, strPort)
        if bCoonectOk == False:

            strLog = "❓💤进程%d 结束成功 💤❓" % iProcessIndex
            ui_log.emit(strLog)
            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateTerminated

        else:
            ui_log.emit("❌进程结束失败❌")
            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateRunning

        #time.sleep(2)
        if p is not None:
            # 强制退出
            #p.terminate()
            #print('强制退出进程')
            #p.poll()
            p = None
            self.processList[iProcessIndex] = None

            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateTerminated

            #bCoonectOk = self.try_connect_server(strAddress, strPort)
            #if bCoonectOk == True:
            #    self.strCurrentProcessState[iProcessIndex] = self.strProcessStateError
        else:

            #dlg = ProgressDlg_Timeout(parent=None, timeOut=60, userHint=" ❌系统错误，退出进程！shutdownEastMoneyZjlxProcess❌")
            #dlg.exec()

            self.strCurrentProcessState[iProcessIndex] = self.strProcessStateTerminated
            #time.sleep(10)
        pass

    #todo fixhere 放到公用类里去
    def stockListSeperateToListCount(self, taskNumber, stockCounts):
        # for i in stock_list_length:

        counts_list = []
        if stockCounts % taskNumber == 0:
            subBlockCount = stockCounts // taskNumber
            for i in range(taskNumber):
                counts_list.append(subBlockCount)
            return counts_list

        taskNumberPlusOne = taskNumber + 1

        subsotck_list_length = stockCounts // taskNumberPlusOne
        substock_list_remain = stockCounts % taskNumberPlusOne

        subRemainDivion = (subsotck_list_length + substock_list_remain) // taskNumber
        subRemainRemain = (subsotck_list_length + substock_list_remain) % taskNumber

        eachBlockSize = subsotck_list_length + subRemainDivion
        lastBlockSize = eachBlockSize + subRemainRemain


        for i in range(taskNumber-1):
            counts_list.append(eachBlockSize)
        counts_list.append(lastBlockSize)

        return counts_list

    #todo fixhere 放到公用类里去
    '''
        to list in list
    '''
    def stockListSeperatorToListList(self, stockAllList, stockSegCountList):
        lastSubCount = 0
        iSegmentIndex = 0

        subSegCodelistInlist = []
        for iSegmentCount in stockSegCountList:
            subCodeList = []
            for iCountSub in range(iSegmentCount):
                subCodeList.append(stockAllList[iCountSub + lastSubCount])
            lastSubCount = lastSubCount + stockSegCountList[iSegmentIndex]
            subSegCodelistInlist.append(subCodeList)
            iSegmentIndex = iSegmentIndex + 1

        return subSegCodelistInlist

    '''
    
    '''

    #todo fixhere 放到公用类里去
    def assignStockListSegment(self, parentWnd):

        self.currentNeedUpdateStockCodeList.clear()
        self.cuurentNeedUpdateCodeSegmentCountLists.clear()
        self.currentNeedUpdateCodeSegemenStockList.clear()

        workThreading = QThread_GetStockList_Partition()

        mongo_uri = QASETTING.mongo_uri
        strMsgTitle = "🔬 尝试连接数据库 🗃"
        strMsg = "📂 正在获取股票列表 📚 {}".format(mongo_uri)
        dlg = ProgressDlg_WithQThread(parentWnd,workThreading,strMsg,strMsgTitle)
        dlg.startMyThread()
        dlg.exec()


        workThreading_for_check_check_zjlx_db = QThread_Check_ZJLX_DB_Status()
        workThreading_for_check_check_zjlx_db.pyqtSignalToLogTable = parentWnd.trigger_table_log_zjlx_db_status
        workThreading_for_check_check_zjlx_db.zjlxRecNeedUpdateStockCodes.clear()

        strMsgTitle = "🔬 检查资金流向数据库中的 记录 🗃"
        strMsg = "📂 正在读取资金资金流向数据库 📚 {}".format(mongo_uri)
        dlg = ProgressDlg_WithQThread(parent= parentWnd,
                qThreadObj=workThreading_for_check_check_zjlx_db,
                    userHint=strMsg, dlgTitle=strMsgTitle)
        dlg.startMyThread()
        dlg.exec()

        needStockCount = len(workThreading_for_check_check_zjlx_db.zjlxRecNeedUpdateStockCodes)
        codeCountsList = self.stockListSeperateToListCount(processNumber, needStockCount)


        strMsg1 = "需要获取 A股 {} 个股票最近100天资金流向 \n".format(needStockCount)
        iCount = 0
        for iSubBlockCount in codeCountsList:
            strMsg1 = strMsg1 + "进程#{} 分配股票个数 {} \n".format(iCount,iSubBlockCount)
            iCount=iCount+1

        dlg = QMessageBox.information(parentWnd,"分配股票每个股票区间个数", strMsg1)

        self.currentNeedUpdateStockCodeList = workThreading_for_check_check_zjlx_db.zjlxRecNeedUpdateStockCodes
        self.cuurentNeedUpdateCodeSegmentCountLists = codeCountsList

        self.currentNeedUpdateCodeSegemenStockList = self.stockListSeperatorToListList(
            self.currentNeedUpdateStockCodeList, self.cuurentNeedUpdateCodeSegmentCountLists
        )


        try:
            iProIndex = 0
            for row in self.currentNeedUpdateCodeSegemenStockList:
                trigger = parentWnd.trigger_sub_process_label_by_index(iProIndex)
                strTxt = '🐌%d进程,没有分配代码段:[%s~%s],进度:0/%d,操作日志'% (iProIndex, row[0], row[len(row)-1],len(row))

                #strTxt = '🐌%d进程,分配代码段:[%s~%s],进度:0/%d,没有开始' % (iProIndex, row[0], row[len(row)-1],len(row))
                trigger.emit(strTxt)
                iProIndex = iProIndex+1
        except Exception as ee:
            print(ee)

        #check point 置0
        for i in range(processNumber):
            self.lastTimeProgressCheckPoint[i] = 0

        pass

    #########################################################################################################

    def getCurrentProcessState(self, iProcessIndex):
        return self.strCurrentProcessState[iProcessIndex]


    def getCurrentThreadState(self, iProcessIndex):
        return self.strCurrentThreadState[iProcessIndex]

    #########################################################################################################

    def cmdProcessDoTheJob(self,parentWnd, iProcessIndex, connectAddress, connectPortInt):

        if self.currentNeedUpdateCodeSegemenStockList[iProcessIndex] is None or len(self.currentNeedUpdateCodeSegemenStockList[iProcessIndex]) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(" 🅾️ 没有分配到股票！ 🅾️ ")
            msg.setInformativeText(" 🅾️ 没有分配到股票 🅾️ ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText(" 🅾️ 没有分配到股票 🅾️ ")
            retval = msg.exec()
            return


        if self.strCurrentProcessState[iProcessIndex] == self.strProcessStateRunning:

            if self.strCurrentThreadState[iProcessIndex] == self.strThreadStateTerminated:

                workThreading = QThread_Fetch_Eastmoney_WebPageData()

                #初始化线程 变量， 从 QT 继承的类 没有 init ？？？
                self.threadList[iProcessIndex] = workThreading
                workThreading.stockCodeList = self.currentNeedUpdateCodeSegemenStockList[iProcessIndex]
                workThreading.connectAddress = connectAddress
                workThreading.connectPortInt = connectPortInt
                workThreading.processIndex= iProcessIndex
                workThreading.pyqtSignalToLogErrorTable = parentWnd.trigger_table_error_log
                workThreading.pyqtSignalToLogOpInfoTable = parentWnd.trigger_table_process_thread_op_log

                workThreading.lastTimeCheckPointStart = self.lastTimeProgressCheckPoint[iProcessIndex]

                workThreading.start()
                self.strCurrentThreadState[iProcessIndex] = self.strThreadStateRunning
                self.threadList[iProcessIndex] = workThreading

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("🌀线程已经启动成功！👻  ")
                msg.setInformativeText("🌀线程已经启动成功👻 ")
                msg.setWindowTitle("操作提示：")
                msg.setDetailedText("🌀线程已经启动成功")
                retval = msg.exec()
            else:

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(" 🅾️ 线程已经启动！🅾️  ")
                msg.setInformativeText("🅾️ 线程已经启动 🅾️ ")
                msg.setWindowTitle("操作提示：")
                msg.setDetailedText("🅾️ 线程已经启动 🅾️ ")
                retval = msg.exec()
        else:

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(" 🅾️ 进程没有启动！🅾️ ")
            msg.setInformativeText("🅾️ 进程没有启动 🅾️")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("进程没有启动")
            retval = msg.exec()


    def cmdProcessStopTheJob(self,parentWnd, iProcessIndex, connectAddress, connectPortInt):


        if self.strCurrentThreadState[iProcessIndex] == self.strThreadStateRunning:

            workThreading = self.threadList[iProcessIndex]
            workThreading.bThreadTobeOver = True

            dlg = ProgressDlg_Timeout(None, 10, '🌀等待线程已经成功结束！💀 ')
            dlg.exec()

            while True:
                if workThreading.isFinished() == True:
                    break


            self.strCurrentThreadState[iProcessIndex] = self.strThreadStateTerminated


            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("🌀线程已经成功结束！💀  ")
            msg.setInformativeText("🌀线程已经成功结束 💀  ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("🌀线程已经成功结束 💀 ")
            retval = msg.exec()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(" 🅾️ 线程没有启动！ 🅾️  ")
            msg.setInformativeText("线程没有启动 🅾️ ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText(" 🅾️ 线程没有启动 🅾️ ")
            retval = msg.exec()


    def addSuccessCodeToCheckPoint(self,strProcessIndex):

        iProcesIndex = int(strProcessIndex)
        self.lastTimeProgressCheckPoint[iProcesIndex] = self.lastTimeProgressCheckPoint[iProcesIndex] + 1

        print("%d 保存记录点！%d",iProcesIndex, self.lastTimeProgressCheckPoint[iProcesIndex])
        pass

    def getSuccessCodeCheckPointCount(self, strProcessIndex):
        iProcesIndex = int(strProcessIndex)
        return self.lastTimeProgressCheckPoint[iProcesIndex]


    def updateCurrentProcessThreadStatus(self, parentWnd : 'TabEastMoneyZJLX'):



        for iIndex in range(processNumber):

            #self.processList[iIndex]
            if self.threadList[iIndex] is not None and self.threadList[iIndex].isFinished():
                self.strCurrentThreadState[iIndex] = self.strThreadStateTerminated

            if self.strCurrentProcessState[iIndex] == self.strProcessStateRunning:
                strStatesLabel = "#%d ✅进程运行中✅ "%(iIndex)

                if self.strCurrentThreadState[iIndex] == self.strThreadStateRunning:
                    strStatesLabel = strStatesLabel + "#%d ✅线程运行中✅ "%(iIndex)
                else:
                    strStatesLabel = strStatesLabel + "#%d ⛔💤️线程未运行💤⛔ "%(iIndex)


            else:
                strStatesLabel = "#%d ⛔💤进程未运行💤⛔ "%iIndex

            parentWnd.lstSubProcessOpMsg[iIndex].setText(strStatesLabel)


        pass
