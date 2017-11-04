#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different types of elements."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np


class Element:
    """Class used to store different elements types."""
    def __init__(self, model, index):
        pass

    def __repr__(self):
        return "<Element %s %d>" % (self.__class__, self.index)  # TODO return only class name as string


class Bar(Element):
    """Element barre pour efforts de traction."""
    def __new__(self, model, index):
        self.__init_subclass__(model, index)
        return super(Element, self).__new__(self)

    def __init_subclass__(self, model, index):
        self.index = index
        self.k = np.matrix([[1, -1], [-1, 1]])
        self.k = self.k * model.material.E * model.material.S * model._elements / model._lenght


class Poutre(Element):
    """Element poutre pour efforts de flexion."""
    def __new__(self, model, index):
        self.__init_subclass__(model, index)
        return super(Element, self).__new__(self)

    def __init_subclass__(self, model, index):
        l = model._elements / model._lenght
        self.index = 1
        self.k = np.matrix([[12, 6*l, -12, 6*l], [6*l, 4*l**2, -6*l, 2*l**2], [-12, -6*l, 12, -6*l], [6*l, 2*l**2, -6*l, 4*l**2]])
        self.k = self.k * model._I*model.material.E / (l**3)
