import ast


from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab0_RootClass import *
from QUANTAXIS_Monitor_GUI.AppMediator import *


#https://blog.csdn.net/henni_719/article/details/71706678
from functools import partial

'''
    ------------ 总体进度条消息  
    --------| 代码段:[600001~600188], 进度:111/188， 正在获取:600001  |地址|端口|启动连接进程|关闭进程操作| 
    日志 
       600000， 打开网页失败
       600111， 解析网页失败
       600111， 打开网页成功
       600111， 解析网页成功
       600111， 插入数据库记录100条 日期从到结束                                                                   
   ...
    分配股票  （开始，关闭所有进程） 
'''

processNumber = 9
portNumberStart = 4500

class TabEastMoneyZJLX(TabRootClass):

    #进程开启关闭操作的日志到UI
    #https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    #https://www.cnblogs.com/tkinter/p/5632266.html
    '''
        ？？？？？？如何程序化动态分配 静态 成员变量 ？？？？？？
    '''
    #todo fixhere
    #use 动态的方法创建 静态变量
    # _array_trigger_sub_process_operation_log = [
    #     pyqtSignal(str), pyqtSignal(str), pyqtSignal(str), pyqtSignal(str),
    #     pyqtSignal(str), pyqtSignal(str), pyqtSignal(str), pyqtSignal(str),
    #     pyqtSignal(str), pyqtSignal(str), pyqtSignal(str), pyqtSignal(str),
    # ]
    #############################################################################################################\
    #
    # 😖😖 只能用这种方式 写 ？ 不能动态创建 静态的 类变量 。。。。
    trigger_sub_process_operation_log_0 = pyqtSignal(str)
    trigger_sub_process_operation_log_1 = pyqtSignal(str)
    trigger_sub_process_operation_log_2 = pyqtSignal(str)
    trigger_sub_process_operation_log_3 = pyqtSignal(str)
    trigger_sub_process_operation_log_4 = pyqtSignal(str)
    trigger_sub_process_operation_log_5 = pyqtSignal(str)
    trigger_sub_process_operation_log_6 = pyqtSignal(str)
    trigger_sub_process_operation_log_7 = pyqtSignal(str)
    trigger_sub_process_operation_log_8 = pyqtSignal(str)

    # 😖😖  没办法， pyqtSignal 要求是 静态类变量，从 QObject继承
    def trigger_sub_process_operation_log_by_index(self, iIndex):
        if iIndex == 0:
            return self.trigger_sub_process_operation_log_0
        elif iIndex == 1:
            return self.trigger_sub_process_operation_log_1
        elif iIndex == 2:
            return self.trigger_sub_process_operation_log_2
        elif iIndex == 3:
            return self.trigger_sub_process_operation_log_3
        elif iIndex == 4:
            return self.trigger_sub_process_operation_log_4
        elif iIndex == 5:
            return self.trigger_sub_process_operation_log_5
        elif iIndex == 6:
            return self.trigger_sub_process_operation_log_6
        elif iIndex == 7:
            return self.trigger_sub_process_operation_log_7
        elif iIndex == 8:
            return self.trigger_sub_process_operation_log_8

    #############################################################################################################

    trigger_sub_process_label_0 = pyqtSignal(str)
    trigger_sub_process_label_1 = pyqtSignal(str)
    trigger_sub_process_label_2 = pyqtSignal(str)
    trigger_sub_process_label_3 = pyqtSignal(str)
    trigger_sub_process_label_4 = pyqtSignal(str)
    trigger_sub_process_label_5 = pyqtSignal(str)
    trigger_sub_process_label_6 = pyqtSignal(str)
    trigger_sub_process_label_7 = pyqtSignal(str)
    trigger_sub_process_label_8 = pyqtSignal(str)

    def trigger_sub_process_label_by_index(self, iIndex):
        if iIndex == 0:
            return self.trigger_sub_process_label_0
        elif iIndex == 1:
            return self.trigger_sub_process_label_1
        elif iIndex == 2:
            return self.trigger_sub_process_label_2
        elif iIndex == 3:
            return self.trigger_sub_process_label_3
        elif iIndex == 4:
            return self.trigger_sub_process_label_4
        elif iIndex == 5:
            return self.trigger_sub_process_label_5
        elif iIndex == 6:
            return self.trigger_sub_process_label_6
        elif iIndex == 7:
            return self.trigger_sub_process_label_7
        elif iIndex == 8:
            return self.trigger_sub_process_label_8

    #############################################################################################################
    trigger_table_log_zjlx_db_status = pyqtSignal(str, str, str, int, str)

    # processId , code, op, ErrorMsg
    trigger_table_process_thread_op_log = pyqtSignal(str,str,str,str)
    trigger_table_error_log = pyqtSignal(str,str,str,str)

    def __init__(self, parent=None):
        super(TabEastMoneyZJLX, self).__init__(parent)

        self.startTimer(500,Qt.CoarseTimer)

    def initUI(self):

        self.totalProgressBar = QProgressBar(self)
        self.totalProgressLabel = QLabel(self)
        self.totalProgressLabel.setMaximumHeight(28)
        self.totalProgressBar.setMaximumHeight(28)
        strTxt = "总体进度 :🐢 共个{} 股票🐍 {}/{}进度🦎".format(0,0,0)
        self.totalProgressLabel.setText(strTxt)

        self.lstSubThreadBar = []
        self.lstSubThreadOpLabel = []

        self.lstSubProcessOpMsg = []
        self.lstBntStartSubProcessSocketServer = []
        self.lstBntStopSubProcessSocketServer = []

        self.lstTextEditAddress = []
        self.lstTextEditPort = []

        self.lstBntStartJob = []
        self.lstBntStopJob = []

        for iIndex in range(processNumber):
            subProgressBar = QProgressBar(self)
            strObjName = "subProcessBar_%d" % iIndex
            subProgressBar.setObjectName(strObjName)
            self.lstSubThreadBar.append(subProgressBar)

            subProgressLabel = QLabel(self)
            strObjName = "subProcessLabel_%d" % iIndex
            subProgressLabel.setObjectName(strObjName)
            self.lstSubThreadOpLabel.append(subProgressLabel)

            '''
            https://blog.csdn.net/fengyu09/article/details/39498777
            '''

            bntStartSubProcessSocketServer = QPushButton(self)
            bntStartSubProcessSocketServer.setText("⚙️启动进程")
            strObjName = "startProcessBnt_%d" % iIndex
            bntStartSubProcessSocketServer.setObjectName(strObjName)
            bntStartSubProcessSocketServerClick = partial(self.doStartSubProcess,strObjName)
            bntStartSubProcessSocketServer.clicked.connect(bntStartSubProcessSocketServerClick)
            bntStartSubProcessSocketServer.setEnabled(True)
            self.lstBntStartSubProcessSocketServer.append(bntStartSubProcessSocketServer)


            bntStopSubProcessSocketServer = QPushButton(self)
            bntStopSubProcessSocketServer.setText("⭕️停止进程")
            strObjName = "stopProcessBnt_%d" % iIndex
            bntStopSubProcessSocketServer.setObjectName(strObjName)
            bntStopSubProcessSocketServerClick = partial(self.doStopSubProcess,strObjName)
            bntStopSubProcessSocketServer.clicked.connect(bntStopSubProcessSocketServerClick)
            bntStopSubProcessSocketServer.setEnabled(True)
            self.lstBntStopSubProcessSocketServer.append(bntStopSubProcessSocketServer)

            #todo check ip address
            #rx = QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b");

            txtEditAddress = QLineEdit(self)
            txtEditAddress.setPlaceholderText("localhost")
            txtEditAddress.setMinimumWidth(105)
            txtEditAddress.setMaximumWidth(90)
            strObjName = "txtAddressLineEdit_%d" % iIndex
            txtEditAddress.setObjectName(strObjName)
            self.lstTextEditAddress.append(txtEditAddress)

            txtEditPort = QLineEdit(self)
            txtEditPort.setPlaceholderText(str(portNumberStart + iIndex))
            txtEditPort.setMaximumWidth(50)
            txtEditPort.setMinimumWidth(40)
            strObjName= "txtPortLineEdit_%d"%iIndex
            txtEditPort.setObjectName(strObjName)
            self.lstTextEditPort.append(txtEditPort)


            subProcessStartJob = QPushButton(self)
            subProcessStartJob.setText("🚩开始获取")
            subProcessStartJob.setMaximumWidth(100)
            strObjName= "startJobBnt_%d"%iIndex
            subProcessStartJob.setObjectName(strObjName)
            subProcessStartJobClick = partial(self.cmdProcessDoJobByThread, strObjName)
            subProcessStartJob.clicked.connect(subProcessStartJobClick)
            self.lstBntStartJob.append(subProcessStartJob)

            subProcessStopJob = QPushButton(self)
            subProcessStopJob.setText("🛑停止获取")
            subProcessStopJob.setMaximumWidth(100)
            strObjName= "stopJobBnt_%d"%iIndex
            subProcessStopJob.setObjectName(strObjName)
            subProcessStopJobClick = partial(self.cmdProcessStopJobByThread, strObjName)
            subProcessStopJob.clicked.connect(subProcessStopJobClick)
            self.lstBntStopJob.append(subProcessStopJob)

            subProcessLogDetailMsg = QLabel(self)
            subProcessLogDetailMsg.setText('.......没有启动.......')
            strObjName= "logDetailLabel_%d"%iIndex
            subProcessLogDetailMsg.setObjectName(strObjName)
            self.lstSubProcessOpMsg.append(subProcessLogDetailMsg)

            # 进程操作状态
            try:
                strObjName = "logProcessOperationLog_%d" % iIndex
                sub_process_op_log_partial_fun = partial(self.doSubProcessOpLog, strObjName)
                self.trigger_sub_process_operation_log_by_index(iIndex).connect(sub_process_op_log_partial_fun)

            except Exception as ee:
                strErrorMsg = ee.__str__()
                print(strErrorMsg)
                pass

            #进程 的工作进度
            try:
                strObjName = "logProcessProgressLog_%d" % iIndex
                sub_process_label_partial_fun = partial(self.doSubProcessProgressLabelUpdate, strObjName)
                self.trigger_sub_process_label_by_index(iIndex).connect(sub_process_label_partial_fun)

            except Exception as ee:
                strErrorMsg = ee.__str__()
                print(strErrorMsg)
                pass

        self.trigger_table_log_zjlx_db_status.connect(self.acceptLogToUI)
        self.trigger_table_process_thread_op_log.connect(self.acceptProcessThreadOpLogToTable)
        self.trigger_table_error_log.connect(self.acceptErrorLogToTable)

        # it does not works
        #for iIndex in range(processNumber):
            #eval(self.lstBntStopSubProcessSocketServer[iIndex].clicked.connect(lambda: self.doStartSubProcess(iIndex)))
            #print("-->", self.lstBntStopSubProcessSocketServer[iIndex])
        #self.lstBntStopSubProcessSocketServer[0].clicked.connect(lambda: self.doStopSubProcess(0))
        #self.lstBntStopSubProcessSocketServer[1].clicked.connect(lambda: self.doStopSubProcess(1))
        #self.lstBntStopSubProcessSocketServer[2].clicked.connect(lambda: self.doStopSubProcess(2))
        #self.lstBntStopSubProcessSocketServer[3].clicked.connect(lambda: self.doStopSubProcess(3))
        #self.lstBntStopSubProcessSocketServer[4].clicked.connect(lambda: self.doStopSubProcess(4))
        #self.lstBntStopSubProcessSocketServer[5].clicked.connect(lambda: self.doStopSubProcess(5))


        self.bntAssignStock = QPushButton(self)
        self.bntAssignStock.setText('🗂分配股票到每个工作进程')

        self.bntStartAllProcsss = QPushButton(self)
        self.bntStartAllProcsss.setText('▶️开始获取数据')


        self.bntStopAllProcsss = QPushButton(self)
        self.bntStopAllProcsss.setText('🔴停止获取')

        ###########################################################################3

        self.bntAssignStock.clicked.connect(self.assignStockListSegment)

        self.bntStopAllProcsss.clicked.connect(self.stopAllThread)
        self.bntStartAllProcsss.clicked.connect(self.startAllThread)

        ###########################################################################3
        self.dbRecordStatusLabel = QLabel(self)
        self.dbRecordStatusLabel.setText('(东方财富网页版只提供最近100天的资金流向)')
        self.tableRecordsStatusLog =QTableWidget(self)
        self.subProcessProgressLabel = QLabel(self)
        self.subProcessProgressLabel.setText('获取操作日志')
        self.tableProcessThreadOpLog = QTableWidget(self)

        self.subProcessErrorLabel = QLabel(self)
        self.subProcessErrorLabel.setText('错误操作日志')
        self.tableErrorLog = QTableWidget(self)

        self.rootHLayout = QHBoxLayout(self)

        self.leftVLayout = QVBoxLayout(self)
        self.rightVLayout = QVBoxLayout(self)

        self.topHLayout = QHBoxLayout(self)

        self.topHLayout.addWidget(self.totalProgressLabel)
        self.topHLayout.addWidget(self.totalProgressBar)

        self.leftVLayout.setSpacing(1)
        self.leftVLayout.addLayout(self.topHLayout)

        index = 0
        for index in range(processNumber):

            middleHLayout0 = QHBoxLayout(self)
            middleHLayout0.addWidget(self.lstBntStartJob[index])
            middleHLayout0.addWidget(self.lstBntStopJob[index])
            middleHLayout0.addWidget(self.lstSubProcessOpMsg[index])

            middleHLayout0.addWidget(self.lstBntStartSubProcessSocketServer[index])
            middleHLayout0.addWidget(self.lstBntStopSubProcessSocketServer[index])
            middleHLayout0.addWidget(self.lstTextEditAddress[index])
            middleHLayout0.addWidget(self.lstTextEditPort[index])

            self.leftVLayout.addLayout(middleHLayout0)

            middleHLayout = QHBoxLayout(self)
            middleHLayout.setSpacing(1)

            middleHLayout.addWidget(self.lstSubThreadOpLabel[index])
            middleHLayout.addWidget(self.lstSubThreadBar[index])


            self.leftVLayout.addLayout(middleHLayout)

        self.bottomBntsHLayout = QHBoxLayout()
        self.bottomBntsHLayout.addWidget(self.bntAssignStock)
        self.bottomBntsHLayout.addWidget(self.bntStartAllProcsss)
        self.bottomBntsHLayout.addWidget(self.bntStopAllProcsss)

        self.leftVLayout.addLayout(self.bottomBntsHLayout)

        self.rightVLayout.addWidget(self.dbRecordStatusLabel)
        self.rightVLayout.addWidget(self.tableRecordsStatusLog)
        self.rightVLayout.addWidget(self.subProcessProgressLabel)
        self.rightVLayout.addWidget(self.tableProcessThreadOpLog)
        self.rightVLayout.addWidget(self.subProcessErrorLabel)
        self.rightVLayout.addWidget(self.tableErrorLog)

        self.rootHLayout.addLayout(self.leftVLayout)
        self.rootHLayout.addLayout(self.rightVLayout)

        self.setLayout(self.rootHLayout)


        #初始化界面
        for iIndex in range(processNumber):
            strLog = "❓💤进程%d还没有启动💤❓" % iIndex
            self.trigger_sub_process_operation_log_by_index(iIndex).emit(strLog)

        for iIndex in range(processNumber):
            strTxt = '🐌%d进程,没有分配代码段:[xxxxxxx,xxxxxx],进度:0/xxxx,操作日志'%iIndex
            self.trigger_sub_process_label_by_index(iIndex).emit(strTxt)


        for iIndex in range(processNumber):
            self.lstSubThreadBar[iIndex].setMaximum(10000)
        # self.dbRecordsStatusLog.setColumnCount(1)
        # self.dbRecordsStatusLog.setHorizontalHeaderLabels(['股票代码'])
        # self.dbRecordsStatusLog.setColumnWidth(0, 700)

        self.tableRecordsStatusLog.setAutoScroll(True)
        self.tableRecordsStatusLog.setColumnCount(5);
        self.tableRecordsStatusLog.setHorizontalHeaderLabels(['股票代码', '开始日期', '结束日期', '记录数', '是否更新'])
        self.tableRecordsStatusLog.setColumnWidth(0, 65)
        self.tableRecordsStatusLog.setColumnWidth(1, 85)
        self.tableRecordsStatusLog.setColumnWidth(2, 85)
        self.tableRecordsStatusLog.setColumnWidth(3, 65)
        self.tableRecordsStatusLog.setColumnWidth(4, 55)



        self.tableProcessThreadOpLog.setColumnCount(4)
        self.tableProcessThreadOpLog.setHorizontalHeaderLabels(['进程#', '代码', '操作', '日志内容'])

        self.tableProcessThreadOpLog.setColumnWidth(0, 18)
        self.tableProcessThreadOpLog.setColumnWidth(1, 95)
        self.tableProcessThreadOpLog.setColumnWidth(2, 95)
        self.tableProcessThreadOpLog.setColumnWidth(3, 95)



        self.tableErrorLog.setHorizontalHeaderLabels(['进程#', '代码', '操作', '日志内容'])
        self.tableErrorLog.setColumnCount(4)

        self.tableErrorLog.setColumnWidth(0, 18)
        self.tableErrorLog.setColumnWidth(1, 95)
        self.tableErrorLog.setColumnWidth(2, 95)
        self.tableErrorLog.setColumnWidth(3, 95)


        self.tableErrorLog.setMaximumWidth(65 + 85 + 85 + 65 + 55 + 50)
        self.tableProcessThreadOpLog.setMaximumWidth(65 + 85 + 85 + 65 + 55 + 50)
        self.tableRecordsStatusLog.setMaximumWidth(65 + 85 + 85 + 65 + 55 + 50)


        #############################################################################################################

    def doDummy(self):
        pass

    def stopAllThread(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("🤑还未实现，请一个个点击 按钮关闭进程！😹  ")
        msg.setInformativeText("🙄一次关闭，电脑会变得很慢，后期实现😹 ")
        msg.setWindowTitle("操作提示：")
        msg.setDetailedText("🤮笔记本电脑严重发烫")
        retval = msg.exec()
        pass

    def startAllThread(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("😯还未实现，请一个个点击 按钮启动进程！😹  ")
        msg.setInformativeText("🤐一次启动，电脑会变得很慢，后期实现😹 ")
        msg.setWindowTitle("😬操作提示：")
        msg.setDetailedText("🤔笔记本电脑严重发烫")
        retval = msg.exec()
        pass
    #############################################################################################################
    def acceptLogToUI(self, strCol0, strCol1, strCol2, intCol3, strCol4):

        # fieldArray = strToLog.split('_')
        # if fieldArray[1] is not None:
        #     jsonRec = ast.literal_eval(fieldArray[1])
        #
        #
        #
        rowCount = self.tableRecordsStatusLog.rowCount()
        try:
            self.tableRecordsStatusLog.setRowCount(rowCount + 1)
            if strCol0 is not None:
                col0 = QTableWidgetItem(strCol0)
                self.tableRecordsStatusLog.setItem(rowCount, 0, col0)

            if strCol1 is not None:
                col1 = QTableWidgetItem(strCol1)
                self.tableRecordsStatusLog.setItem(rowCount, 1, col1)

            if strCol2 is not None:
                col2 = QTableWidgetItem(strCol2)
                self.tableRecordsStatusLog.setItem(rowCount, 2, col2)

            if intCol3 is not None:
                col3 = QTableWidgetItem(str(intCol3))
                self.tableRecordsStatusLog.setItem(rowCount, 3, col3)

            if strCol4 is not None:
                col4 = QTableWidgetItem(strCol4)
                self.tableRecordsStatusLog.setItem(rowCount, 4, col4)
        except Exception as ee:
            print(ee)
    #############################################################################################################

    def acceptProcessThreadOpLogToTable(self, strProcessIndex, strProcessCode, strOperation, strMessage):

        try:

            iProcessIndex = int(strProcessIndex)
            mediator = self.getMediator();

            strOp0 = "✅解析网页中🕷进度日期报告"
            if strOperation == strOp0:

                strTxt = self.lstSubThreadOpLabel[iProcessIndex].text();
                strArr = strTxt.split(',')

                #strTxtNew = '🐌%d进程,没有分配代码段:[xxxxxxx,xxxxxx],进度:0/xxxx,操作日志' % iProcessIndex
                strArr[3] = strMessage

                newStr = strArr[0]+','+strArr[1]+','+strArr[2]+','+strArr[3]
                self.lstSubThreadOpLabel[iProcessIndex].setText(newStr)
                return

            strOp1 = "✅解析网页中🐞进度条报告"
            if strOperation == strOp1:
                iProgress = int(float(strMessage)*100)
                self.lstSubThreadBar[iProcessIndex].setValue(iProgress)

                return

            strOp2 = "✅写入🐜数据库OK"
            # 保存当前 的 check point 进度！
            if strOperation == strOp2:

                #保存当前进度
                mediator.addSuccessCodeToCheckPoint(strProcessIndex)

                # # 更新进度
                # iProcessIndex = int(strProcessIndex)
                strTxt = self.lstSubThreadOpLabel[iProcessIndex].text();
                strArr = strTxt.split(',')
                strProgress = strArr[2].split(':')
                #
                strAllNumberProgress = strProgress[1].split('/')
                strGotNumber = mediator.getSuccessCodeCheckPointCount(strProcessIndex)
                #
                newStr = strArr[0]+','+strArr[1]+','+strProgress[0]+':'+str(strGotNumber)+"/"+strAllNumberProgress[1]+","+strArr[3]
                #
                self.lstSubThreadOpLabel[iProcessIndex].setText(newStr)

            rowCount = self.tableProcessThreadOpLog.rowCount()
            self.tableProcessThreadOpLog.setRowCount(rowCount + 1)

            if strProcessIndex is not None:
                col0 = QTableWidgetItem(strProcessIndex)
                self.tableProcessThreadOpLog.setItem(rowCount, 0, col0)

            if strProcessCode is not None:
                col1 = QTableWidgetItem(strProcessCode)
                self.tableProcessThreadOpLog.setItem(rowCount, 1, col1)

            if strOperation is not None:
                col2 = QTableWidgetItem(strOperation)
                self.tableProcessThreadOpLog.setItem(rowCount, 2, col2)

            if strMessage is not None:
                col3 = QTableWidgetItem(str(strMessage))
                self.tableProcessThreadOpLog.setItem(rowCount, 3, col3)

        except Exception as ee:
            print(ee)



    def acceptErrorLogToTable(self,strProcessIndex, strProcessCode, strOperation, strErrorMessage ):

        rowCount = self.tableErrorLog.rowCount()
        try:
            self.tableErrorLog.setRowCount(rowCount + 1)

            if strProcessIndex is not None:
                col0 = QTableWidgetItem(strProcessIndex)
                self.tableErrorLog.setItem(rowCount, 0, col0)

            if strProcessCode is not None:
                col1 = QTableWidgetItem(strProcessCode)
                self.tableErrorLog.setItem(rowCount, 1, col1)

            if strOperation is not None:
                col2 = QTableWidgetItem(strOperation)
                self.tableErrorLog.setItem(rowCount, 2, col2)

            if strErrorMessage is not None:
                col3 = QTableWidgetItem(str(strErrorMessage))
                self.tableErrorLog.setItem(rowCount, 3, col3)

        except Exception as ee:
            print(ee)


    #############################################################################################################
    def doSubProcessProgressLabelUpdate(self,strObjName, strLabelString):
        print('trigger_sub_process_progress_update {} emit {}'.format(strObjName, strLabelString))
        args0 = strObjName.split('_')
        iIndex = int(args0[1])
        #self.lstSubProcessLogDetialMsg[iIndex].setText(strLogString)
        self.lstSubThreadOpLabel[iIndex].setText(strLabelString)

        pass

    def doSubProcessOpLog(self, strObjName, strLogString):
        print('trigger_sub_process_operation_log {} emit {}'.format(strObjName, strLogString))
        args0 = strObjName.split('_')
        iIndex = int(args0[1])

        self.lstSubProcessOpMsg[iIndex].setText(strLogString)

        pass

    #############################################################################################################
    def doStartSubProcess(self, strObjName):
        print('Button {} clicked'.format(strObjName))

        args0 = strObjName.split('_')
        iIndex = int(args0[1])

        strAddress = self.lstTextEditAddress[iIndex].text()
        strPort = self.lstTextEditPort[iIndex].text()

        #todo fix here
        if strAddress!="" and strAddress!='localhost':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("尝试启动远程服务进程！😹  ")
            msg.setInformativeText("不是本地localhost本地进程😹 ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("请在远程机器上启动本程序启动服务进程")
            retval = msg.exec()
            return

        if strAddress == "":
            strAddress = 'localhost'
        if strPort == "":
            strPort = str(portNumberStart + iIndex)


        mediator = self.getMediator()
        bRetOk = mediator.startUpEastMoneyZjlxProcess(self, iIndex,strAddress,strPort)

        # if bRetOk:
        #     self.lstBntStartSubProcessSocketServer[iIndex].setEnabled(False)
        #     self.lstBntStopSubProcessSocketServer[iIndex].setEnabled(True)
        #
        #     self.lstTextEditPort[iIndex].setEnabled(False)
        #     self.lstTextEditAddress[iIndex].setEnabled(False)

    def doStopSubProcess(self, strObjName):
        print('Button {} clicked'.format(strObjName))
        args0 = strObjName.split('_')
        iIndex = int(args0[1])
        strAddress = self.lstTextEditAddress[iIndex].text()
        strPort = self.lstTextEditPort[iIndex].text()

        #todo fix here
        if strAddress!="" and strAddress!='localhost':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("远程程服务进程！😹  ")
            msg.setInformativeText("不是本地localhost本地进程😹 ")
            msg.setWindowTitle("操作提示：")
            msg.setDetailedText("请在远程机器上关闭服务进程")
            retval = msg.exec()
            return

        if strAddress == "":
            strAddress = 'localhost'
        if strPort == "":
            strPort = portNumberStart + iIndex

        mediator = self.getMediator()



        mediator.shutdownEastMoneyZjlxProcess(self, iIndex,strAddress,strPort)

        # self.lstBntStartSubProcessSocketServer[iIndex].setEnabled(True)
        # self.lstBntStopSubProcessSocketServer[iIndex].setEnabled(False)
        #
        # self.lstTextEditPort[iIndex].setEnabled(True)
        # self.lstTextEditAddress[iIndex].setEnabled(True)
        pass

    #############################################################################################################
    def cmdProcessDoJobByThread(self, strObjName):
        print('Button {} clicked'.format(strObjName))
        args0 = strObjName.split('_')
        iIndex = int(args0[1])

        mediator = self.getMediator()


        strAddress = self.lstTextEditAddress[iIndex].text()
        strPort = self.lstTextEditPort[iIndex].text()

        if strAddress == "":
            strAddress = 'localhost'
        if strPort == "":
            strPort = str(portNumberStart + iIndex)

        mediator.cmdProcessDoTheJob(self,iIndex,strAddress, int(strPort) )


    def cmdProcessStopJobByThread(self, strObjName):
        print('Button {} clicked'.format(strObjName))
        args0 = strObjName.split('_')
        iIndex = int(args0[1])

        mediator = self.getMediator()


        strAddress = self.lstTextEditAddress[iIndex].text()
        strPort = self.lstTextEditPort[iIndex].text()

        if strAddress == "":
            strAddress = 'localhost'
        if strPort == "":
            strPort = str(portNumberStart + iIndex)

        mediator.cmdProcessStopTheJob(self, iIndex, strAddress, int(strPort))


    #############################################################################################################
    def assignStockListSegment(self):
        # ask mediator to fetch the segment of stock code
        mediator = self.getMediator()
        mediator.assignStockListSegment(self)
        pass


    def timerEvent(self, a0: 'QTimerEvent'):

        mediator = self.getMediator()
        mediator.updateCurrentProcessThreadStatus(self)

        pass