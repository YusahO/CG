import sys
from PyQt5 import uic, QtWidgets

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('/home/daria/Документы/CG/lab3/lab3.ui', self)
        self.colorDialog = QtWidgets.QColorDialog()

        self.lineColPB.clicked.connect(lambda: self.colorDialog.setVisible(True))
        self.bgColPB.clicked.connect(lambda: self.colorDialog.setVisible(True))

        self.lineColSwatch.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_2.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_3.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_4.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_5.changeColor.connect(self.colorview.changeCurColor)
        self.lineColSwatch_6.changeColor.connect(self.colorview.changeCurColor)

        self.show()

app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()