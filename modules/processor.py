#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Finite Elements Method Processor."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


class Model:
    """Model class used to solve problem."""
    def __init__(self):
        self.material = Material.Acier
        self.elements = []
        self.n = 5
        self.L = 1000
        self.conditions = self.Conditions(self.n)

    def mesh(self):
        self.elements = []
        for i in range(self.n):
            self.elements.append(Element.Bar(self, i))

    @property
    def K(self):
        K = Matrix(self.n + 1, self.n + 1)
        for i in range(self.n):
            K.compose(self.elements[i].k, i, i)
        self._K = K
        return self._K

    def solve(self):
        self.conditions.fix_at(0)
        self.conditions.apply_effort()
        K1 = self.K.remove_null(0)
        self.U = np.dot(np.linalg.inv(K1), self.conditions._F[1:])
        return self.U

    def elems(self, n):
        self.n = n
        self.mesh()
        self.conditions = self.Conditions(self.n)
        self.conditions.fix_at(0)
        self.solve()
