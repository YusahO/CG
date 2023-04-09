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
            pts.append((cx, cy, rs + st))
            rs += st
    elif hidden == 'step':
        _st = int((re - rs) / amt)
        for _ in range(amt):
            pts.append((cx, cy, rs + _st))
            rs += _st
    elif hidden == 'rend':
        for _ in range(amt):
            pts.append((cx, cy, rs + st))
            rs += st
    elif hidden == 'rstart':
        _rs = re - st * amt
        for _ in range(amt):
            pts.append((cx, cy, _rs + st))
            _rs += st
    
    return pts

def CreateEllipseSpectrum(cx, cy, astart, bstart, aend, bend, st, amt, hidden='amt'):
    pts = []
    if hidden == 'amt':
        _amt = int((aend - astart) / st)
        for _ in range(_amt + 1):
            pts.append((cx, cy, astart + st, bstart + st))
            astart += st
            bstart += st
    elif hidden == 'step':
        _st = int((aend - astart) / st)
        for _ in range(amt):
            pts.append((cx, cy, astart + _st, bstart + _st))
            astart += _st
            bstart += _st
    elif hidden == 'rend':
        for _ in range(amt):
            pts.append((cx, cy, astart + st, bstart + st))
            rs += st
    elif hidden == 'rstart':
        _astart = aend - st * amt
        _bstart = bend - st * amt
        for _ in range(amt):
            pts.append((cx, cy, _astart + st, _bstart + st))
            rs += st
    
    return pts
