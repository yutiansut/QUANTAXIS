from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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


class TabBlockStatistics(QWidget):
    def __init__(self, parent=None):
        super(TabBlockStatistics, self).__init__(parent)



    def initUI(self):

        #######################################################################################
        #self.qTableView = QTableView(self)
        self.tableViewBlock = QTableView(self)

        self.modelBlock = QStandardItemModel()
        titleBlockNames = ['板块名字', '股票个数', '上涨家数', '下跌家数', '上涨比率','下跌比率']
        self.modelBlock.setHorizontalHeaderLabels(titleBlockNames)

        item = QStandardItem(str("1data"))
        self.modelBlock.setItem(1, 0, item)

        item = QStandardItem(str("z3ata"))
        self.modelBlock.setItem(2, 0, item)

        item = QStandardItem(str("f4data"))
        self.modelBlock.setItem(3, 0, item)
        # self.modelBlock.setItem(0, 1, item)
        # self.modelBlock.setItem(0, 2, item)
        # self.modelBlock.setItem(0, 3, item)

        self.tableViewBlock.setModel(self.modelBlock)

        self.tableViewBlock.sortByColumn(0,Qt.AscendingOrder)

        #######################################################################################
        self.tableViewSubBockStocks = QTableView(self)

        self.modelSubBlockStock = QStandardItemModel()
        titleSubBlockNames = ['股票代码', '收盘价', '上涨', '成交额', '成交量']
        self.modelSubBlockStock.setHorizontalHeaderLabels(titleSubBlockNames)

        self.tableViewSubBockStocks.setModel(self.modelSubBlockStock)
        #####################################################################################

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
        self.myLeftLayout.addWidget(self.tableViewSubBockStocks)

        self.myLeftLayout.addLayout(self.myLeftBottomButtonsHLayout)

        self.myRightLayout.addWidget(self.txtArea)

        self.setLayout(self.myRootLayout)

        #######################################################################################
        #


        pass


    def LoadDataClick(self):

        pass


    def doStatistic(self):
        pass