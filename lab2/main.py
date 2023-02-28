from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import sys
from canvas import Canvas
import figures as fig

def remap(v, width, height):
    vx = v.x()
    vy = v.y()
    return QtCore.QPointF(vx - width / 2, height / 2 - vy)

def remap_back(v, width, height):
    vx = v.x()
    vy = v.y()
    return QtCore.QPointF(vx + width / 2, height / 2 - vy)

def replace_in_list(l, x, y):
    for i in range(len(l)):
        if l[i] == x:
            l[i] = y
    return l

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab2/main.ui', self)

        # ---------------- Привязка событий к кнопкам ----------------
        self.translatePB.clicked.connect(self.translateFigure)
        self.rotatePB.clicked.connect(self.rotateFigure)
        self.scalePB.clicked.connect(self.scaleFigure)

        self.undoPB.clicked.connect(self.undo)
        self.resetPB.clicked.connect(self.reset)

        self.scalepxLE.textChanged.connect(lambda text: self.updateLineEdits(self.rotpxLE, text))
        self.scalepyLE.textChanged.connect(lambda text: self.updateLineEdits(self.rotpyLE, text))
        self.rotpxLE.textChanged.connect(lambda text: self.updateLineEdits(self.scalepxLE, text))
        self.rotpyLE.textChanged.connect(lambda text: self.updateLineEdits(self.scalepyLE, text))

        self.show()

    def updateLineEdits(self, dstLE, text):
        if self.centerCB.isChecked():
            dstLE.setText(text)
        self.readPivots()

    
    def toggleLineEditStyle(self, lineEdit, error=True):
        if error:
            lineEdit.setStyleSheet(
                '''
                QLineEdit {
                    background-color: #ff847a;
                    color: white
                }
                '''
            )
        else:
            lineEdit.setStyleSheet(
                '''
                QLineEdit {
                    background-color: white;
                    color: black
                }
                '''
            )

    def tryGetLineEditData(self, lineEdit, vmin=None, vmax=None, vdefault=0):
        try:
            v = float(lineEdit.text())
            if None not in (vmin, vmax):
                if not vmin < v < vmax:
                    raise Exception
            self.toggleLineEditStyle(lineEdit, error=False)
        except:
            v = vdefault
        return v
    
    def readPivots(self):
        rpx = self.tryGetLineEditData(self.rotpxLE)
        rpy = self.tryGetLineEditData(self.rotpyLE)

        spx = self.tryGetLineEditData(self.scalepxLE)
        spy = self.tryGetLineEditData(self.scalepyLE)


        w, h = self.canvas.width(), self.canvas.height()
        piv = remap_back(QtCore.QPointF(rpx, rpy), w, h)
        self.canvas.rotPivot = piv

        piv = remap_back(QtCore.QPointF(spx, spy), w, h)
        self.canvas.scalePivot = piv

        self.canvas.update()
    
    def translateFigure(self):
        dx = self.tryGetLineEditData(self.dxLE, vdefault=None)
        dy = self.tryGetLineEditData(self.dyLE, vdefault=None)

        if dx is None:
            self.dxLE.setText('0.0')
            dx = 0
        if dy is None:
            self.dyLE.setText('0.0')
            dy = 0

        self.canvas.obj.translateObject([dx, -dy])
        self.canvas.update()

    def rotateFigure(self):
        px = self.tryGetLineEditData(self.rotpxLE, vdefault=None)
        py = self.tryGetLineEditData(self.rotpyLE, vdefault=None)
        angle = self.tryGetLineEditData(self.angleLE, vdefault=None)

        if px is None:
            self.rotpxLE.setText('0.0')
            px = 0
        if py is None:
            self.rotpyLE.setText('0.0')
            py = 0
        if angle is None:
            self.angleLE.setText('0.0')
            angle = 0

        w, h = self.canvas.width(), self.canvas.height()
        piv = remap_back(QtCore.QPointF(px, py), w, h)
        self.canvas.obj.rotateObject(piv, angle * 3.1416 / 180)
        self.canvas.update()

    def scaleFigure(self):
        px = self.tryGetLineEditData(self.scalepxLE, vdefault=None)
        py = self.tryGetLineEditData(self.scalepyLE, vdefault=None)
        kx = self.tryGetLineEditData(self.kxLE, vdefault=None)
        ky = self.tryGetLineEditData(self.kyLE, vdefault=None)

        if px is None:
            self.scalepxLE.setText('0.0')
            px = 0
        if py is None:
            self.scalepyLE.setText('0.0')
            py = 0
        if kx is None:
            self.kxLE.setText('1.0')
            kx = 1
        if ky is None:
            self.kyLE.setText('1.0')
            ky = 1

        w, h = self.canvas.width(), self.canvas.height()
        piv = remap_back(QtCore.QPointF(px, py), w, h)
        self.canvas.obj.scaleObject(piv, [kx, ky])
        self.canvas.update()

    def undo(self):
        self.canvas.obj.undo()
        self.canvas.update()

    def reset(self):
        self.canvas.obj.reset()
        self.canvas.update()

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
