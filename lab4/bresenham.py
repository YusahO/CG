from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleBresenhamDraw(cx, cy, R, color=QColor(0, 0, 0)):
    pts = []
    x = 0
    y = R

    D = 2 * (1 - R)

    while x <= y:
        pts.extend(AddSymmetricPointsCircle(cx, cy, x + cx, y + cy))
        x += 1
        if D < 0 and 2 * D + 2 * y - 1 < 0:
            D += 2 * x + 1
        else:
            y -= 1
            D += 2 * (x - y + 1)
        
    pts.append(color)
    pts.append(False)
    return pts

def CircleBresenhamMeasure(R):
    x = 0
    y = R
    D = 2 * (1 - R)

    while x <= y:
        x += 1
        if D < 0 and 2 * D + 2 * y - 1 < 0:
            D += 2 * x + 1
        else:
            y -= 1
            D += 2 * (x - y + 1)


def EllipseBresenhamDraw(cx, cy, a, b, color=QColor(0, 0, 0)):
    pts = []
    x = 0
    y = b

    a_sq = a * a
    b_sq = b * b

    D = b_sq - a_sq * (2 * b + 1)

    while y >= 0:
        pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))
        
        if D < 0:
            d1 = 2 * D + a_sq * (2 * y + 2)
            if d1 < 0:
                x += 1
                D += b_sq * (2 * x + 1)
            else:
                x += 1
                y -= 1
                D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
        elif D > 0:
            d2 = 2 * D + b_sq * (2 - 2 * x)
            if d2 < 0:
                x += 1
                y -= 1
                D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
            else:
                y -= 1
                D += a_sq * (1 - 2 * y)
        else:
            x += 1
            y -= 1
            D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
     
    pts.append(color)
    pts.append(False)
    return pts

def EllipseBresenhamMeasure(a, b):
    x = 0
    y = b

    a_sq = a * a
    b_sq = b * b

    D = b_sq - a_sq * (2 * b + 1)

    while y >= 0:
        if D < 0:
            d1 = 2 * D + a_sq * (2 * y + 2)
            if d1 < 0:
                x += 1
                D += b_sq * (2 * x + 1)
            else:
                x += 1
                y -= 1
                D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
        elif D > 0:
            d2 = 2 * D + b_sq * (2 - 2 * x)
            if d2 < 0:
                x += 1
                y -= 1
                D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
            else:
                y -= 1
                D += a_sq * (1 - 2 * y)
        else:
            x += 1
            y -= 1
            D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
