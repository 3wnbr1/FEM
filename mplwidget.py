"""Matplotlib QtDesigner Widget."""


import numpy as np
from cm import colorline
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):
    """MplCanvas."""

    def __init__(self):
        """Init."""
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def graph(self, model):
        """Plot deformée."""
        self.ax1.cla()
        self.ax1.set_title('Deformée')
        lc = colorline(model.deformee[0], np.sin(model.deformee[0]), cmap='jet')
        self.fig.colorbar(lc)
        self.ax1.plot(model.initial[0], model.initial[1], label="Inital")
        self.ax1.legend()
        self.draw()


class MplWidget(QtWidgets.QWidget):
    """QtDesigner QtWidget Promotion Class."""

    def __init__(self, parent=None):
        """Init."""
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def set_figure(self):
        """Set figure."""
        self.canvas.subplots()
