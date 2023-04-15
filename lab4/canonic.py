from numpy import sqrt
from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleCanonicDraw(cx, cy, R, color=QColor(0, 0, 0)):
    pts = []

    R_sq = R * R
    edge = round(R / sqrt(2))

    x = 0
    while x <= edge:
        y = sqrt(R_sq - x ** 2)
        pts.extend(AddSymmetricPointsCircle(cx, cy, x + cx, y + cy))
        x += 1

    pts.append(color)
    pts.append(False)
    return pts
    
def CircleCanonicMeasure(R):
    R_sq = R * R
    edge = round(R / sqrt(2))

    x = 0
    while x <= edge:
        y = sqrt(R_sq - x ** 2)
        x += 1


def EllipseCanonicDraw(cx, cy, a, b, color=QColor(0, 0, 0)):
    pts = []

    a_sq = a * a
    b_sq = b * b

    edge_x = round(a / sqrt(1 + b_sq / a_sq))
    edge_y = round(b / sqrt(1 + a_sq / b_sq))

    x = 0
    while x <= edge_x:
        y = sqrt(a_sq * b_sq - x ** 2 * b_sq) / a
        pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))
        x += 1

    y = 0
    while y <= edge_y:
        x = sqrt(a_sq * b_sq - y ** 2 * a_sq) / b
        pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))
        y += 1

    pts.append(color)
    pts.append(False)
    return pts


def EllipseCanonicMeasure(a, b):

    a_sq = a * a
    b_sq = b * b

    edge_x = round(a / sqrt(1 + b_sq / a_sq))
    edge_y = round(b / sqrt(1 + a_sq / b_sq))

    x = 0
    while x <= edge_x:
        y = sqrt(a_sq * b_sq - x ** 2 * b_sq) / a
        x += 1

    y = 0
    while y <= edge_y:
        x = sqrt(a_sq * b_sq - y ** 2 * a_sq) / b
        y += 1
