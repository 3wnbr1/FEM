#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""GUI for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import sys
import models
import ast
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


def listModels(models=models):
    """List models."""
    with open(models.__file__, 'r') as source:
        p = ast.parse(source.read())
    return [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]


qtCreatorFile = "ui/mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class App(QMainWindow, Ui_MainWindow):
    """Mainwindow."""

    def __init__(self):
        """Init."""
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.listWidget.addItems(listModels())

        self.listWidget.currentTextChanged.connect(self.modelChanged)

    def modelChanged(self):
        """Change model on selection."""
        self.model = eval("models." + self.listWidget.currentItem().text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
