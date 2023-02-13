from PyQt5 import QtWidgets, QtCore, QtGui, uic

def find_points(p1, p2, p3):
    l1 = abs(p2 - p1)
    l2 = abs(p3 - p1)
    l3 = abs(p3 - p2)

    pl12 = p1 + l1 / l2
