#! /usr/bin/python3
# coding: utf-8


"""Backend module with Mathematic objects and functions for computation."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
from numba import jit


def nodesCombination(lst):
    """Return nodes combinations as list."""
    for x in lst:
        for y in lst:
            yield [x, y]


class Matrix(np.matrix):
    """Extension of the np.matrix."""

    def __new__(self, x, y, value=0.0):
        """Inheritance."""
        return super(Matrix, self).__new__(self, [[value] * x] * y)

    @jit
    def compose(self, matrix, x, y):
        """Composes matrices."""
        m = len(matrix)
        for n in range(m):
            self[y + n, x:x + m] += matrix[n]

    def remove_null(self, n):
        """Remove n-th row and column of the Matrix."""
        return np.delete(np.delete(self, [n], axis=1), [n], axis=0)


class DynamicArray:
    """Dynamic array class for computation purposes."""

    def __init__(self, array, null=[]):
        """Init."""
        self._array = array
        self._null = null

    def array(self):
        """Return array."""
        array = list(self._array)
        for e in self._null:
            array.pop(e)
        return array

    def arrayFromNull(self, null):
        """Array for results."""
        self._null, n = null, 0
        for e in null:
            if e >= 0:
                self._array.insert(e + n, 0)
                n += 1
            else:
                self._array.insert(e, 0)
        return self._array
