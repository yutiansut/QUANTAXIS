from PyQt5.QtGui import *
from PyQt5.QtCore import *

from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockDateRuler import CanvasBottomDateRuler
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockInfo import CanvasStockInfo

class CanvasMouseCursor:

    mouseX = 0.0
    mouseY = 0.0

    xInGrid = 0.0

    def __init__(self):
        self.myCanvasStockInfoMouseMove = QImage()
        pass


    def setDrawImageSize(self,rect:QRect):

        self.myCanvasStockInfoMouseMove = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasStockInfoMouseMove.fill(QColor.fromRgb(0, 0, 0, 0))

        self.parentWidth = self.myCanvasStockInfoMouseMove.width()
        self.parentHeight = self.myCanvasStockInfoMouseMove.height()
        self.parentPosX = 0
        self.parentPoxY = 0

        pass

    def draw(self, canvasDateRule : CanvasBottomDateRuler , canvasStockInfo : CanvasStockInfo):

        try:
            h = self.myCanvasStockInfoMouseMove.height()
            w = self.myCanvasStockInfoMouseMove.width()

            #变成透明，
            self.myCanvasStockInfoMouseMove.fill(QColor.fromRgb(0, 0, 0, 0))

            painter = QPainter(self.myCanvasStockInfoMouseMove)

            painter.fillRect(0, 0, w, h, QColor.fromRgb(0, 0, 0, 0))

            painter.drawLine(self.xInGrid - self.parentPosX, 0, self.xInGrid - self.parentPosX, h)
            painter.drawLine(0, self.mouseY - canvasStockInfo.height, w, self.mouseY - canvasStockInfo.height)


            #canvasDateRule.setMousePositioin()
            #canvasDateRule.drawSelectedDay(self.xInGrid - self.parentPosX)

        except Exception as eee:
            strError = eee.__str__()
            print(strError)


        pass






    def clearImage(self):
        painter = QPainter(self.myCanvasStockInfoMouseMove)
        h = self.myCanvasStockInfoMouseMove.height()
        w = self.myCanvasStockInfoMouseMove.width()
        painter.fillRect(0, 0, w, h, QColor.fromRgb(0, 0, 0, 0))
