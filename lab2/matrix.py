import math as m

class Mat():
    def __init__(self, args):
        if type(args[0]) == int:
            rows, cols = args[0], args[1]
            self.mat = [[0 for _ in range(cols)] for _ in range(rows)]
        else:
            data = args[0]
            shape = args[1]
            self.mat = [[0 for _ in range(shape[1])] for _ in range(shape[0])]
            for i in range(shape[0]):
                for j in range(shape[1]):
                    self.mat[i][j] = data[i * shape[0] + j]
        

    def __mul__(self, other):
        res = Mat((len(self.mat), len(other[0])))
        for i in range(len(self.mat)):
            for j in range(len(res[0])):
                for k in range(len(self.mat[0])):
                    res[i][j] += self.mat[i][k] * other[k][j]
        return res

    def __add__(self, other):
        res = Mat((len(self.mat), len(self.mat[0])))
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                res[i][j] = self.mat[i][j] + other[i][j]
        return res
    
    def __repr__(self):
        res = '['
        for l in self.mat:
            res += str(l) + '\n'
        res = res[:-1] + ']'
        return res
    
    def __getitem__(self, key):
        if type(key) == int:
            return self.mat[key]
        else:
            return self.mat[key[1]][key[0]]

    def __len__(self):
        return len(self.mat)
    
    def unit(self):
        for i in range(len(self.mat)):
            self.mat[i][i] = 1
    
class ScaleMat3(Mat):
    def __init__(self, kx, ky):
        super().__init__((3, 3))
        self.mat[0][0] = kx
        self.mat[1][1] = ky
        self.mat[2][2] = 1
    
class TranslationMat3(Mat):
    def __init__(self, dx, dy):
        super().__init__((3, 3))
        self.unit()
        self.mat[-1][0] = dx
        self.mat[-1][1] = dy
        # self.mat[0][-1] = dx
        # self.mat[1][-1] = dy

class RotationMat3(Mat):
    def __init__(self, angle):
        super().__init__((3, 3))
        cos = m.cos(angle)
        sin = m.sin(angle)
        self.mat[0][0] = cos
        self.mat[0][1] = sin
        self.mat[1][0] = -sin
        self.mat[1][1] = cos
        self.mat[-1][-1] = 1
        # print(self.mat)