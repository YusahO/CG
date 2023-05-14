from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

import re

class LineColorButton(QtWidgets.QPushButton):
    changeColor = QtCore.pyqtSignal(QColor, name='changeColor')
    def __init__(self, parent):
        super().__init__()

    def __get_color_from_line(self, line: str):
        rgb = [int(s) for s in re.findall(r'\b\d+\b', line)]
        return QColor(*rgb)

    def focusInEvent(self, e):
        style = self.styleSheet()
        color = QColor(0, 0, 0)
        for l in style.splitlines():
            if (l.startswith('background-color')):
                color = self.__get_color_from_line(style)

        self.changeColor.emit(color)
