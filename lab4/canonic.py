from numpy import sqrt
from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleCanonic(cx, cy, R, color=QColor(0, 0, 0), draw=True):
    pts = []

    R_sq = R * R
    edge = round(cx + R / sqrt(2))

    x = cx
    while x <= edge:
        y = cy + sqrt(R_sq - (x - cx) ** 2)

        if draw:
            pts.extend(AddSymmetricPointsCircle(cx, cy, x, y))
        x += 1

    if draw:
        pts.append(color)
        pts.append(False)
        return pts


def EllipseCanonic(cx, cy, a, b, color=QColor(0, 0, 0), draw=True):
    pts = []

    a_sq = a * a
    b_sq = b * b

    edge_x = round(cx + a / sqrt(1 + b_sq / a_sq))
    edge_y = round(cy + b / sqrt(1 + a_sq / b_sq))

    x = round(cx)
    while x <= edge_x:
        y = cy + sqrt(a_sq * b_sq - (x - cx) ** 2 * b_sq) / a

        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, x, y))
        x += 1

    y = round(cy)
    while y <= edge_y:
        x = cx + sqrt(a_sq * b_sq - (y - cy) ** 2 * a_sq) / b

        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, x, y))
        y += 1

    if draw:
        pts.append(color)
        pts.append(False)
        return pts
