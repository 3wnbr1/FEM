#! /usr/bin/python3
# coding: utf-8


"""Matplotlib QtDesigner Widget."""


import numpy as np
import matplotlib.image as image
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
        # Initialise l'espace du graphique
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(model.legend['title'])

        # Afiche la courbe de deformee coloree en fonction du resulat selectionné
        if t == 0:
            lc = self.colorline(model.deformee[0], model.deformee[1], np.round(np.absolute(model.deplacements[:-1:]), 12))
            cbar = self.fig.colorbar(lc)
            cbar.ax.set_title(r"Déplacement en $mm$")
        elif t == 1:
            lc = self.colorline(model.deformee[0], model.deformee[1], np.round(np.absolute(model.contraintes), 12))
            cbar = self.fig.colorbar(lc)
            cbar.ax.set_title(r"Contraintes en $MPa$")

        # Affiche l'effort et les liasons
        for effort in model.efforts:
            self.ax.arrow(effort[0], effort[1], effort[2], effort[3], head_width=effort[4], head_length=effort[5], fc='m', ec='m')

        encastrement_horiz = image.imread('ui/liaisons/encastrement_horiz.jpg')
        encastrement_vert = image.imread('ui/liaisons/encastrement_vert.jpg')
        glissiere = image.imread('ui/liaisons/glissiere.jpg')
        rotule = image.imread('ui/liaisons/rotule.jpg')
        ponctuelle = image.imread('ui/liaisons/ponctuelle.jpg')

        if model.__class__.__name__ == "PoutreEnTraction":
            self.ax.set_xlim([-0.1, 0.1])
            self.ax.set_ylim([-50, model._lenght + 50])
            self.ax.get_xaxis().set_visible(False)
            self.ax.imshow(encastrement_horiz, aspect='auto', extent=(-0.01, 0.01, -30, 5))
        elif model.__class__.__name__ == "PoutreEnFlexion":
            if model.selected == 0:
                self.ax.imshow(encastrement_vert, aspect='auto', extent=(-20, 10, -0.5, 0.5))
            if model.selected == 1:
                self.ax.imshow(encastrement_vert, aspect='auto', extent=(-20, 10, -0.005, 0.005))
                self.ax.imshow(glissiere, aspect='auto', extent=(model._lenght-20, model._lenght + 20, -0.01, 0))
            if model.selected == 2:
                self.ax.imshow(rotule, aspect='auto', extent=(-20, 20, -0.03, 0))
                self.ax.imshow(ponctuelle, aspect='auto', extent=(model._lenght-20, model._lenght + 20, -0.03, 0))
        elif model.__class__.__name__ == "TreilliSimple":
            pass

        # Affiche la poutre initiale
        self.ax.plot(model.initial[0], model.initial[1], linewidth=2, color='k', linestyle="-.")
        self.ax.set_xlabel(model.legend['xtitle'])
        self.ax.set_ylabel(model.legend['ytitle'])
        self.draw()

    def colorline(self, x, y, z):
        """Plot a colored line with coordinates x and y."""
        z = np.asarray(z)
        segments = make_segments(x, y)
        lc = LineCollection(segments, array=z, cmap='jet', linewidth=6, alpha=1)
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
