#! /usr/bin/python3
# coding: utf-8


"""Main script for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr, pierre.haon@ecam.fr"


import sys
from app import App
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splashscreen = QSplashScreen(QPixmap('ui/splash.jpg'))
    splashscreen.showMessage(
        "Chargement de l'interface...\n\nCrée dans le cadre des TIPE 2017 - 2018\nPar Ewen BRUN et Pierre HAON\nClasses Préparatoires à l'ECAM Lyon")
    splashscreen.show()
    window = App()
    splashscreen.finish(window)
    window.show()
    sys.exit(app.exec_())
