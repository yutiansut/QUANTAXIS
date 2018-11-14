
from PyQt5.Qt import QLabel
from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import math

from typing import List

import numpy as np


class CanvasStockInfo:
    def __init__(self):
        self.myCanvasStockInfo = QImage()
        self.height = 80

    def setDrawImageSize(self,rect:QRect):
        self.myCanvasStockInfo = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasStockInfo.fill(QColor.fromRgb(0, 0, 0, 0))

        self.parentWidth = self.myCanvasStockInfo.width()
        self.parentHeight = self.myCanvasStockInfo.height()
        pass

    def clearImage(self):
        painter = QPainter(self.myCanvasStockInfo)

        h = self.myCanvasStockInfo.height()
        w = self.myCanvasStockInfo.width()
        painter.fillRect(0,0,w,h, QColor.fromRgb(0,0,0,0))

        self.myCanvasStockInfo.fill(QColor.fromRgb(0, 0, 0, 0))

    strName = None
    strCode = None


    strCurrentDate = ""
    strCurrentPrice = ""
    def setCodeAndName(self, strName: str, strCode: str):
        self.strName = strName
        self.strCode = strCode
        pass

    def setMouseMoveDate(self, strCurrentDate :str):
        self.strCurrentDate = strCurrentDate
        pass


    def setMouseMovePrice(self, oclh: List[float]):
        self.oclh = oclh
        pass

    def setMousePositionInfo(self, xpos: float, ypos: float):
        self.xpos = xpos
        self.ypos = ypos

    def draw(self):
        self.myCanvasStockInfo.fill(QColor.fromRgb(0, 0, 0, 0))

        h = self.myCanvasStockInfo.height()
        w = self.myCanvasStockInfo.width()
        painter = QPainter(self.myCanvasStockInfo)

        painter.fillRect(0, 0, w, h, QColor.fromRgb(200, 200, 199, 255))

        if self.strName is not None and self.strCode is not None:
            pq = QPoint(0,10)
            str = "%s %s"%(self.strName, self.strCode)
            painter.drawText(pq, str)

        if self.strCurrentDate is not None:
            pq = QPoint(100, 10)
            str = "%s %s" % (self.strCurrentPrice, self.strCurrentDate)
            painter.drawText(pq, str)

        if self.oclh is not None:
            pq = QPoint(200,10)
            str = "开盘价%0.2f 收盘价%0.2f 最低价%0.2f 最高价%0.2f" % (self.oclh[0], self.oclh[1], self.oclh[2], self.oclh[3])
            painter.drawText(pq, str)

        if self.xpos is not None and self.ypos is not None:
            pq = QPoint(200, 200)
            str = "%f, %f" % (self.xpos , self.ypos)
            painter.drawText(pq, str)

        pass