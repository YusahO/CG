from PyQt5 import QtWidgets, QtCore, QtGui, uic
import math as m
import itertools as it

EPS = 1e-5


class Mat():
    def __init__(self, rows, cols):
        self.mat = [[0 for _ in range(cols)] for _ in range(rows)]

    def __mul__(self, other):
        res = Mat(len(self.mat), len(other[0]))
        for i in range(len(self.mat)):
            for j in range(len(res[0])):
                for k in range(len(self.mat[0])):
                    res[i][j] += self.mat[i][k] * other[k][j]
        return res

    def __add__(self, other):
        res = Mat(len(self.mat), len(self.mat[0]))
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                res[i][j] = self.mat[i][j] + other[i][j]
        return res
    
    def __repr__(self):
        res = ''
        for l in self.mat:
            res += str(l) + '\n'
        return res[:-1]
    
    def __getitem__(self, key):
        return self.mat[key]
    
    def unit(self):
        for i in range(len(self.mat)):
            self.mat[i][i] = 1
    
class ScaleMat3(Mat):
    def __init__(self, kx, ky):
        super().__init__(3, 3)
        self.mat[0][0] = kx
        self.mat[1][1] = ky
        self.mat[2][2] = 1
    
class TranslationMat3(Mat):
    def __init__(self, dx, dy):
        super().__init__(3, 3)
        self.unit()
        self.mat[-1][0] = dx
        self.mat[-1][1] = dy

class RotationMat3(Mat):
    def __init__(self, angle):
        super().__init__(3, 3)
        self.mat[0][0] = m.cos(angle)
        self.mat[0][1] = m.sin(angle)
        self.mat[1][0] = -m.sin(angle)
        self.mat[1][1] = m.cos(angle)
        self.mat[-1][-1] = 1

def scale_object(piv, pts, k):
    scale_mat = ScaleMat3(k[0], k[1])
    for i in range(len(pts)):
        res = scale_mat * ([pts[i].x() - piv.x()], [pts[i].y() - piv.y()], [1])
        pts[i] = QtCore.QPointF(res[0][0], res[1][0]) + piv
    return pts

# def rotate_object(piv, pts, angle):
#     rot_mat = Mat.

def calculate_vector(a, b) -> list:
    return QtCore.QPointF(b.x() - a.x(), b.y() - a.y())


def vector_len(a, b):
    return m.sqrt((b.x() - a.x())**2 + (b.y() - a.y())**2)


def get_point_on_ellipse(a, r1, r2):
    if (abs(a) <= EPS):
        return QtCore.QPointF(r1, 0)
    elif (abs(a - m.pi) <= EPS):
        return QtCore.QPointF(-r1, 0)
    elif (abs(a - m.pi/2) <= EPS):
        return QtCore.QPointF(0, r2)
    elif (abs(a - 3*m.pi/2) <= EPS):
        return QtCore.QPointF(0, -r2)
    else:
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))


def calculate_arc(c: QtCore.QPoint, a: float, b: float, start: float, end: float, n: int):
    pts = [c for _ in range(n)]
    dangle = (end - start) / n
    angle = start

    r1 = a if abs(a - b) <= EPS else a / 2
    r2 = b if abs(a - b) <= EPS else b / 2

    for i in range(n):
        p = get_point_on_ellipse(angle, r1, r2)
        pts[i] += QtCore.QPointF(p)
        angle += dangle
    return pts


def calculate_ellipse(c: QtCore.QPoint, a: float, b: float, n: int):
    pts = [c for _ in range(n)]
    dangle = 2 * m.pi / n
    angle = 0

    r1 = a if abs(a - b) <= EPS else a / 2
    r2 = b if abs(a - b) <= EPS else b / 2

    for i in range(n):
        p = get_point_on_ellipse(angle, r1, r2)

        pts[i] += QtCore.QPointF(p)
        angle += dangle
    return pts