import math as m
from PyQt5 import QtCore
from matrix import *

EPS = 1e-5

class Figure:
    def __init__(self, *args):
        self.pts = list(args)

    def paint(self, painter, closed=True):
        for i in range(len(self.pts) - 1):
            painter.drawLine(self.pts[i], self.pts[i + 1])  
        if closed and len(self.pts) > 2:
            painter.drawLine(self.pts[-1], self.pts[0])  

    def scale_object(self, piv, k):
        scale_mat = ScaleMat3(k[0], k[1])
        for i in range(len(self.pts)):
            res = scale_mat * ([self.pts[i].x() - piv.x()], [self.pts[i].y() - piv.y()], [1])
            self.pts[i] = QtCore.QPointF(res[0][0], res[1][0]) + piv

    def rotate_object(self, piv, angle):
        rot_mat = RotationMat3(angle)
        for i in range(len(self.pts)):
            res = rot_mat * ([self.pts[i].x() - piv.x()], [self.pts[i].y() - piv.y()], [1])
            self.pts[i] = QtCore.QPointF(res[0][0], res[1][0]) + piv

    def translate_object(self, piv, d):
        translation_mat = TranslationMat3(d[0], d[1])
        for i in range(len(self.pts)):
            res = translation_mat * ([self.pts[i].x() - piv.x()], [self.pts[i].y() - piv.y()], [1])
            self.pts[i] = QtCore.QPointF(res[0][0], res[1][0]) + piv

    def apply_transforms(self, piv, transforms):
        translation_mat, rot_mat, scale_mat = Mat((3,3)).unit(), Mat((3,3)).unit(), Mat((3,3)).unit()
        if transforms is None and piv is None:
            return
        
        if len(transforms[0]) != 0:
            translation_mat = TranslationMat3(*transforms[0])
        if transforms[1] is not None:
            rot_mat = RotationMat3(transforms[1])
        if len(transforms[2]) != 0:
            scale_mat = ScaleMat3(*transforms[2])

        piv_x, piv_y = 401, 286
        for i in range(len(self.pts)):
            res = Mat(([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)))
            res = res * TranslationMat3(-piv_x, -piv_y)
            res = res * scale_mat * rot_mat * translation_mat
            res = res * TranslationMat3(piv_x, piv_y)
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])

    
class Ellipse(Figure):
    def __init__(self, c, n, a, b):
        self.n = n
        self.c = c
        self.a = a
        self.b = b
        self.pts = [c for _ in range(n)]

    def get_points_on_ellipse(self, a, r1, r2):
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))

    def calculate_ellipse(self):
        dangle = 2 * m.pi / self.n
        angle = 0

        r1 = self.a if abs(self.a - self.b) <= EPS else self.a / 2
        r2 = self.b if abs(self.a - self.b) <= EPS else self.b / 2

        for i in range(self.n):
            p = self.get_point_on_ellipse(angle, r1, r2)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle
    
class Circle(Ellipse):
    def __init__(self, c, n, r):
        super().__init__(c, n, r*2, r*2)

class Arc(Ellipse):
    def __init__(self, c, n, a, b, start, end):
        super().__init__(c, n, a, b)
        self.start = start
        self.end = end
    
    def calculate_arc(self, a: float, b: float, start: float, end: float):
        dangle = (end - start) / self.n
        angle = start

        r1 = a if abs(a - b) <= EPS else a / 2
        r2 = b if abs(a - b) <= EPS else b / 2

        for i in range(self.n):
            p = self.get_point_on_ellipse(angle, r1, r2)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle

class BugObject(Figure):
    def __init__(self, c, n):
        self.c = c

        self.body = Ellipse(c, n, 100, 200)
        self.head = Circle(c - QtCore.QPoint(0, 145), n, 45)
        self.smile = Arc(c - QtCore.QPoint(0, 130), n, 40, 20, 3.14/6, 5*3.14/6)
        self.leftEye = Circle(c - QtCore.QPoint(15, 154), n, 10)
        self.rightEye = Circle(c - QtCore.QPoint(-15, 154), n, 10)    
    
    def transformObject(self, piv, transform):
        self.body.apply_transforms(piv, transform)
        self.head.apply_transforms(piv, transform)
        self.smile.apply_transforms(piv, transform)
        self.leftEye.apply_transforms(piv, transform)
        self.rightEye.apply_transforms(piv, transform)

    def paint(self, painter):
        self.body.paint(painter)
        self.head.paint(painter)
        self.smile.paint(painter, closed=False)
        self.leftEye.paint(painter)
        self.rightEye.paint(painter)
