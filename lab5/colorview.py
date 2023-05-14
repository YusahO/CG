from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

class ColorView(QtWidgets.QPushButton):
    color = QColor(0, 0, 0)
    def __init__(self, parent):
        super().__init__()

    def changeCurColor(self, new: QColor):
        self.color = new
        self.setStyleSheet(f'background-color: rgb({new.red()}, {new.green()}, {new.blue()})')
