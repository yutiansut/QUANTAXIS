#encoding:utf-8


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_block


from QUANTAXIS_Monitor_GUI.ProgressDlgs.ProgressDlg_WithThreading import *
from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_CheckStockBlock_DB_Task import *
'''
------------------------------------------------
板块名称| 股票个数 | 上涨家数  | 下跌家数 | 资金流向 |
------------------------------------------------
板块1   |  22    |  10      |  12    |          |
------------------------------------------------
板块2   |  22    |  10      |  12    |          |
------------------------------------------------
板块2   |  22    |  10      |  12    |          |
------------------------------------------------

每个板块的股票列表基本信息
------------------------------------------------
股票名字| 收盘价 |  涨幅  | 成交额 |               |
------------------------------------------------



更新板块统计数据

输出类似的统计信息
2018-07-31 16.56.47:   沪深 上涨板块信息
1: 石油化工 板块 总共24只股票，50.0% 股票上涨

提示:-----以下是板块涨幅小于40%,不建议选择----

2: 原油期货 板块 总共8只股票，37.0% 股票上涨
3: 粤港澳自贸区 板块 总共11只股票，27.0% 股票上涨
4: 农业产品 板块 总共19只股票，26.0% 股票上涨
5: 传感器 板块 总共4只股票，25.0% 股票上涨
6: 动漫 板块 总共4只股票，25.0% 股票上涨
7: 包装食品 板块 总共21只股票，23.0% 股票上涨
8: 白酒 板块 总共17只股票，23.0% 股票上涨
9: 苹果供应链 板块 总共13只股票，23.0% 股票上涨


------------------  下跌板块信息    --------
1: 纺织服装设备 板块 总共7只股票，42.0%（3只）股票下跌
2: 分立器件 板块 总共6只股票，33.0%（2只）股票下跌
3: 新股次新股 板块 总共20只股票，25.0%（5只）股票下跌
4: 航母 板块 总共8只股票，25.0%（2只）股票下跌
5: 高铁 板块 总共12只股票，25.0%（3只）股票下跌
6: 智能家居 板块 总共27只股票，22.0%（6只）股票下跌
7: 船舶制造 板块 总共9只股票，22.0%（2只）股票下跌
8: 装饰工程 板块 总共9只股票，22.0%（2只）股票下跌
9: 超市连锁 板块 总共9只股票，22.0%（2只）股票下跌
'''


class MyTableModel(QAbstractTableModel):
    def __init__(self,stock_block_list=None, parent=None, *args):

        QAbstractTableModel.__init__(self, parent, *args)

        # 🛠 todo 实现排序，
        self.arraydata = [
                    ['22',  '44', '55', '22'],
                    ['050', '01', '02', '33'],
                    ['130', '11', '12', '43'],
                    ['220', '21', '22', '53'],
                    ['30',  '21', '22', '63'],
                    ['290', '21', '22', '73'],
                    ['220', '21', '22', '93']]

        self.stock_block_list = stock_block_list


    allRowNumberCount = 0
    data_row_from_df = None

    def rowCount(self, parent):
        if self.stock_block_list is not None:
            try:
                block_size = len(self.stock_block_list)
            except Exception as ee:
                errMsg = ee.__str__()
                print(errMsg)

            return block_size
        else:
            return 0

    #列的个数

    headerList = ['板块名字', '股票个数', '上涨家数', '下跌家数', '上涨比率','下跌比率']
    def columnCount(self, parent):
        return len(self.headerList)


    def data(self, index, role):
        #print("return date  => %d %d", index.row(), index.column())
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        else:
            #aData = self.arraydata[index.row()][index.column()]

            if self.stock_block_list is not None:
                #data_row_from_df = self.block_list_df.iloc[[2]]
                #print(data_row_from_df)

                if index.column() == 0:
                    dictKey = list(self.stock_block_list)[index.row()]
                    aQVariant = QVariant(dictKey)

                elif index.column() == 1:
                    dictKey = list(self.stock_block_list)[index.row()]
                    stockCount = self.stock_block_list[dictKey]['count']
                    aQVariant = QVariant(stockCount)

                elif index.column() == 2:
                    dictKey = list(self.stock_block_list)[index.row()]
                    stockCount = self.stock_block_list[dictKey]['up']
                    aQVariant = QVariant(stockCount)

                elif index.column() == 3:
                    dictKey = list(self.stock_block_list)[index.row()]
                    stockCount = self.stock_block_list[dictKey]['down']
                    aQVariant = QVariant(stockCount)
                else:
                    aQVariant = QVariant("")
            else:
                strMsg = "{},{}".format(index.row(), index.column())
                aQVariant = QVariant(strMsg)
            return aQVariant


    # 🛠 todo 实现排序，
    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        #self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        #if order == Qt.DescendingOrder:
        #    self.arraydata.reverse()
        #self.emit(SIGNAL("layoutChanged()"))

        try:
            if order == Qt.DescendingOrder:

                for rowIndex in range(len(self.arraydata)):
                    #maxRowLine = self.arraydata[rowIndex]
                    for compareRowIndex in range( len(self.arraydata), rowIndex , -1):
                        if self.arraydata[rowIndex][Ncol] > self.arraydata[compareRowIndex-1][Ncol]:
                            #swap maxRowIndex  compareRowIndex
                            tmepRow = self.arraydata[rowIndex]
                            self.arraydata[rowIndex] = self.arraydata[compareRowIndex-1]
                            self.arraydata[compareRowIndex-1] = tmepRow

            elif order == Qt.AscendingOrder:

                for rowIndex in range(len(self.arraydata)):
                    #maxRowLine = self.arraydata[rowIndex]
                    for compareRowIndex in range( len(self.arraydata), rowIndex , -1):
                        if self.arraydata[rowIndex][Ncol] < self.arraydata[compareRowIndex-1][Ncol]:
                            #swap maxRowIndex  compareRowIndex
                            tmepRow = self.arraydata[rowIndex]
                            self.arraydata[rowIndex] = self.arraydata[compareRowIndex-1]
                            self.arraydata[compareRowIndex-1] = tmepRow

            self.layoutChanged.emit()

        except Exception as ee:
            strError = ee.__str__()
            print(strError)
            pass

            #print("")
            #passself.layoutChanged()
        #self.layoutChanged()



    def headerData(self, col, orientation, role): # real signature unknown; restored from __doc__
        """ headerData(self, int, Qt.Orientation, role: int = Qt.DisplayRole) -> Any """

        # else:
        #     return QVariant("0")
        # #if Qt_Orientation == 1:
        #     # if p_int == 0:
        #     #     return QVariant(self.headerList[0])
        #     # if p_int == 1:
        #     #     return QVariant(self.headerList[0])
        #     # if p_int == 2:
        #     #     return QVariant(self.headerList[0])
        #     # if p_int == 3:
        #     #     return QVariant(self.headerList[0])
        # return QVariant(self.headerList[p_int])

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
           return QVariant(self.headerList[col])
        return QVariant()

        # if role== Qt.DisplayRole:
        #     if orientation == Qt.Horizontal:
        #         return QVariant(self.headerList[col])
        #     else:
        #         return QVariant(col)
        #pass


    def setDataList(self):
        self.allRowNumberCount = self.allRowNumberCount + 1


        #self.layoutAboutToBeChanged.emit()
        #self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        #self.layoutChanged.emit()
        pass

class TabBlockStatistics(QWidget):
    def __init__(self, parent=None):
        super(TabBlockStatistics, self).__init__(parent)



    def initUI(self):

        try:

            #######################################################################################
            self.tableViewBlock = QTableView(self)

            self.modelBlock = MyTableModel(self,stock_block_list=None)

            #titleBlockNames = ['板块名字', '股票个数', '上涨家数', '下跌家数', '上涨比率','下跌比率']

            #self.modelBlock.setHorizontalHeaderLabels(titleBlockNames)

            self.tableViewBlock.setModel(self.modelBlock)

            # set the minimum size
            self.tableViewBlock.setMinimumSize(400, 300)

            # hide grid
            self.tableViewBlock.setShowGrid(True)

            # set the font
            font = QFont("Courier New", 13)
            self.tableViewBlock.setFont(font)

            # hide vertical header
            vh = self.tableViewBlock.verticalHeader()
            vh.setVisible(False)

            # set horizontal header properties
            hh = self.tableViewBlock.horizontalHeader()
            hh.setStretchLastSection(True)

            # set column width to fit contents
            #self.tableViewBlock.resizeColumnsToContents()

            # set row height
            # nrows = len(self.tabledata)
            # for row in xrange(nrows):
            #     tv.setRowHeight(row, 18)

            # enable sorting
            #self.tableViewBlock.setSortingEnabled(True)

            self.tableViewBlock.setSortingEnabled(True)


            #self.modelBlock = QStockBlockListModel()

            # item = QStandardItem(str("1data"))
            # self.modelBlock.setItem(1, 0, item)
            #
            # item = QStandardItem(str("z3ata"))
            # self.modelBlock.setItem(2, 0, item)
            #
            # item = QStandardItem(str("f4data"))
            # self.modelBlock.setItem(3, 0, item)
            # # self.modelBlock.setItem(0, 1, item)
            # self.modelBlock.setItem(0, 2, item)
            # self.modelBlock.setItem(0, 3, item)
            #
            # self.tableViewBlock.setModel(self.modelBlock)
            #
            # self.tableViewBlock.sortByColumn(0,Qt.AscendingOrder)

            #######################################################################################
            # self.tableViewSubBockStocks = QTableView(self)
            #
            # self.modelSubBlockStock = QStandardItemModel()
            # titleSubBlockNames = ['股票代码', '收盘价', '上涨', '成交额', '成交量']
            # self.modelSubBlockStock.setHorizontalHeaderLabels(titleSubBlockNames)
            #
            # self.tableViewSubBockStocks.setModel(self.modelSubBlockStock)
            #####################################################################################
            pass
        except Exception as ee:
            print(ee)

        self.txtArea = QTextEdit(self)
        self.txtArea.setMaximumWidth(300)


        self.bntLoadData = QPushButton()
        self.bntLoadData.setText('加载数据 🥑🍋🥝')

        self.bntLoadData.clicked.connect(self.LoadDataClick)

        self.bntStatistic = QPushButton()
        self.bntStatistic.setText('统计板块涨跌 📊🗂💹')


        self.bntStatistic.clicked.connect(self.doStatistic)

        #######################################################################################
        # layout:
        self.myRootLayout = QHBoxLayout(self)

        self.myLeftLayout = QVBoxLayout(self)
        self.myRightLayout = QVBoxLayout(self)

        self.myLeftBottomButtonsHLayout = QHBoxLayout(self)
        self.myLeftBottomButtonsHLayout.addWidget(self.bntLoadData)
        self.myLeftBottomButtonsHLayout.addWidget(self.bntStatistic)

        self.myRootLayout.addLayout(self.myLeftLayout)
        self.myRootLayout.addLayout(self.myRightLayout)

        self.myLeftLayout.addWidget(self.tableViewBlock)
        #self.myLeftLayout.addWidget(self.tableViewSubBockStocks)
        self.myLeftLayout.addLayout(self.myLeftBottomButtonsHLayout)
        self.myRightLayout.addWidget(self.txtArea)
        self.setLayout(self.myRootLayout)

        #######################################################################################
        #
        pass


    def LoadDataClick(self):



        try:

            # self.block_list_df = QA_fetch_stock_block()
            # print(self.block_list_df)
            #
            # blockNameList = {}
            #
            # self.block_list_df = self.block_list_df.set_index(['blockname'])
            # for iIndex in self.block_list_df.index:
            #     #row = self.block_list_df.iloc(iIndex)
            #     #strBlockName = self.block_list_df.loc[iIndex,'blockname']
            #     strBlockName = iIndex
            #     try:
            #         dict = blockNameList[strBlockName]
            #         dict['count'] = dict['count'] + 1
            #
            #     except Exception as ee:
            #         blockNameList[strBlockName] = 0
            #
            #         dictNew = {}
            #         dictNew['up']=0
            #         dictNew['down']=0
            #         dictNew['count']=0
            #         dictNew['upRatio']=0.0
            #         dictNew['downRation']=0.0
            #         blockNameList[strBlockName] = dictNew


            #统计上涨家数

            thread_check_stock_block = QThread_Check_StockBlock_DB()
            dlg = ProgressDlg_WithQThread(self, thread_check_stock_block,"统计板块信息","统计板块信息")
            dlg.startMyThread()
            dlg.exec()

            blockStatisList = thread_check_stock_block.blockStatisticList


            self.my_model = MyTableModel(stock_block_list = blockStatisList)
            self.tableViewBlock.setModel(self.my_model)
            self.tableViewBlock.update()

        except Exception as ee:
            errorMsg = ee.__str__()
            print(errorMsg)

        #self.
        # model = self.tableViewBlock.model(block_list_df)
        #
        #
        # self.table_model(self.modelBlock)
        #model.reloadDate()
        #model.layoutChanged.emit()

        #self.tableViewBlock.update()
        pass


    def doStatistic(self):
        pass