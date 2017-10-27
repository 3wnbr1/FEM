#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to store Materials characteristics."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


class Material:
    """Class used to store materials."""
    def __init__(self, E=210e3, S=100, description="Acier C40"):
        self.E = E
        self.S = S
        self.description = description

    def __repr__(self):
        return "%s de section %d mm^2 et de module de Young %d MPa" % (self.description, self.S, self.E)

    def __str__(self):
        return "%s de section %d mm^2 et de module de Young %d MPa" % (self.description, self.S, self.E)


class Acier(Material):
    def __init__(self, S=100):
        self.description = "Acier de construction C40"
        self.E = 210e3
        self.S = S


class Aluminium(Material):
    def __init__(self, S=100):
        self.description = "Aluminuim"
        self.E = 69e3
        self.S = S
