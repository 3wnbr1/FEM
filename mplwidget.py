#! /usr/bin/python3
# coding: utf-8


"""Matplotlib QtDesigner Widget."""


import numpy as np
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


def make_segments(x, y):
    """Make segments."""
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


class MplCanvas(FigureCanvasQTAgg):
    """MplCanvas."""

    def __init__(self):
        """Init."""
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def graph(self, model, t=0):
        """Plot deformée."""
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(model.legend['title'])
        lc = self.colorline(model.deformee[0], model.deformee[1], np.absolute(model.deformee[1]))
        cbar = self.fig.colorbar(lc)
        if t == 0:
            cbar.ax.set_title(r"Déformation en $mm$")
        elif t == 1:
            cbar.ax.set_title(r"Contraintes en $MPa$")
        if len(model.initial) == 2:
            self.ax.plot(model.initial[0], model.initial[1], linewidth=3, color='k')
        else:
            for line in model.initial:
                self.ax.plot(line[0], line[1], linewidth=3, color='k')
        self.ax.set_xlabel(model.legend['xtitle'])
        self.ax.set_ylabel(model.legend['ytitle'])
        self.draw()

    def colorline(self, x, y, z):
        """Plot a colored line with coordinates x and y."""
        z = np.asarray(z)
        segments = make_segments(x, y)
        lc = LineCollection(segments, array=z, cmap='jet', linewidth=3, alpha=1)
        self.ax.add_collection(lc)
        return lc


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
