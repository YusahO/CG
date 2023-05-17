from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint, QPointF, QLineF
from Canvas import CanvasPolygon

class CoordTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def rebuildTable(self, li: list[CanvasPolygon]):
        self.setRowCount(0)
        for polygon in li:
            for point in polygon.points:
                item_x = QtWidgets.QTableWidgetItem(f'{point.x()}')
                item_y = QtWidgets.QTableWidgetItem(f'{point.y()}')
                self.insertRow(self.rowCount())
                self.setItem(self.rowCount() - 1, 0, item_x)
                self.setItem(self.rowCount() - 1, 1, item_y)
            
            if polygon.isReady():
                item_x = QtWidgets.QTableWidgetItem(f'---------')
                item_y = QtWidgets.QTableWidgetItem(f'---------')
                # self.insertRow(self.rowCount())
                self.setItem(self.rowCount() - 1, 0, item_x)
                self.setItem(self.rowCount() - 1, 1, item_y)