from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockDateRuler import  *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockLeftPriceRuler import *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockMouseMove import *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockKLine import *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockInfo import *
from QUANTAXIS_Monitor_GUI.MyQtWidgets.MyDrawImgs.QStockGMMA import *
from QUANTAXIS.QAIndicator import QA_indicator_MA


class MidVolume:
    def __init__(self):
        self.myCanvasMidVolume = QImage()
        pass

    def setDrawImageSize(self, rect: QRect):
        pass



class QtStockPriceVolumeFrame(QFrame):
    def __init__(self, parent=None):
        # parent not set to, none , 设置成parent 会死锁
        super(QtStockPriceVolumeFrame, self).__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()

        #self.canvasLeftPriceRuler = LeftPriceRuler()
        self.canvasBottomDateRuler = CanvasBottomDateRuler()
        self.canvasLeftPriceRuler = CanvasLeftPriceRuler()
        self.canvasMouseMove = CanvasMouseCursor()
        self.canvasKLine = CanvasKLines()
        self.canvasStockInfo = CanvasStockInfo()
        self.canvasGMMA = CanvasGMMA()


        self.strCode = "002433"
        self.moveForward = 0

        self.MaxDayLoad = 1000
        self.MinDayLoad = 100

        self.currentLoadKLineDayCount = self.MinDayLoad


    def resizeEvent(self, a0: QResizeEvent):
        try:

            newSizea = a0.size()

            canvasWidth = newSizea.width()
            canvasHeight  = newSizea.height()

            #if self.width() > self.bottomDateRuler.myCanvasDateRuler.width() or \
            #    self.height() > self.bottomDateRuler.myCanvasDateRuler.height():

            stockInfoSize = QSize()
            stockInfoSize.setWidth(canvasWidth)
            stockInfoSize.setHeight(self.canvasStockInfo.height)
            self.canvasStockInfo.setDrawImageSize(stockInfoSize)

            rulerSize = QSize()
            rulerSize.setWidth(canvasWidth - self.canvasLeftPriceRuler.width)
            rulerSize.setHeight(self.canvasBottomDateRuler.height)
            self.canvasBottomDateRuler.setDrawImageSize(rulerSize)


            rulePriceSize = QSize()
            rulePriceSize.setWidth(self.canvasLeftPriceRuler.width)
            rulePriceSize.setHeight(canvasHeight - self.canvasBottomDateRuler.height - self.canvasStockInfo.height)
            self.canvasLeftPriceRuler.setDrawImageSize(rulePriceSize)


            mouseCrossMoveSize = QSize()
            mouseCrossMoveSize.setWidth(canvasWidth - self.canvasLeftPriceRuler.width)
            mouseCrossMoveSize.setHeight(canvasHeight - self.canvasBottomDateRuler.height - self.canvasStockInfo.height)
            self.canvasMouseMove.setDrawImageSize(mouseCrossMoveSize)
            self.canvasMouseMove.parentPosX = self.canvasLeftPriceRuler.width


            klineDrawSize = QSize()
            klineDrawSize.setWidth(canvasWidth - self.canvasLeftPriceRuler.width)
            klineDrawSize.setHeight(canvasHeight - self.canvasBottomDateRuler.height - self.canvasStockInfo.height)
            self.canvasKLine.setDrawImageSize(klineDrawSize)

            kGmmaSize = QSize()
            kGmmaSize.setWidth(canvasWidth - self.canvasLeftPriceRuler.width)
            kGmmaSize.setHeight(canvasHeight - self.canvasBottomDateRuler.height - self.canvasStockInfo.height)
            self.canvasGMMA.setDrawImageSize(kGmmaSize)

            #todo 画成交量
            #self.canvasKLine.parentPosX = self.canvasLeftPriceRuler.width
            # mouseMove

            #rulerRect = (0,newHeightOfBottomDateRuler-20,newWidthOfBottomDateRuler, 20)

            #painter = QPainter(self.bottomDateRuler.myCanvasDateRuler)
            #painter.drawImage(QPoint(200, 200), self.bottomDateRuler.myCanvasDateRuler);

            # self.myCanvasPriceRuler = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # # QPainter painter( & newImage);
            # painter = QPainter(self.myCanvasPriceRuler)
            # painter.drawImage(QPoint(0, 0), self.myCanvasPriceRuler);
            #
            #
            # self.myCanvasKLine = QImage(QSize(newWidth, newHeight) , QImage.Format_ARGB32)
            # # QPainter painter( & newImage);
            # painter = QPainter(self.myCanvasKLine)
            # painter.drawImage(QPoint(0, 0), self.myCanvasKLine);
            #
            # self.myCanvasStockInfoMouseMove = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # # QPainter painter( & newImage);
            # painter = QPainter(self.myCanvasStockInfoMouseMove)
            # painter.drawImage(QPoint(0, 0), self.myCanvasStockInfoMouseMove);
            #
            # self.myCanvasStockInfo = QImage(QSize(newWidth, newHeight), QImage.Format_ARGB32)
            # # QPainter painter( & newImage);
            # painter = QPainter(self.myCanvasStockInfo)
            # painter.drawImage(QPoint(0, 0), self.myCanvasStockInfo);


            pass
        except Exception as eee:
            strError = eee.__str__()
            print(strError)

    def paintEvent(self, qPaintEvent: QPaintEvent):
        try:
            painter = QPainter(self)
            #dirtyRect =QRect()
            dirtyRect = qPaintEvent.rect();

            painter.fillRect(dirtyRect, QColor.fromRgb(255,255,255))

            #painter.drawImage(dirtyRect, self.myCanvasPriceRuler, dirtyRect);
            #painter.drawImage(dirtyRect, self.bottomDateRuler.myCanvasDateRuler, dirtyRect)

            #painter = QPainter(self.bottomDateRuler.myCanvasDateRuler)

            w = self.width()
            h = self.height()

            #股票信息
            painter.drawImage(QPoint(0, 0), self.canvasStockInfo.myCanvasStockInfo)


            #日期坐标尺
            bottomDataRuleY = h - self.canvasBottomDateRuler.height
            bottomDateRuleX = self.canvasLeftPriceRuler.width
            painter.drawImage(QPoint(bottomDateRuleX, bottomDataRuleY), self.canvasBottomDateRuler.myCanvasDateRuler);


            #价格坐标尺
            priceRuleYPos = self.canvasStockInfo.height
            painter.drawImage(QPoint(0,priceRuleYPos), self.canvasLeftPriceRuler.myCanvasPriceRuler)

            #鼠标移动
            painter.drawImage(QPoint(self.canvasLeftPriceRuler.width, priceRuleYPos), self.canvasMouseMove.myCanvasStockInfoMouseMove)

            # k线
            painter.drawImage(QPoint(self.canvasLeftPriceRuler.width, priceRuleYPos), self.canvasKLine.myCanvasKLine)

            #Gmma 均线
            painter.drawImage(QPoint(self.canvasLeftPriceRuler.width, priceRuleYPos), self.canvasGMMA.myCanvasGMMA)


            #鼠标十字光标

            #painter.drawImage(dirtyRect, self.myCanvasKLine, dirtyRect);
            #painter.drawImage(dirtyRect, self.myCanvasStockInfo, dirtyRect);

            #painter.drawImage(dirtyRect, self.myCanvasKLine, dirtyRect);
            #painter.drawImage(dirtyRect, self.myCanvasStockInfoMouseMove, dirtyRect);

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)
        pass


    def mouseMoveEvent(self, a0: QMouseEvent):

        try:
            strDraw = '%0.2f,%0.2f' % (a0.x(), a0.y())

            pos = a0.pos()
            print(pos)

            self.canvasMouseMove.mouseX = pos.x()
            self.canvasMouseMove.mouseY = pos.y()

            self.canvasBottomDateRuler.mouseX = pos.x()
            xInGrid = self.canvasBottomDateRuler.getMoseGapPosX( pos.x() )
            self.canvasMouseMove.xInGrid = xInGrid

            strDate = self.canvasBottomDateRuler.getMouseMouseDateStr(pos.x() - self.canvasLeftPriceRuler.width)


            self.canvasBottomDateRuler.draw()
            self.canvasLeftPriceRuler.draw()
            self.canvasMouseMove.draw(self.canvasBottomDateRuler, self.canvasStockInfo)


            oclhCurrentMouseMove = self.canvasKLine.getMousePositionPrice(self.canvasBottomDateRuler.getMouseGridIndex(pos.x()))

            #strDate = self.canvasBottomDateRuler.getMouseMouseDateStr(pos.x())
            #更新价格
            self.canvasStockInfo.setMouseMoveDate(strDate)
            self.canvasStockInfo.setMouseMovePrice(oclhCurrentMouseMove)

            self.canvasStockInfo.setMousePositionInfo(pos.x() - self.canvasLeftPriceRuler.width ,pos.y() - self.canvasStockInfo.height )

            self.canvasStockInfo.draw()

            self.update()

        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)

    #########################################################################################

    def clearAllImage(self):
        try:

            self.canvasBottomDateRuler.clearImage()
            self.canvasLeftPriceRuler.clearImage()
            self.canvasMouseMove.clearImage()
            self.canvasKLine.clearImage()

            self.update()
        except Exception as eee:
            strErro = eee.__str__()
            print(strErro)

        pass

    def drawCoordinate(self):

        self.canvasBottomDateRuler.draw()
        self.canvasLeftPriceRuler.draw()
        self.canvasMouseMove.draw(self.canvasBottomDateRuler, self.canvasStockInfo)



        pass

    def drawKLine(self):
        self.canvasKLine.draw()
        self.canvasGMMA.draw()
        pass

    def moveLeftChart(self):
        pass

    def moveRightChart(self):
        pass

    def zoomIn(self):

        if self.currentLoadKLineDayCount - 50 >= self.MinDayLoad:
            self.currentLoadKLineDayCount = self.currentLoadKLineDayCount - 50
        pass

    def zoomOut(self):

        if self.currentLoadKLineDayCount + 50 <= self.MaxDayLoad:
            self.currentLoadKLineDayCount = self.currentLoadKLineDayCount + 50
        pass

    def setCode(self, txtInputedCode: str, txtName: str):

        self.strCode = txtInputedCode
        self.strName = txtName
        self.canvasStockInfo.setCodeAndName(self.strName,self.strCode)

        pass



    def loadCodeData(self):


        try:
            #
            #QA_util_date_stamp()
            #self.qaDataStuctDay.select_time(start=)


            strToday=QA_util_today_str()
            strTradeDayEnd = QA_util_get_real_date(strToday)


            strTradeDayEnd = QA_util_get_last_day(strTradeDayEnd, self.moveForward)
            strTradeDayStart = QA_util_get_last_day(strTradeDayEnd, self.currentLoadKLineDayCount)  # 获取近100天的数据

            qaDataStuctDay = QA_fetch_stock_day_adv(self.strCode)
            qaDataStuctDay = qaDataStuctDay.select_time(strTradeDayStart, strTradeDayEnd)
            qaDataStuctDay.to_qfq()

            # 找出最高价和最低价
            h = qaDataStuctDay.high
            l = qaDataStuctDay.low

            #hl serial
            posh = h.values.argmax()
            posl = l.values.argmin()


            lowestPrice = l[posl]
            highestPrice = h[posh]

            maxPriceInScreen = float(math.ceil(highestPrice))
            minPriceInScreen = float(math.floor(lowestPrice))

            tradeDays = []


            ds = qaDataStuctDay.select_code(self.strCode)
            oclh = np.array(ds.data.loc[:, ['open', 'close', 'low', 'high']])
            datesOfThisStockTrade = ds.datetime.to_series()


            dates_value = datesOfThisStockTrade.values
            for i in range(len(dates_value)):
                vdt64 = dates_value[i]
                strTimeOfTradeDay = str(vdt64)[:10]
                tradeDays.append(strTimeOfTradeDay)

            tradeDays.reverse()
            oclh = oclh[::-1]

            assert (len(tradeDays) == len(oclh))

            self.canvasLeftPriceRuler.setPriceRange(maxPriceInScreen,minPriceInScreen)
            self.canvasBottomDateRuler.setTradeDayList(tradeDays, self.currentLoadKLineDayCount)

            self.canvasKLine.setTradeDayListAndOCLH(tradeDays, oclh, maxPriceInScreen, minPriceInScreen, \
                                                    self.currentLoadKLineDayCount)



            ###############################################################################################3
            # self.df_from_Tdx = QA_fetch_stock_day(
            #     '300439', self.time_to_Market_300439, self.time_to_day, 'pd')
            # # print(self.df_from_Tdx)
            #
            # self.ma05 = QA_indicator_MA(self.df_from_Tdx, 5)

            strTradeDayEnd = QA_util_get_last_day(strTradeDayEnd, self.moveForward)
            strTradeDayStart = QA_util_get_last_day(strTradeDayEnd, self.currentLoadKLineDayCount + 60)  # 均线系统需要提前获取

            qaDataStuctDayForMa = QA_fetch_stock_day_adv(self.strCode)
            qaDataStuctDayForMa = qaDataStuctDayForMa.select_time(strTradeDayStart, strTradeDayEnd)
            qaDataStuctDayForMa.to_qfq()

            ma03 = QA_indicator_MA(qaDataStuctDayForMa, 3)
            ma05 = QA_indicator_MA(qaDataStuctDayForMa, 5)
            ma08 = QA_indicator_MA(qaDataStuctDayForMa, 8)
            ma10 = QA_indicator_MA(qaDataStuctDayForMa, 10)
            ma12 = QA_indicator_MA(qaDataStuctDayForMa, 12)

            #30、35、40、45、50 和60
            ma30 = QA_indicator_MA(qaDataStuctDayForMa, 30)
            ma35 = QA_indicator_MA(qaDataStuctDayForMa, 35)
            ma40 = QA_indicator_MA(qaDataStuctDayForMa, 40)
            ma45 = QA_indicator_MA(qaDataStuctDayForMa, 45)
            ma50 = QA_indicator_MA(qaDataStuctDayForMa, 50)
            ma60 = QA_indicator_MA(qaDataStuctDayForMa, 60)


            #self.drawCoordinate()
            self.canvasGMMA.setPriceRange(maxPriceInScreen,minPriceInScreen)
            self.canvasGMMA.setTradeDays(tradeDays)

            self.canvasGMMA.set05MA(ma05, self.currentLoadKLineDayCount)
            self.canvasGMMA.set03MA(ma03, self.currentLoadKLineDayCount)
            self.canvasGMMA.set08MA(ma08, self.currentLoadKLineDayCount)
            self.canvasGMMA.set10MA(ma10, self.currentLoadKLineDayCount)
            self.canvasGMMA.set12MA(ma12, self.currentLoadKLineDayCount)
            #
            self.canvasGMMA.set30MA(ma30, self.currentLoadKLineDayCount)
            self.canvasGMMA.set35MA(ma35, self.currentLoadKLineDayCount)
            self.canvasGMMA.set40MA(ma40, self.currentLoadKLineDayCount)
            self.canvasGMMA.set45MA(ma45, self.currentLoadKLineDayCount)
            self.canvasGMMA.set50MA(ma50, self.currentLoadKLineDayCount)
            self.canvasGMMA.set60MA(ma60, self.currentLoadKLineDayCount)


        except Exception as ee:
            strErro = ee.__str__()
            print(strErro)

        pass