from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from PyQt5.QtGui import QColor

def CircleBresenham(cx, cy, R, color=QColor(0, 0, 0), draw=True):
    pts = []
    x = 0
    y = R
    D = 2 * (1 - R)

    algCase = 1
    while x <= y:
        if draw:
            pts.extend(AddSymmetricPointsCircle(cx, cy, x + cx, y + cy))

        if D < 0:
            d1 = 2 * D + 2 * y - 1
            if d1 < 0:
                algCase = 1
            else:
                algCase = 2
        elif D > 0:
            d2 = 2 * D - 2 * x - 1
            if d2 < 0:
                algCase = 2
            else:
                algCase = 3
        else:
            algCase = 2
        
        match algCase:
            case 1:
                x += 1
                D += 2 * x + 1
            case 2:
                x += 1
                y -= 1
                D += 2 * (x - y + 1)
            case 3:
                y -= 1
                D -= 2 * y + 1

    if draw:
        pts.append(color)
        pts.append(False)
        return pts


def EllipseBresenham(cx, cy, a, b, color=QColor(0, 0, 0), draw=True):
    pts = []
    x = 0
    y = b

    a_sq = a * a
    b_sq = b * b

    D = b_sq - a_sq * (2 * b + 1)

    algCase = 1
    while y >= 0:

        if draw:
            pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))
        
        if D < 0:
            d1 = 2 * D + a_sq * (2 * y + 2)
            if d1 < 0:
                algCase = 1
            else:
                algCase = 2
        elif D > 0:
            d2 = 2 * D + b_sq * (2 - 2 * x)
            if d2 < 0:
                algCase = 2
            else:
                algCase = 3
        else:
            algCase = 2     

        match algCase:
            case 1:
                x += 1
                D += b_sq * (2 * x + 1)
            case 2:
                x += 1
                y -= 1
                D += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
            case 3:
                y -= 1
                D += a_sq * (1 - 2 * y)
     
    if draw:
        pts.append(color)
        pts.append(False)
        return pts
