from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QThread, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
from time import time_ns, sleep

LMB = 1
RMB = 2


class Polygon:
    def __init__(self, color=QColor(0, 0, 0)) -> None:
        self.points = []
        self.color = color
        self.ready = False

    def __getitem__(self, key):
        return self.points[key]

    def __len__(self):
        return len(self.points)

    def __repr__(self) -> str:
        return f'<Canvas>(len={len(self.points)}, ready={self.ready})'

    def draw(self, painter: QPainter):
        pen = QPen(self.color)
        painter.setPen(pen)
        for i in range(1, len(self.points)):
            painter.drawLine(self.points[i - 1], self.points[i])

    def addPoint(self, point: QPointF):
        self.points.append(point)

    def isReady(self):
        return self.ready

    def setReady(self):
        self.points.append(self.points[0])
        self.ready = True


class Canvas(QtWidgets.QLabel):
    fillColor = QColor(255, 255, 255)
    curPosLabel = None
    canvasPolygons = []
    rects = []
    filling = False

    parentPtr = None

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)

        self.painter = QPainter()
        self.pen = QPen(QColor(0, 0, 0))

        self.curMousePos = QPoint(0, 0)
        self.shiftPressed = False

        self.update()

    def drawToPixmap(self):
        painter = QPainter(self.pixmap())
        
        for polygon in self.canvasPolygons:
            polygon.draw(painter)
        
        painter.end()

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

    def addPointToCanvas(self, pos, from_mouse=True):       
        if len(self.canvasPolygons) == 0 or self.canvasPolygons[-1].isReady():
            self.canvasPolygons.append(
                Polygon(self.parentPtr.colorview_1.color))

        if from_mouse:
            pos = self.getValidMpos()

        self.canvasPolygons[-1].addPoint(pos)
        if self.canvasPolygons[-1].points[-1] is not None:
            self.parentPtr.table.addToTable(self.canvasPolygons[-1].points[-1])

    def closeCanvasPolygon(self):
        if len(self.canvasPolygons) != 0 and not self.canvasPolygons[-1].isReady():
            if len(self.canvasPolygons[-1]) > 2:
                self.canvasPolygons[-1].setReady()
                self.parentPtr.table.addToTable(QPoint(-1, -1))

    def mouseMoveEvent(self, event) -> None:
        self.parentPtr.curposLabel.setText(
            f'Текущая позиция ({event.pos().x()}, {event.pos().y()})')
        p = QPainter(self.pixmap())
        p.setPen(self.pen)
        p.drawRect(self.rect())
        self.setFocus(True)
        self.curMousePos = QPointF(event.x(), event.y())
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
        if event.button() == LMB:
            self.addPointToCanvas(event.pos())

        elif event.button() == RMB:
            self.closeCanvasPolygon()

        self.drawToPixmap()
        self.update()

    def drawLinesToCanv(self):
        for polygon in self.canvasPolygons:
            polygon.draw(self.painter)

        if len(self.canvasPolygons) != 0 and not self.canvasPolygons[-1].isReady():
            mpos_to_draw = self.getValidMpos()

            self.painter.drawLine(
                self.canvasPolygons[-1].points[-1], mpos_to_draw)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap())

        self.painter.fillRect(0, 0, self.width(), self.height(), 0xFFFFFF)

        self.__drawCoords(self.painter)

        if not self.filling or True:
            self.drawLinesToCanv()

        self.painter.setPen(self.pen)
        self.painter.end()

    def fillNoDelay(self):
        self.filling = True
        start = time_ns()

        self.fillColor = self.parentPtr.colorview_2.color
        points = []
        for pol in self.canvasPolygons:
            for p in pol.points:
                points.append([int(p.x()), int(p.y())])
        rectPts = GetRect(points)
        self.rects = rectPts

        painter = QtGui.QPainter(self.pixmap())

        for pol in self.canvasPolygons:
            points = [[int(p.x()), int(p.y())] for p in pol.points]
            for i in range(len(points) - 1):
                GetCollisionNoDelay(
                    rectPts, points[i], points[i + 1], painter, self.pixmap(), col=self.fillColor)

        painter.end()
        end = time_ns()
        self.parentPtr.timeLabel.setText(
            f'Время построения {(end - start) / 1e6 : .3f} мс')
        
        self.drawToPixmap()
        self.filling = False
        self.update()

    def fillDelay(self, delay):
        self.filling = True

        self.fillColor = self.parentPtr.colorview_2.color
        points = []
        for pol in self.canvasPolygons:
            for p in pol.points:
                points.append([int(p.x()), int(p.y())])
        rectPts = GetRect(points)
        self.rects = rectPts

        painter = QtGui.QPainter(self.pixmap())
        for pol in self.canvasPolygons:
            points = [[int(p.x()), int(p.y())] for p in pol.points]
            for i in range(len(points) - 1):
                GetCollisionDelay(
                    rectPts, points[i], points[i + 1], painter, self, delay, col=self.fillColor)
        painter.end()

        self.drawToPixmap()
        self.filling = False
        self.update()


def GetRect(pts):
    left, right, top, bottom = float("inf"), float(
        "-inf"), float("inf"), float("-inf")

    for p in pts:
        left = min(left, p[0])
        right = max(right, p[0])
        top = min(top, p[1])
        bottom = max(bottom, p[1])

    return [left, top, right, bottom]


def sameCol(col1, col2):
    for i in range(3):
        if col1[i] != col2[i]:
            return False
    return True


def GetCollisionNoDelay(rect, p1, p2, painter, pixmap, col=QColor(0, 0, 0)):
    if (p1[1] == p2[1]):
        return

    if (p1[1] > p2[1]):
        p1, p2 = p2, p1

    draw_col = [col.red(), col.green(), col.blue()]
    img = pixmap.toImage()

    dx = (p2[0] - p1[0]) / (p2[1] - p1[1])
    xstart = p1[0] + 0.5

    for y in range(p1[1], p2[1]):
        x = xstart

        pen = QtGui.QPen()
        painter.setPen(pen)

        for ix in range(round(x), rect[2]):
            pix = QtGui.QColor(img.pixel(ix, y))
            pix_col = [pix.red(), pix.green(), pix.blue()]

            if (sameCol(pix_col, draw_col)):
                pen.setColor(QColor(0xFFFFFF))
            else:
                pen.setColor(col)

            painter.setPen(pen)
            painter.drawPoint(ix, y)
        xstart += dx


# def GetCollisionDelay(rect, p1, p2, painter, pixmap, col=QColor(0,0,0)):
def GetCollisionDelay(rect, p1, p2, painter, canv, delay, col=QColor(0, 0, 0)):
    if (p1[1] == p2[1]):
        return

    if (p1[1] > p2[1]):
        p1, p2 = p2, p1

    draw_col = [col.red(), col.green(), col.blue()]
    img = canv.pixmap().toImage()

    dx = (p2[0] - p1[0]) / (p2[1] - p1[1])
    xstart = p1[0] + 0.5

    for y in range(p1[1], p2[1]):
        sleep(delay)
        canv.update()

        x = xstart

        pen = QtGui.QPen()
        painter.setPen(pen)

        for ix in range(round(x), rect[2]):
            pix = QtGui.QColor(img.pixel(ix, y))
            pix_col = [pix.red(), pix.green(), pix.blue()]

            if (sameCol(pix_col, draw_col)):
                pen.setColor(QColor(0xFFFFFF))
            else:
                pen.setColor(col)

            painter.setPen(pen)
            painter.drawPoint(ix, y)
        xstart += dx

    # dx, dy = int(p2[0] - p1[0]), int(p2[1] - p1[1])
    # delta_x, delta_y = abs(dx), abs(dy)
    # l = max(delta_x, delta_y)

    # dx /= l
    # dy /= l

    # x, y = int(p1[0]), int(p1[1])
    # draw_y = round(y)

    # for _ in range(l):
    #     x += dx
    #     y += dy
    #     if(draw_y < (y - 0.5)):

    #         draw_y += 1
    #         pen = QtGui.QPen()
    #         painter.setPen(pen)

    #         for i in range(round(x), rect[2]):
    #             pix = QtGui.QColor(img.pixel(i, draw_y))
    #             pix_col = [pix.red(), pix.green(), pix.blue()]
    #             if(sameCol(pix_col, draw_col)):
    #                 pen.setColor(QColor(0xFFFFFF))
    #             else:
    #                 pen.setColor(col)

    #             painter.setPen(pen)
    #             painter.drawPoint(i, draw_y)
