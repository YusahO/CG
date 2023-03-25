from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import figures as fig

def remap(v, width, height):
    vx = v.x()
    vy = v.y()
    return QtCore.QPointF(vx - width / 2, height / 2 - vy)

class Canvas(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.objectCenter = QtCore.QPointF(self.width() / 2, self.height() / 2)

        self.scalePivot = self.objectCenter
        self.rotPivot = self.objectCenter

        self.pen = QtGui.QPen(
            Qt.red, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.painter = QtGui.QPainter()

        self.obj = fig.BugObject(self.objectCenter)

        self.update()

    def resizeEvent(self, event):
        self.objectCenter = QtCore.QPoint(self.width() // 2, self.height() // 2)
        self.obj.c = self.objectCenter

        self.scalePivot = self.objectCenter
        self.rotPivot = self.objectCenter

        self.obj.calculatePoints(self.obj.c)
        self.update()

    def __paintPivot(self, p, text, color):
        self.pen.setColor(color)
        self.pen.setWidth(8)
        self.painter.setPen(self.pen)
        self.painter.drawPoint(p)
        pm = remap(p, self.width(), self.height())
        self.painter.drawStaticText(p - QtCore.QPointF(-5, 25), QtGui.QStaticText(f'{text} ({pm.x():.2f}; {pm.y():.2f})'))

    def paintEvent(self, event):
        self.painter.begin(self)
        self.pen.setStyle(Qt.DashLine)
        self.pen.setColor(Qt.black)
        self.pen.setDashOffset(3)
        self.pen.setWidth(2)
        self.painter.setPen(self.pen)

        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        self.painter.drawLine(QtCore.QPoint(self.width() // 2, self.height()), QtCore.QPoint(self.width() // 2, 0))
        self.painter.drawLine(QtCore.QPoint(0, self.height() // 2), QtCore.QPoint(self.width(), self.height() // 2))

        self.painter.drawLine(QtCore.QPoint(self.width() - 10, self.height() // 2 + 10), QtCore.QPoint(self.width(), self.height() // 2))
        self.painter.drawLine(QtCore.QPoint(self.width() - 10, self.height() // 2 - 10), QtCore.QPoint(self.width(), self.height() // 2))

        self.painter.drawLine(QtCore.QPoint(self.width() // 2, 0), QtCore.QPoint(self.width() // 2 - 10, 10))
        self.painter.drawLine(QtCore.QPoint(self.width() // 2, 0), QtCore.QPoint(self.width() // 2 + 10, 10))

        self.pen.setWidth(8)
        self.pen.setColor(Qt.red)
        self.painter.setPen(self.pen)

        self.pen.setStyle(Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(Qt.black)
        self.painter.setPen(self.pen)
        self.obj.paint(self.painter)

        diff = self.rotPivot - self.scalePivot
        w, h = self.width(), self.height()
        if abs(diff.x()) <= 1e-5 and abs(diff.y()) <= 1e-5:
            self.__paintPivot(self.rotPivot, 'Поворот/Масштабирование', Qt.darkRed)
        else:
            self.__paintPivot(self.rotPivot, 'Поворот', Qt.darkGreen)
            self.__paintPivot(self.scalePivot, 'Масштабирование', Qt.blue)
            
        self.painter.end()