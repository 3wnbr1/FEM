#! /usr/bin/python3
# coding: utf-8


"""Used to store different models."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import numpy as np
import numpy.linalg as nl
from math import sqrt
from db import fem
from modules.Computation import Matrix, DynamicArray
from modules import Elements
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


femEngine = create_engine('sqlite:///db/fem.db')
fem.Base.metadata.bind = femEngine
DBSession = sessionmaker()
DBSession.configure(bind=femEngine)


class Model:
    """Finite elements model base class."""

    def __init__(self):
        """Init base class."""
        self.elements = []
        self.elementsClass = None
        self.session = DBSession()
        self.material = self.session.query(fem.Materials).first()
        self.section = self.session.query(fem.Sections).first()
        self._lenght = 1000
        self._effortsRepartis = False
        self.selected = 0

    def elems(self, n):
        """Set elements number and mesh."""
        self._nodes = n
        self.mesh()

    def mesh(self):
        """Mesh."""
        self.elements = []
        for i in range(0, self._nodes):
            self.elements.append(self.elementsClass(self, i))

    @property
    def ddl(self):
        """Return degrees de liberte."""
        return self.elements[0].k.shape[0] // 2

    def K(self):
        """Return rigidity matrix."""
        K = Matrix((self._nodes + 1) * self.ddl,
                   (self._nodes + 1) * self.ddl)
        for i in range(0, self._nodes):
            K.compose(self.elements[i].k, self.ddl * i, self.ddl * i)
        return K

    @property
    def initial(self):
        """Return the initial poutre."""
        return [0, self._lenght], [0, 0]

    def __repr__(self):
        """Repr."""
        return "Empty baseclass model"


class PoutreEnTraction(Model):
    """Model PoutreEnTraction from baseclass Model."""

    def __init__(self):
        """Init super and current class."""
        super().__init__()
        self._D = 1
        self.elementsClass = Elements.Bar
        self.efforts = [[0, 1000, 0, 25, 0.003, 25]]
        self.links = []

    def applyWeight(self):
        """Apply weight to each node."""
        for e, i in zip(self.elements, range(1, self._nodes)):
            self._F._array[i] = - 9.81 * e.lenght * \
                self.material.rho * self.section.S / 10e9

    def solve(self, effort=10):
        """Solve model."""
        K = self.K()
        self._F = DynamicArray([0] * K.shape[0])
        self._F._unk = [0]
        self._K1 = K.removeNull([0])
        if self.selected == 0:
            self._F._array[-1] = effort
        elif self.selected == 1:
            self._F._array[-1] = effort
            self.applyWeight()
        elif self.selected == 2:
            self._F._array[-1] = 0
            self.efforts = []
            self.applyWeight()
        elif self.selected == 3:
            self._F._array[-1] = -1 * effort
            self.efforts = [[0, 1045, 0, -25, 0.003, 25]]
        elif self.selected == 4:
            self._F._array[-1] = -1 * effort
            self.efforts = [[0, 1045, 0, -25, 0.003, 25]]
            self.applyWeight()
        self._U = DynamicArray(nl.solve(self._K1, self._F.array()).tolist())
        self._U.arrayFromNull(self._F._unk)
        self._FR = np.asarray(np.dot(K, self._U._array))[0]

    @property
    def initial(self):
        """Return the initial poutre."""
        return [0, 0], [0, self._lenght]

    @property
    def deformee(self):
        """Return deformée."""
        u = np.cumsum(np.array(self._U._array))
        d = np.linspace(0, self._lenght, self._nodes + 1)
        y = [uu + dd for uu, dd in zip(u, d)]
        x = [0] * (self._nodes + 1)
        return [x, y]

    @property
    def deplacements(self):
        """Deformations."""
        return np.cumsum(np.array(self._U._array))

    @property
    def contraintes(self):
        """Contraintes."""
        vonMises = []
        for e, i in zip(self.elements, range(len(self.elements))):
            vonMises.append(e.deformationsTensor(
                self._U._array[i + 1] - self._U._array[i]).generalizedHooke().vonMises())
        return vonMises

    @property
    def types(self):
        """Return conditions aux limites."""
        return ["Traction", "Traction + Poids", "Poids Propre", "Compression", "Compression + Poids"]

    @property
    def legend(self):
        """Graph legend."""
        return {"title": "Deformée poutre en Traction", 'xtitle': r'Distance en $mm$', 'ytitle': r'Deformée en $mm$'}

    def __repr__(self):
        """Repr."""
        return "Model Poutre en traction with %i-Dimension" % (self._D)


class PoutreEnFlexion(Model):
    """Model PoutreEnFlexion from baseclass Model."""

    def __init__(self):
        """Init super and current class."""
        super().__init__()
        self._D = 1
        self.elementsClass = Elements.Poutre
        self._effortsRepartis = True

    def partEffort(self, effort, array):
        """Part effort equally on an array."""
        return [-1 * effort / self._nodes] * len(array)

    def solve(self, effort=10, reparti=False):
        """Solve model."""
        K = self.K()
        self._F = DynamicArray([0] * K.shape[0])
        if self.selected == 0:
            self._F._unk = [0, 1]
            self.efforts = [[self._lenght, 0, 0, -1, 20, 0.25]]
            if reparti is False:
                self._F._array[-2] = -1 * effort
            else:
                for i in range(1, 10):
                    self.efforts.append([self._lenght * i / 10, 0, 0, -1, 20, 0.25])
                self._F._array[2::2] = self.partEffort(effort, self._F._array[2::2])
        elif self.selected == 1:
            self._F._unk = [0, 1, -2, -1]
            self.efforts = [[self._lenght / 2, 0, 0, -0.04, 20, 0.01]]
            if reparti is False:
                self._F._array[self._nodes] = -1 * effort
            else:
                for i in [x for x in range(1, 11) if x != 5]:
                    self.efforts.append([self._lenght * i / 10, 0, 0, -0.04, 20, 0.01])
                self._F._array[2:-1:2] = self.partEffort(effort, self._F._array[2:-1:2])
        elif self.selected == 2:
            self._F._unk = [0, -2]
            self.efforts = [[self._lenght / 2, 0, 0, -0.1, 20, 0.05]]
            if reparti is False:
                self._F._array[len(self._F._array) // 2 + 1] = -1 * effort
            else:
                for i in range(1, 10):
                    self.efforts.append([self._lenght * i / 10, 0, 0, -0.1, 20, 0.05])
                self._F._array[2:-1:2] = self.partEffort(effort, self._F._array[2:-1:2])
        self._K1 = K.removeNull(self._F._unk)
        self._U = DynamicArray(nl.solve(self._K1, self._F.array()).tolist())
        self._U.arrayFromNull(self._F._unk)
        self._FR = np.asarray(np.dot(K, self._U._array))[0]

    @property
    def deformee(self):
        """Deformée of model."""
        return np.cumsum(self._lenght / self._nodes * np.cos(self._U._array[1::2])), self._U._array[::2]

    @property
    def deplacements(self):
        """Deformations."""
        return self._U._array[::2]

    @property
    def contraintes(self):
        """Contraintes."""
        vonMises = []
        for e, i in zip(self.elements, range(len(self.elements))):
            vonMises.append(e.deformationsTensor(self._U._array[2 * i + 2] - self._U._array[2 * i],
                                                 self._U._array[2 * i + 3] - self._U._array[2 * i + 1]).generalizedHooke().vonMises())
        return vonMises

    @property
    def types(self):
        """Return conditions aux limites."""
        return ["Encastrée et libre", "Encastrée et glissière", "Rotule et ponctuelle"]

    @property
    def legend(self):
        """Graph legend."""
        return {"title": "Deformée poutre en flexion", 'xtitle': r'Distance en $mm$', 'ytitle': r'Deformée en $mm$'}

    def __repr__(self):
        """Repr."""
        return "Model Poutre en flexion with %i-Dimension" % (self._D)


class TreilliSimple(Model):
    """Model TreilliSimple from baseclass Model."""

    def __init__(self):
        """Init super and current class."""
        super().__init__()
        self._D = 2

    def mesh(self, index=0):
        r"""
        Mesh model.

          3
         / \
        1---2
        """
        self.elements = []
        if index is 0:
            self._nodes = 3
            Mesh = [[[1, 2], sqrt(2) * 100, 0], [[2, 3], 100, 3 * np.pi / 4], [[3, 1], -100, np.pi / 4]]
        else:
            self._nodes = 4
            Mesh = [[[1, 2], 100, np.pi / 4], [[1, 3], 100 * sqrt(2), 0], [[2, 3], 100, 3 * np.pi / -4], [[2, 4], 100 * sqrt(2), 0], [[3, 4], 100, np.pi / 4]]
        for e in Mesh:
            self.elements.append(Elements.TreillisBar(self, e[0], e[1], e[2]))

    def K(self, index=0):
        """Return rigidity matrix."""
        K = Matrix((self._nodes) * 2, (self._nodes) * 2)
        if index == 0:
            K.compose(self.elements[0].k, 0, 0)
            K.compose(self.elements[1].k, 2, 2)
            for x in range(0, 4, 2):
                for y in range(0, 4, 2):
                    K.compose(self.elements[2].k[np.ix_(
                        [x, x + 1], [y, y + 1])], x, y)
        return K

    def solve(self, effort=10):
        """Solve model."""
        K = self.K()
        self._F = DynamicArray([0] * K.shape[0])
        if self.selected == 0:
            self.efforts = [[sqrt(2)*100, 0, 0, -5, 2, 5]]
            self._F._unk = [0, 1, -2]
            self._F._array[-1] = -1 * effort
        self._K1 = K.removeNull(self._F._unk)
        self._U = DynamicArray(nl.solve(self._K1, self._F.array()).tolist())
        self._U.arrayFromNull(self._F._unk)
        self._FR = np.asarray(np.dot(K, self._U._array))[0]

    def nodesCoordinates(self):
        """Return coordinates of the nodes."""
        nodes = [[1, 0, 0]]
        for startn in range(1, self._nodes + 1):
            origin = nodes[startn - 1][1::]
            for e in [i for i in self.elements if startn == i.nodes[0]]:
                if e.nodes[1] not in [i[0] for i in nodes]:
                    nodes.append([e.nodes[1], origin[0] + e.lenght * np.cos(e.alpha), origin[0] + e.lenght * np.sin(e.alpha)])
        return nodes

    @property
    def initial(self):
        """Initial."""
        out, nodes = [[], []], self.nodesCoordinates()
        nodes.append(nodes[0])
        for n in nodes:
            out[0].append(n[1])
            out[1].append(n[2])
        return out

    @property
    def deformee(self):
        """Return Deformée."""
        return self.initial

    @property
    def deplacements(self):
        """Deformations."""
        out = []
        for e in self.elements:
            a, b = e.nodes[0] - 1, e.nodes[1] - 1
            out.append(sqrt((self._U._array[2*b] - self._U._array[2*a])**2+(self._U._array[2*b+1] - self._U._array[2*a+1])**2))
        return out

    @property
    def contraintes(self):
        """Contraintes."""
        vonMises = []
        n = len(self.elements)
        for e, i in zip(self.elements, range(n)):
            vonMises.append(e.deformationsTensor(self._U._array[(2 * i + 2) % (2*n)] - self._U._array[(2 * i) % (2*n)],
                                                 self._U._array[(2 * i + 3) % (2*n)] - self._U._array[(2 * i + 1) % (2*n)]).generalizedHooke().vonMises())
        return vonMises

    @property
    def types(self):
        """Return conditions aux limites."""
        return ["Treillis simple"]

    @property
    def legend(self):
        """Graph legend."""
        return {"title": "Treillis Simple", 'xtitle': r'Distance en $mm$', 'ytitle': r'Distance en $mm$'}

    def __repr__(self):
        """Repr."""
        return "Model TreilliSimple with %i-Dimension" % (self._D)
