import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint
from threading import Thread
from time import time

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab5/lab5.ui', self)

        self.lineColorSwatch_1.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_2.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_3.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_4.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_5.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_6.changeColor.connect(self.colorview_1.changeCurColor)
        self.lineColorSwatch_7.changeColor.connect(self.colorview_1.changeCurColor)

        self.bgColorSwatch_1.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_2.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_3.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_4.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_5.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_6.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_7.changeColor.connect(self.colorview_2.changeCurColor)

        self.ptAddPB.clicked.connect(self.addPoint)
        self.closePB.clicked.connect(self.closePoly)

        self.nodelayRB.toggled.connect(
            lambda: self.stackedWidget.setCurrentIndex(self.nodelayRB.isChecked())
        )

        self.fillPB.clicked.connect(self.launchInThread)
        self.canvasClearPB.clicked.connect(self.clearCanvas)

        self.canvas.setParent(self)

        self.msgbox = QtWidgets.QMessageBox(self)

        self.author.triggered.connect(
            lambda: self.msgbox.information(
                self,
                'Об авторе',
                '<font size=14><b>Шубенина Дарья ИУ7-41Б</b></font>'
            )
        )

        self.prog.triggered.connect(
            lambda: self.msgbox.information(
                self,
                'Условие',
                '''<font size=14><b>Реализовать и исследовать алгоритм заполнения по ребрам</b></font>'''
            )
        )

        self.show()

    def clearCanvas(self):
        self.canvas.canvasPolygons.clear()
        self.canvas.rects.clear()
        self.canvas.pixmap().fill(QColor(0xFFFFFF))
        self.table.clearContents()
        self.table.setRowCount(0)
        self.canvas.update()

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

    def addPoint(self):
        x = self.tryGetLineEditData(self.ptXLE, vmin=0)
        if x is None:
            return
        y = self.tryGetLineEditData(self.ptYLE, vmin=0)
        if y is None:
            return
        
        x = round(x)
        y = round(y)

        self.canvas.addPointToCanvas(QtCore.QPoint(x, y), from_mouse=False)

        self.canvas.update()

    def closePoly(self):
        self.canvas.closeCanvasPolygon()
        self.update()

    def launchInThread(self):
        thread = Thread(target=self.fill)
        thread.start()

    def fill(self):
        if self.delayRB.isChecked():
            delay = self.horizontalSlider.value() * 0.001
            self.canvas.fillDelay(delay)
        else:
            self.canvas.setMouseTracking(False)
            self.canvas.fillNoDelay()
            self.canvas.setMouseTracking(True)

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
