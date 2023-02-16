from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import lab_utils as lu
import sys

WIDTH = 800
HEIGHT = 600

class Canvas(QtWidgets.QWidget):
    def __init__(self, parent, posLabel, points, update_fn):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.pen = QtGui.QPen(Qt.red, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        
        self.painter = QtGui.QPainter()

        self.update_fn = update_fn
        self.posLabel = posLabel

        self.resulting_pts = []

        self.centerPos = None
        self.points = points

    def paintTriangle(self, a, b, c, color=QtGui.QColor(0, 0, 0)):
        self.paintSegment(a, b, color)
        self.paintSegment(a, c, color)
        self.paintSegment(b, c, color)

    def mousePressEvent(self, event):
        if Qt.LeftButton:
            self.centerPos = event.pos()
            self.points.append(self.centerPos)
            self.update_fn(QtCore.QPoint(self.centerPos.x(), self.height() - self.centerPos.y()))
            self.update()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.posLabel.setText(f"Текущая позиция: ({pos.x()}, {self.height() - pos.y()})")

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(self.pen)

        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)
        for p in self.points:
            self.painter.drawPoint(p)

        if len(self.resulting_pts) != 0:
            self.pen.setWidth(2)
            self.pen.setColor(Qt.black)
            self.painter.setPen(self.pen)
            
            self.painter.drawPolygon(self.resulting_pts[4], self.resulting_pts[5], self.resulting_pts[6])
            self.painter.drawLine(self.resulting_pts[1], self.resulting_pts[5])
            self.painter.drawLine(self.resulting_pts[2], self.resulting_pts[6])
            self.painter.drawLine(self.resulting_pts[3], self.resulting_pts[4])

            self.pen.setWidth(8)
            self.pen.setColor(QtGui.QColor(0, 255, 0))
            self.painter.setPen(self.pen)
            for p in self.resulting_pts[:4]:
                self.painter.drawPoint(p)

        self.pen.setWidth(8)
        self.pen.setColor(Qt.red)
        self.painter.end()
    
    def clearCanvas(self, clear_points=True):
        self.pixmap().fill(Qt.white)

        if clear_points:
            self.points = []

        self.update()


class MessageBox(QtWidgets.QMessageBox):
    def __init__(self):
        super().__init__()

    def setInfo(self, title, text, icon=QtWidgets.QMessageBox.Information):
        self.setWindowTitle(title)
        self.setIcon(icon)
        self.setText(text)


class Table(QtWidgets.QTableWidget):
    def __init__(self, rows=0, cols=1):
        super().__init__(rows, cols)
        self.setMaximumWidth(100)
    
    def addEntry(self, data):
        to_insert = QtWidgets.QTableWidgetItem(f'({data.x()}, {data.y()})')
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, self.columnCount() - 1, to_insert)

    def removeEntry(self, ind):
        if ind < 0:
            ind = self.rowCount() + ind
        self.removeRow(ind)
    
    def cellChanged(self, row: int, column: int) -> None:
        return self.item(row, column)

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.points = []

        self.tableWidget = Table()
        self.gridLayout.addWidget(self.tableWidget, 0, 1, -1, -1)

        self.canvas = Canvas(self, self.posLabel, self.points, self.tableWidget.addEntry)

        self.dialog = MessageBox()

        # ---------------- Добавление холста ----------------
        self.verticalLayout.insertWidget(1, self.canvas)

        # ---------------- Привязка событий к кнопкам ----------------
        self.findTriangleButton.clicked.connect(self.getResultingTriangle)
        # self.clearCanvasAction.triggered.connect(self.canvas.clearCanvas)
        # self.clearPointsAction.triggered.connect(
        #     lambda x: self.clearLineEdits(False)
        # )
        self.undoAction.triggered.connect(self.undo)
        self.undoAction.setShortcut('Ctrl+Z')
        # self.clearPointsAction.setShortcut('Ctrl+P')

        self.tableWidget.itemChanged.connect(self.updateTable)

        self.show()

    def clearLineEdits(self):
        self.pxLE.setText('')
        self.pyLE.setText('')

    def getResultingTriangle(self):
        self.madeSearch = True
        min_pts = []
        min_areas = []
        min_area_diff = 0
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                for k in range(j + 1, len(self.points)):
                    pts = lu.get_all_points_in_triangle(self.points[i], self.points[j], self.points[k])
                    areas = lu.calc_areas_and_diff(pts)

                    if i == 0 and j == i + 1 and k == j + 1:
                        min_area_diff = areas[-1]
                        min_pts = pts
                        min_areas = areas

                    elif min_area_diff > areas[-1]:
                        min_area_diff = areas[-1]
                        min_pts = pts
                        min_areas = areas

        self.canvas.resulting_pts = min_pts
        self.canvas.update()

    def undo(self):
        if len(self.points) > 0:
            self.points.pop()
            self.tableWidget.removeEntry(-1)

        self.canvas.resulting_pts = []
        self.canvas.update()

    def toggleLineEditStyle(self, lineEdit, error=True):
        if error:
            lineEdit.setStyleSheet(
                '''
                QLineEdit {
                    background-color: #ff847a;
                    color: white
                }
                '''
            )
        else:
            lineEdit.setStyleSheet(
                '''
                QLineEdit {
                    background-color: white;
                    color: black
                }
                '''
            )
    
    def updateTable(self, data):
        item = None
        try:
            item = list(map(int, data.text().split(' ')))
        except Exception:
            return
        else:
            item = QtCore.QPoint(item[0], self.canvas.height() - item[1])
            self.points[data.row()] = item
            self.canvas.update()

    def tryGetLineEditData(self, lineEdit, vmin=None, vmax=None):
        try:
            v = int(lineEdit.text())
            if None not in (vmin, vmax):
                if not vmin < v < vmax:
                    raise Exception
            self.toggleLineEditStyle(lineEdit, error=False)
        except:
            v = None
            self.toggleLineEditStyle(lineEdit)
        return v

    def getPointData(self):
        x = self.tryGetLineEditData(self.pxLE, 0, WIDTH)
        y = self.tryGetLineEditData(self.pyLE, 0, HEIGHT)
        return x, y


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
