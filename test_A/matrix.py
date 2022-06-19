class Matrix:

    def __init__(self, size):
        if size == 10:
            self.x_axis_row = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        elif size == 9:
            self.x_axis_row = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        elif size == 8:
            self.x_axis_row = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        elif size == 7:
            self.x_axis_row = [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        elif size == 6:
            self.x_axis_row = [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        elif size == 5:
            self.x_axis_row = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        elif size == 4:
            self.x_axis_row = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        elif size == 3:
            self.x_axis_row = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        elif size == 2:
            self.x_axis_row = [
                [0, 0],
                [0, 0],
            ]
        else:
            raise Exception("Size is too small or too big (2-10, inclusive): "+str(size))

    def add(self, value, y, x):
        self.x_axis_row[x][y] = value

    def get_value(self):
        values = {}
        i = 0
        for x in self.x_axis_row:
            values[i] = x
            i += 1
        return values

    def print(self):
        print("   -   0.00   1.00   2.00   3.00   4.00   5.00   6.00   7.00   8.00   9.00   ")
        var = 0
        for x in self.x_axis_row:

            str_list = ""
            for xx in x:
                v = xx.__round__(2).__str__()
                if len(v) == 1:
                    v = v + ".00"
                elif len(v) == 3:
                    v = v + "0"
                str_list += v+"   "

            print("" + var.__str__() + ".00   " + str_list)
            var += 1

    def __iter__(self):
        iters = []
        for x in self.x_axis_row:
            iters.append(iter(x))
        return iter(iters)