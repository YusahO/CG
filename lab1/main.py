from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import lab_utils as lu
import sys
import copy


def remap(v, width, height):
    return QtCore.QPoint(int(v.x() - width//2), int(height//2 - v.y()))


def remap_back(v, width, height):
    return QtCore.QPoint(int(v.x() + width//2), int(height//2 - v.y()))

def classic_map(v, min1, max1, min2, max2):
    return min2 + (v - min1) * (max2 - min2) / (max1 - min1)


class Canvas(QtWidgets.QWidget):
    def __init__(self, parent, posLabel, points, update_fn):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.pen = QtGui.QPen(Qt.red, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        self.painter = QtGui.QPainter()

        self.update_fn = update_fn
        self.posLabel = posLabel

        self.w = self.width()
        self.h = self.height()

        self.midx = self.width() // 2
        self.midy = self.height() // 2

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
            self.update_fn(remap(self.centerPos, self.width(), self.height()))
            self.resulting_pts = []
            self.update()

    def mouseMoveEvent(self, event):
        pos = remap(event.pos(), self.width(), self.height())
        self.posLabel.setText(f"Текущая позиция: ({pos.x()}, {pos.y()})")

    # def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
    #     self.midx = self.width() // 2
    #     self.midy = self.height() // 2


    def paintScalePoints(self, pts):
        if len(self.resulting_pts) < 2:
            return
        min_x = self.width()
        min_y = self.height()
        max_x = 0
        max_y = 0
        for pt in self.resulting_pts:
            px, py = pt.x(), self.height() - pt.y()
            if px < min_x:
                min_x = px
            if py < min_y:
                min_y = py
            if px > max_x:
                max_x = px
            if py > max_y:
                max_y = py

        d_y = max_y - min_y
        d_x = max_x - min_x

        if d_y > d_x * self.height() / self.width():
            d_x = self.width() / self.height() * d_y
        else:
            d_y = self.height() / self.width() * d_x

        max_y = min_y + d_y
        max_x = min_x + d_x

        for point in pts:
            px, py = point.x(), self.height() - point.y()
            px = classic_map(px, min_x, max_x, 15, self.width() - 15)
            py = classic_map(py, min_y, max_y, 15, self.height() - 15)
            point.setX(int(px))
            point.setY(int(self.height() - py))

        self.midx = classic_map(self.midx, min_x, max_x, 15, self.width() - 15)
        self.midy = classic_map(self.midy, min_y, max_y, 15, self.height() - 15)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(self.pen)

        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)

        # ------------------ оси -------------------
        self.pen.setWidth(1)
        self.pen.setColor(Qt.black)
        self.painter.setPen(self.pen)

        # self.painter.drawLine(QtCore.QPoint(self.midx, 0), QtCore.QPoint(self.midx, self.height()))
        # self.painter.drawLine(QtCore.QPoint(0, self.midy), QtCore.QPoint(self.width(), self.midy))

        self.pen.setWidth(8)
        self.pen.setColor(Qt.red)
        self.painter.setPen(self.pen)

        pts_scaled = copy.deepcopy(self.points)

        # self.paintScalePoints(pts_scaled)

        for i in range(len(self.points)):
            pm = remap(self.points[i], self.width(), self.height())
            self.painter.drawStaticText(pts_scaled[i] - QtCore.QPoint(5, 20), QtGui.QStaticText(f'{i + 1} ({pm.x()}; {pm.y()})'))
            self.painter.drawPoint(pts_scaled[i])

        found_scaled = copy.deepcopy(self.resulting_pts)
        # self.paintScalePoints(found_scaled)

        if len(self.resulting_pts) != 0:
            self.pen.setWidth(2)
            self.pen.setColor(Qt.black)
            self.painter.setPen(self.pen)
            
            self.painter.drawPolygon(found_scaled[4], found_scaled[5], found_scaled[6])
            self.painter.drawLine(found_scaled[1], found_scaled[5])
            self.painter.drawLine(found_scaled[2], found_scaled[6])
            self.painter.drawLine(found_scaled[3], found_scaled[4])

            self.pen.setWidth(8)
            self.pen.setColor(QtGui.QColor(0, 255, 0))
            self.painter.setPen(self.pen)
            for p in found_scaled[:4]:
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
    def __init__(self, rows=0, cols=2):
        super().__init__(rows, cols)
        self.setMaximumWidth(190)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 80)
    
    def addEntry(self, data):
        self.insertRow(self.rowCount())

        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(f'{data.x()}'))
        self.setItem(self.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(f'{data.y()}'))

    def removeEntry(self, ind):
        if ind < 0:
            ind = self.rowCount() + ind
        self.removeRow(ind)
    
    def cellChanged(self, row: int, column: int) -> None:
        return self.item(row, column)

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab1/main.ui', self)

        self.points = []

        self.tableWidget = Table()
        self.gridLayout.addWidget(self.tableWidget, 0, 1, -1, -1)

        self.canvas = Canvas(self, self.statLayout.itemAt(2).widget(), self.points, self.tableWidget.addEntry)

        self.dialog = MessageBox()

        # ---------------- Добавление холста ----------------
        self.verticalLayout.insertWidget(1, self.canvas, stretch=4)

        # ---------------- Привязка событий к кнопкам ----------------
        self.findTriangleButton.clicked.connect(self.getResultingTriangle)
        self.drawButton.clicked.connect(self.putPoint)
        self.deleteButton.clicked.connect(self.deletePoint)

        self.undoAction.triggered.connect(self.undo)
        self.undoAction.setShortcut('Ctrl+Z')
        self.clearCanvasAction.triggered.connect(self.clearAll)
        self.showAction.triggered.connect(self.showAuthor)

        self.tableWidget.itemChanged.connect(self.updateTable)

        self.show()

    def clearLineEdits(self):
        self.pxLE.setText('')
        self.pyLE.setText('')

    def getResultingTriangle(self):
        if len(self.points) < 3:
            self.errorLabel.setText('Ошибка: недостаточно точек')
            return 
        self.madeSearch = True
        min_pts = []
        min_areas = []
        min_area_diff = 0
        for i in range(len(self.points) - 2):
            for j in range(i + 1, len(self.points) - 1):
                for k in range(j + 1, len(self.points)):
                    pts = lu.get_all_points_in_triangle(self.points[i], self.points[j], self.points[k])
                    if pts is None:
                        self.errorLabel.setText('Ошибка: треугольник является вырожденным')
                        return

                    areas = lu.calc_areas_and_diff(pts)
                    if areas is None:
                        self.errorLabel.setText('Ошибка: треугольник является вырожденным')
                        return


                    if i == 0 and j == i + 1 and k == j + 1:
                        min_area_diff = areas[-1]
                        min_pts = pts
                        min_areas = areas

                    elif min_area_diff > areas[-1]:
                        min_area_diff = areas[-1]
                        min_pts = pts
                        min_areas = areas

        self.canvas.resulting_pts = min_pts
        self.statLayout.itemAt(3).widget().setText(f"Минимальная разница: {min_area_diff:.3f}")
        self.statLayout.itemAt(1).widget().setText(f"Наиб. площадь: {max(min_areas[:-1]):.3f}")
        self.statLayout.itemAt(0).widget().setText(f"Наим. площадь: {min(min_areas[:-1]):.3f}")
        self.canvas.update()

    def undo(self):
        if len(self.points) > 0:
            self.points.pop()
            self.tableWidget.removeEntry(-1)

        self.canvas.resulting_pts = []
        self.canvas.update()

    def deletePoint(self):
        x = self.tryGetLineEditData(self.deleteLE)
        if x is not None:
            x = int(x)
            if x > 1 and x < len(self.points):
                x -= 1
                self.tableWidget.removeEntry(x)
                self.points = self.points[:x] + self.points[x:]
            else:
                self.errorLabel.setText('Ошибка: недопустимый номер')

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
        if data.isSelected():
            w, h = self.canvas.width(), self.canvas.height()
            item = int(data.text())
            if data.column() == 0:
                if item > w//2 or item < -w//2:
                    self.errorLabel.setText('Ошибка: введенное значение больше допустимого')
                    return
                val = QtCore.QPoint(remap_back(QtCore.QPoint(item, 0), w, h).x(), self.points[data.row()].y())
            else:
                if item > h//2 or item < -h//2:
                    self.errorLabel.setText('Ошибка: введенное значение больше допустимого')
                    return
                val = QtCore.QPoint(self.points[data.row()].x(), remap_back(QtCore.QPoint(0, item), w, h).y())
            self.points[data.row()] = val

            self.canvas.resulting_pts = []
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
            self.errorLabel.setText('Ошибка: Значение поля введено неверно')
        return v

    def putPoint(self):
        w, h = self.canvas.width(), self.canvas.height()
        x = self.tryGetLineEditData(self.pxLE, -w//2, w//2)
        y = self.tryGetLineEditData(self.pyLE, -h//2, h//2)
        if x is None and y is None:
            return

        pt = QtCore.QPoint(
            x if x is not None else 0,
            y if y is not None else 0
        )

        pt = remap_back(pt, w, h)

        if pt not in self.canvas.points:
            self.canvas.points.append(pt)
        else:
            self.toggleLineEditStyle(self.pxLE)
            self.toggleLineEditStyle(self.pyLE)

        self.tableWidget.addEntry(pt)
        self.canvas.resulting_pts = []
        self.canvas.update()
    
    def clearAll(self):
        for i in range(len(self.points) - 1, -1, -1):
            self.tableWidget.removeEntry(i)
        self.points.clear()
        self.canvas.resulting_pts.clear()

        self.canvas.update()

    def showAuthor(self):
        text = '''
        Автор: Шубенина Дарья Вадимовна ИУ7-41Б
        На плоскости дано множество точек. Найти такой треугольник с вершинами в точках этого множества, у которого разность площадей между наибольшим и наименьшим из шести треугольников, образованных пересечением биссектрис минимальна.'''

        self.dialog.setInfo('Условие', text)
        self.dialog.show()

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
