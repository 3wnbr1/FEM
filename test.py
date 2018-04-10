#! /usr/bin/python3
# coding: utf-8


"""Main script for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr, pierre.haon@ecam.fr"


import sys
import time
from models import *
from app import App, listModels
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    for model in range(len(listModels())):
        window.listWidget.setCurrentRow(model)
        for condition in range(len(window.model.types)):
            window.comboBoxConditions.setCurrentIndex(condition)
            window.comboBoxSections.setCurrentIndex(0)
            window.comboBoxMaterials.setCurrentIndex(1)
            window.compute()
            time.sleep(1)
            for result in range(3):
                window.comboBoxResults.setCurrentIndex(result)
                window.updateGraph()
                QApplication.processEvents()
                time.sleep(1)
    sys.exit(0)
