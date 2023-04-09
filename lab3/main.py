import sys
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPainter
from time import time

from dda import dda
from bresenham import bresenham_float, bresenham_integer, bresenham_aa
from vu import vu
from utils import generate_spectrum

from numpy import pi, sin, cos

I = 255
RUNS = 30


class UI(QtWidgets.QMainWindow):
    bgColor = QColor(255, 255, 255)

    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab3/lab3.ui', self)
        self.colorDialog = QtWidgets.QColorDialog()

        self.lineColSwatch.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_2.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_3.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_4.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_5.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_6.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_7.changeColor.connect(self.colorview.changeCurColor)

        self.bgColSwatch.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_2.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_3.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_4.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_5.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_6.changeColor.connect(self.canvas.changeBgColor)
        self.bgColSwatch_7.changeColor.connect(self.canvas.changeBgColor)

        self.drawSegPB.clicked.connect(self.paintSegment)
        self.drawSpectrumPB.clicked.connect(self.paintSpectrum)

        self.timeCompPB.clicked.connect(self.measureTime)
        self.aliasCompPB.clicked.connect(self.measureSteps)

        self.clearPB.clicked.connect(self.clearCanvas)
        self.show()

    def tryGetLineEditData(self, lineEdit, vmin=None, vmax=None, vdefault=0):
        try:
            v = float(lineEdit.text())
            if vmin is not None:
                v = max(vmin, v)
            if vmax is not None:
                v = min(vmax, v)
        except:
            lineEdit.setText(f'{vdefault}')
            v = vdefault
        return v

    def getSegmentPoints(self):
        x1 = self.tryGetLineEditData(self.xStartLE, vmin=0)
        y1 = self.tryGetLineEditData(self.yStartLE, vmin=0)
        x2 = self.tryGetLineEditData(self.xEndLE, vmin=0)
        y2 = self.tryGetLineEditData(self.yEndLE, vmin=0)
        return x1, y1, x2, y2

    def getSpectrumData(self):
        cx = self.tryGetLineEditData(self.cxLE, vmin=0)
        cy = self.tryGetLineEditData(self.cyLE, vmin=0)
        angle = self.tryGetLineEditData(self.angleLE, vmax=360)
        length = self.tryGetLineEditData(self.lengthLE)
        return cx, cy, angle, length

    def chooseAlg(self, pts):
        col = self.colorview.color
        col = (col.red(), col.green(), col.blue())
        if self.ddaRB.isChecked():
            for p in pts:
                p = list(map(round, p))
                self.canvas.lines.append(dda(*p, col))
        elif self.brFloatRB.isChecked():
            for p in pts:
                p = list(map(round, p))
                self.canvas.lines.append(bresenham_float(*p, col))
        elif self.brIntRB.isChecked():
            for p in pts:
                p = list(map(round, p))
                self.canvas.lines.append(bresenham_integer(*p, col))
        elif self.brAARB.isChecked():
            for p in pts:
                p = list(map(round, p))
                self.canvas.lines.append(bresenham_aa(*p, col, I))
        elif self.vuRB.isChecked():
            for p in pts:
                p = list(map(round, p))
                self.canvas.lines.append(vu(*p, col, I))
        elif self.libRB.isChecked():
            for p in pts:
                self.canvas.lines.append((p[:2], p[2:], col, True))

    def clearCanvas(self):
        self.canvas.lines.clear()
        self.canvas.update()

    def paintSegment(self):
        pts = self.getSegmentPoints()
        self.chooseAlg([pts])

        self.canvas.update()

    def paintSpectrum(self):
        cx, cy, angle, length = self.getSpectrumData()
        pts = generate_spectrum((cx, cy), angle, length)
        self.chooseAlg(pts)

        self.canvas.update()

    def measureTime(self):
        painter = QPainter()
        methods = (
            dda,
            bresenham_float,
            bresenham_integer,
            bresenham_aa,
            vu,
            lambda x1, y1, x2, y2: painter.drawLine(
                QPointF(x1, y1), QPointF(x2, y2))
        )

        times = [0 for _ in range(len(methods))]

        cx, cy, angle, length = self.getSpectrumData()
        pts = generate_spectrum((cx, cy), angle, length)
        for i in range(len(methods)):
            for _ in range(RUNS):
                for p in pts:
                    beg = time()
                    methods[i](*p)
                    end = time()
                    times[i] += end - beg
            times[i] /= RUNS

        plt.figure(figsize=(10, 6))
        plt.rcParams['font.size'] = '15'
        plt.title(
            f"Скорость построения спектров (угол {angle:g}°, длина {length:g})\nв зависимости от алгоритма")

        positions = [i for i in range(6)]
        methods = ["ЦДА", "Брезенхем\n(float)", "Брезенхем\n(int)",
                   "Брезенхем\n(с устранением\n ступенчатости)", "Ву", "Библиотечная\nфункция"]

        plt.xticks(positions, methods)
        plt.ylabel("Время")

        plt.bar(positions, times, align="center", alpha=1)

        plt.show()

    def measureSteps(self):
        methods = (
            dda,
            bresenham_float,
            bresenham_integer,
            bresenham_aa,
            vu
        )

        _, _, _, length = self.getSpectrumData()

        da = 2
        angles = [i for i in range(0, 91, da)]

        steps = [[0 for _ in range(len(angles))] for _ in range(len(methods))]
        a = 0
        ia = 0
        while a <= pi / 2:
            p = (cos(a) * length, sin(a) * length)
            for i in range(len(methods)):
                steps[i][ia] = methods[i](0, 0, round(p[0]), round(p[1]), stepmode=True)
            ia += 1
            a += da * pi / 180

        plt.rcParams['font.size'] = '15'
        plt.figure("Исследование ступенчатости алгоритмов.", figsize=(18, 10))

        plt.plot(angles, steps[0], label="ЦДА")
        plt.plot(angles, steps[1], '--',  label="Брензенхем (float)")
        plt.plot(angles, steps[2], '--', label="Брензенхем (int)")
        plt.plot(angles, steps[3], '.-',  label="Брензенхем (устр. ступенч.)")
        plt.plot(angles, steps[4], '-.', label="By")

        plt.title(f"Исследование ступенчатости.\nДлина отрезка: {length:g}")
        plt.xticks([i for i in range(0, 91, 5)])
        plt.legend()
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.show()


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
