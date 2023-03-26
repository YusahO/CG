from PyQt5.QtGui import QColor
from numpy import sign

from utils import get_intensity_gradient

def bresenham_float(x1, y1, x2, y2, color, stepmode=False):
    pts = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]

    dx, dy = x2 - x1,  y2 - y1
    sx, sy = sign(dx), sign(dy)
    dx, dy = abs(dx),  abs(dy)

    exchanged = 0
    if dy > dx:
        dx, dy = dy, dx
        exchanged = 1

    m = dy / dx
    error = m - .5

    xcur = x1
    ycur = y1

    xb = x1
    yb = y1
    steps = 0
    while xcur != x2 or ycur != y2:
        if not stepmode:
            pts.append((xcur, ycur, color))

        if error >= 0:
            if exchanged == 1:
                xcur += sx
            else:
                ycur += sy
            error -= 1

        if error <= 0:
            if exchanged == 1:
                ycur += sy
            else:
                xcur += sx
            error += m

        if stepmode:
            if xb != xcur and yb != ycur:
                steps += 1
            xb = xcur
            yb = ycur
    
    if stepmode:
        return steps
    
    return pts

def bresenham_integer(x1, y1, x2, y2, color, stepmode=False):
    pts = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]

    dx, dy = x2 - x1,  y2 - y1
    sx, sy = sign(dx), sign(dy)
    dx, dy = abs(dx),  abs(dy)

    exchanged = 0
    if dy > dx:
        dx, dy = dy, dx
        exchanged = 1

    error = 2 * dy - dx

    xcur = x1
    ycur = y1

    xb = x1
    yb = y1
    steps = 0
    while xcur != x2 or ycur != y2:
        if not stepmode:
            pts.append((xcur, ycur, color))

        if error >= 0:
            if exchanged == 1:
                xcur += sx
            else:
                ycur += sy
            error -= 2 * dx

        if error <= 0:
            if exchanged == 1:
                ycur += sy
            else:
                xcur += sx
            error += 2 * dy

        if stepmode:
            if xb != xcur and yb != ycur:
                steps += 1
            xb = xcur
            yb = ycur
    
    if stepmode:
        return steps
    
    return pts

def bresenham_aa(x1, y1, x2, y2, color, bgColor, stepmode=False):
    pts = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]
    
    I = 100
    gradient = get_intensity_gradient(color, bgColor, I)

    dx, dy = x2 - x1,  y2 - y1
    sx, sy = sign(dx), sign(dy)
    dx, dy = abs(dx),  abs(dy)

    exchanged = 0
    if dy > dx:
        dx, dy = dy, dx
        exchanged = 1

    m = dy / dx * I
    error = I / 2
    w = I - m

    xcur = x1
    ycur = y1

    xb = x1
    yb = y1 
    steps = 0
    while xcur != x2 or ycur != y2:
        if not stepmode:
            pts.append((xcur, ycur, gradient[round(error) - 1]))

        if error < w:
            if exchanged == 0:
                xcur += sx
            else:
                ycur += sy
            error += m
        
        elif error >= w:
            xcur += sx
            ycur += sy
            error -= w

        if stepmode:
            if xb != xcur and yb != ycur:
                steps += 1
            xb = xcur
            yb = ycur
    
    if stepmode:
        return steps
    
    return pts
