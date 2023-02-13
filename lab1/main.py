from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import lab_utils as lu
import sys

WIDTH = 800
HEIGHT = 600


class Canvas(QtWidgets.QLabel):
    def __init__(self, width, height, posLabel, points):
        super().__init__()
        self.setMouseTracking(True)

        self.posLabel = posLabel

        self.centerPos = None
        self.points = points

        self.pointPen = QtGui.QPen(
            Qt.red, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        canvas = QtGui.QPixmap(width, height)
        canvas.fill(Qt.white)
        self.setPixmap(canvas)

    def toggleDrawPrimitive(self, value):
        self.drawPoint = value

    def paintPoint(self, loc, color=QtGui.QColor(255, 0, 0), new=True):
        if color.getRgb() != self.pointPen.color().getRgb():
            self.pointPen.setColor(color)
        self.pointPen.setWidth(8)
        painter = QtGui.QPainter(self.pixmap())
        painter.setPen(self.pointPen)
        painter.drawPoint(loc)
        painter.end()

        if new:
            self.points.append(loc)
        self.update()

    def paintSegment(self, a, b, color=QtGui.QColor(0, 0, 0)):
        if color.getRgb() != self.pointPen.color().getRgb():
            self.pointPen.setColor(color)
        self.pointPen.setWidth(2)

        painter = QtGui.QPainter(self.pixmap())
        painter.setPen(self.pointPen)
        painter.drawLine(a, b)
        painter.end()

    def paintTriangle(self, a, b, c, color=QtGui.QColor(0, 0, 0)):
        self.paintSegment(a, b, color)
        self.paintSegment(a, c, color)
        self.paintSegment(b, c, color)

    def mousePressEvent(self, event):
        if Qt.LeftButton:
            self.centerPos = event.pos()
            self.updateImage()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.posLabel.setText(f"Текущая позиция: ({pos.x()}, {HEIGHT - pos.y()})")

    def updateImage(self):
        self.paintPoint(self.centerPos)

    def drawResultingTriangle(self, points):
        self.paintTriangle(points[4], points[5], points[6])

        # биссектрисы
        self.paintSegment(points[1], points[5])
        self.paintSegment(points[2], points[6])
        self.paintSegment(points[3], points[4])

        for p in points[:4]:
            self.paintPoint(p, color=QtGui.QColor(0, 255, 0))

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


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.posLabel = QtWidgets.QLabel("Текущая позиция: ")
        self.points = []

        self.madeSearch = False

        self.canvas = Canvas(WIDTH, HEIGHT, self.posLabel, self.points)

        self.dialog = MessageBox()

        # ---------------- Добавление холста ----------------
        self.gridLayout.addWidget(self.canvas)
        self.gridLayout.addWidget(self.posLabel, 5, 0, 1, 1)

        self.drawTriangleButton = QtWidgets.QPushButton("Нарисовать треугольник")
        self.gridLayout.addWidget(self.drawTriangleButton, 6, 0, 1, 1)

        # ---------------- Привязка событий к кнопкам ----------------
        self.drawTriangleButton.clicked.connect(self.getResultingTriangle)
        self.drawButton.clicked.connect(self.drawPrimitive)
        self.clearCanvasAction.triggered.connect(self.canvas.clearCanvas)
        self.clearPointsAction.triggered.connect(
            lambda x: self.clearLineEdits(False)
        )
        self.undoAction.triggered.connect(self.undo)
        self.clearPointsAction.setShortcut('Ctrl+P')
        self.undoAction.setShortcut('Ctrl+Z')

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

        self.canvas.drawResultingTriangle(min_pts)

    def undo(self):
        self.canvas.clearCanvas(clear_points=False)
        if len(self.points) > 0 and self.madeSearch:
            self.points.pop()
        for p in self.points:
            self.canvas.paintPoint(p, new=False)      
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

    def drawPrimitive(self):
        x, y = self.getPointData()
        if None in (x, y):  
            return
        self.canvas.paintPoint(QtCore.QPoint(x, HEIGHT - y))


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
