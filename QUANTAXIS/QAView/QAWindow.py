import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import QUANTAXIS as QA
from QUANTAXIS.QAView.QAKLineChart import *
from QUANTAXIS.QAView.QAMACD import *

class QAWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.roll)
        self.kline_chart = KlineChart()
        self.macd_chart = MACDChart()
        self.get_stock_list()
        self.init_layout()
        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle(r"K线图")
        self.setStyleSheet("background:black")
        self.loadStyleSheet()
        self.center()
        self.show()
        #self.showMaximized()

    def loadStyleSheet(self):
        """
        加载QSS全局样式文件
        :return:
        """
        file = QFile('qss/mainwindow.qss')
        #file = QFile('qss/my.qss')
        file.open(QFile.ReadOnly)
        style = file.readAll()
        sheet = str(style, encoding='utf8')
        qApp.setStyleSheet(sheet)
        file.close()

    def resizeEvent(self, event):
        """
        窗口大小改变时需要动态调整图形
        :param event:
        :return:
        """
        indexList = self._stock_list_bar.selectionModel().selectedIndexes()
        if len(indexList) <=0 :
            pass
        for index in indexList:
            print(index.row())
            self.table_item_selected(index)
            return

    def get_stock_list(self):
        """
        获取股票代码
        :return:
        """
        df = QA.QA_fetch_stock_list_adv().loc[:,['code','name']]
        self.stock_list = df.values

    def center(self):
        """
        主窗口居中显示函数
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def init_layout(self):
        """
        界面布局
        :return:
        """
        #定义GridLayout布局，主界面分成3行3列，第一行放按钮，第一列放表格，第二列放两张图形，最后一列放滚动文字
        self._grid = QGridLayout()
        self._grid.setSpacing(5)
        self._gridwiget = QWidget(self)
        self._gridwiget.setLayout(self._grid)
        self.setCentralWidget(self._gridwiget)
        self._grid.setRowStretch(0, 1)
        self._grid.setRowStretch(1, 20)
        self._grid.setRowStretch(2, 8)
        self._grid.setColumnStretch(0, 1)
        self._grid.setColumnStretch(1, 8)
        self._grid.setColumnStretch(2, 1)
        self._grid.setColumnMinimumWidth(0, 230)
        self._grid.setColumnMinimumWidth(2, 200)

        #表格第一行设置为菜单按钮行
        labTest = QLabel("QUANTAXIS WINDOW")
        labTest.setStyleSheet("background:rgb(255,255,255)")
        self._grid.addWidget(labTest, 0, 0, 1, 3)

        #添加tabwidget,第一列为table,放在tab里，有多个table
        self._left_tabwidget = QTabWidget(self)
        self._left_tabwidget.setTabPosition(QTabWidget.West)
        self._left_tabwidget.setTabShape(QTabWidget.Rounded)
        self._grid.addWidget(self._left_tabwidget, 1, 0, 2, 1)

        #股票代码列表，放进tab里
        self._stock_list_bar = QTableView()
        self._stock_list_bar.setObjectName("stocklisttable")
        column_names = ["序号","代码","名称"]
        self.fill_table(self._stock_list_bar, "股票代码", column_names, self.stock_list)

        #添加kline_chart
        self._k_line_chart = QWebEngineView()
        self._k_line_chart.page().setBackgroundColor(Qt.black)
        self._grid.addWidget(self._k_line_chart, 1, 1)

        #添加bar_chart
        self._macd_bar_chart = QWebEngineView()
        self._macd_bar_chart.page().setBackgroundColor(Qt.black)
        self._grid.addWidget(self._macd_bar_chart, 2, 1)

        #添加滚动文字在最后一列中
        self._news_message_grid = QGridLayout()
        self._news_message_grid_wiget = QWidget(self)
        self._news_message_grid_wiget.setLayout(self._news_message_grid)
        self._news_message_grid_wiget.setStyleSheet("background: rgb(50,50,50)")
        self._grid.addWidget(self._news_message_grid_wiget, 1, 2, 2, 1)

        self._news_title = QLabel("最新资讯")
        self._news_title.setObjectName("news_title")
        self._news_title.setAlignment(Qt.AlignCenter)
        self._news_message_grid.addWidget(self._news_title, 0,0)

        self._news_message_text = QTextEdit()
        self._news_message_text.setReadOnly(True)
        self._news_message_grid.addWidget(self._news_message_text, 1,0)

        self.set_news(self._news_message_text, "NEWS !!!! THIS IS A TEST NEWs BY QA")



    def fill_table(self, table_view, table_view_name, column_names, data_list):
        """
        填充左侧表格内容
        :param table_view:表格对象
        :param table_view_name:
        :param column_names:列名数组
        :param data_list:数据列表
        :return:
        """
        if table_view is None:
            return
        if column_names is None or len(column_names) <= 0:
            return
        self._left_tabwidget.addTab(table_view, table_view_name)
        currentBar = self._left_tabwidget.tabBar()
        currentBar.setShape(QTabBar.RoundedEast)
        model = QStandardItemModel()
        model.setColumnCount(len(column_names))
        for i in range(len(column_names)):
            model.setHeaderData(i, Qt.Horizontal, column_names[i])
        table_view.setModel(model)
        table_view.setColumnWidth(0, 40)
        table_view.setColumnWidth(1, 60)
        table_view.setColumnWidth(2, 80)
        hv = QHeaderView(Qt.Vertical)
        hv.hide()
        table_view.setVerticalHeader(hv)
        table_view.horizontalHeader().setStretchLastSection(True)#最后一列填充整个表头
        table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.clicked.connect(self.table_item_selected)

        if data_list is None or len(column_names) <= 0:
            return
        for j in range(len(data_list)):
            model.setItem(j, 0, QStandardItem("{0}".format(j)))
            model.setItem(j, 1, QStandardItem(data_list[j][0]))
            model.setItem(j, 2, QStandardItem(data_list[j][1]))
            model.item(j, 0).setForeground(QBrush(Qt.white))
            model.item(j, 1).setForeground(QBrush(Qt.darkYellow))
            model.item(j, 2).setForeground(QBrush(Qt.yellow))



    def table_item_selected(self, index):
        row = index.row()
        print(self.stock_list[row][0], self.stock_list[row][1])

        v1 = [[2320.26, 2320.26, 2287.3, 2362.94], [2300, 2291.3, 2288.26, 2308.38],
              [2295.35, 2346.5, 2295.35, 2345.92], [2347.22, 2358.98, 2337.35, 2363.8],
              [2360.75, 2382.48, 2347.89, 2383.76], [2383.43, 2385.42, 2371.23, 2391.82],
              [2377.41, 2419.02, 2369.57, 2421.15], [2425.92, 2428.15, 2417.58, 2440.38],
              [2411, 2433.13, 2403.3, 2437.42], [2432.68, 2334.48, 2427.7, 2441.73],
              [2430.69, 2418.53, 2394.22, 2433.89], [2416.62, 2432.4, 2414.4, 2443.03],
              [2441.91, 2421.56, 2418.43, 2444.8], [2420.26, 2382.91, 2373.53, 2427.07],
              [2383.49, 2397.18, 2370.61, 2397.94], [2378.82, 2325.95, 2309.17, 2378.82],
              [2322.94, 2314.16, 2308.76, 2330.88], [2320.62, 2325.82, 2315.01, 2338.78],
              [2313.74, 2293.34, 2289.89, 2340.71], [2297.77, 2313.22, 2292.03, 2324.63],
              [2322.32, 2365.59, 2308.92, 2366.16], [2364.54, 2359.51, 2330.86, 2369.65],
              [2332.08, 2273.4, 2259.25, 2333.54], [2274.81, 2326.31, 2270.1, 2328.14],
              [2333.61, 2347.18, 2321.6, 2351.44], [2340.44, 2324.29, 2304.27, 2352.02],
              [2326.42, 2318.61, 2314.59, 2333.67], [2314.68, 2310.59, 2296.58, 2320.96],
              [2309.16, 2286.6, 2264.83, 2333.29], [2282.17, 2263.97, 2253.25, 2286.33],
              [2255.77, 2270.28, 2253.31, 2276.22]]

        self.kline_chart.set_chart_size(self._k_line_chart.width()-20, self._k_line_chart.height()-20)
        self.kline_chart.set_html_chart_name(self.generate_random_chart_name())
        self.kline_chart.set_chart_data(["2017/7/{}".format(i + 1) for i in range(31)], *v1)
        self.kline_chart.create_chart("chart")
        self.kline_chart.connect_slot(self.load_kline_chart)

        v2 = [2309.16, 2286.6, 2264.83, 2333.29, 2282.17, 2263.97, 2253.25, 2286.33]

        self.macd_chart.set_chart_size(self._macd_bar_chart.width() - 20, self._macd_bar_chart.height() - 20)
        self.macd_chart.set_bar_chart_name(self.generate_random_chart_name())
        self.macd_chart.set_chart_data(["2017/7/{}".format(i + 1) for i in range(8)], v2)
        self.macd_chart.create_chart("bar")
        self.macd_chart.connect_slot(self.load_macd_chart)



    def load_kline_chart(self, path):
        self._k_line_chart.load(QUrl.fromLocalFile(path))
        self._k_line_chart.show()

    def load_macd_chart(self, path):
        self._macd_bar_chart.load(QUrl.fromLocalFile(path))
        self._macd_bar_chart.show()
        print(path)

    def generate_random_chart_name(self):
        return "kline_chart_{0}.html".format(random.randint(1, 10000))

    def set_news(self, textEdit, message):
        textEdit.setText(message)

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def roll(self):
        print("timer")


def view():
    app = QApplication(sys.argv)
    win = QAWindow()
    sys.exit(app.exec_())
if __name__=="__main__":
    app = QApplication(sys.argv)
    win = QAWindow()
    sys.exit(app.exec_())