#! /Users/ewen/anaconda3/bin/python
# coding: utf-8


"""Used to diplay results of computation."""


__author__ = "Ewen BRUN, Pierre HAON"
__email__ = "ewen.brun@ecam.fr"


import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class DiscreteSlider(Slider):
    """Pass int values in the Slider."""
    def __init__(self, *args, **kwargs):
        self.inc = kwargs.pop('increment', 1)
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        discrete_val = int(val / self.inc) * self.inc
        xy = self.poly.xy
        xy[2] = discrete_val, 1
        xy[3] = discrete_val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon:
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson:
            return
        for cid, func in self.observers.items():
            func(discrete_val)


def Plot():
    """Ploters."""
    n0 = 10

    model = Model()
    fig, ax = plt.subplots()

    def rdm(x):
        return model.conditions._f * x / (model.material.E * model.material.S)

    plt.subplots_adjust(left=0.15, bottom=0.25)
    model.elems(n0)
    x = (model.L/model.n)*np.arange(model.n+1)
    y = np.squeeze(np.asarray(model.U))
    y = np.insert(y, 0, 0)
    l, = plt.plot(x, y, label="FEM")
    plt.plot(x, rdm(x), label="RdM")
    plt.legend()
    plt.title("Etude en traction d'une poutre en %s et de section $%.1f mm^{2}$" % (model.material.description, (model.material.S)))
    plt.xlabel('Longeur de la poutre en m')
    plt.ylabel('Deplaceent en m')

    ax = plt.axes([0.25, 0.1, 0.65, 0.03])
    elements = DiscreteSlider(ax, 'Elements', 1, 50, valinit=n0, increment=1)

    def update(val):
        model.elems(int(elements.val))
        x = (model.L/model.n)*np.arange(model.n+1)
        y = np.squeeze(np.asarray(model.U))
        y = np.insert(y, 0, 0)
        l.set_data(x, y)
        fig.canvas.draw_idle()

    elements.on_changed(update)

    plt.show()
