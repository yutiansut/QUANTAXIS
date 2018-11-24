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

from QUANTAXIS.QAIndicator import QA_indicator_MA



'''
顾比复合移动平均线(GuppyMultipleMovingAverAge，GMMA)。
GMMA使用了两组指数移动平均数进行分析。由3、5、8、10、12和15日移动平均线构成一组“短期组”，
这组指标透露了市场短期投机者的行为；而“长期组”则由30、35、40、45、50和60日移动平均线构成
'''
class CanvasGMMA:
    def __init__(self):
        self.myCanvasGMMA = QImage()

        mouseX = 0.0
        mouseY = 0.0

        xInGrid = 0.0
        self.showDayInGauges = 100


        pass

    def setDrawImageSize(self, rect: QRect):
        self.myCanvasGMMA = QImage(rect, QImage.Format_ARGB32)
        self.myCanvasGMMA.fill(QColor.fromRgb(0, 0, 0, 0))
        pass


    def draw(self):

        try:
            self.myCanvasGMMA.fill(QColor.fromRgb(0, 0, 0, 0))

            h = self.myCanvasGMMA.height()
            w = self.myCanvasGMMA.width()
            painter = QPainter(self.myCanvasGMMA)

            qp = QPoint(10,10)
            strMsg = "%s"%("Guppy Multiple Moving Average Lines")
            painter.drawText(qp,strMsg)

            kLineDayWidth = w / self.showDayInGauges

            painter.save()

            pen = QPen();
            pen.setStyle(Qt.SolidLine)
            pen.setBrush(QBrush(Qt.blue));  # 设置笔刷，

            painter.setPen(pen)

            for iIndex in range(self.showDayInGauges-1):
                if iIndex < len(self.pointsY_Ma03) and iIndex+1 < len(self.pointsY_Ma03):
                    painter.drawLine(iIndex *kLineDayWidth, self.pointsY_Ma03[iIndex], \
                                     iIndex*kLineDayWidth + kLineDayWidth, self.pointsY_Ma03[iIndex+1])

                    #
                if iIndex < len(self.pointsY_Ma05) and iIndex+1 < len(self.pointsY_Ma05):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma05[iIndex], \
                                 iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma05[iIndex + 1])

                if iIndex < len(self.pointsY_Ma08) and iIndex + 1 < len(self.pointsY_Ma08):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma08[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma08[iIndex + 1])

                if iIndex < len(self.pointsY_Ma10) and iIndex + 1 < len(self.pointsY_Ma10):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma10[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma10[iIndex + 1])

                if iIndex < len(self.pointsY_Ma12) and iIndex + 1 < len(self.pointsY_Ma12):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma12[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma12[iIndex + 1])

                    #ppp = QPoint((iIndex * kLineDayWidth), (self.pointsY_Ma12[iIndex])+20)

                if iIndex < len(self.pointsY_Ma15) and iIndex + 1 < len(self.pointsY_Ma15):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma15[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma15[iIndex + 1])




            painter.restore()

            pen = QPen();
            pen.setStyle(Qt.SolidLine)
            pen.setBrush(QBrush(Qt.red));  # 设置笔刷，

            painter.setPen(pen)

            painter.save()


            currentState = 0
            previousState = 0


            for iIndex in range(self.showDayInGauges - 1):
                if iIndex < len(self.pointsY_Ma30) and iIndex + 1 < len(self.pointsY_Ma30):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma30[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma30[iIndex + 1])
                    ppp = QPoint((iIndex * kLineDayWidth), (self.pointsY_Ma30[iIndex]) + 20)

                if iIndex < len(self.pointsY_Ma35) and iIndex + 1 < len(self.pointsY_Ma35):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma35[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma35[iIndex + 1])

                if iIndex < len(self.pointsY_Ma40) and iIndex + 1 < len(self.pointsY_Ma40):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma40[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma40[iIndex + 1])

                if iIndex < len(self.pointsY_Ma45) and iIndex + 1 < len(self.pointsY_Ma45):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma45[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma45[iIndex + 1])

                if iIndex < len(self.pointsY_Ma50) and iIndex + 1 < len(self.pointsY_Ma50):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma50[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma50[iIndex + 1])

                    ppp = QPoint((iIndex * kLineDayWidth), (self.pointsY_Ma50[iIndex])+20)


                if iIndex < len(self.pointsY_Ma60) and iIndex + 1 < len(self.pointsY_Ma60):
                    painter.drawLine(iIndex * kLineDayWidth, self.pointsY_Ma60[iIndex], \
                                     iIndex * kLineDayWidth + kLineDayWidth, self.pointsY_Ma60[iIndex + 1])



                if iIndex < len(self.pointsY_Ma30) and iIndex + 1 < len(self.pointsY_Ma30) and \
                        iIndex < len(self.pointsY_Ma35) and iIndex + 1 < len(self.pointsY_Ma35) and \
                        iIndex < len(self.pointsY_Ma40) and iIndex + 1 < len(self.pointsY_Ma40) and \
                        iIndex < len(self.pointsY_Ma45) and iIndex + 1 < len(self.pointsY_Ma45) and \
                        iIndex < len(self.pointsY_Ma50) and iIndex + 1 < len(self.pointsY_Ma50):

                    if self.pointsY_Ma30[iIndex] < self.pointsY_Ma35[iIndex] and \
                            self.pointsY_Ma35[iIndex] < self.pointsY_Ma40[iIndex]:
                            #self.pointsY_Ma40[iIndex] < self.pointsY_Ma45[iIndex] and \
                            #self.pointsY_Ma45[iIndex] < self.pointsY_Ma50[iIndex]:

                        if currentState == 0 or currentState == previousState or currentState == 2:
                            previousState = currentState
                            currentState = 1

                    elif self.pointsY_Ma30[iIndex] > self.pointsY_Ma35[iIndex] and \
                            self.pointsY_Ma35[iIndex] > self.pointsY_Ma40[iIndex]:
                            # self.pointsY_Ma40[iIndex] > self.pointsY_Ma45[iIndex] and \
                            # self.pointsY_Ma45[iIndex] > self.pointsY_Ma50[iIndex]:

                        if currentState == 0 or currentState == previousState or currentState == 1:
                            previousState = currentState
                            currentState = 2

                    if previousState != currentState:
                        if previousState == 1 and currentState == 2:
                            # painter.drawText(ppp, "卖出")
                            # painter.drawLine((ppp.x()), 0, (ppp.x()), 1000)
                            painter.fillRect(ppp.x(), 0, kLineDayWidth, 1000, QColor(0, 255, 0, 88))
                        elif previousState == 2 and currentState == 1:
                            # painter.drawText(ppp, "买入")
                            # painter.drawLine((ppp.x()), 0, (ppp.x()), 1000)
                            painter.fillRect(ppp.x(), 0, kLineDayWidth, 1000, QColor(255, 0, 0, 88))
                        else:
                            print("current state is %d %d" % (currentState, previousState))

                    else:
                        print("current statis is equal %d %d" % (currentState, previousState))



            painter.restore()




            pass

        except Exception as eee:
            strError = eee.__str__()
            print(strError)


        pass

    def clearImage(self):
        painter = QPainter(self.myCanvasGMMA)
        h = self.myCanvasGMMA.height()
        w = self.myCanvasGMMA.width()
        painter.fillRect(0, 0, w, h, QColor.fromRgb(0, 0, 0, 0))


    def setPriceRange(self, highPrice, lowPrice):
        self.highestPriceInScreen = highPrice
        self.lowestPriceInScreen = lowPrice

    def setTradeDays(self, tradeDateList: List[str]):
        self.tradeDateList = tradeDateList
        pass



    # pointsY_Ma03 = []
    # def set03MA(self, ma03_DataFrame: pd.DataFrame, showDays: int):
    #
    #     h = self.myCanvasGMMA.height()
    #     w = self.myCanvasGMMA.width()
    #
    #     #self.ma03_DataFrame = ma03_DataFrame
    #     self.showDayInGauges = showDays
    #
    #     priceRange = self.highestPriceInScreen - self.lowestPriceInScreen
    #     priceGapCount = priceRange * 100
    #     pricePerGapHeight = h / priceGapCount
    #
    #     iIndex = 0
    #     self.pointsY_Ma03.clear()
    #     for row in ma03_DataFrame.iterrows():
    #
    #         strTimeOfTradeDayMa = str(row[0][0])[:10]
    #
    #         if np.isnan(row[1][0]):
    #             continue
    #         else:
    #             if strTimeOfTradeDayMa in self.tradeDateList:
    #                 heightFromMinPriceOpen = (row[1][0] - self.lowestPriceInScreen) * (100) * pricePerGapHeight
    #                 heihgtFromMaxPriceOpen = h - heightFromMinPriceOpen
    #                 Ma03_ScreenCoorY = 0 + heihgtFromMaxPriceOpen
    #                 self.pointsY_Ma03.append(Ma03_ScreenCoorY)
    #                 iIndex = iIndex + 1
    #
    #
    #
    #
    # pointsY_Ma05 = []
    # def set05MA(self, ma05_DataFrame: pd.DataFrame, showDays :int):
    #
    #     h = self.myCanvasGMMA.height()
    #     w = self.myCanvasGMMA.width()
    #
    #     #self.ma05_DataFrame = ma05_DataFrame
    #     self.showDayInGauges = showDays
    #
    #     priceRange = self.highestPriceInScreen - self.lowestPriceInScreen
    #     priceGapCount = priceRange * 100
    #     pricePerGapHeight = h / priceGapCount
    #
    #     iIndex = 0
    #     self.pointsY_Ma05.clear()
    #     for row in ma05_DataFrame.iterrows():
    #
    #         strTimeOfTradeDayMa = str(row[0][0])[:10]
    #
    #         if np.isnan(row[1][0]):
    #             continue
    #         else:
    #             if strTimeOfTradeDayMa in self.tradeDateList:
    #                 heightFromMinPriceOpen = (row[1][0] - self.lowestPriceInScreen) * (100) * pricePerGapHeight
    #                 heihgtFromMaxPriceOpen = h - heightFromMinPriceOpen
    #                 Ma05_ScreenCoorY = 0 + heihgtFromMaxPriceOpen
    #                 self.pointsY_Ma05.append(Ma05_ScreenCoorY)
    #                 iIndex = iIndex + 1
    #
    # pointsY_Ma08 = []
    # def set08MA(self, ma08_DataFrame: pd.DataFrame, showDays: int):
    #
    #     h = self.myCanvasGMMA.height()
    #     w = self.myCanvasGMMA.width()
    #
    #     # self.ma05_DataFrame = ma05_DataFrame
    #     self.showDayInGauges = showDays
    #
    #     priceRange = self.highestPriceInScreen - self.lowestPriceInScreen
    #     priceGapCount = priceRange * 100
    #     pricePerGapHeight = h / priceGapCount
    #
    #     iIndex = 0
    #     self.pointsY_Ma08.clear()
    #     for row in ma08_DataFrame.iterrows():
    #
    #         strTimeOfTradeDayMa = str(row[0][0])[:10]
    #
    #         if np.isnan(row[1][0]):
    #             continue
    #         else:
    #             if strTimeOfTradeDayMa in self.tradeDateList:
    #                 heightFromMinPriceOpen = (row[1][0] - self.lowestPriceInScreen) * (100) * pricePerGapHeight
    #                 heihgtFromMaxPriceOpen = h - heightFromMinPriceOpen
    #                 Ma08_ScreenCoorY = 0 + heihgtFromMaxPriceOpen
    #                 self.pointsY_Ma08.append(Ma08_ScreenCoorY)
    #                 iIndex = iIndex + 1
    #
    def setXMA(self, maX_DataFrame: pd.DataFrame, showDays: int):

        h = self.myCanvasGMMA.height()
        w = self.myCanvasGMMA.width()

        # self.ma05_DataFrame = ma05_DataFrame
        self.showDayInGauges = showDays

        priceRange = self.highestPriceInScreen - self.lowestPriceInScreen
        priceGapCount = priceRange * 100
        pricePerGapHeight = h / priceGapCount

        iIndex = 0
        pointsY_MaX = []
        pointsY_MaX.clear()
        for row in maX_DataFrame.iterrows():

            strTimeOfTradeDayMa = str(row[0][0])[:10]

            if np.isnan(row[1][0]):
                continue
            else:
                if strTimeOfTradeDayMa in self.tradeDateList:
                    heightFromMinPriceOpen = (row[1][0] - self.lowestPriceInScreen) * (100) * pricePerGapHeight
                    heihgtFromMaxPriceOpen = h - heightFromMinPriceOpen
                    MaX_ScreenCoorY = 0 + heihgtFromMaxPriceOpen
                    pointsY_MaX.append(MaX_ScreenCoorY)
                    iIndex = iIndex + 1

        return pointsY_MaX

    pointsY_Ma03 = []
    def set03MA(self, ma03_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma03 = self.setXMA(ma03_DataFrame, showDays)

    pointsY_Ma05 = []
    def set05MA(self, ma05_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma05 = self.setXMA(ma05_DataFrame, showDays)

    pointsY_Ma08 = []
    def set08MA(self, ma08_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma08 = self.setXMA(ma08_DataFrame, showDays)

    pointsY_Ma10 = []
    def set10MA(self, ma10_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma10 = self.setXMA(ma10_DataFrame, showDays)

    pointsY_Ma12 = []
    def set12MA(self, ma12_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma12 = self.setXMA(ma12_DataFrame, showDays)

    pointsY_Ma15 = []
    def set15MA(self, ma15_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma15 = self.setXMA(ma15_DataFrame, showDays)

    # 30、35、40、45、50 和60

    pointsY_Ma30 = []
    def set30MA(self, ma30_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma30 = self.setXMA(ma30_DataFrame, showDays)

    pointsY_Ma35 = []
    def set35MA(self, ma35_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma35 = self.setXMA(ma35_DataFrame, showDays)

    pointsY_Ma40 = []
    def set40MA(self, ma40_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma40 = self.setXMA(ma40_DataFrame, showDays)

    pointsY_Ma45 = []
    def set45MA(self, ma45_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma45 = self.setXMA(ma45_DataFrame, showDays)

    pointsY_Ma50 = []
    def set50MA(self, ma50_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma50 = self.setXMA(ma50_DataFrame, showDays)

    pointsY_Ma60 = []
    def set60MA(self, ma60_DataFrame: pd.DataFrame, showDays: int):
        self.pointsY_Ma60 = self.setXMA(ma60_DataFrame, showDays)

    # def setTradeDayListAndOCLH(self, tradeDateList: List[str], oclhList :np.ndarray,
    #                            highestPriceInScreen: float, lowestPriceInScreen : float, showDay : int):
    #
    #
    #     #self.oclhList  = oclhList[::-1]
    #     # self.oclhList = oclhList
    #     # self.tradeDayList = tradeDateList
    #     # self.defaultShowDay = showDay
    #     #
    #     # self.lowestPriceInScreen = lowestPriceInScreen
    #     # self.highestPriceInScreen = highestPriceInScreen

    def getMousePositionPrice(self,xInGrid: int):
        if self.oclhList is not None and xInGrid < len(self.oclhList):
            # openP = self.oclhList[xInGrid][0]
            # closeP = self.oclhList[xInGrid][1]
            # lowP = self.oclhList[xInGrid][2]
            # highP = self.oclhList[xInGrid][3]
            #
            # return [openP, closeP, lowP, highP]
            return None
        else:
            return None
        pass
