#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store different models."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


from modules.backend import Effort, Material


class Model:
    def __init__(self):
        self.Efforts = []
        self.Elements = []

        self.Material = Material.Material()

        self._lenght = 1000  # default size is 1 meter
        self._elements_number = 1

    def apply_effort(self, effort=Effort):
        self.Efforts.append(Effort)

    def fix_at(postion):  # 0 is the begining and 1 is the end
        pass

    def __repr__(self):
        return "Empty model"


class Poutre(Model):
    def __new__(self):
        return super(Model, self).__new__(self)

    # @TODO Add ability to init class after superclass init

    def __repr__(self):
        return "Poutre à %iD" % (self._D)
