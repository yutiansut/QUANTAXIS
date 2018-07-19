# -*- coding: utf-8 -*-

'''
    【简介】
    PyQt5中 QTabWidget 例子


'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from QUANTAXIS_Monitor_GUI.MainWindow.TabDataMaintenance import *
from QUANTAXIS_Monitor_GUI.MainWindow.TabWebpageCrawly import *

class TabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)

        self.tab1 = TabDataMaintenance()
        self.tab2 = TabWebpageCrawly()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.addTab(self.tab1, "数据下载")
        self.addTab(self.tab2, "网页数据抓取")
        self.addTab(self.tab3, "数据比对清洗")
        self.addTab(self.tab4, "数据盘后分析任务")
        self.addTab(self.tab5, "系统配置信息")


        self.tab1.initUI()
        self.setTabText(0, "    🗂   数据维护                                        ")
        self.setTabText(1, "    📑   网页数据抓取                                      ")
        self.setTabText(2, "    🖇   数据比对清洗                                      ")
        self.setTabText(3, "    🔍   数据盘后分析任务                                    ")
        self.setTabText(4, "    🛠   系统配置信息                                    ")


        #self.tab2UI()
        #self.tab3UI()
        #self.tab4UI()

        self.setWindowTitle("💫 ⭐️ 🌟QUANTAXIS ☕️🍭 任务监控✨ ☀️ 💥    ver.0.0.0.1")
        #self.setMinimumHeight(800)
        #self.setMinimumWidth(1000)
        #调试的方便使用
        #self.showMaximized()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())