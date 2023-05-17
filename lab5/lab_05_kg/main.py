import itertools
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint, QPointF
from math import pi, sin, cos
import numpy as np
from time import time

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.abspath(os.getcwd()) + '/ui/mainwindow.ui', self)

        self.widgetLinePick.ColorPicked.connect(self.widgetLineCol.setNewColor)
        self.widgetBackPick.ColorPicked.connect(self.widgetBackCol.setNewColor)

        self.msgbox = QtWidgets.QMessageBox()
        task = "<font size=15>Алгоритмы построения окружностей и эллипсов.\n\n" \
            "Реализовать возможность построения " \
            "окружностей и эллипсов методами Брезенхема, Средней точки, Канонического и Параметрического уравненя, " \
            "построение спектра окружностей и " \
            "сравнение времени.</font>"
        self.action.triggered.connect(
            lambda event: self.msgbox.information(self, 'Условие', task))

        self.widgetLineCol.setNewColor(QColor(0, 0, 0))
        self.widgetBackCol.setNewColor(QColor(255, 255, 255))

        self.canvas.setParent(self)

        self.pushButton.clicked.connect(self.canvas.fill)

        # self.checkElStepA.stateChanged.connect(lambda _: pass)

        self.show()


def asInt(line: QtWidgets.QLineEdit):
    return int(line.text())


def asFloat(line: QtWidgets.QLineEdit):
    return float(line.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    app.exec_()
