from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText

LEFT_BTN = 1
RIGHT_BTN = 2

class CanvasPolygon:
    def __init__(self) -> None:
        self.points = []
        self.ready = False
    
    def __getitem__(self, key):
        return self.points[key]

    def __len__(self):
        return len(self.points)

    def draw(self, painter: QPainter):
        for i in range(1, len(self.points)):
            painter.drawLine(self.points[i - 1], self.points[i])

    def addPoint(self, point: QPointF):
        self.points.append(point)

    def isReady(self):
        return self.ready
    
    def setReady(self):
        self.points.append(self.points[0])
        self.ready = True

    def __repr__(self) -> str:
        return f'<Canvas>(len={len(self.points)}, ready={self.ready})'


class Canvas(QtWidgets.QWidget):
    bgColor = QColor(255, 255, 255)
    curPosLabel = None
    canvasPolygons = []

    parentPtr = None
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)

        self.painter = QPainter()
        self.pen = QPen(QColor(0, 0, 0))

        self.update()

    def setParent(self, parent):
        self.parentPtr = parent

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
            painter.drawStaticText(QPoint(i - 10 * (f'{i}'.__len__() // 2), margin), QStaticText(f'{i}'))

        for i in range(start, self.height(), step):
            painter.drawLine(QPoint(0, i), QPoint(mark_len, i))
            painter.drawStaticText(QPoint(margin, i - 10 * (f'{i}'.__len__() // 2)), QStaticText(f'{i}'))
    
    def mouseMoveEvent(self, event):
        self.curMousePos = event.pos()
        self.update()

    def addPointToCanvas(self, pos):
        if len(self.canvasPolygons) == 0 or self.canvasPolygons[-1].isReady():
            self.canvasPolygons.append(CanvasPolygon())
        self.canvasPolygons[-1].addPoint(pos)
        self.parentPtr.table.addToTable(self.canvasPolygons[-1].points[-1])
    
    def closeCanvasPolygon(self):
        if len(self.canvasPolygons) != 0 and not self.canvasPolygons[-1].isReady():
            if len(self.canvasPolygons[-1]) > 2:
                self.canvasPolygons[-1].setReady()  
                self.parentPtr.table.addToTable(QPoint(-1, -1))


    def mousePressEvent(self, event):
        if event.button() == LEFT_BTN:
            self.addPointToCanvas(event.pos())

        elif event.button() == RIGHT_BTN:
            self.closeCanvasPolygon()

        self.update()


    def paintEvent(self, event):
        self.painter.begin(self)

        self.painter.fillRect(0, 0, self.width(), self.height(), self.bgColor)

        self.__drawCoords(self.painter)

        for polygon in self.canvasPolygons:
            polygon.draw(self.painter)

        if len(self.canvasPolygons) != 0 and not self.canvasPolygons[-1].isReady():
            self.painter.drawLine(self.canvasPolygons[-1].points[-1], self.curMousePos)

        self.painter.end()
