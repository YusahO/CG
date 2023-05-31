from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QThread, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
from time import time_ns, sleep

LMB = 1
RMB = 2

class Stack:
    data = []

    def push(self, val):
        self.data.append(val)

    def pop(self):
        return self.data.pop()

    def empty(self):
        return len(self.data) == 0


class Polygon:
    def __init__(self, color=QColor(0, 0, 0)) -> None:
        self.points = []
        self.color = color
        self.ready = False
        self.filling = False

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

    parentPtr = None

    pix_input = False
    pix_pos = QPoint(0, 0)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)

        self.painter = QPainter()
        self.pen = QPen(QColor(0, 0, 0))

        self.curMousePos = QPoint(0, 0)
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

    def addPointToCanvas(self, pos, from_mouse=True):
        if len(self.canvasPolygons) == 0 or self.canvasPolygons[-1].isReady():
            self.canvasPolygons.append(
                Polygon(QColor(0x000000)))

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

        if event.buttons() == Qt.LeftButton and self.pix_input == False:
            self.addPointToCanvas(event.pos())
            self.drawLinesToPixmap()

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
            if self.pix_input == False:
                self.addPointToCanvas(event.pos())
            else:
                self.pix_pos = self.getValidMpos()
                self.pix_pos = QPoint(int(self.pix_pos.x()), int(self.pix_pos.y()))
                self.pix_input = False
                self.parentPtr.ptXLE.setText(f'{self.pix_pos.x()}')
                self.parentPtr.ptYLE.setText(f'{self.pix_pos.y()}')

        elif event.button() == RMB:
            self.closeCanvasPolygon()

        self.drawLinesToPixmap()
        self.update()

    def drawLinesToCanv(self):
        for polygon in self.canvasPolygons:
            polygon.draw(self.painter)

        if len(self.canvasPolygons) != 0 and not self.canvasPolygons[-1].isReady():
            mpos_to_draw = self.getValidMpos()

            self.painter.drawLine(
                self.canvasPolygons[-1].points[-1], mpos_to_draw)
    
    def drawLinesToPixmap(self):
        painter = QPainter(self.pixmap())

        for polygon in self.canvasPolygons:
            polygon.draw(painter)
        
        painter.end()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap())

        self.painter.fillRect(0, 0, self.width(), self.height(), 0xFFFFFF)

        self.__drawCoords(self.painter)

        self.drawLinesToCanv()

        self.painter.setPen(self.pen)
        self.painter.end()

    def fillNoDelay(self):
        start = time_ns()

        self.fillColor = self.parentPtr.colorview_2.color
        points = []
        for pol in self.canvasPolygons:
            for p in pol.points:
                points.append([int(p.x()), int(p.y())])
        rectPts = GetRect(points)
        self.rects = rectPts

        painter = QtGui.QPainter(self.pixmap())

        FillAlgNoDelay(painter, self.pixmap(), [self.pix_pos.x(), self.pix_pos.y()], self.fillColor)

        painter.end()
        end = time_ns()
        self.parentPtr.timeLabel.setText(
            f'Время построения {(end - start) / 1e6 : .3f} мс')
        self.update()

        self.pix_input = False

    def fillDelay(self, delay):
        self.fillColor = self.parentPtr.colorview_2.color
        points = []
        for pol in self.canvasPolygons:
            for p in pol.points:
                points.append([int(p.x()), int(p.y())])
        rectPts = GetRect(points)
        self.rects = rectPts

        painter = QtGui.QPainter(self.pixmap())
        
        FillAlgDelay(painter, self, [self.pix_pos.x(), self.pix_pos.y()], delay, self.fillColor)

        painter.end()
        self.update()

        self.pix_input = False

def FillAlgDelay(painter, canv, begin_pix, delay, col=QColor(0xFF0000), border=QColor(0x000000)):
    img = canv.pixmap().toImage()
    pen = QtGui.QPen()
    pen.setColor(col)
    painter.setPen(pen)
    seed = QPoint(*begin_pix)

    border_color = border.rgb()
    seed_color = col.rgb()

    stack = Stack()

    stack.push(seed)
    while not stack.empty():
        pixel = stack.pop()
        x = pixel.x()
        y = pixel.y()
        
        temp_x = x
        painter.drawPoint(x, y)

        x += 1
        while img.pixel(x, y) != border_color:
            if x > img.width():
                return
            painter.drawPoint(x, y)
            x += 1

        x_right = x - 1

        x = temp_x
        x -= 1
        while img.pixel(x, y) != border_color:
            if x < 0:
                return
            painter.drawPoint(x, y)
            x -= 1
            
        x_left = x + 1
        
        FillSearch(x_left, y + 1, x_right, seed_color, border_color, stack, canv.pixmap().toImage())
        FillSearch(x_left, y - 1, x_right, seed_color, border_color, stack, canv.pixmap().toImage())

        sleep(delay)
        canv.update()
        

def FillAlgNoDelay(painter, pixmap, begin_pix, col=QColor(0xFF0000), border=QColor(0x000000)):
    img = pixmap.toImage()
    pen = QtGui.QPen()
    pen.setColor(col)
    painter.setPen(pen)

    pix_seed = QPoint(*begin_pix)

    border_color = border.rgb()
    seed_color = col.rgb()

    stack = Stack()

    stack.push(pix_seed)
    while not stack.empty():
        pixel = stack.pop()
        x = pixel.x()
        y = pixel.y()
        
        temp_x = x
        painter.drawPoint(x, y)

        x += 1
        while img.pixel(x, y) != border_color:
            if x > pixmap.width():
                return
            painter.drawPoint(x, y)
            x += 1
            
        x_right = x - 1

        x = temp_x
        x -= 1
        
        while img.pixel(x, y) != border_color:
            if x < 0:
                return
            painter.drawPoint(x, y)
            x -= 1

        x_left = x + 1

        FillSearch(x_left, y + 1, x_right, seed_color, border_color, stack, pixmap.toImage())
        FillSearch(x_left, y - 1, x_right, seed_color, border_color, stack, pixmap.toImage())

def FillSearch(x, y, x_right, seed_color, border_color, stack, pixels):
    while x <= x_right:
        flag = False
        cur_pix_color = pixels.pixel(x, y)

        while cur_pix_color != seed_color and cur_pix_color != border_color and x <= x_right:
            if not flag:
                flag = True
            x += 1
            cur_pix_color = pixels.pixel(x, y)

        # Помещаем в стек крайний правый пиксель -- затравка
        if flag:
            # добавляем в стек контура закрашиваемой области точку с координатами (x - 1, y),
            # так как текущая точка (x, y) оказалась за границей области
            if x == x_right and cur_pix_color != border_color and cur_pix_color != seed_color:
                stack.push(QPoint(x, y))
            else:
                stack.push(QPoint(x - 1, y))
        # Продолжаем проверку, если интервал был прерван
        x_last = x
        # Поиск подходящего пикселя
        while (cur_pix_color == border_color or cur_pix_color == seed_color) and x < x_right:
            x += 1
            cur_pix_color = pixels.pixel(x, y)

        if x == x_last:
            x = x + 1


def ColorToArray(color):
    return [color.r(), color.g(), color.b()]


def GetRect(pts):
    left, right, top, bottom = float("inf"), float(
        "-inf"), float("inf"), float("-inf")

    for p in pts:
        left = min(left, p[0])
        right = max(right, p[0])
        top = min(top, p[1])
        bottom = max(bottom, p[1])

    return [left, top, right, bottom]
