import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QAPalette(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1024, 768)

        #self.setStyleSheet("background:black")
        chart = QWebEngineView(self)
        chart.page().setBackgroundColor(Qt.red)
        #button = QPushButton("Test",self)
        #button.resize(50, 50)
        #self.col = QColor(0, 0, 0)
        chart.resize(self.size())
        chart.setAutoFillBackground(True)



        """
        button.setAutoFillBackground(True)
        pa = QPalette()
        #br = pa.dark()
        pa.setColor(QPalette.Window, Qt.red)
        pa.setColor(QPalette.WindowText, Qt.red)
        button.setPalette(pa)

        button.setAutoFillBackground(True)
"""



        self.center()
        self.show()

    def center(self):  # 主窗口居中显示函数
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)






if __name__=="__main__":
    app = QApplication(sys.argv)
    win = QAPalette()
    sys.exit(app.exec_())