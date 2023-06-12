from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QStaticText, QPixmap
from PyQt5.QtWidgets import QTableWidgetItem


class Table(QtWidgets.QTableWidget):
    data = []
    closed = False

    def __init__(self, parent):
        super().__init__(parent)
    
    def rebuildTable(self, new_entry = None):
        self.clearContents()
        self.setRowCount(0)

        if self.closed and new_entry is not None:
            self.closed = False
            self.data = []
        
        if new_entry is not None:
            self.data.append(new_entry)

        for i in range(len(self.data) - 1):
            p1 = self.data[i]
            p2 = self.data[i + 1]
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(f'({p1.x()}, {p1.y()}) -- ({p2.x()}, {p2.y()})'))
        
        p1 = self.data[-1]
        p2 = self.data[0]
        if self.closed:
            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(f'({p1.x()}, {p1.y()}) -- ({p2.x()}, {p2.y()})'))