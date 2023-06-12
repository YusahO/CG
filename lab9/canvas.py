from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
import alg
import math

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

    def getShiftFixedMpos(self):
        mpos = QPointF(self.curMousePos.x(), self.curMousePos.y())
        if len(self.lines) != 0 and len(self.lines) % 3 == 2:
            target_x = self.lines[-1].x()
            target_y = self.lines[-1].y()
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
    
    def getParallelMpos(self):
        if len(self.lines) % 3 == 1:
            return self.curMousePos

        if self.temp_line[1].x() == self.temp_line[0].x():
            return QPoint(self.lines[-1].x(), self.curMousePos.y())
        elif self.temp_line[1].y() == self.temp_line[0].y():
            return QPoint(self.curMousePos.x(), self.lines[-1].y())
        
        m = (self.temp_line[1].y() - self.temp_line[0].y()) / (self.temp_line[1].x() - self.temp_line[0].x())
        b = self.lines[-1].y() - m * self.lines[-1].x()

        mpos = QPoint(self.curMousePos.x(), int(self.curMousePos.x() * m + b))
        return mpos

    def getValidMpos(self):
        pos = self.curMousePos
        if self.shiftPressed:
            pos = self.getShiftFixedMpos()
        elif len(self.temp_line) == 2:
            pos = self.getParallelMpos()
        return pos

    def addPointToCutter(self, point):
        if self.cutter_closed:
            self.cutter.clear()
            self.results = []
            self.cutter_closed = False

        if len(self.cutter) == 0:
            self.cutter.append(
                self.parentPtr.getPBColor(self.parentPtr.sepColor))

        self.parentPtr.table.rebuildTable(point)
        self.cutter.append(point)

    def addPointToPoly(self, point):
        if self.poly_closed:
            self.poly.clear()
            self.results = []
            self.poly_closed = False

        if len(self.poly) == 0:
            self.poly.append(
                self.parentPtr.getPBColor(self.parentPtr.polyColor))

        self.poly.append(point)

    def mousePressEvent(self, event):
        self.temp_line = []
        self.parentPtr.table.clearSelection()

        if event.button() == LMB:
            p = self.getValidMpos()
            self.addPointToPoly(QPoint(int(p.x()), int(p.y())))

        elif event.button() == RMB:
            p = self.getValidMpos()
            self.addPointToCutter(QPoint(int(p.x()), int(p.y())))

        self.update()

    def drawPolyToCanv(self):
        if len(self.poly) > 0:
            self.setColor(self.poly[0])

            for i in range(1, len(self.poly) - 1):
                self.painter.drawLine(self.poly[i], self.poly[i + 1])

            if self.poly_closed:
                self.painter.drawLine(self.poly[-1], self.poly[1])
            else:
                self.painter.drawLine(self.poly[-1], self.getValidMpos())

    def drawCutterToCanv(self):
        if len(self.cutter) > 0:
            self.setColor(self.cutter[0])

            for i in range(1, len(self.cutter) - 1):
                self.painter.drawLine(self.cutter[i], self.cutter[i + 1])

            if self.cutter_closed:
                self.painter.drawLine(self.cutter[-1], self.cutter[1])
            else:
                self.painter.drawLine(self.cutter[-1], self.getValidMpos())

    def doCutting(self):
        if not self.cutter_closed:
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите отсекатель</b></font>')
            return

        if len(self.lines) == 0 or len(self.lines) % 3 != 0:
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите хотя бы один отсекаемый отрезок</b></font>')
            return

        # print('cutter: ', self.cutter)
        vertices = []
        for point in self.cutter[1:]:
            vertices.append([point.x(), point.y()])
        # print('verts: ', vertices)
        # print()
        sections = []
        for i in range(0, len(self.lines) - 2, 3):
            section = self.lines[i: i + 3]
            sections.append([
                [section[1].x(), section[1].y()],
                [section[2].x(), section[2].y()]
            ])

        if not alg.CheckPoly(vertices):
            self.parentPtr.msgbox.critical(
                self.parentPtr, 'Ошибка!', '<font size=14><b>Отсекатель должен быть выпуклым многоугольником</b></font>')
            return

        self.results = []
        self.update()

        normals = alg.GetNormals(vertices)
        for section in sections:
            res = alg.CutSection(section, vertices, normals)
            if res is not None:
                self.results.append(res)

        self.update()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap())

        self.painter.fillRect(0, 0, self.width(), self.height(), 0xFFFFFF)

        self.__drawCoords(self.painter)

        self.drawCutterToCanv()
        self.drawLinesToCanv()

        resColor = self.parentPtr.getPBColor(self.parentPtr.resColor)
        self.pen.setColor(resColor)
        self.painter.setPen(self.pen)

        for line in self.results:
            self.painter.drawLine(*line)

        if len(self.temp_line) == 2:
            col = self.cutter[0]
            col = QColor(255 - col.red(), 255 - col.green(), 255 - col.blue())
            self.pen.setColor(col)
            self.painter.setPen(self.pen)
            self.painter.drawLine(*self.temp_line)

        self.painter.setPen(self.pen)
        self.painter.end()
