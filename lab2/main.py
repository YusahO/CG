from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import lab_utils as lu
import sys


class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.pivotPos = None
        self.objectCenter = QtCore.QPoint(self.width()//2, self.height()//2)

        self.pen = QtGui.QPen(
            Qt.red, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.painter = QtGui.QPainter()

        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.objectCenter = QtCore.QPoint(self.width()//2, self.height()//2)
        self.update()

    def paintTriangle(self, pts, closed=True):
        self.painter.drawLine(pts[0], pts[1])
        self.painter.drawLine(pts[1], pts[2])
        if closed:
            self.painter.drawLine(pts[0], pts[2])

    def paintEllipse(self, c, a, b, n):
        pts = lu.calculate_ellipse(c, a, b, n)
        for i in range(len(pts) - 1):
            self.painter.drawLine(pts[i], pts[i + 1])
        else:
            self.painter.drawLine(pts[-1], pts[0])

    def paintCircle(self, c, r, n):
        pts = lu.calculate_ellipse(c, r, r, n)
        for i in range(len(pts) - 1):
            self.painter.drawLine(pts[i], pts[i + 1])
        else:
            self.painter.drawLine(pts[-1], pts[0])

    def paintArc(self, c, a, b, start, end, n):
        pts = lu.calculate_arc(c, a, b, start, end, n)
        for i in range(len(pts) - 1):
            self.painter.drawLine(pts[i], pts[i + 1])

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(self.pen)

        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        n = 25
        self.paintEllipse(self.objectCenter, 100, 200, n)
        self.paintCircle(self.objectCenter - QtCore.QPoint(0, 145), 45, n)
        self.paintArc(self.objectCenter - QtCore.QPoint(0, 130), 40, 20, 3.14/6, 5*3.14/6, n)

        self.paintCircle(self.objectCenter - QtCore.QPoint(15, 154), 10, n)
        self.paintCircle(self.objectCenter - QtCore.QPoint(-15, 154), 10, n)

        whiskers = [self.objectCenter - QtCore.QPoint(0, 154), 
                    self.objectCenter - QtCore.QPoint(10, 200),
                    self.objectCenter - QtCore.QPoint(50, 200)]
        self.paintTriangle(whiskers, False)
        print('before ', whiskers)

        whiskers = lu.scale_object(self.objectCenter, whiskers, (-1, 1))
        print('after ', whiskers)
        self.paintTriangle(whiskers, False)

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


# class Table(QtWidgets.QTableWidget):
#     def __init__(self, rows=0, cols=1):
#         super().__init__(rows, cols)

#     def addEntry(self, ind, data):
#         to_insert = QtWidgets.QTableWidgetItem(
#             f'({data.x()}, {HEIGHT - data.y()})')
#         self.insertRow(self.rowCount())
#         self.setItem(self.rowCount() - 1, self.columnCount() - 1, to_insert)

#     def removeEntry(self, ind):
#         if ind < 0:
#             ind = self.rowCount() + ind
#         self.removeRow(ind)


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.canvas = Canvas()

        self.dialog = MessageBox()

        # ---------------- Добавление холста ----------------
        self.mainLayout.addWidget(self.canvas)
        # ---------------- Привязка событий к кнопкам ----------------
        self.clearCanvasAction.triggered.connect(self.canvas.clearCanvas)
        self.clearPointsAction.triggered.connect(
            lambda x: self.clearLineEdits(False)
        )
        self.undoAction.triggered.connect(self.undo)
        self.clearPointsAction.setShortcut('Ctrl+P')
        self.undoAction.setShortcut('Ctrl+Z')

        self.drawObject()

        self.show()

    def clearLineEdits(self):
        self.pxLE.setText('')
        self.pyLE.setText('')

    def drawObject(self):
        self.canvas.update()

    def undo(self):
        self.canvas.clearCanvas(clear_points=False)
        if len(self.points) > 0 and not self.madeSearch:
            self.points.pop()
            self.tableWidget.removeEntry(-1)

        for p in self.points:
            self.canvas.paintPoint(p)

        self.madeSearch = False

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

    def updateTable(self):
        self.tableWidget.addEntry(len(self.points), self.points[-1])

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

    # def getPointData(self):
    #     x = self.tryGetLineEditData(self.pxLE, 0, WIDTH)
    #     y = self.tryGetLineEditData(self.pyLE, 0, HEIGHT)
    #     return x, y

    # def drawPrimitive(self):
    #     x, y = self.getPointData()
    #     if None in (x, y):
    #         return
    #     self.canvas.paintPoint(QtCore.QPoint(x, HEIGHT - y))


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
