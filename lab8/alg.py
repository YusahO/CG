from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QPoint, QRect

from copy import deepcopy

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

MASK_LEFT = 0b0001
MASK_RIGHT = 0b0010
MASK_BOTTOM = 0b0100
MASK_TOP = 0b1000


def CrossProd(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def DotProd(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def GetVector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]


def CheckPoly(vertices):
    if len(vertices) < 3:
        return False

    sgn = 1 if CrossProd(GetVector(vertices[1], vertices[2]),
                         GetVector(vertices[0], vertices[1])) > 0 else -1

    for i in range(3, len(vertices)):
        if sgn * CrossProd(GetVector(vertices[i - 1], vertices[i]),
                           GetVector(vertices[i - 2], vertices[i - 1])) < 0:
            return False

    if sgn * CrossProd(GetVector(vertices[-1], vertices[0]),
                       GetVector(vertices[-2], vertices[-1])) < 0:
        return False

    if sgn < 0:
        vertices.reverse()

    return True


def GetNormal(p1, p2, cp):
    vector = GetVector(p1, p2)
    normal = [1, 0] if vector[0] == 0 else [-vector[1] / vector[0], 1]

    if DotProd(GetVector(p2, cp), normal) < 0:
        for i in range(len(normal)):
            normal[i] = -normal[i]

    return normal


def GetNormals(vertices):
    normals = []
    size = len(vertices)
    for i in range(size):
        normals.append(GetNormal(vertices[i], vertices[(
            i + 1) % size], vertices[(i + 2) % size]))

    return normals


def CutSection(section, vertices, normals):
    # граничные значения параметра t
    t_start = 0
    t_end = 1
    # N * (P1 + (P2 - P1) * t - fi) = 03
    # D = P2 - P1 -- директриса (вектор направления отрезка)
    D = GetVector(section[0], section[1])

    for i in range(len(vertices)):
        # Вычисление wi = P1 - fi -- вектор между точкой отрезка и произвольной точкой на границе отсекателя
        if vertices[i] != section[0]:
            wi = GetVector(vertices[i], section[0])
        else:
            wi = GetVector(vertices[(i + 1) % len(vertices)], section[0])

        Dck = DotProd(D, normals[i])
        Wck = DotProd(wi, normals[i])

        # отрезок параллелен границе
        if Dck == 0:
            # отрезок полностью невидим для данной границы
            if Wck < 0:
                return
            else:
                continue

        t = -Wck / Dck
        if Dck > 0:
            if t > t_start:
                t_start = t
        else:
            if t < t_end:
                t_end = t

        # установлен факт полной невидимости
        if t_start > t_end:
            break

    if t_start < t_end:
        p1 = [round(section[0][0] + D[0] * t_start),
              round(section[0][1] + D[1] * t_start)]

        p2 = [round(section[0][0] + D[0] * t_end),
              round(section[0][1] + D[1] * t_end)]

        return [*p1, *p2]
