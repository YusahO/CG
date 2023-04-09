from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from numpy import sqrt
from PyQt5.QtGui import QColor

def CircleMidpoint(cx, cy, R, color=QColor(0, 0, 0), draw=True):
    pts = []

    x = 0
    y = R

    p = 1 - R
    while x <= y:
        if draw:
            pts.extend(AddSymmetricPointsCircle(cx, cy, x + cx, y + cy))
        
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x + 1 - 2 * y

    if draw:
        pts.append(color)
        pts.append(False)
        return pts


def EllipseMidpoint(cx, cy, a, b, color=QColor(0, 0, 0), draw=True):
    pts = []

    a_sq = a * a
    b_sq = b * b

    x = 0
    y = b

    p = b_sq - round(a_sq * (b - 0.25))
    end = round(a / sqrt(1 + b_sq / a_sq))
    while x <= end:
        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))
        
        x += 1
        if p < 0:
            p += b_sq * (2 * x + 1)
        else:
            y -= 1
            p += b_sq * (2 * x + 1) - a_sq * 2 * y
    
    x = a
    y = 0

    p = a_sq - round(b_sq * (a - 0.25))
    end = round(b / sqrt(1 + a_sq / b_sq))
    while y <= end:
        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))

        y += 1
        if p < 0:
            p += a_sq * (2 * y + 1)
        else:
            x -= 1
            p += a_sq * (2 * y + 1) - b_sq * 2 * x

    if draw:
        pts.append(color)
        pts.append(False)
        return pts
