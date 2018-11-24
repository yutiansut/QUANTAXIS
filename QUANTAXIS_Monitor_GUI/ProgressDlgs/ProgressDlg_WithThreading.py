from PyQt5.Qt import QLabel
from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ProgressDlg_WithQThread(QDialog):
    def __init__(self, parent=None, qThreadObj = None, userHint = None, dlgTitle = None):
        super(ProgressDlg_WithQThread, self).__init__(parent)
        self.setModal(True)
        self.qThreadObj = qThreadObj
        self.userHint = userHint


        if dlgTitle is not None:
            self.setWindowTitle(dlgTitle)
        self.initUI()

    def initUI(self):
        #self.setWindowFlags()
        self.label = QLabel(self)
        self.label.setText(self.userHint)

        self.bnt = QPushButton(self)
        self.bnt.setText("确定")
        self.bnt.setMaximumWidth(150)
        self.bnt.clicked.connect(self.Ok)

        self.hLay = QVBoxLayout(self)
        self.hLay.setAlignment(Qt.AlignCenter)
        self.hLay.addWidget(self.label)
        self.hLay.addWidget(self.bnt)
        self.setLayout(self.hLay)
        self.startTimer(200)

    def startMyThread(self):
        self.qThreadObj.strTaskRunningResult = ""
        self.qThreadObj.strTaskRunningLog = ""

        self.qThreadObj.start()

    def timerEvent(self, a0: 'QTimerEvent'):
        boolFinished  = self.qThreadObj.isFinished()
        if boolFinished:
            strTaskRunningResult = self.qThreadObj.strTaskRunningResult
            self.label.setText(strTaskRunningResult)

        else:
            strTaskRunningLog = self.qThreadObj.strTaskRunningLog
            self.label.setText(strTaskRunningLog)

        pass

    def closeEvent(self, event):

        boolFinished = self.qThreadObj.isFinished()
        if boolFinished == True:
            event.accept()
        else:
            QMessageBox.critical(self,"请等待！", ("等待任务完成!"))
            event.ignore()
        pass

    def Ok(self):
        self.close()