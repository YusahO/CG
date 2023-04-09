from utils import get_intensity

def fract(val):
    return val - int(val)

def vu(x1, y1, x2, y2, color=(0,0,0), intensity=255, stepmode=False):
    if x1 == x2 and y1 == y2:
        return [(x1, y1, color), False]
    
    pts = []

    dx = x2 - x1
    dy = y2 - y1

    steps = 0

    step = 1

    if abs(dy) >= abs(dx):
        m = dx / dy if dy != 0 else 1
        ms = m
        if y2 < y1:
            ms *= -1
            step *= -1

        for ycur in range(round(y1), round(y2), step):
            a1 = round(intensity - fract(x1) * intensity)
            a2 = intensity - a1

            pts.append((int(x1),     ycur, get_intensity(color, a1)))
            pts.append((int(x1) + 1, ycur, get_intensity(color, a2)))

            if stepmode and ycur < round(y2) and int(x1) != int(x1 + m):
                steps += 1
                
            x1 += m
    else:
        m = dy / dx if dx != 0 else 1
        ms = m
        if x2 < x1:
            ms *= -1
            step *= -1

        for xcur in range(round(x1), round(x2), step):
            a1 = round(intensity - fract(y1) * intensity)
            a2 = intensity - a1

            pts.append((xcur, int(y1),     get_intensity(color, a1)))
            pts.append((xcur, int(y1) + 1, get_intensity(color, a2)))

            if stepmode and xcur < round(x2) and int(y1) != int(y1 + m):
                steps += 1
                
            y1 += m

    if stepmode:
        return steps
    
    pts.append(False)
    return pts
