
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import os
import time


from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_backtest
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial

from QUANTAXIS.QASU.save_tdx import  (QA_SU_save_stock_day,
                                      QA_SU_save_stock_week,
                                      QA_SU_save_stock_month,
                                      QA_SU_save_stock_year)

from QUANTAXIS.QASU.save_binance import QA_SU_save_binance_symbol, QA_SU_save_binance_1hour, \
                        QA_SU_save_binance_1day, QA_SU_save_binance_1min, QA_SU_save_binance

from QUANTAXIS.QAUtil import DATABASE

'''
    

    QThread
'''


class QA_GUI_Date_Fetch_Task(QThread):

    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_Date_Fetch_Task, self).__init__()

    # 定义一个信号, 更新任务进度
    trigger_new_log = pyqtSignal(str)
    trigger_new_progress = pyqtSignal(int)

    trigger_start_task_begin = pyqtSignal(str)
    trigger_start_task_done = pyqtSignal(str)

    def run(self):
        pass



class QA_GUI_DateFetch_SU_job01_stock_day(QA_GUI_Date_Fetch_Task):
    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_DateFetch_SU_job01_stock_day, self).__init__()

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_day(client=DATABASE, ui_log=self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")




class QA_GUI_DateFetch_SU_job01_stock_week(QA_GUI_Date_Fetch_Task):
    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_DateFetch_SU_job01_stock_week, self).__init__()

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_week(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass


class QA_GUI_DateFetch_SU_job01_stock_month(QA_GUI_Date_Fetch_Task):
    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_DateFetch_SU_job01_stock_month, self).__init__()

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_month(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")
        pass



class QA_GUI_DateFetch_SU_job01_stock_year(QA_GUI_Date_Fetch_Task):
    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_DateFetch_SU_job01_stock_year, self).__init__()

    def run(self):
        self.trigger_start_task_begin.emit("begin")
        QA_SU_save_stock_year(client=DATABASE, ui_log= self.trigger_new_log, ui_progress= self.trigger_new_progress)
        self.trigger_start_task_done.emit("end")

        pass


class QA_GUI_Selected_TaskQueue(QThread):
    def __int__(self):
        # 初始化函数，默认
        super(QA_GUI_Selected_TaskQueue, self).__init__()

    # 定义一个信号,
    trigger_all_task_start = pyqtSignal(str)
    trigger_all_task_done = pyqtSignal(str)

    QA_GUI_Task_List = []
    def run(self):
        self.trigger_all_task_start.emit('all_task_start')

        for iSubTask in self.QA_GUI_Task_List:
            iSubTask.start()
            #wait finish iSubTask
            while( iSubTask.isRunning() ):
                time.sleep(1)

        self.trigger_all_task_done.emit('all_task_done')

    def putTask(self, subTask):
        self.QA_GUI_Task_List.append(subTask)

    def clearTask(self):
        self.QA_GUI_Task_List.clear()