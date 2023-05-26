from PyQt5 import QtWidgets, QtGui, QtCore


class ColorViewer(QtWidgets.QWidget):
    onNewColor = QtCore.pyqtSignal(QtGui.QColor, name='onNewColor')
    def __init__(self, parent):
        super().__init__(parent)

        self.painter = QtGui.QPainter()
        self.active_color = QtGui.QColor(0, 0, 0)
    
    def setNewColor(self, col):
        self.active_color = col
        self.onNewColor.emit(col)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.setFixedWidth(self.height())

        self.painter.begin(self)

        self.painter.drawRect(0, 0, self.size().width() - 1, self.size().height() - 1)
        self.painter_path = QtGui.QPainterPath()
        self.painter_path.addRect(1, 1, self.size().width() - 2, self.size().height() - 2)
        self.painter.fillPath(self.painter_path, self.active_color)

        self.painter.end()

    def getRawColor(self):
        r, g, b = self.active_color.red(), self.active_color.green(), self.active_color.blue()
        return (r, g, b)