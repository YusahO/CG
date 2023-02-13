from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import lab_utils as lu
import sys

WIDTH = 800
HEIGHT = 600
MAX_RADIUS = 500


class Canvas(QtWidgets.QLabel):
    def __init__(self, width, height):
        super().__init__()
        self.setMouseTracking(True)

        self.centerPos = None
        self.endPos = None

        self.adjusting = False
        self.drawPoint = False

        self.circles = []
        self.points = []

        self.circlePen = QtGui.QPen(Qt.black, 3)
        self.pointPen = QtGui.QPen(
            Qt.red, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        canvas = QtGui.QPixmap(width, height)
        canvas.fill(Qt.white)
        self.setPixmap(canvas)

    def toggleDrawPrimitive(self, value):
        self.drawPoint = value

    def paintCircle(self, center, radius):
        painter = QtGui.QPainter(self.pixmap())
        painter.setPen(self.circlePen)
        rect = QtCore.QRect(center.x() - radius,
                            center.y() - radius, radius * 2, radius*2)
        painter.drawEllipse(rect)
        painter.end()
        self.circles.append((center, radius))
        self.update()

    def paintPoint(self, loc):
        painter = QtGui.QPainter(self.pixmap())
        painter.setPen(self.pointPen)
        painter.drawPoint(loc)
        painter.end()
        self.points.append(loc)
        self.update()

    def mousePressEvent(self, event):
        if Qt.LeftButton:
            if self.drawPoint:
                self.centerPos = event.pos()
                self.updateImage()
            else:
                if not self.adjusting:
                    self.centerPos = event.pos()
                    self.adjusting = True
                else:
                    self.adjusting = False
                    self.updateImage()

    def mouseMoveEvent(self, event):
        if (event.type() == QtCore.QEvent.MouseMove and event.buttons() == Qt.NoButton):
            if self.adjusting:
                self.endPos = event.pos()
                self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        dirtyRect = event.rect()
        painter.drawPixmap(dirtyRect, self.pixmap(), dirtyRect)
        if self.centerPos and self.endPos:
            radius = int(((self.centerPos.x() - self.endPos.x()) ** 2 +
                          (self.centerPos.y() - self.endPos.y()) ** 2) ** .5)

            rect = QtCore.QRect(self.centerPos.x() - radius,
                                self.centerPos.y() - radius, radius * 2, radius*2)
            painter.drawEllipse(rect)

    def updateImage(self):
        if self.drawPoint:
            self.paintPoint(self.centerPos)
        else:
            if self.centerPos and self.endPos:
                radius = int(((self.centerPos.x() - self.endPos.x()) ** 2 +
                              (self.centerPos.y() - self.endPos.y()) ** 2) ** .5)
                self.paintCircle(self.centerPos, radius)

        self.centerPos = self.endPos = None

    def drawResultingLine(self):
        resultingLine, rc = lu.findMaxIntersecting(
            self.circles, self.points)
        if rc == 'Не удалось найти линию, пересекающую хотя бы одну окружность':
            return rc

        line = lu.getInfLine(resultingLine)
        painter = QtGui.QPainter(self.pixmap())

        # ---------------- Рисование линии ----------------
        painter.setPen(QtGui.QPen(Qt.black, 3))
        painter.drawLine(line[0], line[1])

        # ---------------- Выделение полученных точек ----------------
        color = QtGui.QColor('#17cf48')
        painter.setPen(QtGui.QPen(color, 10, Qt.SolidLine,
                       Qt.RoundCap, Qt.RoundJoin))
        painter.drawPoint(resultingLine[0])
        painter.drawPoint(resultingLine[1])

        painter.end()
        self.update()
        return rc

    def clearCanvas(self):
        self.pixmap().fill(Qt.white)
        self.circles = []
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
        uic.loadUi('lab4.ui', self)

        self.canvas = Canvas(WIDTH, HEIGHT)

        # ---------------- Добавление координат ----------------
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel('(0, 600)'))
        l = QtWidgets.QLabel('(800, 600)')
        l.setAlignment(Qt.AlignRight)
        layout.addWidget(l)

        self.gridLayout.addLayout(layout, 4, 0, 1, 1)

        # ---------------- Добавление холста ----------------
        self.gridLayout.addWidget(self.canvas)
        self.dialog = MessageBox()

        # ---------------- Добавление координат ----------------
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel('(0, 0)'))
        l = QtWidgets.QLabel('(800, 0)')
        l.setAlignment(Qt.AlignRight)
        layout.addWidget(l)

        self.gridLayout.addLayout(layout, 6, 0, 1, 1)

        # ---------------- Привязка событий к Radio Button ----------------
        self.circleRB.toggled.connect(
            lambda x: self.canvas.toggleDrawPrimitive(False))
        self.pointRB.toggled.connect(
            lambda x: self.canvas.toggleDrawPrimitive(True))

        # ---------------- Привязка событий к кнопкам ----------------
        self.drawLineButton.clicked.connect(self.getResultingLine)
        self.drawButton.clicked.connect(self.drawPrimitive)
        self.clearCanvasAction.triggered.connect(self.clearCanvas)
        self.clearCirclesAction.triggered.connect(
            lambda x: self.clearLineEdits(True)
        )
        self.clearCirclesAction.setShortcut('Ctrl+E')
        self.clearPointsAction.triggered.connect(
            lambda x: self.clearLineEdits(False)
        )
        self.clearPointsAction.setShortcut('Ctrl+P')
        self.show()

    def clearCanvas(self):
        self.canvas.clearCanvas()

    def clearLineEdits(self, circles):
        if circles:
            self.cRadLE.setText('')
            self.cxLE.setText('')
            self.cyLE.setText('')
        else:
            self.pxLE.setText('')
            self.pyLE.setText('')

    def getResultingLine(self):
        rc = self.canvas.drawResultingLine()
        self.dialog.setInfo('Оповещение', rc)
        self.dialog.show()

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

    def getCircleData(self):
        r = self.tryGetLineEditData(self.cRadLE, 1, MAX_RADIUS)
        x = self.tryGetLineEditData(self.cxLE, 0, WIDTH)
        y = self.tryGetLineEditData(self.cyLE, 0, HEIGHT)
        return r, x, y

    def getPointData(self):
        x = self.tryGetLineEditData(self.pxLE, 0, WIDTH)
        y = self.tryGetLineEditData(self.pyLE, 0, HEIGHT)
        return x, y

    def drawPrimitive(self):
        if self.circleRB.isChecked():
            r, x, y = self.getCircleData()
            if None in (r, x, y):
                return
            self.canvas.paintCircle(QtCore.QPoint(x, HEIGHT - y), r)

        elif self.pointRB.isChecked():
            x, y = self.getPointData()
            if None in (x, y):  
                return
            self.canvas.paintPoint(QtCore.QPoint(x, HEIGHT - y))


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
