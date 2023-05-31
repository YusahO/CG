from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap

LMB = 1
RMB = 2

class Canvas(QtWidgets.QLabel):
    parentPtr = None
    cutter = []
    lines = []
    results = []

    input_rect = False
    input_line = False

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)

        self.painter = QPainter()
        self.pen = QPen(QColor(0, 0, 0))

        self.shiftPressed = False

        self.update()

    def resizeEvent(self, event) -> None:
        self.setPixmap(QPixmap(event.size().width(), event.size().height()))
        self.pixmap().fill(QColor(0xFFFFFF))

    def setParent(self, parent):
        self.parentPtr = parent

    def setColor(self, color):
        self.pen.setColor(color)
        self.painter.setPen(self.pen)

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Shift:
            self.shiftPressed = True
            self.update()

    def keyReleaseEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_Shift:
            self.shiftPressed = False
            self.update()

    def __drawCoords(self, painter: QPainter):
        margin = 10
        mark_len = 5
        step = 50
        start = 50

        pen = QPen()
        pen.setColor(QColor(127, 127, 127))
        painter.setPen(pen)

        painter.drawRect(0, 0, int(mark_len * 2/3), self.height())
        painter.drawRect(0, 0, self.width(), int(mark_len * 2/3))

        for i in range(start, self.width(), step):
            painter.drawLine(QPoint(i, 0), QPoint(i, mark_len))
            painter.drawStaticText(
                QPoint(i - 10 * (f'{i}'.__len__() // 2), margin), QStaticText(f'{i}'))

        for i in range(start, self.height(), step):
            painter.drawLine(QPoint(0, i), QPoint(mark_len, i))
            painter.drawStaticText(
                QPoint(margin, i - 10 * (f'{i}'.__len__() // 2)), QStaticText(f'{i}'))

    def mouseMoveEvent(self, event):
        self.curMousePos = event.pos()
        self.update()

    def getShiftFixedMpos(self):
        mpos = QPointF(self.curMousePos.x(), self.curMousePos.y())
        if len(self.canvasPolygons) == 0 or len(self.canvasPolygons[-1]) == 0:
            return mpos

        x_dist = abs(mpos.x() - self.canvasPolygons[-1].points[-1].x())
        y_dist = abs(mpos.y() - self.canvasPolygons[-1].points[-1].y())
        if x_dist < y_dist:
            mpos.setX(self.canvasPolygons[-1].points[-1].x())
        else:
            mpos.setY(self.canvasPolygons[-1].points[-1].y())
        return mpos

    def getValidMpos(self):
        if self.shiftPressed:
            return self.getShiftFixedMpos()
        return self.curMousePos

    def mousePressEvent(self, event):
        if event.button() == LMB and len(self.lines) // 3 < 10:
            if len(self.lines) % 3 == 0:
                self.lines.append(self.parentPtr.getPBColor(self.parentPtr.lineColor))
            self.lines.append(event.pos())
        elif event.button() == RMB:
            if len(self.cutter) + 1 > 3:
                self.cutter.clear()
            if len(self.cutter) == 0:
                self.cutter.append(self.parentPtr.getPBColor(self.parentPtr.sepColor))
            self.cutter.append(event.pos())
        self.update()

    def drawLinesToCanv(self):
        for i in range(0, len(self.lines) - 2, 3):
            self.pen.setColor(self.lines[i])
            self.painter.setPen(self.pen)
            self.painter.drawLine(self.lines[i + 1], self.lines[i + 2])

        if len(self.lines) % 3 == 2:
            self.pen.setColor(self.lines[-2])
            self.painter.setPen(self.pen)
            self.painter.drawLine(self.lines[-1], self.curMousePos)

    def drawCutterToCanv(self):
        if len(self.cutter) > 0:
            self.pen.setColor(self.cutter[0])
            self.painter.setPen(self.pen)

        if len(self.cutter) == 3:
            r = QRectF(QPointF(self.cutter[1]), QPointF(self.cutter[2]))
            self.painter.drawRect(r)
        elif len(self.cutter) == 2:
            r = QRectF(self.cutter[1], self.curMousePos)
            self.painter.drawRect(r)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap())

        self.painter.fillRect(0, 0, self.width(), self.height(), 0xFFFFFF)

        self.__drawCoords(self.painter)

        self.drawCutterToCanv()
        self.drawLinesToCanv()

        self.painter.setPen(self.pen)
        self.painter.end()
