import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint
from threading import Thread
from time import time

func_res = True

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab6/lab6.ui', self)

        self.bgColorSwatch_1.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_2.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_3.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_4.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_5.changeColor.connect(self.colorview_2.changeCurColor)
        self.bgColorSwatch_6.changeColor.connect(self.colorview_2.changeCurColor)

        self.ptAddPB.clicked.connect(self.processAddPoint)
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
        self.canvas.canvasPolygons.clear()
        self.canvas.rects.clear()
        self.canvas.pixmap().fill(QColor(0xFFFFFF))
        self.table.clearContents()
        self.table.setRowCount(0)
        self.canvas.update()

    def processAddPoint(self):
        self.canvas.pix_input = True

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
        if self.ptXLE.text() == '' and self.ptYLE.text() == '':
            self.msgbox.warning(
                self, 'Внимание!', '<font size=14><b>Пожалуйста, введите координаты затравочного пикселя</b></font>')
            return

        x = self.tryGetLineEditData(self.ptXLE, int, vmin=0, vmax=self.canvas.width())
        if x is None:
            return
        y = self.tryGetLineEditData(self.ptYLE, int, vmin=0, vmax=self.canvas.height())
        if y is None:
            return
        
        self.canvas.pix_pos = QPoint(x, y)
        thread = Thread(target=self.fill)
        thread.start()

        global func_res
        if func_res is not None and func_res == False:
            self.msgbox.critical(
                self, 'Ошибка!', '<font size=14><b>Затравочный пиксель должен быть внутри замкнутой области!</b></font>'
            )
        func_res = None

    def fill(self):
        global func_res
        if self.delayRB.isChecked():
            delay = self.horizontalSlider.value() * 0.001
            func_res = self.canvas.fillDelay(delay)
        else:
            self.canvas.setMouseTracking(False)
            func_res = self.canvas.fillNoDelay()
            self.canvas.setMouseTracking(True)

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
