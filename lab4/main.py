import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPainter
from time import time

from canonic import CircleCanonicDraw, EllipseCanonicDraw
from parametric import CircleParametricDraw, EllipseParametricDraw
from midpoint import CircleMidpointDraw, EllipseMidpointDraw
from bresenham import CircleBresenhamDraw, EllipseBresenhamDraw

from canonic import CircleCanonicMeasure, EllipseCanonicMeasure
from parametric import CircleParametricMeasure, EllipseParametricMeasure
from midpoint import CircleMidpointMeasure, EllipseMidpointMeasure
from bresenham import CircleBresenhamMeasure, EllipseBresenhamMeasure

from utils import CreateCircleSpectrum, CreateEllipseSpectrum

REPS = 200
STEP = 10
AMT = 100

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab4/lab4.ui', self)

        self.lineColorSwatch_1.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_2.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_3.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_4.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_5.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_6.changeColor.connect(
            self.colorview.changeCurColor)
        self.lineColorSwatch_7.changeColor.connect(
            self.colorview.changeCurColor)

        self.bgColorSwatch_1.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_2.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_3.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_4.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_5.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_6.changeColor.connect(self.canvas.changeBgColor)
        self.bgColorSwatch_7.changeColor.connect(self.canvas.changeBgColor)

        self.cSpectrumCB.stateChanged.connect(
            lambda: self.circleSW.setCurrentIndex(self.cSpectrumCB.isChecked()))
        self.eSpectrumCB.stateChanged.connect(
            lambda: self.ellipseSW.setCurrentIndex(self.eSpectrumCB.isChecked()))

        self.cSpectRadStartRB.toggled.connect(
            lambda: self.cSpectRadStartLE.setEnabled(not self.cSpectRadStartRB.isChecked()))
        self.cSpectRadEndRB.toggled.connect(
            lambda: self.cSpectRadEndLE.setEnabled(not self.cSpectRadEndRB.isChecked()))
        self.cSpectStepRB.toggled.connect(
            lambda: self.cSpectStepLE.setEnabled(not self.cSpectStepRB.isChecked()))
        self.cSpectAmtRB.toggled.connect(
            lambda: self.cSpectAmtLE.setEnabled(not self.cSpectAmtRB.isChecked()))

        self.eXSpectStepRB.toggled.connect(
            lambda: self.eXSpectStepLE.setEnabled(not self.eXSpectStepRB.isChecked()))
        self.eYSpectStepRB.toggled.connect(
            lambda: self.eYSpectStepLE.setEnabled(not self.eYSpectStepRB.isChecked()))

        self.cPaintPB.clicked.connect(self.paintCircle)
        self.ePaintPB.clicked.connect(self.paintEllipse)

        self.canvasClearPB.clicked.connect(self.clearCanvas)

        self.cCmpPB.clicked.connect(self.measureTimeCircle)
        self.eCmpPB.clicked.connect(self.measureTimeEllipse)

        self.msgbox = QtWidgets.QMessageBox(self)

        self.show()

    def clearCanvas(self):
        self.canvas.shapes.clear()

        self.canvas.update()

    def tryGetLineEditData(self, lineEdit, T=float, vmin=None, vmax=None, vdefault=0):
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

    def selectAlg(self, pts, figure='c'):
        col = self.colorview.color
        if self.canonicRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(CircleCanonicDraw(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(
                        EllipseCanonicDraw(*c, color=col))
        elif self.paramRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(
                        CircleParametricDraw(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(
                        EllipseParametricDraw(*c, color=col))
        elif self.midpointRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(
                        CircleMidpointDraw(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(
                        EllipseMidpointDraw(*c, color=col))
        elif self.bresRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(
                        CircleBresenhamDraw(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(
                        EllipseBresenhamDraw(*c, color=col))
        elif self.libRB.isChecked():
            for c in pts:
                self.canvas.shapes.append((c, col, True))

    def getCircleData(self, spectrum=False):
        if spectrum:
            cx = self.tryGetLineEditData(self.cSpectCXLE, vmin=0)
            cy = self.tryGetLineEditData(self.cSpectCYLE, vmin=0)
            rs = self.tryGetLineEditData(self.cSpectRadStartLE, vmin=0)
            re = self.tryGetLineEditData(self.cSpectRadEndLE, vmin=0)
            st = self.tryGetLineEditData(self.cSpectStepLE, T=int, vmin=1)
            amt = self.tryGetLineEditData(self.cSpectAmtLE, T=int, vmin=1)
            return cx, cy, rs, re, st, amt
        else:
            cx = self.tryGetLineEditData(self.cxLE, vmin=0)
            cy = self.tryGetLineEditData(self.cyLE, vmin=0)
            r = self.tryGetLineEditData(self.rLE, vmin=0)
            return cx, cy, r

    def getEllipseData(self, spectrum=False):
        if spectrum:
            cx = self.tryGetLineEditData(self.eSpectCXLE, vmin=0)
            cy = self.tryGetLineEditData(self.eSpectCYLE, vmin=0)
            astart = self.tryGetLineEditData(self.eSpectAStartLE, vmin=0)
            bstart = self.tryGetLineEditData(self.eSpectBStartLE, vmin=0)
            sta = self.tryGetLineEditData(self.eXSpectStepLE, T=int, vmin=1)
            stb = self.tryGetLineEditData(self.eYSpectStepLE, T=int, vmin=1)
            amt = self.tryGetLineEditData(self.eSpectAmtLE, T=int, vmin=1)
            return cx, cy, astart, bstart, sta, stb, amt
        else:
            cx = self.tryGetLineEditData(self.exLE, vmin=0)
            cy = self.tryGetLineEditData(self.eyLE, vmin=0)
            a = self.tryGetLineEditData(self.aLE, vmin=0)
            b = self.tryGetLineEditData(self.bLE, vmin=0)
            return cx, cy, a, b

    def decideCircleSpectrumAllowedData(self, data: list):
        pts = []
        if self.cSpectRadStartRB.isChecked():
            pts = CreateCircleSpectrum(*data, hidden='rstart')
        elif self.cSpectRadEndRB.isChecked():
            pts = CreateCircleSpectrum(*data, hidden='rend')
        elif self.cSpectStepRB.isChecked():
            pts = CreateCircleSpectrum(*data, hidden='step')
        else:
            pts = CreateCircleSpectrum(*data, hidden='amt')
        return pts

    def decideEllipseSpectrumAllowedData(self, data: list):
        pts = []
        if self.eXSpectStepRB.isChecked():
            pts = CreateEllipseSpectrum(*data, hidden='stepa')
        elif self.eYSpectStepRB.isChecked():
            pts = CreateEllipseSpectrum(*data, hidden='stepb')
        return pts

    def paintCircle(self):
        if self.cSpectrumCB.isChecked():
            pts = self.decideCircleSpectrumAllowedData((0, 0, 1, STEP, AMT, "rend"))
            self.selectAlg(pts)
        else:
            pts = self.getCircleData(spectrum=False)

            if None in pts:
                return

            self.selectAlg([pts])
        self.canvas.update()

    def paintEllipse(self):
        if self.eSpectrumCB.isChecked():
            # data = self.getEllipseData(spectrum=True)

            pts = self.decideEllipseSpectrumAllowedData((0, 0, 2, 1, STEP, STEP, AMT, "stepb"))
            self.selectAlg(pts, figure='e')
        else:
            pts = self.getEllipseData(spectrum=False)

            if None in pts:
                return

            self.selectAlg([pts], figure='e')
        self.canvas.update()

    def measureTimeCircle(self):
        data = self.getCircleData(spectrum=True)

        if None in data:
            return

        pts = self.decideCircleSpectrumAllowedData(data)

        painter = QPainter()
        methods = (
            CircleCanonicMeasure,
            CircleParametricMeasure,
            CircleMidpointMeasure,
            CircleBresenhamMeasure,
            lambda R: painter.drawEllipse(0, 0, R, R)
        )
        times = [[0 for _ in pts] for _ in range(len(methods))]
        radiuses = [round(r[-1]) for r in pts]

        for m in range(len(times)):
            for rad in range(len(times[m])):
                for _ in range(REPS):
                    beg = time()
                    methods[m](radiuses[rad])
                    end = time()
                    times[m][rad] += end - beg
                times[m][rad] /= REPS

        plt.figure(figsize=(10, 6))
        plt.rcParams['font.size'] = '15'
        plt.title(
            f"Скорость построения окружностей в зависимости от радиуса\n(шаг изменения радиуса = {radiuses[1] - radiuses[0]})")

        methods = ["Каноническое\nуравнение", "Параметрическое\nуравнение", "Алгоритм\nсредней точки",
                   "Алгоритм\nБрезенхема", "Библиотечная\nфункция"]
        plt.ylabel("Время")

        for t in range(len(times)):
            plt.plot(radiuses, times[t], label=methods[t])

        plt.legend()
        plt.show()

    def measureTimeEllipse(self):
        data = self.getEllipseData(spectrum=True)

        if None in data:
            return

        pts = self.decideEllipseSpectrumAllowedData(data)

        painter = QPainter()
        methods = (
            EllipseCanonicMeasure,
            EllipseParametricMeasure,
            EllipseMidpointMeasure,
            EllipseBresenhamMeasure,
            lambda a, b: painter.drawEllipse(0, 0, a, b)
        )

        times = [[0 for _ in pts] for _ in range(len(methods))]
        semiaxes = np.array([tuple(map(round, (a[-2:]))) for a in pts])

        for m in range(len(times)):
            for a in range(len(times[m])):
                for _ in range(REPS):
                    beg = time()
                    methods[m](*semiaxes[a])
                    end = time()
                    times[m][a] += end - beg
                times[m][a] /= REPS

        plt.figure(figsize=(10, 6))
        plt.rcParams['font.size'] = '15'
        plt.title(
            f"Скорость построения эллипсов в зависимости от размеров полуосей\n(шаг изменения полуосей = {semiaxes[1, 0] - semiaxes[0, 0]})")

        methods = ["Каноническое\nуравнение", "Параметрическое\nуравнение", "Алгоритм\nсредней точки",
                   "Алгоритм\nБрезенхема", "Библиотечная\nфункция"]

        plt.ylabel("Время")

        for t in range(len(times)):
            plt.plot(semiaxes[:, 0], times[t], label=methods[t])

        plt.legend()
        plt.show()


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
