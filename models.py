#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different models."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


from modules.Computation import Matrix
from modules import Effort, Material, Elements


class Model:
    def __init__(self):
        self.efforts = []
        self.elements = []

        self.material = Material.Material()

        self._lenght = 1000  # default size is 1 meter
        self._elements = 1
        self._I = 1

    def apply_effort(self, effort=Effort):
        self.efforts.append(Effort)

    def fix_at(postion):  # 0 is the begining and 1 is the end
        pass

    def mesh(self):
        self.elements = []
        for i in range(0, self._elements):
            self.elements.append(Elements.Poutre(self, i))

    @property
    def ddl(self):
        return self.elements[0].k.shape[0] // 2

    @property
    def K(self):
        K = Matrix((self._elements+1)*self.ddl, (self._elements+1)*self.ddl)
        for i in range(0, self._elements):
            K.compose(self.elements[i].k, self.ddl*i, self.ddl*i)
        self._K = K
        return self._K

    def __repr__(self):
        return "Empty base model"


class Poutre(Model):
    def __new__(self):
        self.__init_subclass__()
        return super(Model, self).__new__(self)

    def __init_subclass__(self):
        self._D = 1

    def __repr__(self):
        return "Poutre à %iD" % (self._D)
