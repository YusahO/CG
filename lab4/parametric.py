from numpy import pi, cos, sin
from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleParametric(cx, cy, R, color=QColor(0, 0, 0), draw=True):
    pts = []
    t = 1 / R
    da = 0

    while da <= pi / 4 + t:
        x = round(R * cos(da))
        y = round(R * sin(da))

        da += t

        if draw:
            pts.extend(AddSymmetricPointsCircle(cx, cy, cx + x, cy + y))

    if draw:
        pts.append(color)
        pts.append(False)
        return pts


def EllipseParametric(cx, cy, a, b, color=QColor(0, 0, 0), draw=True):
    pts = []
    t = 1 / a if a > b else 1 / b

    da = 0

    while da <= pi / 2 + t:
        x = round(a * cos(da))
        y = round(b * sin(da))

        da += t

        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, cx + x, cy + y))

    if draw:
        pts.append(color)
        pts.append(False)
        return pts
