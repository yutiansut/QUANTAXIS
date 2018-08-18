
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#http://www.widlabs.com/article/no-module-named-pyqt5-qtwebkitwidgets
#from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from QUANTAXIS_Monitor_GUI.MainTabWindows.Tab0_RootClass import *


class TabWelcomeSplash(TabRootClass):
    def __init__(self, parent=None):
        super(TabWelcomeSplash, self).__init__(parent)


    def initUI(self):
        # self.setWindowOpacity(1)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.showFullScreen()
        rect = QApplication.desktop().screenGeometry()
        self.resize(rect.width(), rect.height())
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.webview = QWebEngineView()

        vbox = QVBoxLayout()
        vbox.addWidget(self.webview)

        main = QGridLayout()
        main.setSpacing(0)
        main.addLayout(vbox, 0, 0)

        self.setLayout(main)

        #dirname, filename = os.path.split(os.path.abspath(__file__))
        # dir = os.getcwd(); #

        realPath = os.path.realpath(__file__)
        realDir = os.path.dirname(realPath);
        realHtml = realDir + "/splash_html_page/splash.html"
        realUrl = "file:///"+ realHtml;

        #self.webview.load(QUrl("file:////Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Monitor_GUI/MainTabWindows/splash_html_page/splash.html"))
        self.webview.load(QUrl(realUrl))

        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.show()
        # self.setWindowTitle("CoDataHD")
        # webview.load(QUrl('http://www.cnblogs.com/misoag/archive/2013/01/09/2853515.html'))
        # webview.show()

