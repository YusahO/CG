from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import QPoint, QPointF, QLineF

LEFT_BTN = 1
RIGHT_BTN = 2

class CanvasPolygon:
    def __init__(self) -> None:
        self.points = []
        self.ready = False


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
    
    def __len__(self):
        return len(self.points)

class Canvas(QtWidgets.QLabel):
    canvas_polygons = []
    def __init__(self, parent):
        super().__init__(parent)
        # print(self.pixmap())
        # self.pixmap().fill(QColor(0xFFFFFF))
        self.setMouseTracking(True)
        self.painter = QPainter()
        self.pen = QPen(QColor(0, 0, 0))

        self.cur_mouse = QPoint(0, 0)
        self.shift_pressed = False

    def resizeEvent(self, a0) -> None:
        self.setPixmap(QPixmap(a0.size().width(), a0.size().height()))
        self.pixmap().fill(QColor(0xFFFFFF))
    
    def setParent(self, parent):
        self.parent_ref = parent

    def setColor(self, color):
        self.pen.setColor(color)
        self.painter.setPen(self.pen)

    def keyPressEvent(self, a0) -> None:
        if a0.key() == QtCore.Qt.Key_Shift:
            self.shift_pressed = True
            self.update()
            
    def keyReleaseEvent(self, a0) -> None:
        if a0.key() == QtCore.Qt.Key_Shift:
            self.shift_pressed = False
            self.update()

    def mousePressEvent(self, a0) -> None:
        # self.pixmap().fill(QColor(0xFFFF00))
        if a0.button() == LEFT_BTN:
            if len(self.canvas_polygons) == 0 or self.canvas_polygons[-1].isReady():
                self.canvas_polygons.append(CanvasPolygon())
            a0 = self.getValidMpos()
            self.canvas_polygons[-1].addPoint(QPointF(a0.x(), a0.y()))

        elif a0.button() == RIGHT_BTN:
            if len(self.canvas_polygons) != 0:
                if len(self.canvas_polygons[-1]) <= 2:
                    self.canvas_polygons.pop(-1)
                elif not self.canvas_polygons[-1].isReady():
                    self.canvas_polygons[-1].setReady()
        print(self.canvas_polygons)
        self.parent_ref.tableWidget.rebuildTable(self.canvas_polygons)

        self.update()

    def mouseMoveEvent(self, a0) -> None:
        p = QPainter(self.pixmap())
        p.setPen(self.pen)
        p.drawRect(self.rect())
        self.setFocus(True)
        self.cur_mouse = QPointF(a0.x(), a0.y())
        self.update()

    def getShiftFixedMpos(self):
        mpos = QPointF(self.cur_mouse.x(), self.cur_mouse.y())
        x_dist = abs(mpos.x() - self.canvas_polygons[-1].points[-1].x())
        y_dist = abs(mpos.y() - self.canvas_polygons[-1].points[-1].y())
        if x_dist < y_dist:
            mpos.setX(self.canvas_polygons[-1].points[-1].x())
        else:
            mpos.setY(self.canvas_polygons[-1].points[-1].y())
        return mpos
    
    def getValidMpos(self):
        if self.shift_pressed:
            return self.getShiftFixedMpos()
        return self.cur_mouse
    
    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap())
        self.setColor(QColor(0x000000))
        self.painter.drawRect(0, 0, self.size().width() -
                              1, self.size().height() - 1)
        
        for polygon in self.canvas_polygons:
            polygon.draw(self.painter)

        if len(self.canvas_polygons) != 0 and not self.canvas_polygons[-1].isReady():
            mpos_to_draw = self.getValidMpos()
            self.painter.drawLine(self.canvas_polygons[-1].points[-1], mpos_to_draw)

        self.painter.end()
 
 
    def fill(self):
        print(self.pixmap().rect())
        points = []
        for pol in self.canvas_polygons:
            for p in pol.points:
                points.append([int(p.x()), int(p.y())])
        rectPts = GetRect(points)
        self.recta = rectPts
        # self.DrawImage() 
        painter = QtGui.QPainter(self.pixmap())
        for pol in self.canvas_polygons:
            points = [[int(p.x()), int(p.y())] for p in pol.points]
            for i in range(len(points) - 1):
                GetCollision(rectPts, points[i], points[i + 1], painter, self.pixmap())
        painter.end()
        # self.lbPixmap.setPixmap(self.pixmap())
        self.update()


def GetRect(pts):
    left, right, top, bottom = float("inf"), float("-inf"), float("inf"), float("-inf")

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

def GetCollision(rect, p1, p2, painter, pixmap, col=QColor(0xFF0000)):
    if(p1[1] > p2[1]):
        p1, p2 = p2, p1

    draw_col = [col.red(), col.green(), col.blue()]
    img = pixmap.toImage()

    dx, dy = int(p2[0]) - int(p1[0]), int(p2[1]) - int(p1[1])
    delta_x, delta_y = abs(dx), abs(dy)
    l = delta_x if delta_x > delta_y else delta_y    
    dx /= l
    dy /= l
    x, y = int(p1[0]), int(p1[1])
    draw_y = int(y)

    for _ in range(l):
        x += dx
        y += dy
        if(draw_y < (y - 0.5)):
            draw_y += 1
            pen = QtGui.QPen()
            painter.setPen(pen)
            for i in range(int(x), rect[2]):
                pix = QtGui.QColor(img.pixel(i, draw_y))
                pix_col = [pix.red(), pix.green(), pix.blue()]
                if(sameCol(pix_col, draw_col)):
                    pen.setColor(QColor(0xFFFFFF))
                else:
                    pen.setColor(col)
            
                painter.setPen(pen) 
                painter.drawPoint(i, draw_y)      