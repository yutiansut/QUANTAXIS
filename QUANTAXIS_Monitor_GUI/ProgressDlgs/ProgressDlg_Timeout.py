from PyQt5.Qt import QLabel
from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtGui import QCloseEvent

from abc import ABC, abstractmethod

'''
谨慎使用， 调试的时候会锁死！ 而且 多线程依赖 UI timer 不是很准确！！
移动父窗口 ，会死锁
'''
class ProgressDlg_Timeout(QDialog):
    def __init__(self, parent=None, timeOut = 5, userHint = None):
        #parent not set to, none , 设置成parent 会死锁
        super(ProgressDlg_Timeout, self).__init__(parent)
        self.setModal(True)
        self.timeOut = timeOut
        self.strMsg = userHint
        self.initUI()

    def initUI(self):
        #self.setWindowFlags(Qt.)

        self.label = QLabel(self)
        self.label.setText('{} , 还剩 {} 秒'.format(self.strMsg, self.timeOut))

        self.hLay = QHBoxLayout()
        self.hLay.addWidget(self.label)
        self.setLayout(self.hLay)
        self.startTimer(1000)
        pass

    #todo fixhere 调试的适合， 会锁死， 界面不会倒计时！！！！！
    # 多线程依赖 UI timer 不是很准确！！调试的时候，容易死锁
    def timerEvent(self, a0: 'QTimerEvent'):

        if self.timeOut == 0:
            self.close()
            return

        self.timeOut = self.timeOut - 1
        self.label.setText('{} ，还剩 {} 秒'.format(self.strMsg, self.timeOut))

        pass

    def closeEvent(self, event):
        if self.timeOut == 0:
            event.accept()
        else:
            msg = QMessageBox()
            msg.setText("等待任务完成")
            msg.exec()
            event.ignore()

        pass