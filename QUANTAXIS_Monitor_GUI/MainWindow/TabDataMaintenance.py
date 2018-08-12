import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from QUANTAXIS_Monitor_GUI.MainWindow.QA_Gui_DateFetch_Task import *

#通达信pytdx 会输出消息， 一同输出到gui界面只能够
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))


class TabDataMaintenance(QWidget):
    def __init__(self, parent=None):
        super(TabDataMaintenance, self).__init__(parent)

    def initUI(self):
        '''
        |--------------|------------|
        |              |            |
        |              |            |
        |task list1    | log display|
        |task list1    |            |
        |task list1    |            |
        |task list1    |            |
        |------------- |------------|
        |          button           |
        |---------------------------|
        :return:
        '''

        self.setWindowIconText("获取数据任务列表")
        self.setObjectName("data_maintenance")
        QtCore.QMetaObject.connectSlotsByName(self)

        # 下面将print 系统输出重定向到textEdit中
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)



        self.gridLayut = QGridLayout()
        self.taskListLayout = QVBoxLayout()
        self.logListLayout = QVBoxLayout()
        self.buttonListLayout = QHBoxLayout()

        self.gridLayut.addLayout(self.taskListLayout, 0,0)
        self.gridLayut.addLayout(self.logListLayout , 0,1)

        '''
        void QGridLayout::addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())
        This is an overloaded function.
        This version adds the layout layout to the cell grid, spanning multiple rows/columns. 
        The cell will start at row, column spanning rowSpan rows and columnSpan columns.
        If rowSpan and/or columnSpan is -1, then the layout will extend to the bottom and/or right edge, respectively.
        '''
        self.gridLayut.addLayout(self.buttonListLayout, 1,0,1,2)


        #🛠todo QT 报错 QWidget::setLayout: Attempting to set QLayout "" on QWidget "", which already has a layout
        self.setLayout(self.gridLayut)

        self.qCheckboxWidgetList = []
        self.qProgressWidgetList = []
        self.allSubJobList = []


        ##################################################################################################
        # 🛠todo 继承QWidget ， 写一个类， 里面有 进度条， checkbox ，和绑定到线程

        self.qCheckBoxJob01_save_stock_day = QCheckBox(self);
        self.qCheckBoxJob01_save_stock_day.setText("save stock_day JOB01 日线数据 ")
        self.qProgressJob01_save_stock_day = QProgressBar(self);
        self.qProgressJob01_save_stock_day.setMaximum(100)

        # 🛠todo  应该有更加好的实现方式， 把progress bar 绑定到 任务对象中，这样写实在是太粗糙了。
        # 把job 对象 绑定到界面中 ， 继承 QCheckBox 把相关到对象线程 和 widget 绑定。
        self.job01_save_stock_day = QA_GUI_DateFetch_SU_job01_stock_day()
        self.job01_save_stock_day.trigger_new_log.connect(self.updateLoggin_job01_save_stock_day)
        self.job01_save_stock_day.trigger_new_progress.connect(self.updateProgress_job01_save_stock_day)
        self.job01_save_stock_day.trigger_start_task_begin.connect(self.updateUi_job_start_job0_save_stock_day)
        self.job01_save_stock_day.trigger_start_task_done.connect(self.updateUi_job_done_job0_save_stock_day)


        # 🛠todo 进一步封装 hardcode 1 2 3 不是一种好的的做法
        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_day)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_day)
        self.allSubJobList.append(self.job01_save_stock_day)

        # 🛠todo 进一步封装 hardcode 1 2 3 不是一种好的的做法
        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_day)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_day)
        ##################################################################################################

        self.qCheckBoxJob01_save_stock_week = QCheckBox(self);
        self.qCheckBoxJob01_save_stock_week.setText("save stock_week JOB01 周线数据 ")
        self.qProgressJob01_save_stock_week = QProgressBar(self)

        self.job01_save_stock_week = QA_GUI_DateFetch_SU_job01_stock_week()
        self.job01_save_stock_week.trigger_new_log.connect(self.updateLoggin_job01_save_stock_week)
        self.job01_save_stock_week.trigger_new_progress.connect(self.updateProgress_job01_save_stock_week)
        self.job01_save_stock_week.trigger_start_task_begin.connect(self.updateUi_job_start_job0_save_stock_week)
        self.job01_save_stock_week.trigger_start_task_done.connect(self.updateUi_job_done_job0_save_stock_week)

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_week)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_week)
        self.allSubJobList.append(self.job01_save_stock_week)


        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_week)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_week)
        ##################################################################################################

        self.qCheckBoxJob01_save_stock_month = QCheckBox(self)
        self.qCheckBoxJob01_save_stock_month.setText("save stock_month JOB01 月线数据 ")
        self.qProgressJob01_save_stock_month = QProgressBar(self)

        self.job01_save_stock_month = QA_GUI_DateFetch_SU_job01_stock_month()
        self.job01_save_stock_month.trigger_new_log.connect(self.updateLoggin_job01_save_stock_month)
        self.job01_save_stock_month.trigger_new_progress.connect(self.updateProgress_job01_save_stock_month)
        self.job01_save_stock_month.trigger_start_task_begin.connect(self.updateUi_job_start_job0_save_stock_month)
        self.job01_save_stock_month.trigger_start_task_done.connect(self.updateUi_job_done_job0_save_stock_month)

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_month)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_month)
        self.allSubJobList.append(self.job01_save_stock_month)


        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_month)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_month)
        ##################################################################################################

        self.qCheckBoxJob01_save_stock_year = QCheckBox(self)
        self.qCheckBoxJob01_save_stock_year.setText("save stock_year JOB01 年线数据 ")
        self.qProgressJob01_save_stock_year = QProgressBar(self)

        self.job01_save_stock_year = QA_GUI_DateFetch_SU_job01_stock_month()
        self.job01_save_stock_year.trigger_new_log.connect(self.updateLoggin_job01_save_stock_year)
        self.job01_save_stock_year.trigger_new_progress.connect(self.updateProgress_job01_save_stock_year)
        self.job01_save_stock_year.trigger_start_task_begin.connect(self.updateUi_job_start_job0_save_stock_year)
        self.job01_save_stock_year.trigger_start_task_done.connect(self.updateUi_job_done_job0_save_stock_year)

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_year)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_year)
        self.allSubJobList.append(self.job01_save_stock_year)


        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_year)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_year)
        ##################################################################################################


        self.selectedSubTask = QA_GUI_Selected_TaskQueue()
        self.selectedSubTask.trigger_all_task_start.connect(self.uiAllTaskStart)
        self.selectedSubTask.trigger_all_task_done.connect(self.uiAllTaskDone)

        ##################################################################################################
        # 🛠todo 日志显示，用table list 加入搜索的功能， 行号等， 彩色显示
        self.logDisplay = QTextEdit(self)
        self.logDisplay.setObjectName("textEdit")
        #self.logDisplay.setEnabled(False)
        self.logDisplay.setReadOnly(True)
        self.logDisplay.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.logListLayout.addWidget(self.logDisplay)

        self.bntExecute = QPushButton(self)
        self.bntExecute.setText("执行选中的任务 🐌")
        self.buttonListLayout.addWidget(self.bntExecute)

        # 🛠todo 没有实现！
        self.bntStopTack = QPushButton(self)
        self.bntStopTack.setText("停止执行任务 🚫")
        self.buttonListLayout.addWidget(self.bntStopTack)


        self.bntClearLog = QPushButton(self)
        self.bntClearLog.setText("清除日志 🗑")
        self.buttonListLayout.addWidget(self.bntClearLog)


        self.bntExecute.clicked.connect(self.doSelectedTask)

        self.bntStopTack.clicked.connect(self.doStopTask)

        # layout = QFormLayout()
        # layout.setLabelAlignment(Qt.AlignLeft)
        # layout.addRow("保存日线数据 ", QProgressBar(self))
        # layout.addRow("保存日除权出息数据 ", QProgressBar(self))
        # layout.addRow("保存分钟线数据", QProgressBar(self))
        # layout.addRow("保存指数数据", QProgressBar(self))
        #
        # layout.addRow("保存指数线数据 ", QProgressBar(self))
        # layout.addRow("保存ETF日线数据 ", QProgressBar(self))
        # layout.addRow("保存ET分钟数据", QProgressBar(self))
        # layout.addRow("保存股票列表", QProgressBar(self))
        # layout.addRow("保存板块", QProgressBar(self))
        # layout.addRow("保存tushare数据接口获取的股票列表", QProgressBar(self))
        # layout.addRow("保存高级财务数据(自1996年开始)", QProgressBar(self))
        # layout.addRow("保存50ETF期权日线数据（不包括已经摘牌的数据）", QProgressBar(self))
        #
        # qPushBnt = QPushButton(self);
        # qPushBnt.setText("开始执行")
        # layout.addRow("选中需要执行的任务", qPushBnt)

        # 为这个tab命名显示出来，第一个参数是哪个标签，第二个参数是标签的名字
        # 在标签1中添加这个帧布局


    # 接收信号str的信号槽
    def outputWritten(self, text):
        cursor = self.logDisplay.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logDisplay.setTextCursor(cursor)
        self.logDisplay.ensureCursorVisible()


    def doSelectedTask(self):
        #print("^ 准备执行选中的任务 ^")

        self.selectedSubTask.clearTask()

        # 🛠todo 需要一个总的线程队列按顺序执行 每个任务
        for itaskIndex in range(len(self.qCheckboxWidgetList)):
            if self.qCheckboxWidgetList[itaskIndex].isChecked():
                self.selectedSubTask.putTask(self.allSubJobList[itaskIndex])


        if len(self.selectedSubTask.QA_GUI_Task_List) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("至少选中一个需要执行的任务！😹")
            msg.setInformativeText("至少选中一个需要执行的任务")
            msg.setWindowTitle("提示：")
            msg.setDetailedText("操作提示: 请选勾选中需要执行的任务")
            retval = msg.exec_()
            return


        #if self.qCheckBoxJob01_save_stock_day.isChecked():
        #    self.job01_save_stock_day.start()
        self.selectedSubTask.start()

        pass

    def doStopTask(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("耐心是一种美德， 耐心等等结束哈！😹  ")
        msg.setInformativeText("耐心是一种美德， 耐心等等结束哈😹 ")
        msg.setWindowTitle("提示：")
        msg.setDetailedText("操作提示: 其实是懒，不高兴去停止线程，怕有副作用，把数据库给搞坏了")
        retval = msg.exec_()



    ##################################################################################################
    # 🛠todo 进一步封装 hardcode 1 2 3 不是一种好的的做法
    def updateUi_job_start_job0_save_stock_day(self, info_str):

        palette = self.qCheckBoxJob01_save_stock_day.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.red)
        self.qCheckBoxJob01_save_stock_day.setPalette(palette)

        pass

    def updateUi_job_done_job0_save_stock_day(self, info_str):
        #
        palette = self.qCheckBoxJob01_save_stock_day.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.black)
        self.qCheckBoxJob01_save_stock_day.setPalette(palette)

        #self.qProgressJob01_save_stock_day.setValue(0)
        pass


    def updateLoggin_job01_save_stock_day(self, log):
        #print("append task log emite triggered!", log);
        self.logDisplay.append(log)

    def updateProgress_job01_save_stock_day(self, progress):
        #print('update task progress ', progress);
        self.qProgressJob01_save_stock_day.setValue(progress)

    ##################################################################################################

    def updateUi_job_start_job0_save_stock_week(self, info_str):

        palette = self.qCheckBoxJob01_save_stock_week.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.red)
        self.qCheckBoxJob01_save_stock_week.setPalette(palette)


        pass

    def updateUi_job_done_job0_save_stock_week(self, info_str):
        #
        palette = self.qCheckBoxJob01_save_stock_week.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.black)
        self.qCheckBoxJob01_save_stock_week.setPalette(palette)

        #self.qProgressJob01_save_stock_day.setValue(0)
        pass


    def updateLoggin_job01_save_stock_week(self, log):
        #print("append task log emite triggered!", log);
        self.logDisplay.append(log)

    def updateProgress_job01_save_stock_week(self, progress):
        #print('update task progress ', progress);
        self.qProgressJob01_save_stock_week.setValue(progress)

    ##################################################################################################

    def updateUi_job_start_job0_save_stock_month(self, info_str):

        palette = self.qCheckBoxJob01_save_stock_month.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.red)
        self.qCheckBoxJob01_save_stock_month.setPalette(palette)

        pass

    def updateUi_job_done_job0_save_stock_month(self, info_str):
        #
        palette = self.qCheckBoxJob01_save_stock_month.palette()
        palette.setColor(QPalette.Active,QPalette.WindowText, QtCore.Qt.black)
        self.qCheckBoxJob01_save_stock_month.setPalette(palette)

        #self.qProgressJob01_save_stock_day.setValue(0)
        pass


    def updateLoggin_job01_save_stock_month(self, log):
        #print("append task log emite triggered!", log);
        self.logDisplay.append(log)

    def updateProgress_job01_save_stock_month(self, progress):
        #print('update task progress ', progress);
        self.qProgressJob01_save_stock_month.setValue(progress)

    ##################################################################################################

    def updateUi_job_start_job0_save_stock_year(self, info_str):

        palette = self.qCheckBoxJob01_save_stock_year.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, QtCore.Qt.red)
        self.qCheckBoxJob01_save_stock_year.setPalette(palette)

        pass

    def updateUi_job_done_job0_save_stock_year(self, info_str):
        #
        palette = self.qCheckBoxJob01_save_stock_year.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, QtCore.Qt.black)
        self.qCheckBoxJob01_save_stock_year.setPalette(palette)

        # self.qProgressJob01_save_stock_day.setValue(0)
        pass

    def updateLoggin_job01_save_stock_year(self, log):
        # print("append task log emite triggered!", log);
        self.logDisplay.append(log)

    def updateProgress_job01_save_stock_year(self, progress):
        # print('update task progress ', progress);
        self.qProgressJob01_save_stock_year.setValue(progress)

    ##################################################################################################

    def uiAllTaskStart(self, logInfo):
        self.bntExecute.setEnabled(False)
        pass

    def uiAllTaskDone(self, logInfo):
        self.bntExecute.setEnabled(True)
        pass