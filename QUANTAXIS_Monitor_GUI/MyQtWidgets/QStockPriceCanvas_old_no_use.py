from PyQt5.Qt import QLabel
from PyQt5.Qt import QDialog
from PyQt5.Qt import QMessageBox
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import math
import numpy as np

from QUANTAXIS.QAFetch.QAQuery_Advance import *

from QUANTAXIS.QAUtil.QADate import *
from QUANTAXIS.QAUtil.QADate_trade import *


class QtStockPriceCanvas(QFrame):
    def __init__(self, parent=None):
        # parent not set to, none , 设置成parent 会死锁
        super(QtStockPriceCanvas, self).__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()

        self.myCanvasKLine = QImage()
        self.myCanvasStockInfoMouseMove = QImage()
        self.myCanvasStockInfo = QImage()
        self.myCanvasPriceRuler = QImage()
        self.myCanvasDateRuler = QImage()

    # def sizeHint(self):
    #     qsize = QSize()
    #     qsize.setHeight(800)
    #     qsize.setWidth(900)
    #     return qsize

    # draw somethings on the canvas

    ###############################
    # 股票信息栏                    #
    ###############################
    # 价格 #
    #     #
    #     #
    #     #
    #     #    k线图
    #     #
    #     #
    #     #
    ################################




    LeftPriceWidth = 50
    BottomDateHeight = 20
    BottomCoordDatePt = []
    LeftPriceDatePt = []
    TopInfoHeight = 80

    strCode = ""  # 代码
    strFQ = ""  # 复权
    strCyc = ""  # 周期
    strCord = ""  # 坐标类型
    #iZoomIn = 0  # 放到缩小

    qaDataStuctDay = None

    oclh = None

    maxPriceInScreen = 0
    minPriceInScreen = 0


    tradeDays = None

    #默认加载的天数
    defaultLoadKLineDayCount = 300
    #显示的天数
    showKLineDayCount = 100

    moveForward = 0
    strCurrentMouseDate = ""






    def setCode(self, strCode):
        self.strCode = strCode


    def loadCodeData(self):

        try:
            self.qaDataStuctDay = QA_fetch_stock_day_adv(self.strCode)


            #QA_util_date_stamp()
            #self.qaDataStuctDay.select_time(start=)


            strToday=QA_util_today_str()
            strTradeDayEnd = QA_util_get_real_date(strToday)


            strTradeDayEnd = QA_util_get_last_day(strTradeDayEnd, self.moveForward)


            strTradeDayStart = QA_util_get_last_day(strTradeDayEnd, self.defaultLoadKLineDayCount)  # 获取近100天的数据


            self.qaDataStuctDay = self.qaDataStuctDay.select_time(strTradeDayStart, strTradeDayEnd)
            self.qaDataStuctDay.to_qfq()

            # 找出最高价和最低价
            h = self.qaDataStuctDay.high
            l = self.qaDataStuctDay.low

            #hl serial
            posh = h.values.argmax()
            posl = l.values.argmin()

            self.maxPriceInScreen = h[posh]
            self.minPriceInScreen = l[posl]

            self.lowestPrice = l[posl]
            self.highestPrice = h[posh]


            self.maxPriceInScreen = float(math.ceil(self.maxPriceInScreen))
            self.minPriceInScreen = float(math.floor(self.minPriceInScreen))

            ds = self.qaDataStuctDay.select_code(self.strCode)
            self.oclh = np.array(ds.data.loc[:, ['open', 'close', 'low', 'high']])
            self.datesOfThisStockTrade = ds.datetime.to_series()

            self.tradeDays = []

            dates_value = self.datesOfThisStockTrade.values
            for i in range(len(dates_value)):
                vdt64 = dates_value[i]
                strTimeOfTradeDay = str(vdt64)[:10]
                self.tradeDays.append(strTimeOfTradeDay)

            self.tradeDays.reverse()
            self.oclh = self.oclh[::-1]

            self.oclh[0][0]
            self.oclh[0][1]
            self.oclh[0][2]
            self.oclh[0][3]



        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)

    def moveLeftChart(self):

        try:
            if self.moveForward <= self.defaultLoadKLineDayCount - self.showKLineDayCount:
                self.moveForward = self.moveForward + 1

                self.loadCodeData()
                self.drawCoordinate()
                self.drawKLine()
                self.drawStockInfo()


        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)

        pass

    def moveRightChart(self):


        try:
            if self.moveForward >= 0:
                self.moveForward = self.moveForward - 1

                self.loadCodeData()
                self.drawCoordinate()
                self.drawKLine()
                self.drawStockInfo()


            pass
        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)

        pass

    def zoomIn(self):
        try:
            if (self.showKLineDayCount-30)  >= 100:
                self.showKLineDayCount = self.showKLineDayCount - 30

                self.loadCodeData()
                self.drawCoordinate()
                self.drawKLine()
                self.drawStockInfo()

            pass
        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)
        pass

    def zoomOut(self):

        try:
            if (self.showKLineDayCount+30)  <= self.defaultLoadKLineDayCount:
                self.showKLineDayCount = self.showKLineDayCount + 30

                self.loadCodeData()
                self.drawCoordinate()
                self.drawKLine()
                self.drawStockInfo()


            pass
        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)

        pass

    def clearAllImage(self):

        try:
            widthOfCurrentDraw = self.width()
            heightOfCurrentDraw = self.height()

            c = QColor.fromRgb(0, 0, 0, alpha=0)
            self.myCanvasStockInfoMouseMove.fill(c)
            self.myCanvasStockInfo.fill(c)
            self.myCanvasPriceRuler.fill(c)
            self.myCanvasKLine.fill(c)
            self.myCanvasDateRuler.fill(c)

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)
        pass

    ################################################################################################

    def drawCoordinate(self):

        try:

            #alpha = 0 透明
            #全部清除
            self.myCanvasPriceRuler.fill(QColor.fromRgb(0,0,0,0))
            painterPriceRuler = QPainter(self.myCanvasPriceRuler)
            painterPriceRuler.fillRect(0,0,self.width(),self.height(), QColor.fromRgb(0,0,0,0))

            ############################################################################################################

            widthOfCurrentDraw = self.LeftPriceWidth
            heightOfCurrentDraw = self.height() - self.TopInfoHeight -self.BottomDateHeight


            painterPriceRuler.fillRect(0, self.TopInfoHeight  , widthOfCurrentDraw, heightOfCurrentDraw  , QColor.fromRgb(0x00FFFF))


            if self.maxPriceInScreen == 0 and self.minPriceInScreen == 0:
                self.maxPriceInScreen = 88
                self.minPriceInScreen = 8

            priceRange = (self.maxPriceInScreen - self.minPriceInScreen)


            priceGapCount = 20

            priceSegmentHeight = heightOfCurrentDraw / priceGapCount
            #
            for i in range(priceGapCount):
                priceScreenCoorY = self.height() - self.BottomDateHeight - (priceSegmentHeight * i )
                #
                # if i == 0:
                #      #priceScreenCoorY +
                #
                #      qp = QPoint(0, priceScreenCoorY)
                #      priceShow = '%0.2f' % (self.lowestPrice + priceRange / 10 * i)
                #      painterPriceRuler.drawText(qp, priceShow)
                #
                #      qp2 = QPoint(self.LeftPriceWidth, priceScreenCoorY)
                #      painterPriceRuler.drawLine(qp, qp2)

                #if i == 50:
                    #priceScreenCoorY = priceScreenCoorY + 10

                qp = QPoint(0, priceScreenCoorY+5)
                priceShow = '%0.2f' % (self.minPriceInScreen + priceRange / priceGapCount * i)
                painterPriceRuler.drawText(qp, priceShow)

                qp = QPoint(self.LeftPriceWidth-10, priceScreenCoorY)
                qp2 = QPoint(self.LeftPriceWidth, priceScreenCoorY)
                painterPriceRuler.drawLine(qp, qp2)


                painterPriceRuler.save()

                pen= QPen();
                pen.setStyle(Qt.DashDotDotLine)
                pen.setBrush(QBrush(Qt.blue)); # 设置笔刷，


                painterPriceRuler.setPen(pen)

                qp3 = QPoint(self.width(), priceScreenCoorY)
                painterPriceRuler.drawLine(qp2, qp3)

                painterPriceRuler.restore()

            centCount = priceRange * 10

            centCountPart = math.modf(centCount)
            iCount = int(centCountPart[1])

            iRuleGapSize = heightOfCurrentDraw / iCount

            # for i in range(iCount):
            #
            #     rulerScreenCoorY = self.height() - self.BottomDateHeight - (iRuleGapSize * i)
            #
            #     aRect = QRectF(self.LeftPriceWidth-5, rulerScreenCoorY, self.LeftPriceWidth, rulerScreenCoorY + iRuleGapSize)
            #     painterPriceRuler.drawRect(aRect)

            pass

            ############################################################################################################

            # alpha = 0 透明
            # 全部清除
            self.myCanvasDateRuler.fill(QColor.fromRgb(0, 0, 0, 0))
            painterDateRuler = QPainter(self.myCanvasDateRuler)
            painterDateRuler.fillRect(0, 0, self.width(), self.height(), QColor.fromRgb(0, 0, 0, 0))

            widthOfCurrentDraw = self.width() - self.LeftPriceWidth
            heightOfCurrentDraw = self.height()


            if self.tradeDays is None:
                strToday = QA_util_today_str()
                strTradeDayEnd = QA_util_get_real_date(strToday)


            painterDateRuler.fillRect(self.LeftPriceWidth, heightOfCurrentDraw- self.BottomDateHeight, widthOfCurrentDraw, heightOfCurrentDraw, QColor.fromRgb(120,221,232,255))

            dateGapCount = ((widthOfCurrentDraw)/ self.showKLineDayCount)

            self.BottomCoordDatePt = []
            for i in range(self.showKLineDayCount): # 计算坐标的时候需要

                # painter.drawLine(self.LeftPriceWidth+dateGapCount*i, heightOfCurrentDraw - self.BottomDateHeight, self.LeftPriceWidth+dateGapCount*i, heightOfCurrentDraw-10)
                if self.tradeDays is not None and i >= len(self.tradeDays):
                    continue


                painterDateRuler.drawRect(self.LeftPriceWidth+dateGapCount*i, heightOfCurrentDraw - self.BottomDateHeight, dateGapCount, 5)
                self.BottomCoordDatePt.append(self.LeftPriceWidth+dateGapCount*i)

                if (i % 20 == 0) or i ==0 or i == (self.showKLineDayCount-1):

                    painterDateRuler.fillRect(self.LeftPriceWidth+dateGapCount*i, heightOfCurrentDraw - self.BottomDateHeight, dateGapCount, 5, QColor.fromRgb(0,255,0))

                    if self.tradeDays is None:
                        strDateOnRuler = QA_util_get_last_day(strTradeDayEnd, (self.showKLineDayCount-1) - i )  # 获取近100天的数据
                        strDateOnRuler = QA_util_get_real_date(strDateOnRuler)
                    else:
                        if ((self.showKLineDayCount-1)-i) < len(self.tradeDays):
                            strDateOnRuler = self.tradeDays[(self.showKLineDayCount-1)-i]

                    print(strDateOnRuler)

                    if i == 0:
                        qp1 = QPoint(self.LeftPriceWidth+dateGapCount*i, heightOfCurrentDraw)
                    elif i == (self.showKLineDayCount-1):
                        qp1 = QPoint(self.LeftPriceWidth+dateGapCount*i-70, heightOfCurrentDraw)
                    else:
                        qp1 = QPoint(self.LeftPriceWidth+dateGapCount*i-35, heightOfCurrentDraw)

                    painterDateRuler.drawText(qp1,"{}".format(strDateOnRuler))

            #添加最后一个日期坐标轴
            self.BottomCoordDatePt.append(self.LeftPriceWidth + dateGapCount * self.showKLineDayCount)

            self.update()

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)


    def drawStockInfo(self):

        try:

            widthOfCurrentDraw = self.width()
            heightOfCurrentDraw = self.height()

            # 全部清除，变成透明
            self.myCanvasStockInfo.fill(QColor.fromRgb(0, 0, 0, alpha=0))
            painterMouse = QPainter(self.myCanvasStockInfo);

            rectClear = QRect(0, 0, self.width(), self.height())
            painterMouse.fillRect(rectClear, QColor.fromRgb(0, 0, 0, alpha=0))

            painterMouse.fillRect(0,0, widthOfCurrentDraw, self.TopInfoHeight, QColor.fromRgb(111,111,222,alpha=255))


        except Exception as eeee:
            strErro = eeee.__str__()
            print(strErro)




    def drawKLine(self):

        try:

            # alpha = 0 透明
            # 全部清除
            self.myCanvasKLine.fill(QColor.fromRgb(0, 0, 0, 0))
            painterKLine = QPainter(self.myCanvasKLine)
            painterKLine.fillRect(0, 0, self.width(), self.height(), QColor.fromRgb(0, 0, 0, 0))

            ############################################################################################################

            # painter = QPainter(self.myCanvas)
            # self.myCanvas.fill(QColor.fromRgb(255,255,255))
            #

            widthOfCurrentDraw = self.width() - self.LeftPriceWidth
            heightOfCurrentDraw = self.height() - self.TopInfoHeight - self.BottomDateHeight

            # # ruleGapY = heightOfCurrentDraw / 10
            ruleGapX = widthOfCurrentDraw / (self.showKLineDayCount)

            if self.maxPriceInScreen != 0 and self.minPriceInScreen != 0:
                if self.oclh is not None:

                    priceRange = (self.maxPriceInScreen - self.minPriceInScreen) * (self.showKLineDayCount)
                    pixelCountInUnit = (heightOfCurrentDraw / priceRange)

                    #for i in range(len(self.ohlc)):

                    #if len(self.oclh) < self.showKLineDayCount:
                        #break;

                    for i in range((self.showKLineDayCount)):
                        #print(self.oclh[i])


                        if ((self.showKLineDayCount-1)-i) >= len(self.oclh):
                            # openprice =0
                            # closeprice=0
                            # lowprice =0
                            # highprice=0
                            continue
                        else:

                            openprice = self.oclh[(self.showKLineDayCount-1)-i][0]
                            closeprice = self.oclh[(self.showKLineDayCount-1)-i][1]
                            lowprice = self.oclh[(self.showKLineDayCount-1)-i][2]
                            highprice = self.oclh[(self.showKLineDayCount-1)-i][3]

                        if self.maxPriceInScreen != 0 and self.minPriceInScreen != 0:

                            heightFromMinPriceOpen = (openprice - self.minPriceInScreen) * (self.showKLineDayCount) * pixelCountInUnit
                            heihgtFromMaxPriceOpen = heightOfCurrentDraw - heightFromMinPriceOpen
                            openPrice_ScreenCoorY = self.TopInfoHeight + heihgtFromMaxPriceOpen

                            heightFromMinPriceClose = (closeprice - self.minPriceInScreen) * (self.showKLineDayCount) * pixelCountInUnit
                            heihgtFromMaxPriceClose = heightOfCurrentDraw - heightFromMinPriceClose
                            closePrice_ScreenCoorY = self.TopInfoHeight + heihgtFromMaxPriceClose

                            heightFromMinPriceLow = (lowprice - self.minPriceInScreen) * (self.showKLineDayCount) * pixelCountInUnit
                            heihgtFromMaxPriceLow = heightOfCurrentDraw - heightFromMinPriceLow
                            lowPrice_ScreenCoorY = self.TopInfoHeight + heihgtFromMaxPriceLow

                            heightFromMinPriceHigh = (highprice - self.minPriceInScreen) * (self.showKLineDayCount) * pixelCountInUnit
                            heihgtFromMaxPriceHigh = heightOfCurrentDraw - heightFromMinPriceHigh
                            highPrice_ScreenCoorY = self.TopInfoHeight + heihgtFromMaxPriceHigh


                            #painterKLine.drawLine(self.LeftPriceWidth+i*ruleGapX, openPrice_ScreenCoorY,self.LeftPriceWidth+i*ruleGapX+ruleGapX, openPrice_ScreenCoorY )
                            rectKLineEntityHigh = abs(closePrice_ScreenCoorY - openPrice_ScreenCoorY)


                            painterKLine.drawLine(self.LeftPriceWidth + i * ruleGapX + ruleGapX / 2,
                                                  highPrice_ScreenCoorY,
                                                  self.LeftPriceWidth + i * ruleGapX + ruleGapX / 2,
                                                  lowPrice_ScreenCoorY)

                            if openprice >= closeprice:
                                rectKLineEntiry = QRectF(self.LeftPriceWidth+i*ruleGapX,openPrice_ScreenCoorY,ruleGapX, rectKLineEntityHigh)
                                painterKLine.fillRect(rectKLineEntiry,QColor.fromRgb(0,255,0))
                                painterKLine.drawRect(rectKLineEntiry)


                            else:
                                rectKLineEntiry = QRectF(self.LeftPriceWidth+i*ruleGapX,closePrice_ScreenCoorY,ruleGapX, rectKLineEntityHigh)
                                painterKLine.fillRect(rectKLineEntiry,QColor.fromRgb(255,0,0))
                                painterKLine.drawRect(rectKLineEntiry)




            self.update()
        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)
        pass

    ################################################################################################################
    def mouseMoveEvent(self, a0: QMouseEvent):

        try:
            widthOfCurrentDraw = self.width()
            heightOfCurrentDraw = self.height()

            pos = a0.pos()

            #全部清除，变成透明
            self.myCanvasStockInfoMouseMove.fill(QColor.fromRgb(0, 0, 0, alpha=0))
            painterMouse = QPainter(self.myCanvasStockInfoMouseMove);

            rectClear = QRect(0,0,self.width(), self.height())
            painterMouse.fillRect(rectClear, QColor.fromRgb(0,0,0,alpha=0))


            strToday = QA_util_today_str()
            strTradeDayEnd = QA_util_get_real_date(strToday)

            if  self.maxPriceInScreen != 0 and   self.minPriceInScreen != 0:

                priceRange = (self.maxPriceInScreen - self.minPriceInScreen) * (self.showKLineDayCount)
                priceCountInUnit = ( priceRange / heightOfCurrentDraw)
                priceLogicalCoorY =   (priceCountInUnit  * (heightOfCurrentDraw -pos.y())) /(self.showKLineDayCount)  + self.minPriceInScreen
                #strDraw = '屏幕坐标%0.2f,%0.2f ，价格区间%f , 单位价格占用屏幕像素 %f 价格%0.2f ' % (pos.x(), pos.y(), priceRange, priceLogicalCoorY, priceLogicalCoorY)
            else:
                strDraw = '%0.2f,%0.2f' % (pos.x(),pos.y())

                qp = QPoint(self.LeftPriceWidth, 10)
                painterMouse.drawText(qp,strDraw)

            '''
                ' ' ' ' ' '
            '''
            #fix here 使用股票价格的日期数据
            mouseXPt = pos.x()
            if len(self.BottomCoordDatePt)  >0:
                for indexOfDate in range(len(self.BottomCoordDatePt)):

                    if indexOfDate < len(self.BottomCoordDatePt) and indexOfDate+1 < len(self.BottomCoordDatePt):

                        if  indexOfDate<len(self.BottomCoordDatePt)  and mouseXPt >= self.BottomCoordDatePt[indexOfDate] and mouseXPt < self.BottomCoordDatePt[indexOfDate+1]:


                            if self.tradeDays is None:
                                strDateOnRuler = QA_util_get_last_day(strTradeDayEnd, (self.showKLineDayCount-1)-indexOfDate)  # 获取近100天的数据
                                self.strCurrentMouseDate = strDateOnRuler
                            else:
                                self.strCurrentMouseDate = self.tradeDays[(self.showKLineDayCount-1)-indexOfDate]

                            qp = QPoint(self.LeftPriceWidth + (self.showKLineDayCount), 10)
                            strDraw = "日期：%s" % (self.strCurrentMouseDate)
                            painterMouse.drawText(qp, strDraw)

                            qp = QPoint(self.LeftPriceWidth + 300, 10)

                            #if len(self.oclh) <
                            if ((self.showKLineDayCount-1)-indexOfDate) >= len(self.oclh):
                                strDrawPrice =""
                            else:

                                strDrawPrice = "开盘: {} 收盘: {} 最低：{} 最高：{}".format(
                                    self.oclh[(self.showKLineDayCount-1)-indexOfDate][0],
                                    self.oclh[(self.showKLineDayCount-1)-indexOfDate][1],
                                    self.oclh[(self.showKLineDayCount-1)-indexOfDate][2],
                                    self.oclh[(self.showKLineDayCount-1)-indexOfDate][3])
                            painterMouse.drawText(qp, strDrawPrice)

                            #dateGapCountWidth = ((widthOfCurrentDraw)/100)

                            dateGapCountInScreen = (self.BottomCoordDatePt[indexOfDate] + self.BottomCoordDatePt[indexOfDate+1])/2
                            #纵坐标
                            painterMouse.drawLine(dateGapCountInScreen, self.TopInfoHeight, dateGapCountInScreen, heightOfCurrentDraw)
                            #横坐标
                            painterMouse.drawLine(0, pos.y(), widthOfCurrentDraw, pos.y())

                            break

                self.update()
            pass
        except Exception as eeee:
            strErro = eeee.__str__()
            print(strErro)

    def keyPressEvent(self, a0: QKeyEvent):

        if Qt.Key_Left  == a0.key():
            print("left key")
            pass

        if Qt.Key_Right == a0.key():
            print("right key")

            pass

        pass

    def resizeEvent(self, a0: QResizeEvent):
        if self.width() > self.myCanvasKLine.width() or self.height() > self.myCanvasKLine.height() or \
            self.width() > self.myCanvasPriceRuler.width() or self.height() > self.myCanvasPriceRuler.height() or \
            self.width() > self.myCanvasStockInfoMouseMove.width() or self.height() > self.myCanvasStockInfoMouseMove.height() or \
            self.width() > self.myCanvasStockInfo.width() or self.height() > self.myCanvasStockInfo.height() or \
            self.width() > self.myCanvasDateRuler.width() or self.height() > self.myCanvasDateRuler.height() :

            newSizea = a0.size()
            newWidth = newSizea.width()
            newHeight = newSizea.height()



            self.myCanvasPriceRuler = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # QPainter painter( & newImage);
            painter = QPainter(self.myCanvasPriceRuler)
            painter.drawImage(QPoint(0, 0), self.myCanvasPriceRuler);

            self.myCanvasDateRuler = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # QPainter painter( & newImage);
            painter = QPainter(self.myCanvasDateRuler)
            painter.drawImage(QPoint(0, 0), self.myCanvasDateRuler);

            self.myCanvasKLine = QImage(QSize(newWidth, newHeight) , QImage.Format_ARGB32)
            # QPainter painter( & newImage);
            painter = QPainter(self.myCanvasKLine)
            painter.drawImage(QPoint(0, 0), self.myCanvasKLine);

            self.myCanvasStockInfoMouseMove = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # QPainter painter( & newImage);
            painter = QPainter(self.myCanvasStockInfoMouseMove)
            painter.drawImage(QPoint(0, 0), self.myCanvasStockInfoMouseMove);

            self.myCanvasStockInfo = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # QPainter painter( & newImage);
            painter = QPainter(self.myCanvasStockInfo)
            painter.drawImage(QPoint(0, 0), self.myCanvasStockInfo);

    def paintEvent(self,qPaintEvent):

        try:
            painter = QPainter(self)
            #dirtyRect =QRect()
            dirtyRect = qPaintEvent.rect();

            painter.fillRect(dirtyRect, QColor.fromRgb(255,255,255))

            painter.drawImage(dirtyRect, self.myCanvasPriceRuler, dirtyRect);
            painter.drawImage(dirtyRect, self.myCanvasDateRuler, dirtyRect)

            painter.drawImage(dirtyRect, self.myCanvasKLine, dirtyRect);
            painter.drawImage(dirtyRect, self.myCanvasStockInfo, dirtyRect);

            painter.drawImage(dirtyRect, self.myCanvasKLine, dirtyRect);
            painter.drawImage(dirtyRect, self.myCanvasStockInfoMouseMove, dirtyRect);

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)
        pass







