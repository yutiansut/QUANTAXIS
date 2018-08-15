# -*- coding: utf-8 -*-

'''
  GUI 实现 QuantAxis 的基本功能
  author： tauruswang
  date： 2018-07-21
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from QUANTAXIS_Monitor_GUI.AppMediator import *


from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab00_WelcomeSplash import *


from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab01_DataMaintenance import *
#from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab02_WebpageCrawly_Old import *
from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab02_WebpageEastMoneyZJLX import *
from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab04_BlockStatistics import *
#from QUANTAXIS_Monitor_GUI.MainWindow.TabForecastStockTrends import *

class TabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)

        self.mediator = Mediator()

        self.tab0 = TabWelcomeSplash(parent=self)
        self.tab1 = TabDataMaintenance(parent=self)


        self.tab2 = TabEastMoneyZJLX(parent=self)
        self.tab2.setMediator(self.mediator)

        self.tab3 = QWidget()
        self.tab4 = TabBlockStatistics(parent=self)
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()

        self.addTab(self.tab0, "欢迎")
        self.addTab(self.tab1, "数据下载")
        self.addTab(self.tab2, "东方财富资金流向（近100天）")
        self.addTab(self.tab3, "数据比对清洗")
        self.addTab(self.tab4, "数据盘后分析任务")
        self.addTab(self.tab5, "策略概率回测")
        self.addTab(self.tab6, "近期上涨下跌股票预测")
        self.addTab(self.tab7, "系统配置信息")

        self.tab0.initUI()
        self.tab1.initUI()
        self.tab2.initUI()

        self.tab4.initUI()


        self.setTabText(0, "    🎉   欢迎                                        ")
        self.setTabText(1, "    🗂   数据维护                                        ")
        self.setTabText(2, "    📑   东方财富资金流向                      ")
        self.setTabText(3, "    🖇   数据比对清洗                                      ")
        self.setTabText(4, "    🔍   数据盘后分析任务                                  ")
        self.setTabText(5, "    🎲   策略概率回测                                    ")
        self.setTabText(6, "    📈   近期上涨下跌股票预测                              ")
        self.setTabText(7, "    🛠   系统配置信息                                    ")


        #self.tab2UI()
        #self.tab3UI()
        #self.tab4UI()
        self.setMinimumHeight(700)
        self.setWindowTitle("QUANTAXIS MONITOR ver.0.0.0.1")
        #self.setMinimumHeight(800)
        #self.setMinimumWidth(1000)
        #调试的方便使用
        #self.showMaximized()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())