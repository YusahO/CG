from utils import get_intensity

def dda(x1, y1, x2, y2, color=(0, 0, 0), stepmode=False):

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color], False]

    dx = x2 - x1
    dy = y2 - y1
    
    length = max(abs(dx), abs(dy))

    dx /= length
    dy /= length

    x = x1
    y = y1

    pts = [[x, y, color]]

    i = 1
    steps = 0

    while i <= length:

        if stepmode:
            xprev = x
            yprev = y

        x += dx
        y += dy

        if not stepmode:
            pts.append([int(round(x)), int(round(y)), color])
        elif (round(xprev) != round(x) and round(yprev) != round(y)):
            steps += 1

        i += 1

    if stepmode:
        return steps
    
    pts.append(False)
    return pts
    
