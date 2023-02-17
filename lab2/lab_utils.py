from PyQt5 import QtWidgets, QtCore, QtGui, uic
import math as m
import itertools as it
from matrix import *

EPS = 1e-5



# print(apply_transforms(QtCore.QPointF(0, 0), [QtCore.QPointF(-5, -5), QtCore.QPointF(-5, 5), QtCore.QPointF(5, -5), QtCore.QPointF(5, 5)], [[1, 1], 0, [1, 1]]))