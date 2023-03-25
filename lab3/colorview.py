from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

class ColorView(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__()

        # self.clicked.connect()
    
    def changeCurColor(self, new: QColor):
        print(new)