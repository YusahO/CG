from PyQt5.QtGui import QColor

def dda(x1, y1, x2, y2, color=QColor(0, 0, 0), stepmode=False):
    pts = []
    steps = 0

    if x1 == x2 and y1 == y2:
        return [(x1, y1, color)]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    length = dx if dx >= dy else dy

    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    xcur, ycur = x1, y1

    for _ in range(int(length) + 1):
        if not stepmode:
            pts.append((round(xcur), round(ycur), color))
        elif round(xcur + dx) != round(xcur) and round(ycur + dy) != round(ycur):
            steps += 1

        xcur += dx
        ycur += dy

    if stepmode:
        return steps
    return pts
