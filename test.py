#! /usr/bin/python3
# coding: utf-8


"""Main script for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr, pierre.haon@ecam.fr"


import sys
import time
from app import App, listModels
from PyQt5.QtWidgets import QApplication


def test_conditions():
    """Parse initial conditions dropdown."""
    for condition in range(len(window.model.types)):
        window.comboBoxConditions.setCurrentIndex(condition)
        window.comboBoxSections.setCurrentIndex(1)
        window.comboBoxMaterials.setCurrentIndex(1)
        window.compute()


def test_graphs():
    """Parse graph results dropdown."""
    for result in range(3):
        window.comboBoxResults.setCurrentIndex(result)
        window.updateGraph()
        QApplication.processEvents()
        time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window._showAgain = False
    window.show()
    window.updateWindowSize(False)
    window.elementsNumberChanged()
    for model in range(len(listModels())):
        window.checkBoxReparti.setChecked(False)
        window.listWidget.setCurrentRow(model)
        test_conditions()
        test_graphs()
        if window.model._effortsRepartis:
            window.checkBoxReparti.setChecked(True)
            test_conditions()
            test_graphs()
    sys.exit(0)
