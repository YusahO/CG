from PyQt5.QtGui import QColor

from numpy import floor, modf
from utils import get_intensity_gradient

def vu(x1, y1, x2, y2, color, bgColor, stepmode=False):
    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]
    
    pts = []

    I = 100
    gradient = get_intensity_gradient(color, bgColor, I)

    exchanged = abs(y2 - y1) > abs(x2 - x1)
    if exchanged:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    m = dy / dx if dx != 0 else 1

    xend = round(x1)
    yend = y1 + m * (xend - x1)
    # xpx1 = xend
    ycur = yend + m

    xend = int(x2 + .5)
    # xpx2 = xend

    steps = 0

    if not exchanged:
        for xcur in range(x1, x2):
            pts.append((xcur, int(ycur), gradient[round((I - 1) * (abs(1 - ycur + floor(ycur))))]))
            pts.append((xcur, int(ycur) + 1, gradient[round((I - 1) * (abs(1 - ycur + floor(ycur))))]))

            if stepmode and xcur < round(x2) and int(ycur) != int(ycur + m):
                steps += 1
                
            ycur += m
