#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to diplay results of computa."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class DiscreteSlider(Slider):
    """Pass int values in the Slider."""
    def __init__(self, *args, **kwargs):
        self.inc = kwargs.pop('increment', 1)
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
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
