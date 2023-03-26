from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText

class Canvas(QtWidgets.QWidget):
    dda_lines = []
    bfloat_lines = []
    bint_lines = []
    baa_lines = []
    vu_lines = []
    lib_lines = []

    bgColor = QColor(255, 255, 255)
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.update()
        
    def changeBgColor(self, new):
        self.bgColor = new
        self.update()

    def __draw_coords(self, painter: QPainter):
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

    def __draw_dda(self, painter: QPainter):
        pen = QPen()
        for l in self.dda_lines:
            for p in l:
                pen.setColor(p[2])
                painter.setPen(pen)
                painter.drawPoint(QPointF(p[0], p[1]))

    def __draw_bresenham_float(self, painter: QPainter):
        pen = QPen()
        for l in self.bfloat_lines:
            for p in l:
                pen.setColor(p[2])
                painter.setPen(pen)
                painter.drawPoint(QPointF(p[0], p[1]))

    def __draw_bresenham_int(self, painter: QPainter):
        pen = QPen()
        for l in self.bint_lines:
            for p in l:
                pen.setColor(p[2])
                painter.setPen(pen)
                painter.drawPoint(QPointF(p[0], p[1]))

    def __draw_bresenham_AA(self, painter: QPainter):
        pen = QPen()
        for l in self.baa_lines:
            for p in l:
                pen.setColor(QColor(*p[2]))
                painter.setPen(pen)
                painter.drawPoint(QPointF(p[0], p[1]))

    def __draw_vu(self, painter):
        pen = QPen()
        for l in self.vu_lines:
            for p in l:
                pen.setColor(QColor(*p[2]))
                painter.setPen(pen)
                painter.drawPoint(QPointF(p[0], p[1]))

    def __draw_lib(self, painter: QPainter):
        pen = QPen()
        for l in self.lib_lines:
            pen.setColor(l[-1])
            painter.setPen(pen)
            painter.drawLine(QPointF(*l[0]), QPointF(*l[1]))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.fillRect(0, 0, self.width(), self.height(), self.bgColor)
        self.__draw_coords(painter)
        self.__draw_dda(painter)
        self.__draw_bresenham_float(painter)
        self.__draw_bresenham_int(painter)
        self.__draw_bresenham_AA(painter)
        self.__draw_lib(painter)
        painter.end()
