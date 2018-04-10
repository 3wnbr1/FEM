#! /usr/bin/python3
# coding: utf-8


"""Main script for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr, pierre.haon@ecam.fr"


import sys
from app import App
from models import PoutreEnFlexion, PoutreEnTraction, TreilliSimple
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.model = PoutreEnFlexion()
    window.compute()
    window.model = PoutreEnTraction()
    window.compute()
    window.model = TreilliSimple()
    window.compute()
    sys.exit(0)
