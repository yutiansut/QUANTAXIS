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


class CanvasBottomDateRuler:
    def __init__(self):
        self.myCanvasDateRuler = QImage()

        #放大缩小使用
        #默认100天
        self.showDayInGauges = 100
        self.showWeekInGauges = 100
        self.showMonthInGauges = 100


        self.tradeDayList = []
        self.height = 18

        self.parentHeight = 0
        self.parentWidth = 0


        self.mouseX = 0
        self.currentPosGap = -1

        pass

    def setDrawImageSize(self, rect: QRect):
        self.myCanvasDateRuler = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasDateRuler.fill(QColor.fromRgb(0, 0, 0, 0))

        self.parentWidth = self.myCanvasDateRuler.width()
        self.parentHeight = self.myCanvasDateRuler.height()

        pass

    def clearImage(self):
        painter = QPainter(self.myCanvasDateRuler)

        h = self.myCanvasDateRuler.height()
        w = self.myCanvasDateRuler.width()
        painter.fillRect(0,0,w,h, QColor.fromRgb(0,0,0,0))

        self.myCanvasDateRuler.fill(QColor.fromRgb(0, 0, 0, 0))



        #self.myCanvasDateRuler.


    def getMouseGridIndex(self, mousex:float):
        try:
            h = self.myCanvasDateRuler.height()
            w = self.myCanvasDateRuler.width()


            guageWidth = float(w) / self.showDayInGauges
            self.mouseX = mousex
            self.currentPosGap = math.floor(mousex / guageWidth)

            return self.currentPosGap

        except Exception as eee:
            strError = eee.__str__()
            print(strError)


    # mouse grid-snap in day
    def getMoseGapPosX(self, mousex: float):
        try:
            h = self.myCanvasDateRuler.height()
            w = self.myCanvasDateRuler.width()


            guageWidth = float(w) / self.showDayInGauges

            self.mouseX = mousex
            self.currentPosGap = math.floor(mousex / guageWidth)

            print("currentPosGap ", self.currentPosGap)

            x = self.currentPosGap*guageWidth + guageWidth/2
            return x

        except Exception as eee:
            strError = eee.__str__()
            print(strError)

    def getMouseMouseDateStr(self,mousex: float):

        try:
            #h = self.myCanvasDateRuler.height()
            w = self.myCanvasDateRuler.width()

            guageWidth = w / self.showDayInGauges

            self.mouseX = mousex
            self.currentPosGap = math.floor(mousex / guageWidth)

            sizeOfLoadTradeDayList = len(self.tradeDayList)

            if sizeOfLoadTradeDayList - self.showDayInGauges >= 0:
                strDay = self.tradeDayList[self.showDayInGauges - self.currentPosGap - 1]

            else:

                if sizeOfLoadTradeDayList - self.currentPosGap > 0:
                    strDay = self.tradeDayList[sizeOfLoadTradeDayList - self.currentPosGap - 1]

            return strDay



        except Exception as eee:
            strError = eee.__str__()
            print(strError)

    def drawSelectedDay(self,positionx :float):
        try:
            h = self.myCanvasDateRuler.height()
            w = self.myCanvasDateRuler.width()
            painter = QPainter(self.myCanvasDateRuler)


            guageWidth = w / self.showDayInGauges

            #painter.fillRect(positionx - guageWidth/2, 0,  guageWidth  , h/4, QColor.fromRgb(125,125,0))

        except Exception as eee:
            strError = eee.__str__()
            print(strError)


    def draw(self):

        try:

            h = self.myCanvasDateRuler.height()
            w = self.myCanvasDateRuler.width()

            self.myCanvasDateRuler.fill(QColor.fromRgb(0, 0, 0, 0))

            painter = QPainter(self.myCanvasDateRuler)

            #painter.fillRect(0, 0, w, h, QColor.fromRgb(255, 255, 255, 255))

            guageWidth = w / self.showDayInGauges

            for iIndex in range(self.showDayInGauges):

                rectGuage = QRectF(iIndex * guageWidth, 0,   guageWidth, h/4)
                #painter.fillRect(rectGuage,QColor.fromRgb(127,127,255,0))

                painter.drawRect(rectGuage)

                # if iIndex == self.currentPosGap:
                #     painter.fillRect(rectGuage,QColor.fromRgb(0,128,128))

                sizeOfLoadTradeDayList = len(self.tradeDayList)

                if iIndex % 20 == 0 and sizeOfLoadTradeDayList > 0:
                    strDay = ""
                    p = QPoint(iIndex * guageWidth, h/4 *3 +2)

                    if (sizeOfLoadTradeDayList - self.showDayInGauges) >= 0:

                        painter.drawText(p, strDay1)
                        painter.fillRect(rectGuage, QColor.fromRgb(128,11,11))



                    else:

                        if (sizeOfLoadTradeDayList - iIndex) > 0:
                            strDay1 = self.tradeDayList[sizeOfLoadTradeDayList - iIndex -1]
                            painter.drawText(p, strDay1)
                            painter.fillRect(rectGuage, QColor.fromRgb(128, 111, 11))

                #painter.fillRect(rectGuage, QColor.fromRgb(100, 100, 100))
            print("ok")


        except Exception as eee:
            strError = eee.__str__()
            print(strError)


    def setShowDays(self, showDays : int):


        pass

    def setTradeWeekList(self, tradeDateList: List[str], showWeeks : int):

        pass

    def setTradeMonthList(self, tradeWeekList: List[str], showMonths : int):

        pass

    def setTradeDayList(self, tradeDateList: List[str], showDay : int):

        self.tradeDayList = tradeDateList
        self.showDayInGauges = showDay
        pass



        sizeOfDate = len(tradeDateList)

        # 往后计算
        #if sizeOfDate < showDaysCount:




        pass