#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different models."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"

import numpy as np
import numpy.linalg as nl
import matplotlib.pyplot as plt
from numba import jit
from modules.Computation import Matrix
from modules import Conditions, Material, Elements


class Model:
    def __init__(self):
        self.elements = []
        self.conditions = []
        self.material = Material.Material()

        self._lenght = 1000  # default size is 1 meter
        self._I = (10*10**3)/12  # h * b**3 / 12
        self._D = 1
        self.elems(1)

    def fix_at(postion):  # 0 is the begining and 1 is the end
        pass

    def elems(self, n):
        self._elements = n
        self.mesh()

    @jit
    def mesh(self):
        self.elements = []
        if self._D == 1:
            for i in range(0, self._elements):
                self.elements.append(Elements.Bar(self, i))
        elif self._D == 2:
            for i in range(0, self._elements):
                self.elements.append(Elements.Poutre(self, i))
        else:
            print("Not supported yet")

    def solve(self, conditions):
        nl.solve(self.K().remove_null(0), conditions)

    @property
    def ddl(self):
        return self.elements[0].k.shape[0] // 2

    @jit
    def K(self):
        K = Matrix((self._elements+1)*self.ddl, (self._elements+1)*self.ddl)
        for i in range(0, self._elements):
            K.compose(self.elements[i].k, self.ddl*i, self.ddl*i)
        return K

    def __repr__(self):
        return "Empty baseclass model"


class PoutreEnTraction(Model):
    def __new__(self):
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        self._D = 1

    @jit
    def mesh(self):
        self.elements = []
        for i in range(0, self._elements):
            self.elements.append(Elements.Bar(self, i))

    @jit
    def solve(self):
        self._F = [0]*(self.K().shape[0] - 1)
        self._F[-1] = 10
        self._U = nl.solve(self.K().remove_null(0), self._F)
        self._U = np.concatenate([[0], self._U])
        self._U = self._U.reshape(len(self._U), 1)
        self._R = self.K()[1]*self._U
        self._F2 = nl.solve(self.K().remove_null(0), self._U[1:])

    def __repr__(self):
        return "Model Poutre en traction with %i-Dimension" % (self._D)


class PoutreEnFlexion(Model):
    def __new__(self):
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        self._D = 1

    def mesh(self):
        self.elements = []
        for i in range(0, self._elements):
            self.elements.append(Elements.Poutre(self, i))

    def solve(self):
        self._K1 = self.K().remove_null(0).remove_null(1)
        self._F = [0]*(self._K1.shape[0])
        self._F[-2] = -10
        self._F[-1] = 0
        self._U = nl.solve(self._K1, self._F)

        # plt.matshow(self._K1)

        x = np.cumsum(self._lenght/self._elements*np.cos(self._U[1::2]))
        plt.plot(x, self._U[::2], label="FEM")

        # xx = np.arange(0, 1001)
        # plt.plot(xx, self._F[-2]*(xx)**3/(3*self._I*self.material.E), label=r"Flèche RDM : $\frac{F.L^{3}}{3.I_{gz}.E}$")

        plt.plot([0, self._lenght], [0, 0], label="Situation initiale")
        plt.title("FEM - Etude d'une poutre en flexion")
        plt.xlabel(r"Longeur de la poutre en $mm$")
        plt.ylabel(r"Déformation en $mm$")
        plt.legend()
        plt.show()

    def __repr__(self):
        return "Model Poutre en flexion with %i-Dimension" % (self._D)
