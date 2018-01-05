"""Tabed Options Widget Promotion class."""


from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTabWidget


class TabOptionWidget(QWidget):
    """Tab option widget from QWidget."""

    def __init__(self, parent):
        """Init."""
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.Tabs = QTabWidget()
        self.tabs = []

    def addTabFromList(self, l, layouts=[]):
        """Add tabs from list."""
        self.clear()
        for e in l:
            self.tabs.append(QWidget())
            self.Tabs.addTab(self.tabs[-1], e)
        self.setLayouts()

    def setLayouts(self):
        """Set layout."""
        self.layout.addWidget(self.Tabs)
        self.setLayout(self.layout)

    def clear(self):
        """Clear."""
        self.tabs.clear()
        for i in range(self.Tabs.count()):
            self.Tabs.removeTab(0)


"""
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
"""
