#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different types of elements."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np


class Element:
    """Class used to store different elements types."""
    class Bar:
        def __init__(self, model, index):
            self.index = index
            self.k = np.matrix([[1, -1], [-1, 1]])
            self.k = self.k * model.material.E * model.material.S * model.n / model.L

        def __repr__(self):
            return "<Element barre %d>" % self.index
