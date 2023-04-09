from PyQt5.QtGui import QColor

def dda(x1, y1, x2, y2, color=QColor(0, 0, 0), stepmode=False):
    pts = []
    steps = 0

    if x2 == x1 and y2 == y1:
        return [(x1, y1, color), False]

    dx = x2 - x1
    dy = y2 - y1
    
    length = abs(dy)
    if abs(dx) >= abs(dy): 
        length = abs(dx) 

    dx /= length
    dy /= length

    xcur = x1
    ycur = y1

    i = 1
    while i <= length + 1:
        if not stepmode:
            pts.append((round(xcur), round(ycur), color))
        elif round(xcur + dx) != round(xcur) and round(ycur + dy) != round(ycur):
            steps += 1

        xcur += dx
        ycur += dy

        i += 1

    if stepmode:
        return steps
    
    pts.append(False)
    return pts
