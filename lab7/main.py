import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint
from threading import Thread
from time import time
import re

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab7/lab7.ui', self)

        self.canvas.setParent(self)

        self.msgbox = QtWidgets.QMessageBox(self)

        self.lineColor.clicked.connect(lambda: self.setPBColor(self.lineColor))
        self.sepColor.clicked.connect(lambda: self.setPBColor(self.sepColor))
        self.resColor.clicked.connect(lambda: self.setPBColor(self.resColor))

        self.canvClearPB.clicked.connect(self.clearCanvas)

        self.author.triggered.connect(
            lambda: self.msgbox.information(
                self, 'Об авторе', '<font size=14><b>ИУ7-41Б Шубенина Дарья</b></font>'
            )
        )

        self.prog.triggered.connect(
            lambda: self.msgbox.information(
                self, 'О программе', '<font size=14><b>Реализовать и исследовать алгоритм построчного затравочного заполнения.</b></font>'
            )
        )

        self.show()

    def clearCanvas(self):
        self.canvas.lines.clear()
        self.canvas.cutter.clear()
        self.canvas.results.clear()

        self.canvas.update()

    def setPBColor(self, pb):
        newcol = QtWidgets.QColorDialog().getColor()

        style = pb.styleSheet()
        new_style = ''

        for l in style.splitlines():
            if (l.startswith('background-color')):
                l = f'background-color: rgb({newcol.red()},{newcol.green()},{newcol.blue()});\n'
                new_style += l

        pb.setStyleSheet(new_style)
        
    def getPBColor(self, pb: QtWidgets.QPushButton):
        style = pb.styleSheet()
        color = QColor(0, 0, 0)
        for l in style.splitlines():
            if (l.startswith('background-color')):
                rgb = [int(s) for s in re.findall(r'\b\d+\b', l)]
                color = QColor(*rgb)
        
        return color

    def tryGetLineEditData(self, lineEdit, T=float, vmin=None, vmax=None):
        try:
            v = T(lineEdit.text())
            if vmin is not None and v < vmin:
                raise Exception
            if vmax is not None and v > vmax:
                raise Exception
        except:
            message = ''
            if vmin is not None and vmax is not None:
                message = f'Значение должно быть числом в промежутке [{vmin}, {vmax}]'
            elif vmin is None and vmax is not None:
                message = f'Значение должно быть числом <= {vmax}'
            elif vmin is not None and vmax is None:
                message = f'Значение должно быть числом >= {vmin}'

            self.msgbox.critical(
                self, 'Ошибка!', '<font size=14><b>Неверный ввод!\n' + message + '</b></font>')
            v = None
        return v
    


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
