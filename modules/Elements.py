#! /usr/bin/python3
# coding: utf-8


"""Used to store different types of elements."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
from modules.Computation import Matrix, DeformationTensor


class Bar:
    """Element barre pour efforts de traction."""

    def __init__(self, model, index):
        """Init."""
        self.index = index
        self.material = model.material
        self.lenght = model._lenght / model._nodes
        self.k = np.matrix([[1, -1], [-1, 1]])
        self.k *= model.material.E * model.section.S * self.lenght

    def deformationsTensor(self, u):
        """Return -> DeformationTensor."""
        d = DeformationTensor(self)
        d.vector[0] = u / self.lenght
        return d


class Poutre:
    """Element poutre pour efforts de flexion."""

    def __init__(self, model, index):
        """Init."""
        self.material = model.material
        self.lenght = model._lenght / model._nodes
        self.index = index
        a, b, c , d = 12, 6*self.lenght, 4*self.lenght**2, 2*self.lenght**2
        self.k = np.matrix([[a, b, -1*a, b],[b,c,-1*b, d],[-1*a, -1*b, a, -1*b],[b, d, -1*b, c]])
        self.k = model.section.IG * model.material.E / (self.lenght**3) * self.k

    def deformationsTensor(self, v, theta):
        """Return -> DeformationTensor."""
        d = DeformationTensor(self)
        d.vector[3] = v / (2*self.lenght)
        return d


class TreillisBar:
    """Element barre pour les treillis."""

    def __init__(self, model, nodes, lenght, alpha=0):
        """Init."""
        self.material = model.material
        self.lenght = lenght
        self.nodes = nodes
        self.alpha = alpha
        self.A = np.matrix([[np.cos(self.alpha)**2, np.cos(self.alpha) * np.sin(self.alpha)],
                            [np.cos(self.alpha) * np.sin(self.alpha), np.sin(self.alpha)**2]])
        self.k = Matrix(4, 4)
        self.k.compose(self.A, 0, 0)
        self.k.compose(self.A, 2, 2)
        self.k.compose(-1 * self.A, 2, 0)
        self.k.compose(-1 * self.A, 0, 2)
        self.k *= model.material.E * model.section.S / self.lenght
