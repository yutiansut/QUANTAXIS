import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class TabStrategyBacktraceRunning(QWidget):
    def __init__(self, parent=None):
        super(TabStrategyBacktraceRunning, self).__init__(parent)

    def initUI(self):
        '''
            ---------------------------------------------------------|
            | 策略目录名称    |  回测 停止 报告                          |
            | kdj指标策略1   |-------------------------------——-------|
            | macd策略2      |    * * *        *                      |
            | boll策略       |   *     *      *                       |
            | MA均线策略      |          * * *                         |
            |               |                                         |
            --------------------------------------------------------——
        :return:
        '''
        pass



