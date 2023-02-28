import math as m
from PyQt5 import QtCore
from matrix import *

from copy import deepcopy

EPS = 1e-5

class Figure:
    def __init__(self, *args):
        self.pts = list(args)
        self.initial_pts = deepcopy(self.pts)
        self.previous_pts = deepcopy(self.pts)

    def paint(self, painter, closed=True):
        for i in range(len(self.pts) - 1):
            painter.drawLine(self.pts[i], self.pts[i + 1])  
        if closed and len(self.pts) > 2:
            painter.drawLine(self.pts[-1], self.pts[0])  

    def scale_object(self, piv, k):
        self.previous_pts = deepcopy(self.pts)
        scale_mat = ScaleMat3(*k)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * TranslationMat3(-piv.x(), -piv.y())
            res = res * scale_mat * TranslationMat3(piv.x(), piv.y())
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])

    def rotate_object(self, piv, angle):
        self.previous_pts = deepcopy(self.pts)
        rot_mat = RotationMat3(angle)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * TranslationMat3(-piv.x(), -piv.y())
            res = res * rot_mat * TranslationMat3(piv.x(), piv.y())
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])

    def translate_object(self, d):
        self.previous_pts = deepcopy(self.pts)
        translation_mat = TranslationMat3(*d)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * translation_mat
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])

    def undo(self):
        self.pts = self.previous_pts

    def reset(self):
        self.pts = self.initial_pts

class Ellipse(Figure):
    def __init__(self, c, n, a, b):
        self.n = n
        self.c = c
        self.a = a
        self.b = b
        self.pts = [c for _ in range(n)]

        self.__calculate_ellipse()

        self.initial_pts = deepcopy(self.pts)
        self.previous_pts = deepcopy(self.pts)


    def get_points_on_ellipse(self, a, r1, r2):
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))

    def __calculate_ellipse(self):
        dangle = 2 * m.pi / self.n
        angle = 0

        r1 = self.a if abs(self.a - self.b) <= EPS else self.a / 2
        r2 = self.b if abs(self.a - self.b) <= EPS else self.b / 2

        for i in range(self.n):
            p = self.get_points_on_ellipse(angle, r1, r2)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle
    
class Circle(Figure):
    def __init__(self, c, n, r):
        self.c = c
        self.n = n
        self.r = r
        self.pts = [c for _ in range(n)]

        self.__calculate_circle()

        self.initial_pts = deepcopy(self.pts)
        self.previous_pts = deepcopy(self.pts)

    def get_points_on_ellipse(self, a, r):
        return QtCore.QPointF(r * m.cos(a), r * m.sin(a))

    def __calculate_circle(self):
        dangle = 2 * m.pi / self.n
        angle = 0
        
        for i in range(self.n):
            p = self.get_points_on_ellipse(angle, self.r)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle

class Arc(Figure):
    def __init__(self, c, n, a, b, start, end):
        self.c = c
        self.n = n
        self.a = a
        self.b = b
        self.start = start
        self.end = end
        self.pts = [c for _ in range(n)]

        self.__calculate_arc()

        self.initial_pts = deepcopy(self.pts)
        self.previous_pts = deepcopy(self.pts)

    def get_points_on_ellipse(self, a, r1, r2):
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))
    
    def __calculate_arc(self):
        dangle = (self.end - self.start) / self.n
        angle = self.start

        r1 = self.a if abs(self.a - self.b) <= EPS else self.a / 2
        r2 = self.b if abs(self.a - self.b) <= EPS else self.b / 2

        for i in range(self.n):
            p = self.get_points_on_ellipse(angle, r1, r2)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle

class BugObject(Figure):
    def __init__(self, c, n):
        self.c = c
        self.n = n
        self.calculatePoints(self.c)

    def translateObject(self, d: list[float, float]):
        for f in vars(self).values():
            if type(f) in (Figure, *Figure.__subclasses__()):
                f.translate_object(d)
    
    def rotateObject(self, piv, angle):
        for f in vars(self).values():
            if type(f) in (Figure, *Figure.__subclasses__()):
                f.rotate_object(piv, angle)

    def scaleObject(self, piv, k):
        for f in vars(self).values():
            if type(f) in (Figure, *Figure.__subclasses__()):
                f.scale_object(piv, k)

    def undo(self):
        for f in vars(self).values():
            if type(f) in (Figure, *Figure.__subclasses__()):
                f.undo()

    def reset(self):
        self.calculatePoints(self.c)

    def paint(self, painter):
        self.body.paint(painter)
        self.head.paint(painter)
        self.smile.paint(painter, closed=False)
        self.leftEye.paint(painter)
        self.rightEye.paint(painter)
        self.leftArm.paint(painter)
        self.rightArm.paint(painter)
        self.leftWhisker.paint(painter, closed=False)
        self.rightWhisker.paint(painter, closed=False)
        self.leftLeg.paint(painter, closed=False)
        self.rightLeg.paint(painter, closed=False)
    
    def calculatePoints(self, c):
        self.body = Ellipse(c, self.n, 100, 200)
        self.head = Circle(c - QtCore.QPoint(0, 145), self.n, 45)
        self.smile = Arc(c - QtCore.QPoint(0, 130), self.n, 40, 20, 3.14/6, 5*3.14/6)
        self.leftEye = Circle(c - QtCore.QPoint(17, 154), self.n, 10)
        self.rightEye = deepcopy(self.leftEye)
        self.rightEye.scale_object(self.c, [-1, 1])

        self.leftArm =  Figure(self.c - QtCore.QPoint(30, -20),
                               self.c - QtCore.QPoint(30, 20),
                               self.c - QtCore.QPoint(100, 90))
        self.rightArm = deepcopy(self.leftArm)
        self.rightArm.scale_object(self.c, [-1, 1])

        self.leftWhisker = Figure(self.c - QtCore.QPoint(0, 154), 
                                  self.c - QtCore.QPoint(10, 200),
                                  self.c - QtCore.QPoint(50, 200))
        self.rightWhisker = deepcopy(self.leftWhisker)
        self.rightWhisker.scale_object(self.c, [-1, 1])

        self.leftLeg = Figure(self.c + QtCore.QPoint(20, 90), 
                              self.c + QtCore.QPoint(25, 120),
                              self.c + QtCore.QPoint(50, 120))
        self.rightLeg = deepcopy(self.leftLeg)
        self.rightLeg.scale_object(self.c, [-1, 1])
    
