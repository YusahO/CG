import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QColor

from dda import dda
from bresenham import bresenham_float, bresenham_integer, bresenham_aa
from utils import generate_spectrum

class UI(QtWidgets.QMainWindow):
    bgColor = QColor(255, 255, 255)
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab3/lab3.ui', self)
        self.colorDialog = QtWidgets.QColorDialog()

        self.lineColPB.clicked.connect(self.setLineColorWithDialog)
        self.bgColPB.clicked.connect(self.setBgColorWithDialog)

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

        self.clearPB.clicked.connect(self.clearCanvas)
        self.show()

    def setLineColorWithDialog(self):
        color = self.colorDialog.getColor()
        self.colorview.changeCurColor(color)

    def setBgColorWithDialog(self):
        color = self.colorDialog.getColor()
        self.canvas.changeBgColor(color)

    def tryGetLineEditData(self, lineEdit, vmin=None, vmax=None, vdefault=0):
        try:
            v = float(lineEdit.text())
            if vmin is not None:
                v = max(vmin, v)
            if vmax is not None:
                v = min(vmax, v)
        except:
            v = vdefault
        return v

    def getSegmentPoints(self):
        x1 = round(self.tryGetLineEditData(self.xStartLE, vmin=0))
        y1 = round(self.tryGetLineEditData(self.yStartLE, vmin=0))
        x2 = round(self.tryGetLineEditData(self.xEndLE, vmin=0))
        y2 = round(self.tryGetLineEditData(self.yEndLE, vmin=0))
        return x1, y1, x2, y2
    
    def getSpectrumData(self):
        cx = round(self.tryGetLineEditData(self.cxLE, vmin=0))
        cy = round(self.tryGetLineEditData(self.cyLE, vmin=0))
        angle = self.tryGetLineEditData(self.angleLE, vmax=360)
        length = self.tryGetLineEditData(self.lengthLE)
        return cx, cy, angle, length

    def chooseAlg(self, pts):
        if self.ddaRB.isChecked():
            for p in pts:
                self.canvas.dda_lines.append(dda(*p, self.colorview.color))
        elif self.brFloatRB.isChecked():
            for p in pts:
                self.canvas.bfloat_lines.append(bresenham_float(*p, self.colorview.color))
        elif self.brIntRB.isChecked():
            for p in pts:
                self.canvas.bint_lines.append(bresenham_integer(*p, self.colorview.color))
        elif self.brAARB.isChecked():
            for p in pts:
                self.canvas.baa_lines.append(bresenham_aa(*p, self.colorview.color, self.canvas.bgColor))
        elif self.libRB.isChecked():
            for p in pts:
                self.canvas.lib_lines.append((p[:2], p[2:], self.colorview.color))

    def clearCanvas(self):
        self.canvas.dda_lines.clear()
        self.canvas.bfloat_lines.clear()
        self.canvas.bint_lines.clear()
        self.canvas.baa_lines.clear()
        self.canvas.vu_lines.clear()
        self.canvas.lib_lines.clear()
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


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
