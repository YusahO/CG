import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPoint
import re

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab9/lab9.ui', self)

        self.canvas.setParent(self)

        self.msgbox = QtWidgets.QMessageBox(self)

        self.polyColor.clicked.connect(lambda: self.setPBColor(self.polyColor))
        self.sepColor.clicked.connect(lambda: self.setPBColor(self.sepColor))
        self.resColor.clicked.connect(lambda: self.setPBColor(self.resColor))
        
        self.closeSepPB.clicked.connect(self.closeCutter)
        self.closeNgonPB.clicked.connect(self.closePoly)

        self.table.cellClicked.connect(self.highlightParallel)

        self.canvClearPB.clicked.connect(self.clearCanvas)

        self.sepDrawPB.clicked.connect(self.addCutterPoint)
        self.ngonDrawPB.clicked.connect(self.addPolyPoint)

        self.deselectPB.clicked.connect(self.deselect)
        self.doPB.clicked.connect(self.canvas.doCutting)

        self.author.triggered.connect(
            lambda: self.msgbox.information(
                self, 'Об авторе', '<font size=14><b>ИУ7-41Б Шубенина Дарья</b></font>'
            )
        )

        self.prog.triggered.connect(
            lambda: self.msgbox.information(
                self, 'О программе', '<font size=14><b>Реализация алгоритма отсечения многоугольников Сазерленда Ходжмена</b></font>'
            )
        )
        self.show()

    def deselect(self):
        self.canvas.temp_line = []
        selected_rows = self.table.selectionModel().selectedRows()
        for row in selected_rows:
            self.table.item(row.row(), 0).setSelected(False)
        self.canvas.update()

    def highlightParallel(self, r, c):
        if r == -1:
            self.msgbox.warning(
                self, 'Предупреждение!', '<font size=14><b>Не выбрана соответствующая граница отсекателя</b></font>'
            )
            return
        
        data = self.table.item(r, c)
        x1, y1, x2, y2 = [int(f) for f in re.findall('[0-9]*', data.text()) if f != '']
        self.canvas.temp_line = [QPoint(x1, y1), QPoint(x2, y2)]
        self.canvas.update()

    def closeCutter(self):
        if len(self.canvas.cutter) == 0:
            return
        
        self.canvas.cutter_closed = True
        self.table.closed = True
        self.table.rebuildTable()
        self.canvas.update()
    
    def closePoly(self):
        if len(self.canvas.poly) == 0:
            return
        
        self.canvas.poly_closed = True
        self.canvas.update()

    def clearCanvas(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        self.canvas.temp_line = []

        self.canvas.poly = []
        self.canvas.poly_closed = False

        self.canvas.cutter = []
        self.canvas.cutter_closed = False

        self.canvas.results.clear()

        self.canvas.update()

    def addCutterPoint(self):
        x = self.tryGetLineEditData(self.sepXLE, int, 0)
        if x is None:
            return
        y = self.tryGetLineEditData(self.sepYLE, int, 0)
        if y is None:
            return
        
        self.canvas.addPointToCutter(QPoint(x, y))
        self.canvas.update()

    def addPolyPoint(self):
        x = self.tryGetLineEditData(self.ngonXLE, int, 0)
        if x is None:
            return
        y = self.tryGetLineEditData(self.ngonYLE, int, 0)
        if y is None:
            return
        
        self.canvas.addPointToPoly(QPoint(x, y))
        self.canvas.update()


    def setPBColor(self, pb):
        newcol = QtWidgets.QColorDialog().getColor()

        style = pb.styleSheet()
        new_style = ''

        for l in style.splitlines():
            if (l.startswith('background-color')):
                l = f'background-color: rgb({newcol.red()},{newcol.green()},{newcol.blue()});\n'
                new_style += l

        pb.setStyleSheet(new_style)
        
    def getPBColor(self, pb: QtWidgets.QPushButton):
        style = pb.styleSheet()
        color = QColor(0, 0, 0)
        for l in style.splitlines():
            if (l.startswith('background-color')):
                rgb = [int(s) for s in re.findall(r'\b\d+\b', l)]
                color = QColor(*rgb)
        
        return color

    def tryGetLineEditData(self, lineEdit, T=float, vmin=None, vmax=None):
        try:
            v = T(lineEdit.text())
            if vmin is not None and v < vmin:
                raise Exception
            if vmax is not None and v > vmax:
                raise Exception
        except:
            message = ''
            if vmin is not None and vmax is not None:
                message = f'Значение должно быть числом в промежутке [{vmin}, {vmax}]'
            elif vmin is None and vmax is not None:
                message = f'Значение должно быть числом <= {vmax}'
            elif vmin is not None and vmax is None:
                message = f'Значение должно быть числом >= {vmin}'

            self.msgbox.critical(
                self, 'Ошибка!', '<font size=14><b>Неверный ввод!\n' + message + '</b></font>')
            v = None
        return v
    


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()
