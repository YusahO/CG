from PyQt5 import QtWidgets, QtCore, QtGui, uic
import math as m
import itertools as it
EPS = 1e-5

def calculate_vector(a, b) -> list:
    return QtCore.QPointF(b.x() - a.x(), b.y() - a.y())

def vector_len(a, b):
    return m.sqrt((b.x() - a.x())**2 + (b.y() - a.y())**2)

def bisec(a, b, c):
    '''Поиск точки пересечения биссектрисы с прямой a, c'''
    ab = vector_len(a, b)
    bc = vector_len(b, c)

    v_ac = calculate_vector(a, c)
    if ((v_ac.x() * v_ac.x() + v_ac.y() * v_ac.y()) <= EPS):
        return None

    t = 1 / (1 + bc / ab)

    xpos = a.x() + t * v_ac.x()
    ypos = a.y() + t * v_ac.y()

    return QtCore.QPointF(xpos, ypos)

def triangle_area(a, b, c) -> float:
    return 0.5 * abs((b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y()))

def get_all_points_in_triangle(a, b, c) -> QtCore.QPoint:
    points = [a, b, c]
    new_points = []
    for i in range(len(points)):
        p = bisec(points[0], points[1], points[2])
        if p is None:
            return None
        new_points.append(p)

        if i == 0:
            new_points.insert(0, bisec(new_points[0], points[0], points[1]))

        points.append(points.pop(0))
    # print(points)
    return new_points + points

def calc_areas_and_diff(points):
    areas = [0] * 7
    for i in range(len(points)):
        if (points[i] is None):
            return None
    areas[0] = triangle_area(points[0], points[4], points[1])
    areas[1] = triangle_area(points[0], points[4], points[2])
    areas[2] = triangle_area(points[0], points[5], points[2])
    areas[3] = triangle_area(points[0], points[5], points[3])
    areas[4] = triangle_area(points[0], points[6], points[3])
    areas[5] = triangle_area(points[0], points[6], points[1])

    areas[-1] = max(areas[:-1]) - min(areas[:-1])

    return areas
