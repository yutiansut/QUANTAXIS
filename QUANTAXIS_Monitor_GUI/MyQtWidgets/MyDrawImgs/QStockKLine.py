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



class CanvasKLines:
    def __init__(self):
        self.myCanvasKLine = QImage()

        mouseX = 0.0
        mouseY = 0.0

        xInGrid = 0.0
        self.showDayInGauges = 100


        pass

    def setDrawImageSize(self, rect: QRect):

        self.myCanvasKLine = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasKLine.fill(QColor.fromRgb(0, 0, 0, 0))

        self.parentHeight = self.myCanvasKLine.height()
        self.parentWidth = self.myCanvasKLine.width()

        pass


    def draw(self):

        try:


            self.myCanvasKLine.fill(QColor.fromRgb(0, 0, 0, 0))

            if self.oclhList is None:
                return

            h = self.myCanvasKLine.height()
            w = self.myCanvasKLine.width()
            painter = QPainter(self.myCanvasKLine)


            priceRange = self.highestPriceInScreen - self.lowestPriceInScreen
            priceGapCount = priceRange *100

            pricePerGapHeight = h / priceGapCount

            kLineDayWidth = w / self.showDayInGauges

            sizeOfLoadTradeDayList = len(self.tradeDayList)

            for iIndexKLine in range(len(self.oclhList)):

                if (sizeOfLoadTradeDayList - self.showDayInGauges) >= 0:


                    aKlineData = self.oclhList[self.showDayInGauges - iIndexKLine - 1]

                elif (sizeOfLoadTradeDayList - iIndexKLine) > 0:

                    aKlineData = self.oclhList[sizeOfLoadTradeDayList - iIndexKLine - 1]


                openprice = aKlineData[0]
                closeprice = aKlineData[1]
                lowprice = aKlineData[2]
                highprice = aKlineData[3]

                # openPriceInScreen = (self.highestPriceInScreen - openprice) *100 *pricePerGapHeight
                # closePriceInScreen = (self.highestPriceInScreen - closeprice) *100 *pricePerGapHeight
                #
                # lowPriceInScreen = (self.highestPriceInScreen- lp) *100 *pricePerGapHeight
                # highpriceInScreen = (self.highestPriceInScreen - hp) *100 *pricePerGapHeight
                #


                # openPriceInScreen = (openprice - self.lowestPriceInScreen ) *100 *pricePerGapHeight
                # closePriceInScreen = (closeprice - self.lowestPriceInScreen) *100 *pricePerGapHeight
                # lowPriceInScreen = (lowprice - self.lowestPriceInScreen) *100 *pricePerGapHeight
                # highpriceInScreen = (highprice - self.lowestPriceInScreen) *100 *pricePerGapHeight

                heightFromMinPriceOpen = (openprice - self.lowestPriceInScreen) * (100) * pricePerGapHeight
                heihgtFromMaxPriceOpen = h - heightFromMinPriceOpen
                openPrice_ScreenCoorY = 0 + heihgtFromMaxPriceOpen

                heightFromMinPriceClose = (closeprice - self.lowestPriceInScreen) * (100) * pricePerGapHeight
                heihgtFromMaxPriceClose = h - heightFromMinPriceClose
                closePrice_ScreenCoorY = 0 + heihgtFromMaxPriceClose

                heightFromMinPriceLow = (lowprice - self.lowestPriceInScreen) * (100) * pricePerGapHeight
                heihgtFromMaxPriceLow = h - heightFromMinPriceLow
                lowPrice_ScreenCoorY = 0  + heihgtFromMaxPriceLow

                heightFromMinPriceHigh = (highprice - self.lowestPriceInScreen) * (100) * pricePerGapHeight
                heihgtFromMaxPriceHigh = h - heightFromMinPriceHigh
                highPrice_ScreenCoorY = 0 + heihgtFromMaxPriceHigh

                #qp = QPoint(iIndexKLine * kLineDayWidth, openPriceInScreen)
                #painter.drawPoint(qp)
                kLineHeight = abs(closePrice_ScreenCoorY - openPrice_ScreenCoorY)

                qline = QLineF(iIndexKLine * kLineDayWidth + kLineDayWidth / 2, lowPrice_ScreenCoorY, \
                                  iIndexKLine * kLineDayWidth + kLineDayWidth / 2, highPrice_ScreenCoorY)
                painter.drawLine(qline)

                if openprice > closeprice:
                    rectKLine = QRectF(iIndexKLine*kLineDayWidth, openPrice_ScreenCoorY, kLineDayWidth, kLineHeight )

                    painter.fillRect(rectKLine, QColor.fromRgb(0,200,0))


                else:
                    rectKLine = QRectF(iIndexKLine*kLineDayWidth, closePrice_ScreenCoorY, kLineDayWidth, kLineHeight)

                    painter.fillRect(rectKLine, QColor.fromRgb(200,0,0))


                painter.drawRect(rectKLine)

            pass
        except Exception as eee:
            strError = eee.__str__()
            print(strError)


        pass

    def clearImage(self):
        painter = QPainter(self.myCanvasKLine)
        h = self.myCanvasKLine.height()
        w = self.myCanvasKLine.width()
        painter.fillRect(0, 0, w, h, QColor.fromRgb(0, 0, 0, 0))

    oclhList = None
    tradeDayList = None


    # todo 直接使用 dataframe 来使用数据
    def setTradeDayListAndOCLH(self, tradeDateList: List[str], oclhList :np.ndarray,
                               highestPriceInScreen: float, lowestPriceInScreen : float, showDay : int):


        #self.oclhList  = oclhList[::-1]
        self.oclhList = oclhList
        self.tradeDayList = tradeDateList
        self.showDayInGauges = showDay

        self.lowestPriceInScreen = lowestPriceInScreen
        self.highestPriceInScreen = highestPriceInScreen

    def getMousePositionPrice(self,xInGrid: int):


        if self.oclhList is not None and xInGrid < len(self.oclhList):

            openP = self.oclhList[xInGrid][0]
            closeP = self.oclhList[xInGrid][1]
            lowP = self.oclhList[xInGrid][2]
            highP = self.oclhList[xInGrid][3]

            return [openP, closeP, lowP, highP]
        else:
            return None
        pass
