from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
import alg
from copy import deepcopy

LMB = 1
RMB = 2


class Canvas(QtWidgets.QLabel):
    parentPtr = None

    cutter = []
    cutter_closed = False

    poly = []
    poly_closed = []

    results = []
    temp_line = []

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
        self.setFocus(True)
        self.update()

    def clamp(self, value, min_, max_):
        return max(min_, min(max_, value))
    
    def restrict(self, value, a, b):
        return self.clamp(value, min(a, b), max(a, b))

    def getMousePosOnEdge(self):
        # if not self.active:
        #     return point
        
        point = deepcopy(self.curMousePos)
        p1 = self.temp_line[0]
        p2 = self.temp_line[1]

        dy = p1.y() - p2.y()
        dx = p1.x() - p2.x()

        if dy == 0:
            point.setY(p1.y())
            point.setX(self.restrict(point.x(), p1.x(), p2.x()))
            return point
        
        if dx == 0:
            point.setX(self.p1.x())
            point.setY(self.restrict(point.y(), p1.y(), p2.y()))
            return point
        
        k = dy / dx
        m = p1.y() - p1.x() * k

        point.setX(self.restrict(point.x(), p1.x(), p2.x()))
        point.setY(round(point.x() * k + m))
        return point

    def getShiftFixedMpos(self):
        mpos = QPointF(self.curMousePos.x(), self.curMousePos.y())
        if len(self.poly) != 0 and not self.poly_closed:
            target_x = self.poly[-1].x()
            target_y = self.poly[-1].y()
        else:
            if len(self.cutter) <= 1:
                return self.curMousePos
            target_x = self.cutter[-1].x()
            target_y = self.cutter[-1].y()

        x_dist = abs(mpos.x() - target_x)
        y_dist = abs(mpos.y() - target_y)
        if x_dist < y_dist:
            mpos.setX(target_x)
        else:
            mpos.setY(target_y)
        return mpos
    

    def getValidMpos(self):
        pos = self.curMousePos
        if self.shiftPressed:
            pos = self.getShiftFixedMpos()
        elif len(self.temp_line) == 2:
            pos = self.getMousePosOnEdge()
        return pos

    def addPointToCutter(self, point):
        if self.cutter_closed:
            self.cutter.clear()
            self.results = []
            self.cutter_closed = False

        self.parentPtr.table.rebuildTable(point)
        self.cutter.append(point)

    def addPointToPoly(self, point):
        if self.poly_closed:
            self.poly.clear()
            self.results = []
            self.poly_closed = False

        self.poly.append(point)

    def mousePressEvent(self, event):

        if event.button() == LMB:
            p = self.getValidMpos()
            self.addPointToPoly(QPoint(int(p.x()), int(p.y())))

        elif event.button() == RMB:
            self.temp_line = []
            self.parentPtr.table.clearSelection()
            p = self.getValidMpos()
            self.addPointToCutter(QPoint(int(p.x()), int(p.y())))

        self.update()

    def drawPolyToCanv(self):
        if len(self.poly) > 0:
            self.setColor(self.parentPtr.getPBColor(self.parentPtr.polyColor))

            for i in range(len(self.poly) - 1):
                self.painter.drawLine(self.poly[i], self.poly[i + 1])

            if self.poly_closed:
                self.painter.drawLine(self.poly[-1], self.poly[0])
            else:
                self.painter.drawLine(self.poly[-1], self.getValidMpos())

    def drawCutterToCanv(self):
        if len(self.cutter) > 0:
            self.setColor(self.parentPtr.getPBColor(self.parentPtr.sepColor))

            for i in range(len(self.cutter) - 1):
                self.painter.drawLine(self.cutter[i], self.cutter[i + 1])

            if self.cutter_closed:
                self.painter.drawLine(self.cutter[-1], self.cutter[0])
            else:
                self.painter.drawLine(self.cutter[-1], self.getValidMpos())

    def doCutting(self):
        if not self.cutter_closed:
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите отсекатель</b></font>')
            return

        if len(self.poly) == 0 or not self.poly_closed:
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите хотя бы один отсекаемый отрезок</b></font>')
            return

        cutter_vertices = []
        for point in self.cutter:
            cutter_vertices.append([point.x(), point.y()])
        
        figure = []
        for point in self.poly:
            figure.append([point.x(), point.y()])

        if not alg.CheckPoly(cutter_vertices):
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Отсекатель должен быть выпуклым многоугольником</b></font>')
            return

        self.results = []
        self.update()

        normals = alg.GetNormals(cutter_vertices)
        res = alg.CutFigure(figure, cutter_vertices, normals)

        if res is not None:
            self.results = list(map(lambda li: [int(li[0]+0.5), int(li[1]+0.5)], res))

        self.update()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.pixmap().fill(QColor(0xFFFFFF))
        self.painter.drawPixmap(self.rect(), self.pixmap())

        self.__drawCoords(self.painter)

        self.drawCutterToCanv()

        if len(self.temp_line) == 2:
            col = self.parentPtr.getPBColor(self.parentPtr.sepColor)
            col = QColor(255 - col.red(), 255 - col.green(), 255 - col.blue())
            self.setColor(col)
            self.painter.drawLine(*self.temp_line)

        self.drawPolyToCanv()

        resColor = self.parentPtr.getPBColor(self.parentPtr.resColor)
        self.setColor(resColor)

        for i in range(len(self.results) - 1):
            self.painter.drawLine(self.results[i][0], self.results[i][1], self.results[i + 1][0], self.results[i + 1][1])
        if len(self.results) > 0:
            self.painter.drawLine(self.results[-1][0], self.results[-1][1], self.results[0][0], self.results[0][1])

        self.painter.end()
