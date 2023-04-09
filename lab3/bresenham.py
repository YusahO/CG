from numpy import sign
from utils import get_intensity

def bresenham_float(x1, y1, x2, y2, color=(0, 0, 0), stepmode=False):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [[x1, y1, get_intensity(color, 255)], False]
    
    x = x1
    y = y1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    exchanged = False
    if dy > dx:
        exchanged = True
        dx, dy = dy, dx

    m = dy / dx
    error = m - 0.5

    xprev = x
    yprev = y

    pts = []
    steps = 0

    i = 0
    while i <= dx:
        if not stepmode:
            pts.append([x, y, get_intensity(color, 255)])

        if error >= 0:
            if exchanged:
                x += sx
            else:
                y += sy
            
            error -= 1
        
        if exchanged:
            y += sy
        else:
            x += sx

        error += m

        if stepmode:
            if xprev != x and yprev != y:
                steps += 1

            xprev = x
            yprev = y

        i += 1

    if stepmode:
        return steps
    
    pts.append(False)
    return pts


def bresenham_integer(x1, y1, x2, y2, color=(0, 0, 0), stepmode=False):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [[x1, y1, get_intensity(color, 255)], False]
    
    x = x1
    y = y1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    exchanged = False
    if dy > dx:
        exchanged = True
        dx, dy = dy, dx

    error = 2 * dy - dx

    xprev = x
    yprev = y

    pts = []
    steps = 0

    i = 0
    while i <= dx:
        if not stepmode:
            pts.append((x, y, get_intensity(color, 255)))

        if error >= 0:
            if exchanged:
                x += sx
            else:
                y += sy
            
            error -= 2 * dx
        
        if exchanged:
            y += sy
        else:
            x += sx

        error += 2 * dy

        if stepmode:
            if xprev != x and yprev != y:
                steps += 1

            xprev = x
            yprev = y

        i += 1

    if stepmode:
        return steps
    
    pts.append(False)
    return pts

def bresenham_aa(x1, y1, x2, y2, color=(0,0,0), intensity=255, stepmode=False):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [[x1, y1, get_intensity(color, 255)], False]
    
    x = x1
    y = y1

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    exchanged = False
    if dy > dx:
        exchanged = True
        dx, dy = dy, dx

    m = dy / dx
    w = 1 - m
    error = 0.5

    pts = []

    xprev = x
    yprev = y

    i = 0
    steps = 0

    while i <= dx:
        if not stepmode:
            pts.append([x, y, get_intensity(color, round(intensity * error))])

        if error < w:
            if exchanged:
                y += sy
            else:
                x += sx
            error += m
            
        else:
            x += sx
            y += sy

            error -= w

        if stepmode:
            if xprev != x and yprev != y:
                steps += 1

            xprev = x
            yprev = y

        i += 1

    if stepmode:
        return steps
    
    pts.append(False)
    return pts
