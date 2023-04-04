from PyQt5.QtGui import QColor

def dda(x1, y1, x2, y2, color=QColor(0, 0, 0), stepmode=False):
    pts = []
    steps = 0

    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    length = dy
    if dx >= dy:
        length = dx

    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    xcur = x1
    ycur = y1

    i = 1
    while i <= int(length):
        if not stepmode:
            pts.append((round(xcur), round(ycur), color))
        elif round(xcur + dx) != round(xcur) and round(ycur + dy) != round(ycur):
            steps += 1

        xcur += dx
        ycur += dy

        i += 1

    if stepmode:
        return steps
    return pts
