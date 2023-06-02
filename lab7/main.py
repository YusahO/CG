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

        self.sepDrawPB.clicked.connect(self.addCutter)
        self.lineDrawPB.clicked.connect(self.addLine)
        self.doPB.clicked.connect(self.canvas.doCutting)

        self.author.triggered.connect(
            lambda: self.msgbox.information(
                self, 'Об авторе', '<font size=14><b>ИУ7-41Б Шубенина Дарья</b></font>'
            )
        )

        self.prog.triggered.connect(
            lambda: self.msgbox.information(
                self, 'О программе', '<font size=14><b>Реализация простого алгоритма отсечения отрезка регулярным отсекателем.</b></font>'
            )
        )

        self.show()

    def clearCanvas(self):
        self.canvas.lines.clear()
        self.canvas.cutter = []
        self.canvas.results.clear()

        self.canvas.update()

    def addCutter(self):
        x0 = self.tryGetLineEditData(self.sepTLXLE, int, 0)
        if x0 is None:
            return
        y0 = self.tryGetLineEditData(self.sepTLYLE, int, 0)
        if y0 is None:
            return
        x1 = self.tryGetLineEditData(self.sepRBXLE, int, 0)
        if x1 is None:
            return
        y1 = self.tryGetLineEditData(self.sepRBYLE, int, 0)
        if y1 is None:
            return

        self.canvas.addCutter(x0, y0, x1, y1)

    def addLine(self):
        x0 = self.tryGetLineEditData(self.lineXSLE, int, 0)
        if x0 is None:
            return
        y0 = self.tryGetLineEditData(self.lineYSLE, int, 0)
        if y0 is None:
            return
        x1 = self.tryGetLineEditData(self.lineXELE, int, 0)
        if x1 is None:
            return
        y1 = self.tryGetLineEditData(self.lineYELE, int, 0)
        if y1 is None:
            return

        self.canvas.addLine(x0, y0, x1, y1)

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
