#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different types of elements."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
from modules.Computation import Matrix


class Bar:
    """Element barre pour efforts de traction."""

    def __init__(self, model, index):
        """Init."""
        self.index = index
        self.k = np.matrix([[1, -1], [-1, 1]])
        self.k *= model.material.E * model.material.S * model._nodes / model._lenght


class Poutre:
    """Element poutre pour efforts de flexion."""

    def __init__(self, model, index):
        """Init."""
        self.lenght = model._lenght / model._nodes
        self.index = index
        self.k = np.matrix([[12, 6 * self.lenght, -12, 6 * self.lenght], [6 * self.lenght, 4 * self.lenght**2, -6 * self.lenght, 2 * self.lenght**2],
                            [-12, -6 * self.lenght, 12, -6 * self.lenght], [6 * self.lenght, 2 * self.lenght**2, -6 * self.lenght, 4 * self.lenght**2]])
        self.k = model._I * model.material.E / (self.lenght**3) * self.k


class TreillisBar:
    """Element barre pour les treillis."""

    def __init__(self, model, nodes, lenght, alpha=0):
        """Init."""
        self.lenght = lenght
        self.nodes = nodes
        self.alpha = alpha
        self.A = np.matrix([[np.cos(self.alpha)**2, np.cos(self.alpha) * np.sin(self.alpha)],
                            [np.cos(self.alpha) * np.sin(self.alpha), np.sin(self.alpha)**2]])
        self.k = Matrix(4, 4)
        self.k.compose(self.A, 0, 0)
        self.k.compose(self.A, 2, 2)
        self.k.compose(-1*self.A, 2, 0)
        self.k.compose(-1*self.A, 0, 2)
        self.k *= model.material.E * model.material.S / self.lenght
