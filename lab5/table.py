from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import QPoint

class Table(QTableWidget):

    def __init__(self, parent):
        super().__init__(parent)

        header = self.horizontalHeader()       
        header.setSectionResizeMode(QHeaderView.Stretch)

    def addToTable(self, point: QPoint):
        self.insertRow(self.rowCount())

        if (point.x() != -1 and point.y() != -1):
            self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(f'{point.x()}'))
            self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(f'{point.y()}'))
        else:
            self.setItem(self.rowCount() - 1, 0, QTableWidgetItem('---'))
            self.setItem(self.rowCount() - 1, 1, QTableWidgetItem('---'))
