from PyQt5 import QtWidgets, QtGui, QtCore


class ColorPicker(QtWidgets.QOpenGLWidget):
    ColorPicked = QtCore.pyqtSignal(QtGui.QColor, name='ColorPicked')

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.painter = QtGui.QPainter()
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))

        self.cur_col = QtCore.QPointF(0, 0)
        self.setMouseTracking(True)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatePickedColor)

        self.colors = []

    def updatePickedColor(self):
        self.cur_col = self.mapFromGlobal(QtGui.QCursor().pos())
        self.cur_col.setX(min(self.width(), max(0, self.cur_col.x())))
        self.cur_col.setY(min(self.height(), max(0, self.cur_col.y())))
        self.ColorPicked.emit(
            self.colors[(self.cur_col.x() * 7 - 1) // self.width()])
        self.update()

    def get_color_by_n(self, x, w):
        funny_constant = 255 * 6 / w
        r = int_col_clamp(abs(funny_constant * (x - w / 2)) - 255)
        g = int_col_clamp(255 * 2 - abs(funny_constant * (x - w / 3)))
        b = int_col_clamp(255 * 2 - abs(funny_constant * (x - w * 2 / 3)))
        return QtGui.QColor(r, g, b)

    def get_color_by_y(self, y, h):
        return

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.timer.start(10)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.timer.stop()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # self.setFixedHeight(self.width() // 7)
        self.painter.begin(self)
        
        self.painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        self.colors.clear()
        for i in range(5):
            x = i * self.width() // 7
            painter_path = QtGui.QPainterPath()
            painter_path.addRect(x, 1, self.width() // 7, self.height() - 2)
            self.painter.fillPath(painter_path, self.get_color_by_n(i, 5))
            self.colors.append(self.get_color_by_n(i, 5))

        x = 5 * self.width() // 7
        painter_path = QtGui.QPainterPath()
        painter_path.addRect(x, 1, self.width() // 7, self.height() - 2)
        self.painter.fillPath(painter_path, QtGui.QColor(0, 0, 0))
        self.colors.append(QtGui.QColor(0, 0, 0))

        x = 6 * self.width() // 7
        painter_path = QtGui.QPainterPath()
        painter_path.addRect(x, 1, self.width() // 7, self.height() - 2)
        self.painter.fillPath(painter_path, QtGui.QColor(255, 255, 255))
        self.colors.append(QtGui.QColor(255, 255, 255))

        self.pen.setColor(QtGui.QColor(0, 0, 0))
        self.painter.setPen(self.pen)
        self.painter.drawEllipse(self.cur_col, 5, 5)
        self.painter.end()


def int_col_clamp(value):
    return min(255, max(0, int(value)))
