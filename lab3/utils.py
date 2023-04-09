from PyQt5.QtGui import QColor

from numpy import sin, cos, pi

def generate_spectrum(center: tuple, angle: float, length: float):
    a = 0
    angle = angle * pi / 180
    pts = []
    while a < 2 * pi:
        pts.append((*center, center[0] + round(length * cos(a)), center[1] + round(length * sin(a))))
        a += angle
        
    return pts

def remap(min1, max1, min2, max2, val):
    return min2 + (val - min1) * (max2 - min2) / (max1 - min1)
