import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from QUANTAXIS_Monitor_GUI.MainWindow.QA_Gui_DateFetch_Task import *

#https://www.cnblogs.com/gaigaige/p/7883713.html 改改哥
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

        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)


        # 🛠todo 日志显示，用table view list 加入搜索的功能， 行号等， 彩色显示,
        self.logDisplay = QTableWidget(self)

        self.logDisplay.setObjectName("tableForLog")
        # self.logDisplay.setEnabled(False)
        #self.logDisplay.set(True)
        #self.logDisplay.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.logDisplay.setColumnCount(2);
        self.logDisplay.setHorizontalHeaderLabels(['日志内容','来源'])
        self.logDisplay.setColumnWidth(0,700)
        self.logDisplay.setColumnWidth(1,100)


        #https://stackoverflow.com/questions/47910192/pyqt-qgridlayout-different-column-width
        self.gridLayut = QGridLayout()
        self.taskListLayout = QVBoxLayout()
        self.logListLayout = QVBoxLayout()
        self.buttonListLayout = QHBoxLayout()

        self.gridLayut.addLayout(self.taskListLayout, 0,0, 1,1)
        self.gridLayut.addLayout(self.logListLayout , 0,1, 1,1)

        self.gridLayut.setColumnMinimumWidth(1,1400)
        '''
        void QGridLayout::addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())
        This is an overloaded function.
        This version adds the layout layout to the cell grid, spanning multiple rows/columns. 
        The cell will start at row, column spanning rowSpan rows and columnSpan columns.
        If rowSpan and/or columnSpan is -1, then the layout will extend to the bottom and/or right edge, respectively.
        '''
        self.gridLayut.addLayout(self.buttonListLayout, 1,0,1,3)


        #🛠todo QT 报错 QWidget::setLayout: Attempting to set QLayout "" on QWidget "", which already has a layout
        self.setLayout(self.gridLayut)

        self.qCheckboxWidgetList = []
        self.qProgressWidgetList = []
        self.allSubJobList = []

        # 🛠todo this is really stupid 01 02 03 04,... should use template ? does python have some template feature like c++
        ##################################################################################################
        self.create_job_01_save_stock_day()
        ##################################################################################################
        #self.create_job01_save_stock_week()
        ##################################################################################################
        #self.create_job01_save_stock_month()
        ##################################################################################################
        #self.create_job_01_save_stock_year()
        ##################################################################################################
        self.create_job_02_save_stock_xdxr()
        ##################################################################################################
        self.create_job_03_save_stock_min()
        ##################################################################################################
        self.create_job_04_save_index_day()
        ##################################################################################################
        self.create_job_05_save_index_min()
        ##################################################################################################
        self.create_job_06_save_etf_day()
        ##################################################################################################
        self.create_job_07_save_etf_min()
        ##################################################################################################
        self.create_job_08_save_stock_list()
        ##################################################################################################
        self.create_job_09_save_stock_block()
        ##################################################################################################
        self.create_job_10_save_stock_info()
        ##################################################################################################
        #self.create_job_11_save_stock_transaction()
        ##################################################################################################
        self.create_job_12_save_option_day()
        ##################################################################################################

        self.selectedSubTask = QA_GUI_Selected_TaskQueue(self.logDisplay)
        self.selectedSubTask.trigger_all_task_start.connect(self.uiAllTaskStart)
        self.selectedSubTask.trigger_all_task_done.connect(self.uiAllTaskDone)

        ##################################################################################################

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

    def outputWritten(self, text):
        # 🛠todo logDisplay QTableWidget
        #cursor = self.logDisplay.textCursor()
        # cursor.movePosition(QtGui.QTextCursor.End)
        # cursor.insertText(text)
        # self.logDisplay.setTextCursor(cursor)
        # self.logDisplay.ensureCursorVisible()
        if text and text.strip():
            rowCount = self.logDisplay.rowCount()
            newItem1 = QTableWidgetItem(text)
            newItem2 = QTableWidgetItem("stdout/stderr")

            self.logDisplay.setRowCount(rowCount+1)
            self.logDisplay.setItem(rowCount,0,newItem1)
            self.logDisplay.setItem(rowCount,1,newItem2)
            self.logDisplay.scrollToBottom()

    ##################################################################################################

    def create_job_01_save_stock_day(self):
        # 🛠todo 继承QWidget ， 写一个类， 里面有 进度条， checkbox ，和绑定到线程
        self.qCheckBoxJob01_save_stock_day = QCheckBox(self);
        self.qCheckBoxJob01_save_stock_day.setText("JOB01 日线数据 📊")
        self.qProgressJob01_save_stock_day = QProgressBar(self);
        self.qProgressJob01_save_stock_day.setMaximum(100)
        # 🛠todo  应该有更加好的实现方式， 把progress bar 绑定到 任务对象中，这样写实在是太粗糙了。
        # 把job 对象 绑定到界面中 ， 继承 QCheckBox 把相关到对象线程 和 widget 绑定。
        self.job01_save_stock_day = QA_GUI_DateFetch_SU_job01_stock_day()

        self.job01_save_stock_day.setLoggingUIWidget(self.logDisplay)
        self.job01_save_stock_day.setProgressUIWidget(self.qProgressJob01_save_stock_day)
        self.job01_save_stock_day.setCheckboxUIWidget(self.qCheckBoxJob01_save_stock_day)

        self.job01_save_stock_day.connectSignalSlot();

        # 🛠todo 进一步封装 hardcode 1 2 3 不是一种好的的做法
        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_day)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_day)
        self.allSubJobList.append(self.job01_save_stock_day)
        # 🛠todo 进一步封装 hardcode 1 2 3 不是一种好的的做法
        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_day)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_day)

    ##################################################################################################
    def create_job01_save_stock_week(self):
        self.qCheckBoxJob01_save_stock_week = QCheckBox(self);
        self.qCheckBoxJob01_save_stock_week.setText("JOB01 周线数据 📊")
        self.qProgressJob01_save_stock_week = QProgressBar(self)
        self.qProgressJob01_save_stock_week.setMaximum(100)

        # 🛠todo 不知道为何，QThread 继承的 都不执行 __init__
        self.job01_save_stock_week = QA_GUI_DateFetch_SU_job01_stock_week()

        self.job01_save_stock_week.setLoggingUIWidget(self.logDisplay)
        self.job01_save_stock_week.setProgressUIWidget(self.qProgressJob01_save_stock_week)
        self.job01_save_stock_week.setCheckboxUIWidget(self.qCheckBoxJob01_save_stock_week)

        self.job01_save_stock_week.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_week)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_week)
        self.allSubJobList.append(self.job01_save_stock_week)
        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_week)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_week)

    ##################################################################################################
    def create_job01_save_stock_month(self):

        self.qCheckBoxJob01_save_stock_month = QCheckBox(self)
        self.qCheckBoxJob01_save_stock_month.setText("JOB01 月线数据 📊")
        self.qProgressJob01_save_stock_month = QProgressBar(self)
        self.qProgressJob01_save_stock_month.setMaximum(100)

        self.job01_save_stock_month = QA_GUI_DateFetch_SU_job01_stock_month()

        self.job01_save_stock_month.setLoggingUIWidget(self.logDisplay)
        self.job01_save_stock_month.setProgressUIWidget(self.qProgressJob01_save_stock_month)
        self.job01_save_stock_month.setCheckboxUIWidget(self.qCheckBoxJob01_save_stock_month)

        self.job01_save_stock_month.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_month)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_month)
        self.allSubJobList.append(self.job01_save_stock_month)
        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_month)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_month)

    ##################################################################################################
    def create_job_01_save_stock_year(self):
        self.qCheckBoxJob01_save_stock_year = QCheckBox(self)
        self.qCheckBoxJob01_save_stock_year.setText("JOB01 年线数据 📊")
        self.qProgressJob01_save_stock_year = QProgressBar(self)
        self.qProgressJob01_save_stock_year.setMaximum(100)

        self.job01_save_stock_year = QA_GUI_DateFetch_SU_job01_stock_year()

        self.job01_save_stock_year.setLoggingUIWidget(self.logDisplay)
        self.job01_save_stock_year.setProgressUIWidget(self.qProgressJob01_save_stock_year)
        self.job01_save_stock_year.setCheckboxUIWidget(self.qCheckBoxJob01_save_stock_year)

        self.job01_save_stock_year.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob01_save_stock_year)
        self.qProgressWidgetList.append(self.qProgressJob01_save_stock_year)
        self.allSubJobList.append(self.job01_save_stock_year)
        self.taskListLayout.addWidget(self.qCheckBoxJob01_save_stock_year)
        self.taskListLayout.addWidget(self.qProgressJob01_save_stock_year)

    ##################################################################################################
    def create_job_02_save_stock_xdxr(self):
        self.qCheckBoxJob02_save_stock_xdxr = QCheckBox(self)
        self.qCheckBoxJob02_save_stock_xdxr.setText("JOB02 除权除息数据 📊")
        self.qProgressJob02_save_stock_xdxr = QProgressBar(self)
        self.qProgressJob02_save_stock_xdxr.setMaximum(100)

        self.job02_save_stock_xdxr = QA_GUI_DateFetch_SU_job02_stock_xdxr()

        self.job02_save_stock_xdxr.setLoggingUIWidget(self.logDisplay)
        self.job02_save_stock_xdxr.setProgressUIWidget(self.qProgressJob02_save_stock_xdxr)
        self.job02_save_stock_xdxr.setCheckboxUIWidget(self.qCheckBoxJob02_save_stock_xdxr)

        self.job02_save_stock_xdxr.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob02_save_stock_xdxr)
        self.qProgressWidgetList.append(self.qProgressJob02_save_stock_xdxr)
        self.allSubJobList.append(self.job02_save_stock_xdxr)
        self.taskListLayout.addWidget(self.qCheckBoxJob02_save_stock_xdxr)
        self.taskListLayout.addWidget(self.qProgressJob02_save_stock_xdxr)

    ##################################################################################################

    def create_job_03_save_stock_min(self):
        self.qCheckBoxJob03_save_stock_min = QCheckBox(self)
        self.qCheckBoxJob03_save_stock_min.setText("JOB03 分钟数据 📊")
        self.qProgressJob03_save_stock_min = QProgressBar(self)
        self.qProgressJob03_save_stock_min.setMaximum(10000) # 最小变动单位 0.01

        self.job03_save_stock_min = QA_GUI_DateFetch_SU_job03_stock_min()

        self.job03_save_stock_min.setLoggingUIWidget(self.logDisplay)
        self.job03_save_stock_min.setProgressUIWidget(self.qProgressJob03_save_stock_min)
        self.job03_save_stock_min.setCheckboxUIWidget(self.qCheckBoxJob03_save_stock_min)

        self.job03_save_stock_min.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob03_save_stock_min)
        self.qProgressWidgetList.append(self.qProgressJob03_save_stock_min)
        self.allSubJobList.append(self.job03_save_stock_min)
        self.taskListLayout.addWidget(self.qCheckBoxJob03_save_stock_min)
        self.taskListLayout.addWidget(self.qProgressJob03_save_stock_min)

    ##################################################################################################

    def create_job_04_save_index_day(self):
        self.qCheckBoxJob04_save_index_day = QCheckBox(self)
        self.qCheckBoxJob04_save_index_day.setText("JOB04 指数日线数据 📊")
        self.qProgressJob04_save_index_day = QProgressBar(self)
        self.qProgressJob04_save_index_day.setMaximum(10000)  # 最小变动单位 0.01

        self.job04_save_index_day = QA_GUI_DateFetch_SU_job04_index_day()

        self.job04_save_index_day.setLoggingUIWidget(self.logDisplay)
        self.job04_save_index_day.setProgressUIWidget(self.qProgressJob04_save_index_day)
        self.job04_save_index_day.setCheckboxUIWidget(self.qCheckBoxJob04_save_index_day)

        self.job04_save_index_day.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob04_save_index_day)
        self.qProgressWidgetList.append(self.qProgressJob04_save_index_day)
        self.allSubJobList.append(self.job04_save_index_day)
        self.taskListLayout.addWidget(self.qCheckBoxJob04_save_index_day)
        self.taskListLayout.addWidget(self.qProgressJob04_save_index_day)

    ##################################################################################################

    def create_job_05_save_index_min(self):
        self.qCheckBoxJob05_save_index_min = QCheckBox(self)
        self.qCheckBoxJob05_save_index_min.setText("JOB05 指数分钟数据 📊")
        self.qProgressJob05_save_index_min = QProgressBar(self)
        self.qProgressJob05_save_index_min.setMaximum(10000)  # 最小变动单位 0.01

        self.job05_save_index_min = QA_GUI_DateFetch_SU_job05_index_min()

        self.job05_save_index_min.setLoggingUIWidget(self.logDisplay)
        self.job05_save_index_min.setProgressUIWidget(self.qProgressJob05_save_index_min)
        self.job05_save_index_min.setCheckboxUIWidget(self.qCheckBoxJob05_save_index_min)

        self.job05_save_index_min.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob05_save_index_min)
        self.qProgressWidgetList.append(self.qProgressJob05_save_index_min)
        self.allSubJobList.append(self.job05_save_index_min)
        self.taskListLayout.addWidget(self.qCheckBoxJob05_save_index_min)
        self.taskListLayout.addWidget(self.qProgressJob05_save_index_min)

    ##################################################################################################

    def create_job_06_save_etf_day(self):
        self.qCheckBoxJob06_save_etf_day = QCheckBox(self)
        self.qCheckBoxJob06_save_etf_day.setText("JOB06 ETF日线数据 📊")
        self.qProgressJob06_save_etf_day = QProgressBar(self)
        self.qProgressJob06_save_etf_day.setMaximum(10000)  # 最小变动单位 0.01

        self.job06_save_etf_day = QA_GUI_DateFetch_SU_job06_etf_day()

        self.job06_save_etf_day.setLoggingUIWidget(self.logDisplay)
        self.job06_save_etf_day.setProgressUIWidget(self.qProgressJob06_save_etf_day)
        self.job06_save_etf_day.setCheckboxUIWidget(self.qCheckBoxJob06_save_etf_day)

        self.job06_save_etf_day.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob06_save_etf_day)
        self.qProgressWidgetList.append(self.qProgressJob06_save_etf_day)
        self.allSubJobList.append(self.job06_save_etf_day)
        self.taskListLayout.addWidget(self.qCheckBoxJob06_save_etf_day)
        self.taskListLayout.addWidget(self.qProgressJob06_save_etf_day)

    ##################################################################################################

    def create_job_07_save_etf_min(self):
        self.qCheckBoxJob07_save_etf_min = QCheckBox(self)
        self.qCheckBoxJob07_save_etf_min.setText("JOB07 ETF分钟数据 📊")
        self.qProgressJob07_save_etf_min = QProgressBar(self)
        self.qProgressJob07_save_etf_min.setMaximum(10000)  # 最小变动单位 0.01

        self.job07_save_etf_min = QA_GUI_DateFetch_SU_job07_etf_min()

        self.job07_save_etf_min.setLoggingUIWidget(self.logDisplay)
        self.job07_save_etf_min.setProgressUIWidget(self.qProgressJob07_save_etf_min)
        self.job07_save_etf_min.setCheckboxUIWidget(self.qCheckBoxJob07_save_etf_min)

        self.job07_save_etf_min.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob07_save_etf_min)
        self.qProgressWidgetList.append(self.qProgressJob07_save_etf_min)
        self.allSubJobList.append(self.job07_save_etf_min)
        self.taskListLayout.addWidget(self.qCheckBoxJob07_save_etf_min)
        self.taskListLayout.addWidget(self.qProgressJob07_save_etf_min)

    ##################################################################################################

    def create_job_08_save_stock_list(self):
        self.qCheckBoxJob08_save_stock_list = QCheckBox(self)
        self.qCheckBoxJob08_save_stock_list.setText("JOB08 股票列表 📊")
        self.qProgressJob08_save_stock_list = QProgressBar(self)
        self.qProgressJob08_save_stock_list.setMaximum(10000)  # 最小变动单位 0.01

        self.job08_save_stock_list = QA_GUI_DateFetch_SU_job08_stock_list()

        self.job08_save_stock_list.setLoggingUIWidget(self.logDisplay)
        self.job08_save_stock_list.setProgressUIWidget(self.qProgressJob08_save_stock_list)
        self.job08_save_stock_list.setCheckboxUIWidget(self.qCheckBoxJob08_save_stock_list)

        self.job08_save_stock_list.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob08_save_stock_list)
        self.qProgressWidgetList.append(self.qProgressJob08_save_stock_list)
        self.allSubJobList.append(self.job08_save_stock_list)
        self.taskListLayout.addWidget(self.qCheckBoxJob08_save_stock_list)
        self.taskListLayout.addWidget(self.qProgressJob08_save_stock_list)

    ##################################################################################################

    def create_job_09_save_stock_block(self):
        self.qCheckBoxJob09_save_stock_block = QCheckBox(self)
        self.qCheckBoxJob09_save_stock_block.setText("JOB08 股票板块数据 📊")
        self.qProgressJob09_save_stock_block = QProgressBar(self)
        self.qProgressJob09_save_stock_block.setMaximum(10000)  # 最小变动单位 0.01

        self.job09_save_stock_block = QA_GUI_DateFetch_SU_job09_stock_block()

        self.job09_save_stock_block.setLoggingUIWidget(self.logDisplay)
        self.job09_save_stock_block.setProgressUIWidget(self.qProgressJob09_save_stock_block)
        self.job09_save_stock_block.setCheckboxUIWidget(self.qCheckBoxJob09_save_stock_block)

        self.job09_save_stock_block.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob09_save_stock_block)
        self.qProgressWidgetList.append(self.qProgressJob09_save_stock_block)
        self.allSubJobList.append(self.job09_save_stock_block)
        self.taskListLayout.addWidget(self.qCheckBoxJob09_save_stock_block)
        self.taskListLayout.addWidget(self.qProgressJob09_save_stock_block)

    ##################################################################################################
    def create_job_10_save_stock_info(self):
        self.qCheckBoxJob10_save_stock_info = QCheckBox(self)
        self.qCheckBoxJob10_save_stock_info.setText("JOB10 股票基本数据 📊")
        self.qProgressJob10_save_stock_info = QProgressBar(self)
        self.qProgressJob10_save_stock_info.setMaximum(10000)  # 最小变动单位 0.01

        self.job10_save_stock_info = QA_GUI_DateFetch_SU_job10_stock_info()

        self.job10_save_stock_info.setLoggingUIWidget(self.logDisplay)
        self.job10_save_stock_info.setProgressUIWidget(self.qProgressJob10_save_stock_info)
        self.job10_save_stock_info.setCheckboxUIWidget(self.qCheckBoxJob10_save_stock_info)

        self.job10_save_stock_info.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob10_save_stock_info)
        self.qProgressWidgetList.append(self.qProgressJob10_save_stock_info)
        self.allSubJobList.append(self.job10_save_stock_info)
        self.taskListLayout.addWidget(self.qCheckBoxJob10_save_stock_info)
        self.taskListLayout.addWidget(self.qProgressJob10_save_stock_info)

    def create_job_11_save_stock_transaction(self):

        self.qCheckBoxJob11_save_stock_transaction = QCheckBox(self)
        self.qCheckBoxJob11_save_stock_transaction.setText("JOB11 股票3秒的tick数据 📊")
        self.qProgressJob11_save_stock_transaction = QProgressBar(self)
        self.qProgressJob11_save_stock_transaction.setMaximum(10000)  # 最小变动单位 0.01

        self.job11_save_stock_transaction = QA_GUI_DateFetch_SU_job11_stock_transaction()

        self.job11_save_stock_transaction.setLoggingUIWidget(self.logDisplay)
        self.job11_save_stock_transaction.setProgressUIWidget(self.qProgressJob11_save_stock_transaction)
        self.job11_save_stock_transaction.setCheckboxUIWidget(self.qCheckBoxJob11_save_stock_transaction)

        self.job11_save_stock_transaction.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob11_save_stock_transaction)
        self.qProgressWidgetList.append(self.qProgressJob11_save_stock_transaction)
        self.allSubJobList.append(self.job11_save_stock_transaction)
        self.taskListLayout.addWidget(self.qCheckBoxJob11_save_stock_transaction)
        self.taskListLayout.addWidget(self.qProgressJob11_save_stock_transaction)

    def create_job_12_save_option_day(self):

        self.qCheckBoxJob12_save_option_day = QCheckBox(self)
        self.qCheckBoxJob12_save_option_day.setText("JOB12 50ETF期权日线数据 📊")
        self.qProgressJob12_save_option_day = QProgressBar(self)
        self.qProgressJob12_save_option_day.setMaximum(10000)  # 最小变动单位 0.01

        self.job12_save_option_day = QA_GUI_DateFetch_SU_job12_option_day()

        self.job12_save_option_day.setLoggingUIWidget(self.logDisplay)
        self.job12_save_option_day.setProgressUIWidget(self.qProgressJob12_save_option_day)
        self.job12_save_option_day.setCheckboxUIWidget(self.qCheckBoxJob12_save_option_day)

        self.job12_save_option_day.connectSignalSlot();

        self.qCheckboxWidgetList.append(self.qCheckBoxJob12_save_option_day)
        self.qProgressWidgetList.append(self.qProgressJob12_save_option_day)
        self.allSubJobList.append(self.job12_save_option_day)
        self.taskListLayout.addWidget(self.qCheckBoxJob12_save_option_day)
        self.taskListLayout.addWidget(self.qProgressJob12_save_option_day)

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


    def uiAllTaskStart(self, logInfo):
        self.bntExecute.setEnabled(False)
        pass

    def uiAllTaskDone(self, logInfo):
        self.bntExecute.setEnabled(True)
        pass