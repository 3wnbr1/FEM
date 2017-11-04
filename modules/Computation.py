#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Backend module with Mathematic objects and functions for computation."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np


class Matrix(np.matrix):
    """Extension of the np.matrix. """

    def __new__(self, x, y, value=0.0):
        return super(Matrix, self).__new__(self, [[value] * x] * y)

    def compose(self, matrix, x, y):
        m = len(matrix)
        for n in range(m):
            self[y + n, x:x + m] += matrix[n]

    def remove_null(self, n):
        return np.delete(np.delete(self, [n], axis=1), [n], axis=0)
