from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

class ColorButton(QtWidgets.QPushButton):
    changeColor = QtCore.pyqtSignal(QColor, name='changeColor')
    def __init__(self, parent):
        super().__init__()

    def focusInEvent(self, e):
        self.changeColor.emit(QColor(0, 0, 0))