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

def get_intensity(color, intensity):
    return [*color, intensity]
