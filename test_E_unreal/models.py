'''import math
from enum import Enum

from PIL import Image, ImageDraw


class Form(Enum):
    RECTANGLE = 0  # rechteck
    TRIANGLE = 1  # dreieck
    CIRCLE = 2  # kreis
    TRAPEZOID = 3  # trapez


class Rect:
    def __init__(self, x, y, x0, y0, r_angle, t):
        """
        putting the input data in a readable class
        :param x: the x coordinate of start of the form
        :param y: the y coordinate of start of the form
        :param x0: the x coordinate of end of the form
        :param y0: the y coordinate of end of the form
        :param r_angle: the rotation angle, defined in °
        :param t: the form type

        Data about position, size, rotation, form

        """

        self.x = x
        self.y = y
        self.x0 = x0
        self.y0 = y0
        self.height = abs(y0 - y)
        self.width = abs(x0 - x)
        self.rotation_angle = r_angle
        self.form = Form(t)
        e = [rotated_about(x, y, abs(self.x0 - self.x) / 2 + self.x, abs(self.y0 - self.y) / 2 + self.y,
                           math.radians(self.rotation_angle)) for x, y in
             ((self.x, self.y), (self.x0, self.y), (self.x0, self.y0), (self.x, self.y0))]
        e0 = sorted([e[0][0], e[2][0]])
        e1 = sorted([e[1][1], e[3][1]])
        self.min_x = e0[0]
        self.max_x = e0[-1]
        self.min_y = e1[0]
        self.max_y = e1[-1]
        print(self.min_x)
        print(self.max_x)
        print(self.min_y)
        print("-")


def distance(ax, ay, bx, by):
    return math.sqrt((by - ay) ** 2 + (bx - ax) ** 2)


def rotated_about(ax, ay, bx, by, angle):
    radius = distance(ax, ay, bx, by)
    angle += math.atan2(ay - by, ax - bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )


"""
algorithm creates similar structures by adding other forms to a base figure
"""


class Figure:
    def __init__(self, rectangles: list):
        self.rectangles = rectangles

    def to_img(self, name):
        """
        :param name: name of the file (without file ending tag)
        :return: nothing
        """
        im = Image.new('RGB', (500, 500), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for rect in self.rectangles:
            if rect.form == Form.RECTANGLE:
                square_center = (abs(rect.x0 - rect.x) / 2 + rect.x, abs(rect.y0 - rect.y) / 2 + rect.y)
                square_length_y = abs(rect.y0 - rect.y)
                square_length = abs(rect.x0 - rect.x)

                square_vertices = (
                    (square_center[0] + square_length / 2, square_center[1] + square_length_y / 2),
                    (square_center[0] + square_length_y / 2, square_center[1] - square_length / 2),
                    (square_center[0] - square_length / 2, square_center[1] - square_length_y / 2),
                    (square_center[0] - square_length_y / 2, square_center[1] + square_length / 2)
                )

                square_vertices = [
                    rotated_about(x, y, square_center[0], square_center[1], math.radians(rect.rotation_angle)) for x, y
                    in
                    square_vertices]

                draw.polygon(square_vertices,
                             fill=(255, 255, 255), outline=(0, 0, 0))
            elif rect.form == Form.CIRCLE:
                draw.ellipse((rect.x, rect.y, rect.x0, rect.y0), fill=(255, 255, 255), outline=(0, 0, 0))
            elif rect.form == Form.TRIANGLE:

                square_center = (abs(rect.x0 - rect.x) / 2 + rect.x, abs(rect.y0 - rect.y) / 2 + rect.y)

                square_vertices = (
                    (rect.x, rect.y),
                    (rect.x0, rect.y),
                    (rect.x0, rect.y0),
                )

                square_vertices = [
                    rotated_about(x, y, square_center[0], square_center[1], math.radians(rect.rotation_angle)) for x, y
                    in
                    square_vertices]
                draw.polygon(square_vertices,
                             fill=(255, 255, 255), outline=(0, 0, 0))
            elif rect.form == Form.TRAPEZOID:
                square_center = (abs(rect.x0 - rect.x) / 2 + rect.x, abs(rect.y0 - rect.y) / 2 + rect.y)

                square_vertices = (
                    (rect.x, rect.y),
                    (rect.x0, rect.y),
                    (rect.x0 - 10, rect.y0),
                    (rect.x + 10, rect.y0)
                )

                square_vertices = [
                    rotated_about(x, y, square_center[0], square_center[1], math.radians(rect.rotation_angle)) for x, y
                    in
                    square_vertices]

                draw.polygon(square_vertices,
                             fill=(255, 255, 255), outline=(0, 0, 0))

        im.save(name + '.jpg', quality=95)

    def calculate_outline(self):
        """
        calculation is not exact, elements outlines are rounded to 1
        :return: the list of outline points
        """

        points = []

        """min_x, min_y, max_x, max_y = [], [], [], []
        for x in self.rectangles:
            min_x.append(x.x)
            min_y.append(x.y)
            max_x.append(x.x0)
            max_y.append(x.y0)
        min_x = list(sorted(min_x))
        min_y = list(sorted(min_y))
        max_x = reversed(sorted(max_x))
        max_y = reversed(sorted(max_y))"""

        for xx in range(0, 2):
            height_x = {}
            point0 = []

            for rect in self.rectangles:
                if xx == 0:
                    a = list((rect.min_x, rect.min_y))
                    b = list((rect.max_x, rect.max_y))
                else:
                    a = list((rect.min_y, rect.min_x))
                    b = list((rect.max_y, rect.max_x))
                print(a)
                print(b)
                print(height_x)
                print(".")

                if len(height_x) > 0:
                    """for k in sorted(height_x.keys()):
                        if k >= rect.min_y:
                            lt = height_x[k]
                            v = 0
                            for a0, b0 in lt:
                                if a[0] >= a0 and b[0] <= b0:
                                    lt[v] = (a0, a[0])
                                    lt.append((b[0], b0))

                                v += 1
                            height_x[k] = lt"""
                    if height_x.keys().__contains__(a[1]):
                        lt = height_x[a[1]]
                        k = 0
                        inserted = False
                        for a0, b0 in lt:
                            print(lt)
                            if a[0] <= a0 < b[0] <= b0:
                                lt[k] = (a[0], b0)
                                k += 1
                                continue
                            elif a0 < a[0] < b0 < b[0]:
                                lt[k] = (a0, b[0])
                                k += 1
                                continue
                            elif a[0] <= a0 and b[0] > b0:
                                lt[k] = (a[0], b[0])
                                k += 1
                                continue
                            elif a[0] > b0 or b[0] < a0 and not inserted:
                                print("x" + str(a[0]) + "/" + str(b0))
                                lt.insert(k, (a[0], b[0]))
                                inserted = True
                            else:
                                inserted = False
                            k += 1

                        height_x[a[1]] = lt
                    else:
                        height_x[a[1]] = [(a[0], b[0])]
                else:
                    height_x[a[1]] = [(a[0], b[0])]
            print("items_" + str(height_x))
            km = 0
            m = 500
            hm = 0
            for k, v in height_x.items():
                if v[0][0] < m:
                    m = v[0][0]
                    km = k
                    hm = v[0][1]
            start_point = height_x[km][0] + (km,)
            point0.append(start_point)
            height_x[km].pop(0)

            # end point ?

            kmx = 0
            hx = 0
            last = hx
            for k, v in height_x.items():
                last = hx
                if len(v) == 0:
                    continue
                if v[-1][-1] > hx:
                    kmx = k
                    hx = v[-1][0]
            end_point = height_x[kmx][-1] + (kmx,)
            # points.append(start_point)
            height_x[kmx].pop(-1)

            while last >= hm:
                print("iter")
                may = []
                for k, v in height_x.items():
                    if len(v) == 0:
                        continue
                    if v[0][0] <= hm:
                        may.append((v[0][1], k))
                if len(may) == 0:
                    print(hm)
                    print("Problem")
                    print(point0)
                    return
                else:
                    xt = 500
                    for r, t in may:
                        if t < xt:
                            xt = t
                    start_point = height_x[xt][0] + (xt,)
                    hm = start_point[1]
                    point0.append(start_point)
                    height_x[xt].pop(0)
            point0.append(end_point)
            points.extend(point0)

            lengths = []
            pos = 0

            for i in range(0, len(point0)):
                p = point0[i]
                """if i + 1 < len(point0):
                    p0 = point0[i + 1]
                    lengths.append(p0[0] - p[0])
                else:"""
                """if pos >= p[1]:
                    continue"""
                x = p[0]
                if i > 0 and p[2] < point0[i-1][2] and x < pos:
                    print("?")
                    lengths[-1] -= p[1] - p[0] - (p[1] - pos)
                elif x < pos:
                    x = pos
                pos = p[1]
                lengths.append(p[1] - x)
            print(point0)
            print("l"+str(lengths))

        """---"""

        height_x = {}
        point0 = []

        for rect in self.rectangles:
            if 0 == 0:
                a = list((rect.min_x, rect.max_y))
                b = list((rect.max_x, rect.min_y))
            print(a)
            print(b)
            print(height_x)
            print(".")

            if len(height_x) > 0:
                """for k in sorted(height_x.keys()):
                    if k >= rect.min_y:
                        lt = height_x[k]
                        v = 0
                        for a0, b0 in lt:
                            if a[0] >= a0 and b[0] <= b0:
                                lt[v] = (a0, a[0])
                                lt.append((b[0], b0))

                            v += 1
                        height_x[k] = lt"""
                if height_x.keys().__contains__(a[1]):
                    lt = height_x[a[1]]
                    k = 0
                    inserted = False
                    for a0, b0 in lt:
                        print(lt)
                        if a[0] <= a0 < b[0] <= b0:
                            lt[k] = (a[0], b0)
                            k += 1
                            continue
                        elif a0 < a[0] < b0 < b[0]:
                            lt[k] = (a0, b[0])
                            k += 1
                            continue
                        elif a[0] <= a0 and b[0] > b0:
                            lt[k] = (a[0], b[0])
                            k += 1
                            continue
                        elif a[0] > b0 or b[0] < a0 and not inserted:
                            print("x" + str(a[0]) + "/" + str(b0))
                            lt.insert(k, (a[0], b[0]))
                            inserted = True
                        else:
                            inserted = False
                        k += 1

                    height_x[a[1]] = lt
                else:
                    height_x[a[1]] = [(a[0], b[0])]
            else:
                height_x[a[1]] = [(a[0], b[0])]
        print("items_" + str(height_x))
        km = 0
        m = 500
        hm = 0
        for k, v in height_x.items():
            if v[0][0] < m:
                m = v[0][0]
                km = k
                hm = v[0][1]
        start_point = height_x[km][0] + (km,)
        point0.append(start_point)
        height_x[km].pop(0)

        # end point ?

        kmx = 0
        hx = 0
        last = hx
        for k, v in height_x.items():
            last = hx
            if len(v) == 0:
                continue
            if v[-1][-1] > hx:
                kmx = k
                hx = v[-1][0]
        end_point = height_x[kmx][-1] + (kmx,)
        # points.append(start_point)
        height_x[kmx].pop(-1)

        while last >= hm:
            print("iter")
            may = []
            for k, v in height_x.items():
                if len(v) == 0:
                    continue
                if v[0][0] <= hm:
                    may.append((v[0][1], k))
            if len(may) == 0:
                print(hm)
                print("Problem")
                print(point0)
                return
            else:
                xt = 0
                for r, t in may:
                    if t > xt:
                        xt = t
                start_point = height_x[xt][0] + (xt,)
                hm = start_point[1]
                point0.append(start_point)
                height_x[xt].pop(0)
        point0.append(end_point)
        points.extend(point0)

        lengths = []
        pos = 0

        for i in range(0, len(point0)):
            p = point0[i]
            """if i + 1 < len(point0):
                p0 = point0[i + 1]
                lengths.append(p0[0] - p[0])
            else:"""
            x = p[0]
            print(pos)
            print(x)
            print("/")
            if i > 0 and p[2] > point0[i - 1][2] and x < pos:
                print("?")
                lengths[-1] -= p[1] - p[0] - (p[1] - pos)
            elif x < pos:
                x = pos
            pos = p[1]
            lengths.append(p[1] - x)
        print(point0)
        print("l" + str(lengths))

        """----"""

        height_x = {}
        point0 = []

        for rect in self.rectangles:
            if 0 == 0:
                a = list((rect.max_y, rect.min_x))
                b = list((rect.min_y, rect.max_x))
            print(a)
            print(b)
            print(height_x)
            print(".")

            if len(height_x) > 0:
                """for k in sorted(height_x.keys()):
                    if k >= rect.min_y:
                        lt = height_x[k]
                        v = 0
                        for a0, b0 in lt:
                            if a[0] >= a0 and b[0] <= b0:
                                lt[v] = (a0, a[0])
                                lt.append((b[0], b0))

                            v += 1
                        height_x[k] = lt"""
                if height_x.keys().__contains__(a[1]):
                    lt = height_x[a[1]]
                    k = 0
                    inserted = False
                    for a0, b0 in lt:
                        print(lt)
                        if a[0] <= a0 < b[0] <= b0:
                            lt[k] = (a[0], b0)
                            k += 1
                            continue
                        elif a0 < a[0] < b0 < b[0]:
                            lt[k] = (a0, b[0])
                            k += 1
                            continue
                        elif a[0] <= a0 and b[0] > b0:
                            lt[k] = (a[0], b[0])
                            k += 1
                            continue
                        elif a[0] > b0 or b[0] < a0 and not inserted:
                            print("x" + str(a[0]) + "/" + str(b0))
                            lt.insert(k, (a[0], b[0]))
                            inserted = True
                        else:
                            inserted = False
                        k += 1

                    height_x[a[1]] = lt
                else:
                    height_x[a[1]] = [(a[0], b[0])]
            else:
                height_x[a[1]] = [(a[0], b[0])]
        print("items_" + str(height_x))
        km = 0
        m = 500
        hm = 0
        for k, v in height_x.items():
            if v[0][0] < m:
                m = v[0][0]
                km = k
                hm = v[0][1]
        start_point = height_x[km][0] + (km,)
        point0.append(start_point)
        height_x[km].pop(0)
        # end point ?

        kmx = 0
        hx = 0
        last = hx
        for k, v in height_x.items():
            last = hx
            if len(v) == 0:
                continue
            if v[-1][-1] > hx:
                kmx = k
                hx = v[-1][0]
        end_point = height_x[kmx][-1] + (kmx,)
        # points.append(start_point)
        height_x[kmx].pop(-1)

        while last >= hm:
            print("iter")
            may = []
            for k, v in height_x.items():
                if len(v) == 0:
                    continue
                if v[0][1] > hm:
                    may.append((v[0][0], k))
            if len(may) == 0:
                print(hm)
                print("Problem")
                print(point0)
                return
            else:
                xt = 500
                for r, t in may:
                    if t < xt:
                        xt = t
                start_point = height_x[xt][0] + (xt,)
                hm = start_point[0]
                point0.append(start_point)
                height_x[xt].pop(0)
        point0.append(end_point)
        points.extend(point0)

        lengths = []
        pos = 0

        """sort = []
        for p0 in point0:
            if len(sort) > 0:
                c = 0
                for s in sort:
                    if s[1] >= p0[1]:
                        sort.insert(c, p0)
                        c = -1
                        break
                    c += 1
                if c != -1:
                    sort.append(p0)
            else:
                sort.append(p0)"""
        for i in range(0, len(point0)):
            p = point0[i]
            """if i + 1 < len(point0):
                p0 = point0[i + 1]
                lengths.append(p0[0] - p[0])
            else:"""
            x = p[0]
            print(pos)
            print(x)
            print("/")

            if i > 0 and p[2] > point0[i - 1][2] and x < pos:
                print("?")
                lengths[-1] -= p[0] - p[1] - (pos - p[1])
            elif x < pos:
                x = pos
            pos = p[1]
            lengths.append(x - p[1])
        print(point0)
        print("l" + str(lengths))
'''