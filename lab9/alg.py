from copy import deepcopy
from numpy import matrix

def make_uniq(sections):
    for section in sections:
        section.sort()
    return list(filter(lambda x: (sections.count(x) % 2) == 1, sections))


def point_in_section(point, section):
    if abs(CrossProd(GetVector(point, section[0]), GetVector(*section))) <= 1e-6:
        if (section[0] < point < section[1] or section[1] < point < section[0]):
            return True
    return False


def get_sections(section, rest_points):
    points_list = [section[0], section[1]]
    for p in rest_points:
        if point_in_section(p, section):
            points_list.append(p)

    points_list.sort()

    sections_list = list()
    for i in range(len(points_list) - 1):
        sections_list.append([points_list[i], points_list[i + 1]])

    return sections_list


def get_uniq_sections(figure):
    all_sections = list()
    rest_points = figure[2:]
    for i in range(len(figure)):
        cur_section = [figure[i], figure[(i + 1) % len(figure)]]

        all_sections.extend(get_sections(cur_section, rest_points))

        rest_points.pop(0)
        rest_points.append(figure[i])

    return make_uniq(all_sections)


def CrossProd(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def DotProd(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def GetVector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]


def CheckPoly(vertices):
    if len(vertices) < 3:
        return False

    sgn = 1 if CrossProd(GetVector(vertices[1], vertices[2]),
                         GetVector(vertices[0], vertices[1])) > 0 else -1

    for i in range(3, len(vertices)):
        if sgn * CrossProd(GetVector(vertices[i - 1], vertices[i]),
                           GetVector(vertices[i - 2], vertices[i - 1])) < 0:
            return False

    if sgn * CrossProd(GetVector(vertices[-1], vertices[0]),
                       GetVector(vertices[-2], vertices[-1])) < 0:
        return False

    if sgn < 0:
        vertices.reverse()

    return True


def GetNormal(p1, p2, cp):
    vector = GetVector(p1, p2)
    normal = [1, 0] if vector[0] == 0 else [-vector[1] / vector[0], 1]

    if DotProd(GetVector(p2, cp), normal) < 0:
        for i in range(len(normal)):
            normal[i] = -normal[i]

    return normal


def GetNormals(vertices):
    normals = []
    size = len(vertices)
    for i in range(size):
        normals.append(GetNormal(vertices[i], vertices[(i + 1) % size], vertices[(i + 2) % size]))

    return normals


def CheckPoint(point, p1, p2):
    return True if CrossProd(GetVector(p1, p2), GetVector(p1, point)) <= 0 else False


def GetIntersection(edge, cutter):
    begin1, end1 = edge
    begin2, end2 = cutter

    coef = []
    coef.append([end1[0] - begin1[0], begin2[0] - end2[0]])
    coef.append([end1[1] - begin1[1], begin2[1] - end2[1]])

    rights = []
    rights.append([begin2[0] - begin1[0]])
    rights.append([begin2[1] - begin1[1]])

    coef_tmp = matrix(coef)
    coef_tmp = coef_tmp.I
    coef = [[coef_tmp.item(0), coef_tmp.item(1)], [coef_tmp.item(2), coef_tmp.item(3)]]

    coef_tmp = matrix(coef)
    param = coef_tmp.__mul__(rights)

    x, y = begin1[0] + (end1[0] - begin1[0]) * param.item(0), begin1[1] + (end1[1] - begin1[1]) * param.item(0)

    return [x, y]


def EdgecutFigure(figure, edge, normal):
    res_figure = list()
    if len(figure) < 3:
        return []

    prev_check = CheckPoint(figure[0], *edge)

    for i in range(1, len(figure) + 1):
        cur_check = CheckPoint(figure[i % len(figure)], *edge)

        if prev_check:
            if cur_check:
                res_figure.append(figure[i % len(figure)])
            else:
                res_figure.append(GetIntersection(
                    [figure[i - 1], figure[i % len(figure)]], edge))

        else:
            if cur_check:
                res_figure.append(GetIntersection(
                    [figure[i - 1], figure[i % len(figure)]], edge))
                res_figure.append(figure[i % len(figure)])

        prev_check = cur_check

    return res_figure


def CutFigure(figure, cutter_vertices, normals):
    res_figure = deepcopy(figure)
    for i in range(len(cutter_vertices)):
        cur_edge = [cutter_vertices[i], cutter_vertices[(i + 1) % len(cutter_vertices)]]
        res_figure = EdgecutFigure(res_figure, cur_edge, normals[i])

        if len(res_figure) < 3:
            return []
    
    return res_figure
