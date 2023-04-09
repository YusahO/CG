from PyQt5.QtGui import QColor
from numpy import sign

from utils import remap

def bresenham_float(x1, y1, x2, y2, color = QColor(0,0,0), stepmode=False):
    pts = []

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [(x1, y1, color), False]

    sx, sy = sign(dx), sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    exchanged = False
    if dy > dx:
        dx, dy = dy, dx
        exchanged = True

    m = dy / dx
    error = m - .5

    xcur = x1
    ycur = y1

    xprev = x1
    yprev = y1

    steps = 0
    i = 0
    while i <= dx:
        if not stepmode:
            pts.append((xcur, ycur, color))

        if error >= 0:
            if exchanged:
                xcur += sx
            else:
                ycur += sy
            error -= 1

        if exchanged:
            ycur += sy
        else:
            xcur += sx
        error += m

        if stepmode:
            if xprev != xcur and yprev != ycur:
                steps += 1
            xprev = xcur
            yprev = ycur
        
        i += 1
    
    if stepmode:
        return steps
    
    pts.append(False)
    return pts

def bresenham_integer(x1, y1, x2, y2, color = QColor(0,0,0), stepmode=False):
    pts = []

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [(x1, y1, color), False]

    sx, sy = sign(dx), sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    exchanged = False
    if dy > dx:
        dx, dy = dy, dx
        exchanged = True

    error = 2 * dy - dx

    xcur = x1
    ycur = y1

    xprev = x1
    yprev = y1
    steps = 0

    i = 0
    while i <= dx:
        if not stepmode:
            pts.append((xcur, ycur, color))

        if error >= 0:
            if exchanged:
                xcur += sx
            else:
                ycur += sy
            error -= 2 * dx

        if exchanged:
            ycur += sy
        else:
            xcur += sx
        error += 2 * dy

        if stepmode:
            if xprev != xcur and yprev != ycur:
                steps += 1
            xprev = xcur
            yprev = ycur

        i += 1
    
    if stepmode:
        return steps
    
    pts.append(False)
    return pts

def bresenham_aa(x1, y1, x2, y2, color = QColor(0,0,0), intensity=100, stepmode=False):
    pts = []

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [(x1, y1, QColor(color.red(), color.green(), color.blue(), 255)), False]

    sx, sy = sign(dx), sign(dy)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    exchanged = False
    if dy > dx:
        dx, dy = dy, dx
        exchanged = True

    m = dy / dx
    error = .5
    w = 1 - m

    xcur = x1
    ycur = y1

    xprev = x1
    yprev = y1 
    steps = 0

    i = 0
    while i <= dx:
        if not stepmode:
            a = error * intensity
            pts.append((xcur, ycur, QColor(color.red(), color.green(), color.blue(), round(remap(0, intensity, 0, 255, a)))))

        if error < w:
            if exchanged == 0:
                xcur += sx
            else:
                ycur += sy
            error += m
        
        else:
            xcur += sx
            ycur += sy

            error -= w

        if stepmode:
            if xprev != xcur and yprev != ycur:
                steps += 1
            xprev = xcur
            yprev = ycur
        
        i += 1
    
    if stepmode:
        return steps

    pts.append(False)
    return pts
