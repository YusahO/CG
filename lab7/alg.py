from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QPoint, QRect

from copy import deepcopy

LEFT =   0
RIGHT =  1
TOP =    2
BOTTOM = 3

MASK_LEFT =   0b0001
MASK_RIGHT =  0b0010
MASK_BOTTOM = 0b0100
MASK_TOP =    0b1000


def PointToArr(p: QPoint):
    return [p.x(), p.y()]

def RectToArr(rect: QRect):
    x0, x1, y1, y0 = int(rect.left()), int(rect.right()), int(rect.bottom()), int(rect.top())
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    return [ x0, x1, y1, y0 ]


def SetBits(point, rect_sides):
    bits = 0b0000
    print('rect_sides', rect_sides)
    print('point', point)
    if point[0] < rect_sides[LEFT]:
        bits += MASK_LEFT
    if point[0] > rect_sides[RIGHT]:
        bits += MASK_RIGHT
    if point[1] < rect_sides[BOTTOM]:
        bits += MASK_BOTTOM
    if point[1] > rect_sides[TOP]:
        bits += MASK_TOP
    return bits


def FindVertical(p, ind, rect):
    if p[ind][1] > rect[TOP]:
        return [p[ind][0], rect[TOP]]
    elif p[ind][1] < BOTTOM:
        return [p[ind][0], rect[BOTTOM]]
    else:
        return p[ind]


def CutSection(_rect: QRect, _p):
    rect = RectToArr(_rect)
    p = deepcopy(_p)

    s = list()
    for i in range(2):
        s.append(SetBits(p[i], rect))

    print('s: ', *list(map(bin, s)))

    # полностью видимый отрезок
    if s[0] == 0 and s[1] == 0:
        return [p[0][0], p[0][1], p[1][0], p[1][1]]

    # полностью невидимый отрезок
    if s[0] & s[1]:
        return

    icur = 0  # индекс текущей обрабатываемой вершины
    res = []

    # Проверка, нет ли одной точки внутри отсекателя (первая проверка для точки с индексом 0,
    # вторая - с индексом 1). Если вторая точка внутри области - поставим ее на первое место
    # и работаем с другой (смена мест нужна, чтобы в начале была обработанная точка, а за ней - нет)
    if s[0] == 0:
        icur = 1
        res.append(p[0])

    elif s[1] == 0:
        res.append(p[1])
        icur = 1
        # Вторая вершина уже внутри области, поменяем местами вершины, чтобы работать с необработанной
        p.reverse()
        s.reverse()

    while icur < 2:
        if p[0][0] == p[1][0]:
            res.append(FindVertical(p, icur, rect))
            icur += 1
            continue

        m = (p[1][1] - p[0][1]) / (p[1][0] - p[0][0])

        # если есть пересечение с левой границей, ищем его
        if s[icur] & MASK_LEFT:
            y = round(m * (rect[LEFT] - p[icur][0]) + p[icur][1])
            if y <= rect[TOP] and y >= rect[BOTTOM]:
                res.append([rect[LEFT], y])
                icur += 1
                continue

        # если есть пересечение с правой границей, ищем его
        elif s[icur] & MASK_RIGHT:
            y = round(m * (rect[RIGHT] - p[icur][0]) + p[icur][1])
            if y <= rect[TOP] and y >= rect[BOTTOM]:
                res.append([rect[RIGHT], y])
                icur += 1
                continue

        # Если прямая горизонтальна, пересечения с верхней и нижней границей быть не может
        # (заканчиваем обработку текущей вершины)
        if m == 0:
            icur += 1
            continue

        # Нахождение пересечений с верхней и нижней границами

        # С верхней (если рассматриваемая вершина выше верхней границы)
        if s[icur] & MASK_TOP:
            x = round((rect[TOP] - p[icur][1]) / m + p[icur][0])
            if x <= rect[RIGHT] and x >= rect[LEFT]:
                res.append([x, rect[TOP]])
                icur += 1
                continue
        
        # С нижней (если рассматриваемая вершина ниже нижней границы)
        elif s[icur] & MASK_BOTTOM:
            x = round((rect[BOTTOM] - p[icur][1]) / m + p[icur][0])
            if x <= rect[RIGHT] and x >= rect[LEFT]:
                res.append([x, rect[BOTTOM]])
                icur += 1
                continue

        icur += 1

    if res:
        return [res[0][0], res[0][1], res[1][0], res[1][1]]

