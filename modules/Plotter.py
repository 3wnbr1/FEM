#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to diplay results of computa."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class Canvas(FigureCanvasQTAgg):
    """Matplotlib Figure for FEM model."""

    def __new__(self):
        self.__init_subclass__()
        return super(FigureCanvasQTAgg, self).__new__(self)

    def __init_subclass__(self):
        """Init."""
        self.fig = plt.figure()
        self.ax = []

    def deformee(self, x, y):
        self.ax.append(self.fig.add_subplot())
        self.ax[-1].plot(x, y, label="déformée")


class DiscreteSlider(Slider):
    """Pass int values in the Slider."""

    def __init__(self, *args, **kwargs):
        """Init."""
        self.inc = kwargs.pop('increment', 1)
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        """Set slider value."""
        discrete_val = int(val / self.inc) * self.inc
        xy = self.poly.xy
        xy[2] = discrete_val, 1
        xy[3] = discrete_val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon:
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson:
            return
        for cid, func in self.observers.items():
            func(discrete_val)
