"""Matplotlib QtDesigner Widget."""


from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):
    """MplCanvas."""

    def __init__(self):
        """Init."""
        self.fig = Figure()
        # self.fig.text(0.03, 0.5, 'Selectionnez un modèle de calcul', fontsize=25, color='gray', alpha=0.5)
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_title('Deformée')
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_title('Contraintes')
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def deformee(self, x, y):
        self.ax1.cla()
        self.ax1.plot(x, y)
        self.draw()

    def contraintes(self, x, y):
        self.ax2.cla()


class MplWidget(QtWidgets.QWidget):
    """QtDesigner QtWidget Promotion Class."""

    def __init__(self, parent=None):
        """Init."""
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def set_figure(self):
        """Set figure."""
        self.canvas.subplots()
