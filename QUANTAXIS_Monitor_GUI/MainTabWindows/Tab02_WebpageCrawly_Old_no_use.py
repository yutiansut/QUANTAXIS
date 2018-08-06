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



from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
'''
    spaghetti code 🍝,  really need to more modulize
    
    main approach is:
        launch the sepearte process to fire the chromedirver to fetch the eastmoney zjlx
        use the socket communicate with the main GUI process 
     
    抓取东方财富的资金流向
    
    日期	收盘价	涨跌幅	    主力净流入	超大单净流入     	大单净流入	中单净流入	小单净流入
                净额	净占比	净额	净占比	净额	净占比	净额	净占比	净额	净占比
'''

processNum = 8
port_number_start = 4800


mutex = threading.Lock()


# QRunnable 太高级，
# #emit the current sub process progress and log info the UI
#class Worker(QRunnable):
class Worker(QThread):
    '''

    '''
    def fetchCodeZjlx(self, fetchCode, process_port_int):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', process_port_int)
        #print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        try:

            # Send data
            # message = b'This is the message.  It will be repeated.'
            strMsg = 'read:%s' % fetchCode
            message = strMsg.encode()
            sock.sendall(message)
            #print('sending {!r}'.format(message))

            while True:
                data = sock.recv(512)
                if len(data) == 0:
                    time.sleep(1)
                    continue

                # print('received {!r}'.format(data))

                cmdString = data.decode();
                cmdArry = cmdString.split('@')

                #print(cmdArry[0])
                cmd = cmdArry[0].strip('0')
                #print(cmd)

                if (cmd == 'progress'):
                    #print('progress')
                    #print(cmdArry[1])
                    strFloat = cmdArry[1]
                    iProgress = int(float(strFloat)*100)
                    self.trigger_new_sub_process_progress.emit(iProgress)
                    continue

                if (cmd == 'logging'):
                    #print('logging')
                    #print(cmdArry[1])
                    strLogStr = cmdArry[1]
                    #self..emit(strLogStr)
                    self.trigger_new_sub_process_log.emit(strLogStr)
                    continue

                # if (cmd == 'data'):
                #     #print("收到 data is ")
                #     #print(cmdArry[1].encode('utf-8'))
                #     pass

                if (cmd == 'finished'):
                    #print('finish')
                    #print(cmdArry[1].encode('utf-8'))
                    strLogStr = cmdArry[1]
                    self.trigger_new_sub_process_log.emit(strLogStr)

                    break;
        except Exception as ee:
            print(ee)
            pass

        finally:
            #print('closing socket')
            sock.close()

    '''
    Worker thread
    '''
    process_port = 0

    #emit the current sub process progress and log info the UI
    trigger_new_sub_process_log = pyqtSignal(str)
    trigger_new_sub_process_progress = pyqtSignal(int)

    def handleNewSubProcessLog(self, vLog):

        self.progressLabel.setText(vLog)

        #filter the log message
        if '股票资金流向' in vLog:
            return

        rowCount = self.logTbl.rowCount()
        newItem1 = QTableWidgetItem(vLog)
        # newItem2 = QTableWidgetItem("QA_SU_save_stock_transaction")
        self.logTbl.setRowCount(rowCount + 1)
        self.logTbl.setItem(rowCount, 0, newItem1)
        # self.logDisplay.setItem(rowCount, 1, newItem2)

        pass

    def handleNewSubProcessProgress(self, iProgress):
        self.progressBar.setValue(iProgress)
        pass

    #set the progress and label for the test
    progressBar = None
    progressLabel  = None
    totalProgressBar = None
    totalProgressLabel = None
    logTbl = None

    #@pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        try:

            stockList = QA_fetch_stock_list()
            stockCount =len(stockList)

            subStockList = []


            quotient = stockCount // processNum
            remainder = stockCount % processNum
            thread_num = self.process_port - port_number_start

            formStock = 0
            toStock = 0

            if thread_num < processNum-1:
                fromStock = thread_num * quotient + 0
                toStock = thread_num * quotient + quotient-1
                for i in range(quotient):
                    aStock = stockList[thread_num * quotient+i]
                    subStockList.append(aStock)
            else:
                if remainder != 0:
                    fromStock = thread_num * quotient + 0
                    toStock = thread_num * quotient + remainder - 1
                    for i in range(remainder):
                        aStock = stockList[thread_num * quotient + i]
                        subStockList.append(aStock)
                else:
                    fromStock = thread_num * quotient + 0
                    toStock = thread_num * quotient + quotient - 1
                    for i in range(quotient):
                        aStock = stockList[thread_num * quotient + i]
                        subStockList.append(aStock)


            subStockList.reverse()

            for i in range(50):
                if i < len(subStockList[i]):
                    subStockList.remove(subStockList[i])


            print("thread_Port%d,一共获取股票%d个,  当前线程分配 %d， from %d to %d"%(self.process_port, stockCount, len(subStockList), fromStock, toStock))

        except Exception as ee:
            print(ee)
            return

        for aStock in subStockList:
            try:
                fetchCode = aStock['code']
                #print("准备获取代码{}".format(fetchCode))
                self.fetchCodeZjlx(fetchCode, self.process_port)
                #print("完成获取代码{}".format(fetchCode))

                if mutex.acquire():
                    #更新总体进度，这个是多线程 ,1/100 , 还剩1 , 1%
                    #labelAll = "%d/%d,还剩:%d,进度:%f" % (0, stockCountAll, stockCountAll, 0.0)

                    txt = self.totalProgressLabel.text();

                    progres_lables = txt.split(',')
                    progress_stock_number = progres_lables[0].split('/')

                    already_got = int(progress_stock_number[0])
                    total_remain = int(progress_stock_number[1])
                    already_got = already_got + 1

                    reamin_stock = total_remain - already_got
                    progress_percent = already_got / total_remain

                    sRemainHour = progres_lables[3].split(':')[1]
                    labelAll = "%d/%d,还剩:%d,进度:%f,剩余小时:%s" % (already_got, total_remain, reamin_stock, progress_percent, sRemainHour)
                    self.totalProgressLabel.setText(labelAll)
                    mutex.release()

            except Exception as ee:
                mutex.release()
                print(ee)
                pass
                return




class TabWebpageCrawly(QWidget):
    def __init__(self, parent=None):
        super(TabWebpageCrawly, self).__init__(parent)


    '''              
    ------------ 总体进度条  
    -------- 每个进程的进度
    -------- 每个进程的进度   日志
    -------- 每个进程的进度
    -------- 每个进程的进度
    
    启动所有进程  关闭所有进程 
    '''
    def initUI(self):
        '''

        :return:
        '''

        self.hbox = QHBoxLayout(self)

        self.vboxR = QVBoxLayout(self)
        self.vboxL = QVBoxLayout(self)

        self.labelAllProgress = QLabel(self)
        self.labelAllProgress.setText("总体进度")
        self.progressBarAll = QProgressBar(self)

        self.vboxL.addWidget(self.labelAllProgress)
        self.vboxL.addWidget(self.progressBarAll)


        self.subProgressBar  = []
        self.subProcessLabel = []
        for i in range(processNum):
            aBar = QProgressBar(self)
            aLabel = QLabel(self)

            aLabel.setText("子进程%d:"%i)
            self.subProgressBar.append(aBar)
            self.subProcessLabel.append(aLabel)

            self.vboxL.addWidget(aLabel)
            self.vboxL.addWidget(aBar)

        self.CmdLayout = QHBoxLayout(self)

        self.bntStart = QPushButton(self)
        self.CmdLayout.addWidget(self.bntStart)
        self.bntStart.setText("开始抓取")

        self.bntStop = QPushButton(self)
        self.CmdLayout.addWidget(self.bntStop)
        self.bntStop.setText("停止抓取")

        self.vboxL.addLayout(self.CmdLayout)

        self.logTbl = QTableWidget(self)
        self.vboxR.addWidget(self.logTbl)

        self.hbox.addLayout(self.vboxL)
        self.hbox.addLayout(self.vboxR)

        self.setLayout(self.hbox)

        self.bntStop.clicked.connect(self.doStop)
        self.bntStart.clicked.connect(self.doStart)
        #self.threadpool = QThreadPool()

        self.Thread_List = []
        # print("")

        self.logTbl.setColumnCount(5);
        self.logTbl.setHorizontalHeaderLabels(['股票代码','记录数','开始日期','结束日期','是否需要更新'])
        self.logTbl.setColumnWidth(0, 28)
        self.logTbl.setColumnWidth(1, 28)
        self.logTbl.setColumnWidth(2, 28)
        self.logTbl.setColumnWidth(3, 28)
        self.logTbl.setColumnWidth(4, 28)


        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.updateTotalProgress)  # 计时结束调用operate()方法


        pass

    # def xrange(x):
    #     return iter(range(x))


    def updateTotalProgress(self):

        try:
            #if mutex.acquire():
            self.startup_task_time
            current_task_time = datetime.now()

            # 任务运行的多长时间了
            already_elapse_second = (current_task_time - self.startup_task_time).seconds


            txt = self.labelAllProgress.text();
            progres_lables = txt.split(',')
            progress_stock_number = progres_lables[0].split('/')

            already_got = int(progress_stock_number[0])
            total_remain = int(progress_stock_number[1])

            reamin_stock = total_remain - already_got
            progress_percent = already_got / total_remain
            sRemainHour = progres_lables[3].split(':')[1]


            #计算 获取股票 需要的平均 秒数

            if already_got > 0:
                average_seconds_need_for_one_stock = already_elapse_second / already_got

                average_seconds_need_for_remain_stock = average_seconds_need_for_one_stock * reamin_stock
                average_hours_need_for_remain_stock = average_seconds_need_for_remain_stock / 60.0 / 60.0

                labelAll = "%d/%d,还剩:%d,进度:%f,剩余小时:%f" % \
                           (already_got, total_remain, reamin_stock, progress_percent, average_hours_need_for_remain_stock)
                self.labelAllProgress.setText(labelAll)

                #mutex.release()

                self.progressBarAll.setValue(int(progress_percent*10000))
        except Exception as ee:
            print(ee)
        pass


    def doStart(self):

        self.bntStop.setEnabled(False)
        self.bntStart.setEnabled(False)

        # 🛠todo 关闭上一次启动的服务区进程
        for i in range(processNum):
            try:
                process_port = str(port_number_start + i)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect the socket to the port where the server is listening
                server_address = ('localhost', int(process_port))
                # print('connecting to {} port {}'.format(*server_address))

                sock.connect(server_address)

                strMsg = 'shutdown:shutdown'
                message = strMsg.encode()
                sock.sendall(message)
                # print('sending {!r}'.format(message))

                # print('closing socket')
                #sock.close()
            except Exception as ee:
                # print(ee)
                pass

            finally:
                pass


        # 检查数据库是否已经开启
        try:
            stockListAll = QA_fetch_stock_list()
        except   Exception as ee:
            #print(ee)
            strError = ee.__str__()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("获取股票代码失败，无法连接数据库！😹")
            msg.setInformativeText(strError)
            msg.setWindowTitle("提示：")
            msg.setDetailedText(": 请确认mongodb 是否运行正常")
            #retval = msg.exec_()
            msg.exec()
            return

        stockCountAll = len(stockListAll)

        labelAll = "%d/%d,还剩:%d,进度:%f,剩余小时:%s"%(0,stockCountAll,stockCountAll,0.0,'未知')
        self.labelAllProgress.setText(labelAll)

        # 🛠todo
        #print("启动服务进程")

        # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI/MainTables/__file__
        realPath = os.path.realpath(__file__) # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI/MainTables/__file__
        realDir0 = os.path.dirname(realPath); # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI/MainTables
        realDir1 = os.path.dirname(realDir0); # xxxx/QUANTAXIS/QUANTAXIS_Monitor_GUI
        realDir2 = os.path.dirname(realDir1);

        for i in range(processNum):
            process_port = str(port_number_start + i)
            p = subprocess.Popen(
                ['python', './QUANTAXIS_Monitor_GUI/TasksByProcess/SubSeleniumProcess.py', process_port],
                cwd=realDir2)
                #stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #print(p)
            time.sleep(1)
            # 尝试连接是否正常工作

        # 🛠todo 判断服务进程socket是否已经就绪
        time.sleep(30)

        for i in range(processNum):
            try:
                #print("连接服务进程的线程")
                worker = Worker()

                worker.logTbl = self.logTbl

                worker.totalProgressBar = self.progressBarAll
                worker.totalProgressLabel = self.labelAllProgress

                worker.process_port = port_number_start + i
                worker.progressBar = self.subProgressBar[i]
                worker.progressLabel = self.subProcessLabel[i]

                worker.progressBar.setMaximum(10000)
                worker.progressLabel.setText("准备开始。。。")

                # ﻿Worker cannot be converted to PyQt5.QtCore.QObject in this context
                worker.trigger_new_sub_process_log.connect( worker.handleNewSubProcessLog)
                worker.trigger_new_sub_process_progress.connect( worker.handleNewSubProcessProgress)



                #self.threadpool.start(self.worker)
                #todo  fix here 没有用到赞的
                self.Thread_List.append(worker)

                worker.start()

                time.sleep(1)

            except Exception as ee:
                    #print(ee)
                pass

        self.startup_task_time = datetime.now()
        self.timer.start(15000)  # 设置计时间隔并启动, 更新整体进度

        self.progressBarAll.setMaximum(1000000)

        self.bntStop.setEnabled(True)
        #todo fixhere 完成所有的任务恢复这个按钮
        #self.bntStart.setEnabled(True)

    def doStop(self):
        # self.threadpool.
        self.bntStop.setEnabled(False)

        # 🛠todo 关闭chrome driver
        for i in range(processNum):
            try:
                process_port = str(port_number_start + i)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect the socket to the port where the server is listening
                server_address = ('localhost', int(process_port))
                #print('connecting to {} port {}'.format(*server_address))

                sock.connect(server_address)

                strMsg = 'shutdown:shutdown'
                message = strMsg.encode()
                sock.sendall(message)
                #print('sending {!r}'.format(message))
                #print('closing socket')
                #sock.close()
            except Exception as ee:
                    #print(ee)
                pass

            finally:
                pass

        # 🛠todo mac 下面无效，
        os.system("kill -9 $(ps -ef | grep chromedriver | awk '$0 !~/grep/ {print $2}' | tr -s '\n' ' ')")

        time.sleep(10)
        #

        for iThread in self.Thread_List:
            iThread.terminate()

        self.Thread_List.clear()

        self.bntStop.setEnabled(True)
        self.bntStart.setEnabled(True)

        pass

