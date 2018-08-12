

import os
import random
import sys

import matplotlib
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from AnyQt import QtCore, QtWidgets
from AnyQt.QtWidgets import *
from AnyQt.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
                             QMessageBox, QSizePolicy, QVBoxLayout, QWidget)

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')



progname = os.path.basename(sys.argv[0])
progversion = "0.1"

global n_drops
global scat
global rain_drops
n_drops = 100


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        x = range(1, 7)
        y = (22, 30, 30, 29, 32, 31)
        self.ax.set_xticklabels([i+100 for i in x])
        self.ax.set_yticklabels(y)
        self.ax.grid(True)

        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.main_widget = QtWidgets.QWidget(self)

        vbox = QtWidgets.QVBoxLayout(self.main_widget)

        self.canvas = MyMplCanvas(
            self.main_widget, width=5, height=4, dpi=100)  # attention###
        vbox.addWidget(self.canvas)

        hbox = QtWidgets.QHBoxLayout(self.main_widget)
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
        self.exit_button = QPushButton("exit", self)

        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.exit_button.clicked.connect(self.on_exit)

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.exit_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        global n_drops
        global scat
        global rain_drops
        rain_drops = np.zeros(n_drops, dtype=[('position', float, 2)])
        self.scat = self.canvas.axes.scatter(
            rain_drops['position'][:, 0], rain_drops['position'][:, 1], s=10, lw=0.5)

    def update_line(self, i):
        global n_drops
        global scat
        global rain_drops
        rain_drops['position'] = np.random.uniform(0, 100, (n_drops, 2))

        self.scat.set_offsets(rain_drops['position'])

        return self.scat,

    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line,
                                 blit=True, interval=25)

    def on_stop(self):
        self.ani._stop()

    def on_exit(self):
        self.close()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    App.exit()
    sys.exit(App.exec_())
