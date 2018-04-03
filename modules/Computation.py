#! /usr/bin/python3
# coding: utf-8


"""Backend module with Mathematic objects and functions for computation."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
from numba import jit
from math import sqrt


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


class Tensor:
    """Baseclasss for Sysmetric Tensor."""

    def __init__(self, element):
        """Init baseclass."""
        self._type = "Baseclass Symetric Tensor"
        self.vector = [0] * 6
        self.element = element

    def tensor(self):
        """Symetric tensor structure."""
        tensor = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            tensor[i][i] = self.vector[i]
        for l, i in zip([[0, 1], [2, 0], [1, 2]], range(3, 6)):
            for x, y in zip(l, l[::-1]):
                tensor[x][y] = self.vector[i]
        return tensor

    def __repr__(self):
        """Repr."""
        return ("<%s>\n" + self.__str__()) % self._type

    def __str__(self):
        """Str."""
        return "%s\n%s\n%s" % tuple(self.tensor())


class DeformationTensor(Tensor):
    """Tenseur des deformations."""

    def __init__(self, element):
        """Init super and current class."""
        super().__init__(element)
        self._type = "Deformations Tensor"
        self.element = element

    def HookeMatrix(self):
        """Matrix of Hooke."""
        E, nu = self.element.material.E, self.element.material.nu
        mu, lbda = nu * E / ((1 + nu) * (1 - 2 * nu)), E / (2 * (1 + nu))
        mat = Matrix(6, 6, 0.0)
        for i in range(9):
            mat[i % 6, i % 6] = mu
        mat.compose(Matrix(3, 3, lbda), 0, 0)
        return mat

    def generalizedHooke(self):
        """Loi de Hooke Generalisée -> ConstraintTensor."""
        c = ConstraintTensor(self)
        c.vector = np.asarray(np.dot(self.HookeMatrix(), self.vector))[0]
        return c


class ConstraintTensor(Tensor):
    """Tenseur des contraintes."""

    def __init__(self, element):
        """Init super and current class."""
        super().__init__(element)
        self._type = "Constraints Tensor"

    def vonMises(self):
        """Von Mises Constraints."""
        diag = (self.vector[0] - self.vector[1])**2 + (self.vector[1] - self.vector[2])**2 + (self.vector[2] - self.vector[0])**2
        return 1 / sqrt(2) * sqrt(diag + 6 * sum([v**2 for v in self.vector[3:6:]]))


d = DeformationTensor(1)
d.vector = [1, 2, 3, 4, 5, 6]
