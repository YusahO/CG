import math as m
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from matrix import *

from copy import deepcopy

EPS = 1e-5

class Figure:
    def __init__(self, *args):
        self.pts = list(args)
        self.current_pts = [list(args)]

    def paint(self, painter, color, closed=True):
        pen = QtGui.QPen(color, 2)
        painter.setPen(pen)
        for i in range(len(self.pts) - 1):
            painter.drawLine(self.pts[i], self.pts[i + 1])  
        if closed and len(self.pts) > 2:
            painter.drawLine(self.pts[-1], self.pts[0])  

    def scale_object(self, piv, k):
        scale_mat = ScaleMat3(*k)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * TranslationMat3(-piv.x(), -piv.y())
            res = res * scale_mat * TranslationMat3(piv.x(), piv.y())
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])
        self.current_pts.append(deepcopy(self.pts))

    def rotate_object(self, piv, angle):
        rot_mat = RotationMat3(-angle)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * TranslationMat3(-piv.x(), -piv.y())
            res = res * rot_mat * TranslationMat3(piv.x(), piv.y())
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])
        self.current_pts.append(deepcopy(self.pts))

    def translate_object(self, d):
        translation_mat = TranslationMat3(*d)
        for i in range(len(self.pts)):
            res = Mat([self.pts[i].x(), self.pts[i].y(), 1], (1, 3)) * translation_mat
            self.pts[i] = QtCore.QPointF(res[0][0], res[0][1])
        self.current_pts.append(deepcopy(self.pts))

    def undo(self):
        if len(self.current_pts) > 1:
            self.current_pts.pop(-1)
            self.pts = deepcopy(self.current_pts[-1])

    def reset(self):
        self.pts = deepcopy(self.current_pts[0])
        self.current_pts = [deepcopy(self.current_pts[0])]

class Ellipse(Figure):
    def __init__(self, c, n, a, b):
        self.n = n
        self.c = c
        self.a = a
        self.b = b
        self.pts = [c for _ in range(n)]

        self.__calculate_ellipse()

        self.current_pts = [deepcopy(self.pts)]


    def get_points_on_ellipse(self, a, r1, r2):
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))

    def __calculate_ellipse(self):
        dangle = 2 * m.pi / self.n
        angle = 0

        r1 = self.a
        r2 = self.b

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
        
        self.current_pts = [deepcopy(self.pts)]

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

        self.current_pts = [deepcopy(self.pts)]

    def get_points_on_ellipse(self, a, r1, r2):
        return QtCore.QPointF(r1 * m.cos(a), r2 * m.sin(a))
    
    def __calculate_arc(self):
        dangle = (self.end - self.start) / self.n
        angle = self.start

        r1 = self.a / 2
        r2 = self.b / 2

        for i in range(self.n):
            p = self.get_points_on_ellipse(angle, r1, r2)
            self.pts[i] += QtCore.QPointF(p)
            angle += dangle

class BugObject(Figure):
    def __init__(self, c):
        self.c = c
        self.n = 128
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
        self.body.paint(painter, QtGui.QColor(0, 127, 0))
        self.head.paint(painter,  QtGui.QColor(100, 127, 255))
        self.smile.paint(painter, QtGui.QColor(0, 127, 255), closed=False)
        self.leftEye.paint(painter, QtGui.QColor(127, 0, 127))
        self.rightEye.paint(painter, QtGui.QColor(255, 100, 100))
        self.leftArm.paint(painter, QtGui.QColor(127, 0, 255))
        self.rightArm.paint(painter, QtGui.QColor(0, 0, 0))
        self.leftWhisker.paint(painter, QtGui.QColor(255, 0, 0), closed=False)
        self.rightWhisker.paint(painter, QtGui.QColor(0, 0, 255), closed=False)
        self.leftLeg.paint(painter, QtGui.QColor(255, 127, 255), closed=False)
        self.rightLeg.paint(painter, QtGui.QColor(200, 50, 100), closed=False)
    
    def calculatePoints(self, c):
        p = 100
        self.body = Ellipse(c, self.n, p // 2, p)
        self.head = Circle(c - QtCore.QPoint(0, 3 * p // 2), self.n, p // 2)
        self.smile = Arc(c - QtCore.QPoint(0, 4 * p // 3), self.n, p // 3, p // 6, 3.14/6, 5*3.14/6)
        self.leftEye = Circle(c - QtCore.QPoint(p // 5, 5 * p // 3), self.n, p // 10)

        self.rightEye = deepcopy(self.leftEye)
        self.rightEye.scale_object(self.c, [-1, 1])
        self.rightEye.current_pts = [deepcopy(self.rightEye.pts)]
        self.rightEye.initial_pts = deepcopy(self.rightEye.pts)

        self.leftArm =  Figure(self.c - QtCore.QPoint(p // 3, -(p // 5)),
                               self.c - QtCore.QPoint(p // 3,   p // 5),
                               self.c - QtCore.QPoint(p, int(p * .9)))
        self.rightArm = deepcopy(self.leftArm)
        self.rightArm.scale_object(self.c, [-1, 1])
        self.rightArm.current_pts = [deepcopy(self.rightArm.pts)]
        self.rightArm.initial_pts = deepcopy(self.rightArm.pts)

        self.leftWhisker = Figure(self.c - QtCore.QPoint(0, 5 * p // 3), 
                                  self.c - QtCore.QPoint(p // 10, int(p * 2.1)),
                                  self.c - QtCore.QPoint(p // 2,  int(p * 2.1)))
        self.rightWhisker = deepcopy(self.leftWhisker)
        self.rightWhisker.scale_object(self.c, [-1, 1])
        self.rightWhisker.current_pts = [deepcopy(self.rightWhisker.pts)]
        self.rightWhisker.initial_pts = deepcopy(self.rightWhisker.pts)

        x = p // 4
        a = p // 2
        b = p

        y = -int((1 - (x / a)**2) ** .5 * b)

        self.leftLeg = Figure(self.c - QtCore.QPoint(x, y), 
                              self.c - QtCore.QPoint(x + p//10, y - p//3),
                              self.c - QtCore.QPoint(x + p//3, y - p//3))
        
        self.rightLeg = deepcopy(self.leftLeg)
        self.rightLeg.scale_object(self.c, [-1, 1])
        self.rightLeg.current_pts = [deepcopy(self.rightLeg.pts)]
        self.rightLeg.initial_pts = deepcopy(self.rightLeg.pts)
    
