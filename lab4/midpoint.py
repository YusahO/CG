from utils import AddSymmetricPointsCircle, AddSymmetricPointsEllipse
from numpy import sqrt
from PyQt5.QtGui import QColor


def CircleMidpointDraw(cx, cy, R, color=QColor(0, 0, 0)):
    pts = []

    x = 0
    y = R

    p = 1 - R
    while x <= y:
        pts.extend(AddSymmetricPointsCircle(cx, cy, x + cx, y + cy))

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x + 1 - 2 * y

    pts.append(color)
    pts.append(False)
    return pts


def CircleMidpointMeasure(R):

    x = 0
    y = R

    p = 1 - R
    while x <= y:

        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x + 1 - 2 * y


def EllipseMidpointDraw(cx, cy, a, b, color=QColor(0, 0, 0)):
    pts = []

    a_sq = a * a
    b_sq = b * b

    x = 0
    y = b

    p = b_sq - round(a_sq * (b - 0.25))
    end = round(a / sqrt(1 + b_sq / a_sq))
    while x <= end:
        pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))

        x += 1
        if p < 0:
            p += b_sq * (2 * x + 1)
        else:
            y -= 1
            p += b_sq * (2 * x + 1) - a_sq * 2 * y

    x = a
    y = 0

    p = a_sq - round(b_sq * (a - 0.25))
    end = round(b / sqrt(1 + a_sq / b_sq))
    while y <= end:
        pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))

        y += 1
        if p < 0:
            p += a_sq * (2 * y + 1)
        else:
            x -= 1
            p += a_sq * (2 * y + 1) - b_sq * 2 * x

    pts.append(color)
    pts.append(False)
    return pts


def EllipseMidpointMeasure(a, b):

    a_sq = a * a
    b_sq = b * b

    x = 0
    y = b

    p = b_sq - round(a_sq * (b - 0.25))
    end = round(a / sqrt(1 + b_sq / a_sq))
    while x <= end:
        x += 1
        if p < 0:
            p += b_sq * (2 * x + 1)
        else:
            y -= 1
            p += b_sq * (2 * x + 1) - a_sq * 2 * y

    x = a
    y = 0

    p = a_sq - round(b_sq * (a - 0.25))
    end = round(b / sqrt(1 + a_sq / b_sq))
    while y <= end:
        y += 1
        if p < 0:
            p += a_sq * (2 * y + 1)
        else:
            x -= 1
            p += a_sq * (2 * y + 1) - b_sq * 2 * x


# def EllipseMidpointDraw(cx, cy, a, b, color=QColor(0, 0, 0)):
#     pts = []

#     a_sq = a * a
#     b_sq = b * b

#     x = 0
#     y = b

#     p = b_sq - round((a_sq * (b - 0.25)))
#     end = round(a / sqrt(1 + b_sq / a_sq))
#     while x <= end:
#         pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))

#         x += 1
#         if p < 0:
#             p += b_sq * (2 * x + 1)
#         else:
#             y -= 1
#             p += b_sq * (2 * x + 1) - a_sq * 2 * y

#     p += 0.75 * (a_sq + b_sq) - (a_sq * y + b_sq * x)

#     while y >= 0:
#         pts.extend(AddSymmetricPointsEllipse(cx, cy, x + cx, y + cy))

#         y -= 1
#         if p <= 0:
#             p += 2 * a_sq * y + a_sq
#         else:
#             x += 1
#             p += a_sq * 2 * y + a_sq - b_sq * 2 * x

#     pts.append(color)
#     pts.append(False)
#     return pts


# def EllipseMidpointMeasure(a, b):

#     a_sq = a * a
#     b_sq = b * b

#     x = 0
#     y = b

#     p = b_sq - a_sq * b + 0.25 * a_sq
#     end = a / sqrt(1 + b_sq / a_sq)

#     while x <= end:
#         x += 1
#         if p < 0:
#             p += b_sq * (2 * x + 1)
#         else:
#             y -= 1
#             p += b_sq * (2 * x + 1) - a_sq * 2 * y

#     p += 0.75 * (a_sq + b_sq) - (a_sq * y + b_sq * x)

#     while y >= 0:
#         y -= 1
#         if p <= 0:
#             p += 2 * a_sq * y + a_sq
#         else:
#             x += 1
#             p += a_sq * 2 * y + a_sq - b_sq * 2 * x
