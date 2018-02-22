#! /usr/bin/python3
# coding: utf-8


"""GUI for Finite Elements Method."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import ast
import models
from numpy import exp
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QProgressDialog, QFileDialog, QMessageBox
from sqlalchemy import text
from db.fem import Materials, Sections


def listModels(models=models):
    """List models."""
    with open(models.__file__, 'r') as source:
        p = ast.parse(source.read())
    return [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef) and node.name != "Model"]


qtCreatorFile = "ui/mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class App(QMainWindow, Ui_MainWindow):
    """Mainwindow."""

    def __init__(self):
        """Init."""
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.elements_horizontalSlider.setVisible(False)
        self.elements_plainTextEdit.setVisible(False)
        self.elements_plainTextEdit.setPlainText("100")
        self.listWidget.addItems(listModels())
        self.model = models.Model()
        self.loadMaterials()
        self.loadSections()
        self.loadSectionImage()

        self.dockWidget.topLevelChanged.connect(self.updateWindowSize)
        self.listWidget.currentTextChanged.connect(self.modelChanged)
        self.tabwidget.Tabs.currentChanged.connect(self.typeChanged)
        self.materials_comboBox.currentTextChanged.connect(self.materialChanged)
        self.sections_comboBox.currentTextChanged.connect(self.sectionChanged)
        self.elements_horizontalSlider.valueChanged.connect(
            self.elementsNumberChanged)
        self.startComputationPushButton.clicked.connect(self.compute)
        self.pushButtonSave.clicked.connect(self.saveFigure)

    def updateWindowSize(self, onTop):
        """Update window size if dockWidget is on Top."""
        if onTop:
            self.resize(self.minimumSize())
        else:
            self.resize(self.maximumSize())

    def modelChanged(self):
        """Change model on selection."""
        self.selectModelLabel.setHidden(True)
        self.modelStatusLabel.setText("✅")
        self.model = eval(
            "models." + self.listWidget.currentItem().text() + '()')
        self.tabwidget.addTabFromList(self.model.types)

    def materialChanged(self):
        """Change material on selection."""
        self.model.material = self.model.session.query(Materials).filter(
            Materials.Name == self.materials_comboBox.currentText()).first()

    def sectionChanged(self):
        """Change section on selection."""
        self.model.section = self.model.session.query(Sections).filter(
            Sections.Name == self.sections_comboBox.currentText()).first()
        self.loadSectionImage()

    def loadMaterials(self):
        """Load materials from db."""
        self.materials_comboBox.addItems(
            [i[0] for i in self.model.session.execute(text('select Name from Materials'))])

    def loadSections(self):
        """Load scetion names from db."""
        self.sections_comboBox.addItems(
            [i[0] for i in self.model.session.execute(text('select Name from Sections'))])

    def loadSectionImage(self):
        """Load image corresponding to section from db."""
        p = QPixmap()
        p.loadFromData(self.model.section.raw_Image)
        p = p.scaled(32, 32)
        self.sectionImageLabel.setPixmap(p)
        self.sectionImageLabel.resize(p.width(), p.height())
        self.sectionImageLabel.show()

    def typeChanged(self):
        """Change type of study."""
        if self.tabwidget.Tabs.currentIndex() != -1:
            self.model.elems(int(self.elements_plainTextEdit.toPlainText()))
            self.model.solve(self.tabwidget.Tabs.currentIndex())
            self.mpl.canvas.graph(self.model)

    def elementsNumberChanged(self):
        """Change in number of elements."""
        self.elements_plainTextEdit.setPlainText(
            str(int(exp(self.elements_horizontalSlider.value()))))
        print(self.elements_plainTextEdit.toPlainText())

    def saveFigure(self):
        """Save figure."""
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File')
            if name[0] != "":
                self.mpl.canvas.fig.savefig(name[0], dpi=300)
        except BaseException:
            QMessageBox.warning(self, 'Avertissement',
                                'Le fichier n\'as pas pu etre enregistré')

    def compute(self):
        """Compute."""
        diag = QProgressDialog(self)
        diag.setRange(0, 0)
        diag.setValue(0)
        diag.setModal(True)
        diag.setWindowTitle("Calcul en cours")
        diag.setLabelText("Resolution en cours...")
        diag.show()
        self.model.elems(self.elements_horizontalSlider.value())
        diag.show()
        QApplication.processEvents()
        self.model.solve()
        diag.reset()
        self.typeChanged()
