from PyQt5.Qt import QLabel
from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from typing import List

import math
import numpy as np


from QUANTAXIS.QAUtil.QADate import *
from QUANTAXIS.QAUtil.QADate_trade import *

from QUANTAXIS.QAFetch.QAQuery_Advance import *


#from QUANTAXIS_Monitor_GUI.MyQtWidgets.QStockDateRuler import  *


class CanvasLeftPriceRuler:
    def __init__(self):
        self.myCanvasPriceRuler = QImage()

        self.width = 35

        self.minPrice = 8.0
        self.maxPrice = 88.0

        self.parentHeight = 0
        self.parentWidth = 0


        self.defaultPriceGapCount = 50
        self.priceTextWidth = 30

        pass

    def setPriceRange(self, maxP :float , minP :float):
        self.maxPrice = maxP
        self.minPrice = minP


    def setDrawImageSize(self, rect: QRect):

        self.myCanvasPriceRuler = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasPriceRuler.fill(QColor.fromRgb(0, 0, 0, 0))

        self.parentWidth = self.myCanvasPriceRuler.width()
        self.parentHeight = self.myCanvasPriceRuler.height()

    #
    #     pass

    def clearImage(self):
        painter = QPainter(self.myCanvasPriceRuler)
        h = self.myCanvasPriceRuler.height()
        w = self.myCanvasPriceRuler.width()
        painter.fillRect(0, 0, w, h, QColor.fromRgb(0, 0, 0,0))


    def draw(self):

        try:
            self.myCanvasPriceRuler.fill(QColor.fromRgb(0, 0, 0, 0))


            priceRangeGap = int(self.maxPrice - self.minPrice)

            heightGuage = (self.myCanvasPriceRuler.height() / self.defaultPriceGapCount)

            priceGap = priceRangeGap / self.defaultPriceGapCount

            painter = QPainter(self.myCanvasPriceRuler)

            if heightGuage > 0:
                painter.save()

                for i in range(self.defaultPriceGapCount):
                    #painter.fillRect(0, 0, w, h, QColor.fromRgb(255, 255, 255))
                    painter.drawRect(self.priceTextWidth, heightGuage*i, self.width, heightGuage )


                    qp = QPoint(0, heightGuage*i+ heightGuage/2)

                    painter.setFont(QFont('SansSerif', 10))

                    strPrice = "%0.2f"%(self.maxPrice  - priceGap * i)

                    painter.drawText(qp,strPrice)


                painter.restore()


        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)

        pass