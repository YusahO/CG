from numpy import pi, cos, sin
from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleParametricDraw(cx, cy, R, color=QColor(0, 0, 0)):
    pts = []
    t = 1 / R
    da = 0

    while da <= pi / 4:
        x = round(R * cos(da))
        y = round(R * sin(da))

        da += t

        pts.extend(AddSymmetricPointsCircle(cx, cy, cx + x, cy + y))

    pts.append(color)
    pts.append(False)
    return pts

def CircleParametricMeasure(R):
    t = 1 / R
    da = 0

    while da <= pi / 4:
        x = round(R * cos(da))
        y = round(R * sin(da))

        da += t


def EllipseParametricDraw(cx, cy, a, b, color=QColor(0, 0, 0)):
    pts = []
    t = 1 / a if a > b else 1 / b

    da = 0

    while da <= pi / 2:
        x = round(a * cos(da))
        y = round(b * sin(da))

        da += t

        pts.extend(AddSymmetricPointsEllipse(cx, cy, cx + x, cy + y))

    pts.append(color)
    pts.append(False)
    return pts


def EllipseParametricMeasure(a, b):
    t = 1 / a if a > b else 1 / b

    da = 0

    while da <= pi / 2:
        x = round(a * cos(da))
        y = round(b * sin(da))

        da += t
