def AddSymmetricPointsCircle(cx, cy, x, y):
    pts = []
    
    dx = x - cx
    dy = y - cy

    pts.append((x, y))
    pts.append((cx - dx, y))
    pts.append((x, cy - dy))
    pts.append((cx - dx, cy - dy))

    pts.append((cx + dy, cy + dx))
    pts.append((cx - dy, cy + dx))
    pts.append((cx + dy, cy - dx))
    pts.append((cx - dy, cy - dx))

    return pts


def AddSymmetricPointsEllipse(cx, cy, x, y):
    pts = []
    
    dx = x - cx
    dy = y - cy

    pts.append((cx + dx, cy + dy))
    pts.append((cx - dx, cy + dy))
    pts.append((cx + dx, cy - dy))
    pts.append((cx - dx, cy - dy))

    return pts

def CreateCircleSpectrum(cx, cy, rs, re, st, amt, hidden='amt'):
    pts = []
    if hidden == 'amt':
        _amt = int((re - rs) / st)
        for _ in range(_amt + 1):
            pts.append((cx, cy, rs))
            rs += st
    elif hidden == 'step':
        _st = int((re - rs) / amt)
        for _ in range(amt):
            pts.append((cx, cy, rs))
            rs += _st
    elif hidden == 'rend':
        for _ in range(amt):
            pts.append((cx, cy, rs))
            rs += st
    elif hidden == 'rstart':
        _rs = re - st * amt
        for _ in range(amt):
            pts.append((cx, cy, _rs))
            _rs += st
    
    return pts

def CreateEllipseSpectrum(cx, cy, astart, bstart, sta, stb, amt, hidden='stepa'):
    pts = []
    if hidden == 'stepa':
        for _ in range(amt):
            _sta = round(astart / bstart * stb)
            pts.append((cx, cy, astart + _sta, bstart + stb))
            astart += _sta
            bstart += stb
    elif hidden == 'stepb':
        for _ in range(amt):
            _stb = round(bstart / astart * sta) 
            pts.append((cx, cy, astart + sta, bstart + _stb))
            astart += sta
            bstart += _stb

    return pts
