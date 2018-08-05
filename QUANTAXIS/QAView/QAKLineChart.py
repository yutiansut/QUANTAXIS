import os
import time
from pyecharts import Kline
from PyQt5.QtCore import QObject, pyqtSignal

class KlineChartSignal(QObject):
    html_chart_generated = pyqtSignal(str)

    def connect_html_chart_generated(self, function, message=None):
        if function is not None:
            self.html_chart_generated.connect(function)
            self.html_chart_generated.emit(message)

class KlineChart(Kline):

    signal = KlineChartSignal()

    def __init__(self):
        super().__init__( background_color = '#0000000')
        self._html_chart_directory = ".\\"
        self._html_chart_name = None
        self._kline_data = [] #[[2320.26, 2320.26, 2287.3, 2362.94], [2300, 2291.3, 2288.26, 2308.38]]
        self._x_coordinate = []

    def clear_kline_data(self):
        self._kline_data.clear()

    def add_kline_data(self, d1, d2, d3, d4):
        """
        K线图四个要素
        :param d1:开盘价
        :param d2:收盘价
        :param d3:最低价
        :param d4:最高价
        :return:
        """
        self._kline_data.append([d1, d2, d3, d4])

    def set_chart_data(self, xargs, *args):
        self._kline_data.clear()
        for data in args:
            self._kline_data.append(data)
            print(data)
        self._x_coordinate.clear()
        self._x_coordinate = xargs

    def set_chart_size(self, width, height):
        self.set_width(width)
        self.set_height(height)

    def set_width(self, width = 800):
        """
        设置图形输出的宽度
        :param width:
        :return:
        """
        if width < 100:
            return
        self.width = width

    def set_height(self, height = 600):
        """
        设置图形输出的高度
        :param height:
        :return:
        """
        if height < 100:
            return
        self.height = height

    def set_html_chart_name(self, name):
        self._html_chart_name = name

    def connect_slot(self, function):
        path = "{0}\\{1}".format(self._html_chart_directory, self._html_chart_name)
        absolute_path = os.getcwd() + "\\" + path
        tryCount = 3
        while tryCount > 0:
            if os.path.exists(absolute_path):
                self.signal.connect_html_chart_generated(function, absolute_path)
                return
            else:
                time.sleep(1)
            tryCount =- 1

    def create_chart(self, legend):
        #self.clear_chart_html_file()
        self.add(legend, self._x_coordinate, self._kline_data)
        #self.use_theme('dark')
        if self._html_chart_name is not None:
            path = "{0}\\{1}".format(self._html_chart_directory, self._html_chart_name)
            self.render(path)
        else:
            pass

    def clear_chart_html_file(self):
        self.del_file(self._html_chart_directory)

    def del_file(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)

    def on_chart_generated(self, path):
        print(path)



if __name__=="__main__":

    print(os.getcwd())

    def on_generated(message):
        print(message)



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
    chart = KlineChart()
    chart.set_chart_size(1024, 600)
    chart.set_html_chart_name("adadada.html")
    chart.set_chart_data(["2017/7/{}".format(i + 1) for i in range(31)], *v1)
    chart.create_chart("chart")
    chart.connect_slot(on_generated)




















"""
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
kline = Kline("K 线图示例")
kline.width = 1024
kline.height = 768
kline.add("日K", ["2017/7/{}".format(i + 1) for i in range(31)], v1)
kline.render()
"""


