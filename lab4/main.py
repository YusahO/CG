import sys
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPainter
from time import time

from canonic import CircleCanonic, EllipseCanonic
from parametric import CircleParametric, EllipseParametric
from midpoint import CircleMidpoint, EllipseMidpoint
from bresenham import CircleBresenham, EllipseBresenham

from utils import CreateCircleSpectrum, CreateEllipseSpectrum

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

        self.cSpectrumCB.stateChanged.connect(lambda: self.circleSW.setCurrentIndex(self.cSpectrumCB.isChecked()))
        self.eSpectrumCB.stateChanged.connect(lambda: self.ellipseSW.setCurrentIndex(self.eSpectrumCB.isChecked()))

        self.cSpectRadStartRB.toggled.connect(lambda: self.cSpectRadStartLE.setEnabled(not self.cSpectRadStartRB.isChecked()))
        self.cSpectRadEndRB.toggled.connect(lambda: self.cSpectRadEndLE.setEnabled(not self.cSpectRadEndRB.isChecked()))
        self.cSpectStepRB.toggled.connect(lambda: self.cSpectStepLE.setEnabled(not self.cSpectStepRB.isChecked()))
        self.cSpectAmtRB.toggled.connect(lambda: self.cSpectAmtLE.setEnabled(not self.cSpectAmtRB.isChecked()))


        self.eSpectAxisStartRB.toggled.connect(lambda: self.eSpectAStartLE.setEnabled(not self.eSpectAxisStartRB.isChecked()))
        self.eSpectAxisStartRB.toggled.connect(lambda: self.eSpectBStartLE.setEnabled(not self.eSpectAxisStartRB.isChecked()))
        self.eSpectAxisEndRB.toggled.connect(lambda: self.eSpectAEndLE.setEnabled(not self.eSpectAxisEndRB.isChecked()))
        self.eSpectAxisEndRB.toggled.connect(lambda: self.eSpectBEndLE.setEnabled(not self.eSpectAxisEndRB.isChecked()))
        self.eSpectStepRB.toggled.connect(lambda: self.eSpectStepLE.setEnabled(not self.eSpectStepRB.isChecked()))
        self.eSpectAmtRB.toggled.connect(lambda: self.eSpectAmtLE.setEnabled(not self.eSpectAmtRB.isChecked()))


        self.cPaintPB.clicked.connect(self.paintCircle)
        self.ePaintPB.clicked.connect(self.paintEllipse)

        self.canvasClearPB.clicked.connect(self.clearCanvas)

        self.show()

    def clearCanvas(self):
        self.canvas.shapes.clear()

        self.canvas.update()

    def tryGetLineEditData(self, lineEdit, T=float, vmin=None, vmax=None, vdefault=0):
        try:
            v = T(lineEdit.text())
            if vmin is not None:
                v = max(vmin, v)
            if vmax is not None:
                v = min(vmax, v)
        except:
            v = vdefault
        return v

    def selectAlg(self, pts, figure='c'):
        col = self.colorview.color
        if self.canonicRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(CircleCanonic(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(EllipseCanonic(*c, color=col))
        elif self.paramRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(CircleParametric(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(EllipseParametric(*c, color=col))
        elif self.midpointRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(CircleMidpoint(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(EllipseMidpoint(*c, color=col))
        elif self.bresRB.isChecked():
            for c in pts:
                if figure == 'c':
                    self.canvas.shapes.append(CircleBresenham(*c, color=col))
                elif figure == 'e':
                    self.canvas.shapes.append(EllipseBresenham(*c, color=col))
        elif self.libRB.isChecked():
            for c in pts:
                self.canvas.shapes.append((c, col, True))


    def getCircleData(self, spectrum=False):
        if spectrum:
            cx = self.tryGetLineEditData(self.cSpectCXLE)
            cy = self.tryGetLineEditData(self.cSpectCYLE)
            rs = self.tryGetLineEditData(self.cSpectRadStartLE)
            re = self.tryGetLineEditData(self.cSpectRadEndLE)
            st = self.tryGetLineEditData(self.cSpectStepLE, T=int)
            amt = self.tryGetLineEditData(self.cSpectAmtLE, T=int)
            return cx, cy, rs, re, st, amt
        else:
            cx = self.tryGetLineEditData(self.cxLE)
            cy = self.tryGetLineEditData(self.cyLE)
            r = self.tryGetLineEditData(self.rLE)
            return cx, cy, r

    def getEllipseData(self, spectrum=False):
        if spectrum:
            cx = self.tryGetLineEditData(self.eSpectCXLE)
            cy = self.tryGetLineEditData(self.eSpectCYLE)
            astart = self.tryGetLineEditData(self.eSpectAStartLE)
            bstart = self.tryGetLineEditData(self.eSpectBStartLE)
            aend = self.tryGetLineEditData(self.eSpectAEndLE)
            bend = self.tryGetLineEditData(self.eSpectBEndLE)
            st = self.tryGetLineEditData(self.eSpectStepLE, T=int)
            amt = self.tryGetLineEditData(self.eSpectAmtLE, T=int)
            return cx, cy, astart, bstart, aend, bend, st, amt
        else:
            cx = self.tryGetLineEditData(self.exLE)
            cy = self.tryGetLineEditData(self.eyLE)
            a = self.tryGetLineEditData(self.aLE)
            b = self.tryGetLineEditData(self.bLE)
            return cx, cy, a, b

    def paintCircle(self):
        if self.cSpectrumCB.isChecked():
            data = self.getCircleData(spectrum=True)
            pts = []
            if self.cSpectRadStartRB.isChecked():
                pts = CreateCircleSpectrum(*data, hidden='rstart')
            elif self.cSpectRadEndRB.isChecked():
                pts = CreateCircleSpectrum(*data, hidden='rend')
            elif self.cSpectStepRB.isChecked():
                pts = CreateCircleSpectrum(*data, hidden='step')
            else:
                pts = CreateCircleSpectrum(*data, hidden='amt')
            self.selectAlg(pts)
        else:
            pts = self.getCircleData(spectrum=False)
            self.selectAlg([pts])
        self.canvas.update()

    def paintEllipse(self):
        if self.eSpectrumCB.isChecked():
            data = self.getEllipseData(spectrum=True)
            pts = []
            if self.cSpectRadStartRB.isChecked():
                pts = CreateEllipseSpectrum(*data, hidden='rstart')
            elif self.cSpectRadEndRB.isChecked():
                pts = CreateEllipseSpectrum(*data, hidden='rend')
            elif self.cSpectStepRB.isChecked():
                pts = CreateEllipseSpectrum(*data, hidden='step')
            else:
                pts = CreateEllipseSpectrum(*data, hidden='amt')
            self.selectAlg(pts, figure='e')
        else:
            pts = self.getEllipseData(spectrum=False)
            self.selectAlg([pts], figure='e')
        self.canvas.update()


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
