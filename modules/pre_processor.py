#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to prepare model for processing."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


from modules import models
from modules.backend import Material


def list_material():
    return [m for m in dir(Material) if (not m.startswith('__') and m != "Material")]


def mesh(model):
    assert isinstance(model, models.Model), "Not a model object"
