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
        self.ax2 = self.fig.add_subplot(212)
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def deformee(self, deformee, poutre):
        """Plot deformée."""
        self.ax1.cla()
        self.ax1.set_title('Deformée')
        self.ax1.plot(poutre[0], poutre[1])
        self.ax1.plot(deformee[0], deformee[1])
        self.draw()

    def contraintes(self, contraintes):
        """Plot contraintes."""
        self.ax2.cla()
        self.ax2.set_title('Contraintes')


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
