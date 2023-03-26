from PyQt5.QtGui import QColor

from numpy import sin, cos, pi

def get_intensity_gradient(color: QColor, bgColor: QColor, intensity: int):
    gradient = []

    r1, g1, b1 = color.red(), color.green(), color.blue()
    r2, g2, b2 = bgColor.red(), bgColor.green(), bgColor.blue()

    rstep = float(r2 - r1) / intensity
    gstep = float(g2 - g1) / intensity
    bstep = float(b2 - b1) / intensity

    for i in range(intensity):
        nr = int(r1 + rstep * i)
        ng = int(g1 + gstep * i)
        nb = int(b1 + bstep * i)

        gradient.append((nr, ng, nb))
    gradient.reverse()
    
    return gradient

def generate_spectrum(center: tuple, angle: float, length: float):
    a = 0
    angle = angle * pi / 180
    pts = []
    while a <= 2 * pi:
        pts.append((*center, center[0] + round(length * cos(a)), center[1] + round(length * sin(a))))
        a += angle
    
    return pts
