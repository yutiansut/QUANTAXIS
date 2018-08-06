
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from abc import ABC, abstractmethod

class TabRootClass(QWidget):
    def __init__(self, parent=None):
        super(TabRootClass, self).__init__(parent)

    @abstractmethod
    def initUI(self):
        pass


    def setMediator(self, mediator):
        self._mediator = mediator

    def getMediator(self):
        return self._mediator