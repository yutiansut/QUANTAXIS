# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab0_RootClass import *
#from QUANTAXIS_Monitor_GUI.MyQtWidgets.QStockPriceCanvas import *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.QStockPriceVolumeCanvas import *


from QUANTAXIS.QAFetch.QAQuery_Advance import *
from QUANTAXIS.QAFetch.QAQuery import *

class TabForecastStockTrends(TabRootClass):
    def __init__(self, parent=None):
        super(TabForecastStockTrends, self).__init__(parent)

    def initUI(self):
        '''
            ---------------------------------------------------------——|————————|
            | 周期（）  复权（）坐标类型（） 股票名字  代码  R是否融券标的             |   top
            --------------------------------------------------------——----------|
            |                                                          |        |
            |                                                          |        |
            |                                                          |        |
                    ##                                                 | 筹码分布|   middle
            |          #                                               |        |
                        #                                              |        |
                        ####  k线走势计算  B点 S点                       |        |
            |       操作建议                                            |        |
            |                                                          |        |
            ————————————————————————————————————————————————————————————————————————
            |                                                          |基本财务数据|
            |  成交量                                                   |          |  button
            ———————————————————————————————————————————————————————————|          |
            |  技术指标 macd                                            |          |
            |                                                          |          |
            ——————————————————————————————————————————————————————————————————————


        :return:
        '''

        self.comboCyc = QComboBox(self)
        self.comboFQ = QComboBox(self)
        self.comboCoordType = QComboBox(self)
        self.editCodeName = QLineEdit(self)
        self.lbCodeName = QLabel(self)

        self.bntZoomIn = QPushButton(self)
        self.bntZoomOut = QPushButton(self)

        self.bntMoveLeft = QPushButton(self)
        self.bntMoveRight= QPushButton(self)

        #self.stockpriceChart = QtStockPriceCanvas(self) # k线图

        self.stockpriceChart = QtStockPriceVolumeFrame()
        self.stockpriceChart.setMouseTracking(True) #跟踪鼠标操作
        self.stockpriceChart.setFocusPolicy(Qt.StrongFocus)

        #self.stockChipDistrubuteChart = QWidget(self) # 筹码分布

        #self.volumeChart =
        #self.volumeChart = QStockPriceCanvas(self)


        self.technicalChart = QWidget(self)
        self.financialChart = QWidget(self)

        #

        self.comboCyc.addItem('日线')
        self.comboCyc.addItem('周线')
        self.comboCyc.addItem('月线')
        self.comboCyc.addItem('年线')
        self.comboCyc.addItem('60分钟线')
        self.comboCyc.addItem('30分钟线')
        self.comboCyc.addItem('15分钟线')
        self.comboCyc.addItem('5分钟线')
        self.comboCyc.addItem('1分钟线')

        self.comboFQ.addItem('前复权')
        self.comboFQ.addItem('后复权')
        self.comboFQ.addItem('不复权')

        self.comboCoordType.addItem('对数坐标')
        self.comboCoordType.addItem('算数坐标')

        self.bntMoveRight.setText("➡️")
        self.bntMoveLeft.setText("⬅️️")
        self.bntZoomOut.setText("🔍-")
        self.bntZoomIn.setText("🔎+")

        self.bntMoveLeft.clicked.connect(self.moveLeft)
        self.bntMoveRight.clicked.connect(self.moveRight)

        self.bntZoomOut.clicked.connect(self.zoomOut)
        self.bntZoomIn.clicked.connect(self.zoomIn)
        #self.editCodeName.setText('sh000001')

        # #self.
        self.vboxRootLayout = QVBoxLayout(self)
        self.vBoxTop = QHBoxLayout(self)
        self.vBoxMiddle = QHBoxLayout(self)
        #self.vBoxBottom = QHBoxLayout(self)
        #

        self.setLayout(self.vboxRootLayout)

        self.vboxRootLayout.addLayout(self.vBoxTop)
        self.vboxRootLayout.addLayout(self.vBoxMiddle)
        #self.vboxRootLayout.addLayout(self.vBoxBottom)

        #self.vboxRootLayout.setSizeConstraint()

        self.vboxRootLayout.setSpacing(1)
        self.vboxRootLayout.setContentsMargins(1,1,1,1)
        #
        self.vBoxTop.addWidget(self.comboFQ)
        self.vBoxTop.addWidget(self.comboCyc)

        self.vBoxTop.addWidget(self.comboCoordType)
        self.vBoxTop.addWidget(self.editCodeName)
        self.vBoxTop.addWidget(self.lbCodeName)
        self.vBoxTop.addWidget(self.bntZoomIn)
        self.vBoxTop.addWidget(self.bntZoomOut)
        self.vBoxTop.addWidget(self.bntMoveLeft)
        self.vBoxTop.addWidget(self.bntMoveRight)

        self.vBoxTop.setSpacing(1)
        self.vBoxTop.setContentsMargins(1,1,1,1)

        #

        self.vBoxMiddle.addWidget(self.stockpriceChart)

        self.vBoxMiddle.setSpacing(1)
        self.vBoxMiddle.setContentsMargins(1,1,1,1)


        #self.vBoxBottom.addWidget(self.volumeChart)

        #rect = QRect(0,0,300,300)
        #self.vBoxBottom.setGeometry(rect)

        #self.volumeChart.setMinimumHeight(100)
        #self.volumeChart.setMaximumHeight(100)

        #self.vboxRootLayout.

        #self.editCodeName.editingFinished.connect(self.code_editingFinished)
        self.editCodeName.setPlaceholderText("输入股票代 sz000001 按回车加载图表")
        self.editCodeName.returnPressed.connect(self.code_returnPressed)

        pass





    def showEvent(self, a0: QtGui.QShowEvent):

        self.stockpriceChart.clearAllImage()
        self.stockpriceChart.drawCoordinate()
        self.stockpriceChart.setFocus()

        pass

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.stockpriceChart.clearAllImage()
        self.stockpriceChart.drawCoordinate()
        self.stockpriceChart.setFocus()

        pass


    def moveLeft(self):
        self.stockpriceChart.moveLeftChart()


    def moveRight(self):

        self.stockpriceChart.moveRightChart()

    def zoomIn(self):
        self.stockpriceChart.zoomIn()
        self.code_returnPressed()


    def zoomOut(self):
        self.stockpriceChart.zoomOut()
        self.code_returnPressed()

    def code_returnPressed(self):

        try:

            txtInputed = self.editCodeName.text()
            print("code return pressed %s"%txtInputed)

            #look up the stock code
            strName = QA_fetch_stock_name(txtInputed)

            if strName is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("输入的股票代码无效！😹")
                msg.setInformativeText("请输入股票代码")
                msg.setWindowTitle("提示：")
                msg.setDetailedText("指数 sz000001 上证指数， 600003")
                retval = msg.exec_()
            else:
                self.lbCodeName.setText(strName)


            self.stockpriceChart.setCode(txtInputed,strName)

            #self.stockpriceChart.update()
            # self.stockpriceChart.repaint()

            self.stockpriceChart.loadCodeData()
            self.stockpriceChart.drawCoordinate()
            self.stockpriceChart.drawKLine()

            #self.stockpriceChart.drawStockInfo()
            self.update()

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)

        #set code
        #stockpriceChart.setFQ()
        #stockpriceChart.setCycle()
        #stockpriceChart.setDateRange()
        pass
