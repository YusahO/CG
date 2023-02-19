from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import sys
import figures as fig

def remap(v, width, height):
    return QtCore.QPoint(int(v.x() - width//2), int(height//2 - v.y()))

def remap_back(v, width, height):
    return QtCore.QPoint(int(v.x() + width//2), int(height//2 - v.y()))

def replace_in_list(l, x, y):
    for i in range(len(l)):
        if l[i] == x:
            l[i] = y
    return l

class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.objectCenter = QtCore.QPoint(self.width() // 2, self.height() // 2)

        self.pivotFieldEmpty = True

        self.transforms = [[0, 0], 0, [1, 1]]
        self.pivotPos = self.objectCenter

        self.pen = QtGui.QPen(
            Qt.red, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.painter = QtGui.QPainter()

        self.obj = fig.BugObject(self.objectCenter, 25)

        self.update()

    def resizeEvent(self, event):
        self.objectCenter = QtCore.QPoint(self.width()//2, self.height()//2)
        if self.pivotFieldEmpty:
            self.pivotPos = self.objectCenter

        self.obj.c = self.objectCenter
        self.obj.calculatePoints(self.obj.c)
        self.update()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(self.pen)

        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        self.pen.setWidth(8)
        self.pen.setColor(Qt.red)
        self.painter.setPen(self.pen)
        self.painter.drawPoint(self.pivotPos)

        self.pen.setWidth(2)
        self.pen.setColor(Qt.black)
        self.painter.setPen(self.pen)
        self.obj.paint(self.painter)

        self.painter.end()

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
        uic.loadUi('/home/daria/Документы/CG/lab2/main.ui', self)

        self.canvas = Canvas()

        self.dialog = MessageBox()

        # ---------------- Добавление холста ----------------
        self.mainLayout.addWidget(self.canvas)

        # ---------------- Привязка событий к кнопкам ----------------
        self.transformButton.clicked.connect(self.makeTransforms)
        self.undoAction.triggered.connect(self.undo)
        self.clearPointsAction.setShortcut('Ctrl+P')
        self.undoAction.setShortcut('Ctrl+Z')

        self.show()


    def undo(self):
        pass

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
            v = float(lineEdit.text())
            if None not in (vmin, vmax):
                if not vmin < v < vmax:
                    raise Exception
            self.toggleLineEditStyle(lineEdit, error=False)
        except:
            v = None
        return v

    def makeTransforms(self):
        translation = [self.tryGetLineEditData(self.translationXLE), self.tryGetLineEditData(self.translationYLE)]
        rotation = self.tryGetLineEditData(self.rotationAngleLE)
        scale = [self.tryGetLineEditData(self.scaleXLE), self.tryGetLineEditData(self.scaleYLE)]
        pivot = [self.tryGetLineEditData(self.pivotXLE), self.tryGetLineEditData(self.pivotYLE)]

        translation = replace_in_list(translation, None, 0)
        translation[1] = -translation[1]
        rotation = 0 if rotation is None else rotation * 3.14 / 180
        scale = replace_in_list(scale, None, 1)

        self.canvas.pivotPos = QtCore.QPoint(
            int(pivot[0] + self.canvas.width() // 2) if pivot[0] is not None else self.canvas.pivotPos.x(),
            int(self.canvas.height() // 2 - pivot[1]) if pivot[1] is not None else self.canvas.pivotPos.y(),
        )

        if not any(pivot):
            self.canvas.pivotFieldEmpty = False

        self.canvas.transforms = [translation, rotation, scale]
        # print([translation, rotation, scale])
        self.canvas.obj.transformObject(self.canvas.pivotPos, self.canvas.transforms)
        self.canvas.update()

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
