
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import os
import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_backtest
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial

from QUANTAXIS.QASU.save_tdx import  (QA_SU_save_stock_day,
                                      QA_SU_save_stock_week,
                                      QA_SU_save_stock_month,
                                      QA_SU_save_stock_year,
                                      QA_SU_save_stock_xdxr,
                                      QA_SU_save_stock_min,
                                      QA_SU_save_index_day,
                                      QA_SU_save_index_min,
                                      QA_SU_save_etf_day,
                                      QA_SU_save_etf_min,
                                      QA_SU_save_stock_list,
                                      QA_SU_save_stock_block,
                                      QA_SU_save_stock_info,
                                      QA_SU_save_stock_transaction,
                                      QA_SU_save_option_day)


from QUANTAXIS.QAUtil import DATABASE

'''
    
https://martinfitzpatrick.name/article/multithreading-pyqt-applications-with-qthreadpool/
    QThread
'''


class QA_GUI_Date_Fetch_Task(QThread ):
    #todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    #
    #def __int__(self, qParentWidget):
        # 初始化函数，默认
    #    super(QA_GUI_Date_Fetch_Task, self).__init__()
    #    self.qParentWidget = qParentWidget;

    # abstract method, 线程工作的地方
    def run(self):
        pass

    # 定义一个信号, 更新任务进度
    trigger_new_log = pyqtSignal(str)
    trigger_new_progress = pyqtSignal(int)

    trigger_start_task_begin = pyqtSignal(str)
    trigger_start_task_done = pyqtSignal(str)

    #abstract method ?
    def connectSignalSlot(self):
        self.trigger_new_log.connect(self.updateLogTriggerHandler)
        self.trigger_new_progress.connect(self.updateProgressTriggerHandler)
        self.trigger_start_task_begin.connect(self.startTaskTriggerHandler)
        self.trigger_start_task_done.connect(self.doneTaskTriggerHandler)

    def setLoggingUIWidget(self, logDisplay):
        self.logDisplay = logDisplay

    def setProgressUIWidget(self, qProgressBar):
        self.qProgressBar = qProgressBar

    def setCheckboxUIWidget(self, qCheckBox):
        self.qCheckBox = qCheckBox


    #abstract method
    def changeRunningTaskColor(self, qColor=QtCore.Qt.black):
        palette = self.qCheckBox.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, qColor)
        self.qCheckBox.setPalette(palette)
        pass


    #abstract method
    def updateLogTriggerHandler(self):
        pass

    #abstract method
    def updateProgressTriggerHandler(self):
        pass

    #abstract method
    def startTaskTriggerHandler(self):
        pass

    #abstract method
    def doneTaskTriggerHandler(self):
        pass



class QA_GUI_DateFetch_SU_job01_stock_day(QA_GUI_Date_Fetch_Task):

    # todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    #def __int__(self, qParentWidget):
        #super(QA_GUI_DateFetch_SU_job01_stock_day, self).__init__()
        #self.qCheckBox = qParentWidget.qCheckBoxJob01_save_stock_day
        #self.qProgressBar = qParentWidget.qProgressJob01_save_stock_day;

    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor( QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.black)
        pass

    def updateLogTriggerHandler(self, log):
        #print("append task log emite triggered!", log);
        #self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_day")
            self.logDisplay.setRowCount(rowCount+1)
            self.logDisplay.setItem(rowCount,0,newItem1)
            self.logDisplay.setItem(rowCount,1,newItem2)
            #self.logDisplay.scrollToBottom()

        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass


    # thread is working here
    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_day(client=DATABASE, ui_log=self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")

###################################################################################################################\

class QA_GUI_DateFetch_SU_job01_stock_week(QA_GUI_Date_Fetch_Task):
    # 🛠todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    # def __int__(self):
    #     # 初始化函数，默认
    #     super(QA_GUI_DateFetch_SU_job01_stock_week, self).__init__()

    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.yellow)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_week")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            #self.logDisplay.scrollToBottom()

        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_week(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################\

class QA_GUI_DateFetch_SU_job01_stock_month(QA_GUI_Date_Fetch_Task):
    # todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    # def __int__(self):
    #     # 初始化函数，默认
    #     super(QA_GUI_DateFetch_SU_job01_stock_month, self).__init__()


    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.blue)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_month")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            #self.logDisplay.scrollToBottom()

        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_month(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################\
class QA_GUI_DateFetch_SU_job01_stock_year(QA_GUI_Date_Fetch_Task):
    # todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    # def __int__(self):
    #     #         # 初始化函数，默认
    #     super(QA_GUI_DateFetch_SU_job01_stock_year, self).__init__()

    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.magenta)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_year")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            #self.logDisplay.scrollToBottom()

        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_year(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")

        pass
###################################################################################################################\
class QA_GUI_DateFetch_SU_job02_stock_xdxr(QA_GUI_Date_Fetch_Task):
    # todo fix here 不会执行 __init__的  QThread  是一个很特别的对象。
    # def _init_(self):
    #     # 初始化函数，默认
    #     super(QA_GUI_DateFetch_SU_job02_stock_xdxr, self).__init__()

    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_xdxr")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            #self.logDisplay.scrollToBottom()
        pass


    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_xdxr(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################\

class QA_GUI_DateFetch_SU_job03_stock_min(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_min")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            #self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_min(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass
###################################################################################################################

class QA_GUI_DateFetch_SU_job04_index_day(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_index_day")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_index_day(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################

class QA_GUI_DateFetch_SU_job05_index_min(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_index_min")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_index_min(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################

class QA_GUI_DateFetch_SU_job06_etf_day(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_etf_day")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_etf_day(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################
class QA_GUI_DateFetch_SU_job07_etf_min(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_etf_min")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_etf_min(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

###################################################################################################################
class QA_GUI_DateFetch_SU_job08_stock_list(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_list")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_list(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass



class QA_GUI_DateFetch_SU_job09_stock_block(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_list")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_block(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

class QA_GUI_DateFetch_SU_job10_stock_info(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_list")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_info(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass


class QA_GUI_DateFetch_SU_job11_stock_transaction(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_transaction")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_transaction(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass



class QA_GUI_DateFetch_SU_job12_option_day(QA_GUI_Date_Fetch_Task):
    def startTaskTriggerHandler(self, info_str):
        self.changeRunningTaskColor(QtCore.Qt.red)
        pass

    def doneTaskTriggerHandler(self, info_str):
        #
        self.changeRunningTaskColor(QtCore.Qt.green)
        pass

    def updateProgressTriggerHandler(self, progress):
        # print('update task progress ', progress);
        self.qProgressBar.setValue(progress)
        pass

    def updateLogTriggerHandler(self, log):
        # print("append task log emite triggered!", log);
        # self.logDisplay.append(log)
        if log and log.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(log)
            newItem2 = QTableWidgetItem("QA_SU_save_stock_transaction")
            self.logDisplay.setRowCount(rowCount + 1)
            self.logDisplay.setItem(rowCount, 0, newItem1)
            self.logDisplay.setItem(rowCount, 1, newItem2)
            # self.logDisplay.scrollToBottom()
        pass

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_option_day(client=DATABASE, ui_log=self.trigger_new_log, ui_progress=self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass

#通达信pytdx 会输出消息， 一同输出到gui界面只能够
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))



class QA_GUI_Selected_TaskQueue(QThread):

    # QThread 继承的不执行__init__
    #def __int__(self, logDisplay):
        # 奇怪的问题， 不执行 __init__
        # 初始化函数，默认
    #    super().__init__()
        #sfassda
        #print("run here")
        #exit(0)
        #self.logDisplay = logDisplay
        #sys.stderr.textWritten.connect(self.outputWrittenStderr)



    # 下面将print 系统输出重定向到textEdit中
    #sys.stdout = EmittingStream()
    #sys.stderr = EmittingStream()


    # 接收信号str的信号槽
    '''
      def outputWrittenStdout(self, text):
        cursor = self.logDisplay.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logDisplay.setTextCursor(cursor)
        self.logDisplay.ensureCursorVisible()

    def outputWrittenStderr(self, text):
        cursor = self.logDisplay.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logDisplay.setTextCursor(cursor)
        self.logDisplay.ensureCursorVisible()
    '''



    # 定义一个信号,
    trigger_all_task_start = pyqtSignal(str)
    trigger_all_task_done  = pyqtSignal(str)

    #定义任务（每个是一个线程）
    QA_GUI_Task_List = []
    def run(self):

        self.trigger_all_task_start.emit('all_task_start')

        for iSubTask in self.QA_GUI_Task_List:
            iSubTask.start()
            # wait finish iSubTask
            while (iSubTask.isRunning()):
                time.sleep(1)

        self.trigger_all_task_done.emit('all_task_done')

    def putTask(self, subTask):
        self.QA_GUI_Task_List.append(subTask)

    def clearTask(self):
        self.QA_GUI_Task_List.clear()