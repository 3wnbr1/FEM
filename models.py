#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different models."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
import numpy.linalg as nl
from numba import jit
from math import sqrt
from modules.Computation import Matrix, DynamicArray, nodesCombination
from modules import Material, Elements


class Model:
    """Finite elements model base class."""

    def __init__(self):
        """Init base class."""
        self.elements = []
        self.conditions = []
        self.material = Material.Material()

        self._lenght = 1000  # default size is 1 meter
        self._I = (10 * 10**3) / 12  # h * b**3 / 12
        self._D = 1
        self.elems(1)
        self.poutres = [[0, self._lenght], [0, 0]]
        self.legend = {"title": "Not defined",
                       "xtitle": "None", "ytitle": "None"}

    def elems(self, n):
        """Set elements number and mesh."""
        self._nodes = n
        self.mesh()

    @property
    def ddl(self):
        """Return degrees de liberte."""
        return self.elements[0].k.shape[0] // 2

    @jit
    def K(self):
        """Return rigidity matrix."""
        K = Matrix((self._nodes + 1) * self.ddl,
                   (self._nodes + 1) * self.ddl)
        for i in range(0, self._nodes):
            K.compose(self.elements[i].k, self.ddl * i, self.ddl * i)
        return K

    @property
    def contraintes(self):
        """Contraintes."""
        return [[0, 1], [0, 1]]

    @property
    def initial(self):
        """Return the initial poutre."""
        return [0, self._lenght], [0, 0]

    def __repr__(self):
        """Repr."""
        return "Empty baseclass model"


class PoutreEnTraction(Model):
    """Model PoutreEnTraction from baseclass Model."""

    def __new__(self):
        """Init super and current class."""
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        """Init subclass from Model."""
        self._D = 1

    @jit
    def mesh(self):
        """Mesh model."""
        self.elements = []
        for i in range(0, self._nodes):
            self.elements.append(Elements.Bar(self, i))

    @jit
    def solve(self, selected=0):
        """Solve model."""
        self._F = DynamicArray([0] * self.K().shape[0])
        self._F._array[-1] = 10
        self._F._null = [0]
        self._U = nl.solve(self.K().remove_null(0), self._F.array())
        self._U = np.concatenate([[0], self._U])
        self._U = self._U.reshape(len(self._U), 1)

    @property
    def deformee(self):
        """Return deformée."""
        return [np.linspace(0, self._lenght, self._nodes + 1), self._U]

    @property
    def types(self):
        """Return conditions aux limites."""
        return ["Traction", "Compression"]

    def __repr__(self):
        """Repr."""
        return "Model Poutre en traction with %i-Dimension" % (self._D)


class PoutreEnFlexion(Model):
    """Model PoutreEnFlexion from baseclass Model."""

    def __new__(self):
        """New."""
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        """Init subclass."""
        self._D = 1
        self.legend = {"title": "Deformée poutre en flexion",
                       'xtitle': r'Distance en $m$', 'ytitle': r'Deformée en $m$'}

    def mesh(self):
        """Mesh."""
        self.elements = []
        for i in range(0, self._nodes):
            self.elements.append(Elements.Poutre(self, i))

    def solve(self, selected=0):
        """Solve model."""
        K = self.K()
        self._F = DynamicArray([0] * K.shape[0])
        if selected == 0:
            self._K1 = K.remove_null(1).remove_null(0)
            self._F._null = [0, 1]
            self._F._array[-2] = -10
        elif selected == 1:
            self._K1 = K.remove_null(self._nodes * 2 - 1).remove_null(
                self._nodes * 2 - 1).remove_null(1).remove_null(0)
            self._F._null = [-1, -1, 1, 0]
            self._F._array[self._nodes] = -10
        elif selected == 2:
            self._K1 = K.remove_null(K.shape[0] - 2).remove_null(0)
            self._F._null = [0, -2]
            self._F._array[len(self._F._array) // 2 + 1] = -10
        self._U = DynamicArray(nl.solve(self._K1, self._F.array()).tolist())
        self._U.arrayFromNull(self._F._null)

    @property
    def deformee(self):
        """Deformée of model."""
        return np.cumsum(self._lenght / self._nodes * np.cos(self._U._array[1::2])), self._U._array[::2]

    @property
    def types(self):
        """Return conditions aux limites."""
        return ["Extremité", "Central", "Autre"]

    def __repr__(self):
        """Repr."""
        return "Model Poutre en flexion with %i-Dimension" % (self._D)


class TreilliSimple(Model):
    """Model TreilliSimple from baseclass Model."""

    def __new__(self):
        """New."""
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        """Init subclass."""
        self._D = 2

    @jit
    def mesh(self):
        r"""
        Mesh model.

          2---4
         / \ /
        1---3
        """
        self._nodes = 4
        self.elements = []
        self.elements.append(Elements.TreillisBar(self, [1, 2], 1, np.pi / 2))
        self.elements.append(Elements.TreillisBar(self, [1, 3], sqrt(2), 0))
        self.elements.append(Elements.TreillisBar(self, [2, 3], 1, np.pi / -2))
        self.elements.append(Elements.TreillisBar(self, [2, 4], sqrt(2), 0))
        self.elements.append(Elements.TreillisBar(self, [3, 4], 1, np.pi / 2))

    @jit
    def K(self):
        """Return rigidity matrix."""
        K = Matrix((self._nodes) * 2, (self._nodes) * 2)
        x, y = 0, 0
        for e in self.elements[0::2]:
            K.compose(e.k, 2 * x, 2 * y)
            x, y = x + 1, y + 1
        for e in self.elements[1::2]:
            c = nodesCombination(e.nodes)
            for x in range(0, 4, 2):
                for y in range(0, 4, 2):
                    k = e.k[np.ix_([x, x + 1], [y, y + 1])]
                    xx, yy = next(c)
                    K[np.ix_([xx, xx+1], [yy, yy+1])] += k
        return K

    def __repr__(self):
        """Repr."""
        return "Model TreilliSimple with %i-Dimension" % (self._D)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    m = TreilliSimple()
    m.mesh()
    plt.matshow(m.K())
    plt.show()
