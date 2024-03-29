from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
import alg

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

    def addLine(self, x0, y0, x1, y1):
        p1 = QPoint(x0, y0)
        p2 = QPoint(x1, y1)

        self.lines.extend(
            [self.parentPtr.getPBColor(self.parentPtr.lineColor), p1, p2]
        )

        self.update()
    
    def addCutter(self, x0, y0, x1, y1):
        tl = QPoint(x0, y0)
        br = QPoint(x1, y1)

        self.cutter = [
            self.parentPtr.getPBColor(self.parentPtr.sepColor),
            tl, br
        ]

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
        if len(self.lines) == 0 or len(self.lines) % 3 == 1:
            return mpos

        x_dist = abs(mpos.x() - self.lines[-1].x())
        y_dist = abs(mpos.y() - self.lines[-1].y())
        if x_dist < y_dist:
            mpos.setX(self.lines[-1].x())
        else:
            mpos.setY(self.lines[-1].y())
        return mpos

    def getValidMpos(self):
        if self.shiftPressed:
            return self.getShiftFixedMpos()
        return self.curMousePos

    def mousePressEvent(self, event):
        if len(self.lines) // 3 >= 10:
            self.parentPtr.msgbox.warning(self.parentPtr, 'Предупреждение!', '<font size=14><b>Число отсекаемых отрезков не может быть более 10</b></font>')
            return

        if event.button() == LMB and len(self.lines) // 3 < 10:
            if len(self.lines) % 3 == 0:
                self.lines.append(self.parentPtr.getPBColor(self.parentPtr.lineColor))
            p = self.getValidMpos()
            self.lines.append(QPoint(int(p.x()), int(p.y())))

            if len(self.lines) % 3 == 0:
                p = (self.lines[-2], self.lines[-1])
                self.parentPtr.lineXSLE.setText(f'{p[0].x()}')
                self.parentPtr.lineYSLE.setText(f'{p[0].y()}')
                self.parentPtr.lineXELE.setText(f'{p[1].x()}')
                self.parentPtr.lineYELE.setText(f'{p[1].y()}')

        elif event.button() == RMB:
            if len(self.cutter) + 1 > 3:
                self.cutter.clear()
                self.results = []
            if len(self.cutter) == 0:
                self.cutter.append(self.parentPtr.getPBColor(self.parentPtr.sepColor))
            self.cutter.append(event.pos())

            if len(self.cutter) == 3:
                p1, p2 = self.cutter[1:]
                x1, x2, y1, y2 = p1.x(), p2.x(), p1.y(), p2.y()
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])
                self.cutter[1] = QPoint(x1, y1)
                self.cutter[2] = QPoint(x2, y2)
                self.parentPtr.sepTLXLE.setText(f'{self.cutter[-2].x()}')
                self.parentPtr.sepTLYLE.setText(f'{self.cutter[-2].y()}')
                self.parentPtr.sepRBXLE.setText(f'{self.cutter[-1].x()}')
                self.parentPtr.sepRBYLE.setText(f'{self.cutter[-1].y()}')

        self.update()

    def drawLinesToCanv(self):
        for i in range(0, len(self.lines) - 2, 3):
            self.pen.setColor(self.lines[i])
            self.painter.setPen(self.pen)
            self.painter.drawLine(self.lines[i + 1], self.lines[i + 2])

        if len(self.lines) % 3 == 2:
            self.pen.setColor(self.lines[-2])
            self.painter.setPen(self.pen)
            self.painter.drawLine(self.lines[-1], self.getValidMpos())

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

    def doCutting(self):
        if len(self.cutter) < 3:
            self.parentPtr.msgbox.critical(self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите отсекатель</b></font>')
            return

        if len(self.lines) == 0 or len(self.lines) % 3 != 0:
            self.parentPtr.msgbox.critical(self.parentPtr, 'Ошибка!', '<font size=14><b>Пожалуйста, введите хотя бы один отсекаемый отрезок</b></font>')
            return
        
        self.results = []
        self.update()

        for i in range(0, len(self.lines) - 2, 3):
            l = \
            [
                [self.lines[i + 1].x(), self.lines[i + 1].y()], 
                [self.lines[i + 2].x(), self.lines[i + 2].y()]
            ]

            res = alg.CutSection(QRectF(*self.cutter[1:]), l)
            print(res)
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

        self.painter.setPen(self.pen)
        self.painter.end()
