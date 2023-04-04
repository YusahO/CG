import sys
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPainter
from time import time

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab4/lab4.ui', self)

        self.lineColorSwatch_1.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_2.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_3.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_4.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_5.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_6.changeColor.connect(self.colorview.changeCurColor)
        self.lineColorSwatch_7.changeColor.connect(self.colorview.changeCurColor)

        self.bgColorSwatch_1.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_2.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_3.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_4.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_5.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_6.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_7.changeColor.connect(self.canvas.changeBgColor)

        self.show()

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()