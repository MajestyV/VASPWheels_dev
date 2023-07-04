# This script is designed for crystallography analysis in aid of performing first-principle calculations.
# This code has referred to the article below when developing.
# W. Setyawan, S. Curtarolo. High-throughput electronic band structure calculations: Challenges and tools, Computational Materials Science, 49 (2010) 299-312.
# 此函数包利用numpy进行线性代数相关运算，详见：https://www.runoob.com/numpy/numpy-tutorial.html
# 以及：https://numpy.org/doc/stable/reference/array_api.html

import numpy as np

########################################################################################################################
# 基础模块：通过晶格常数计算晶胞基矢
# There are 14 kinds of Bravais lattice within 7 kinds of lattice system. (7大晶系，14种布拉菲晶格）
# Each lattice has its own set of lattice parameters, which is a list consisting with 6 parameters.
# Typical lattice_parameter = [a, b, c, alpha, beta, gamma]
# a, b, c is the three lattice constant, and alpha, beta, gamma is the three interaxial angle.
# There are two types of lattice vectors: unitcell and primitive.
# unitcell - The conventional lattice usually used in crystallography analysis.
# primitive - The lattice consistent with the stoichiometry, used in first-principle calculations.
def Bravais_lattice(lattice, lattice_parameter, lattice_type='primitive'):
    # 提取晶格常数
    a, b, c, alpha, beta, gamma = lattice_parameter

    # 从晶格常数计算对应晶格unitcell的基矢，并以字典形式储存
    unitcell_vectors = {'Orthorhombic': [[a, 0, 0],
                                         [0, b, 0],
                                         [0, 0, c]],
                        'Cubic': [[a, 0, 0],
                                  [0, a, 0],
                                  [0, 0, a]],
                        'Face-centered cubic': [[a, 0, 0],
                                                [0, a, 0],
                                                [0, 0, a]],
                        'Body-centered cubic': [[a, 0, 0],
                                                [0, a, 0],
                                                [0, 0, a]],
                        'Hexagonal': [[a / 2.0, -a * np.sqrt(3) / 2.0, 0],
                                      [a / 2.0, a * np.sqrt(3) / 2.0, 0],
                                      [0, 0, c]]}
    # 将缩写的键指向全称的值，并以字典形式记录
    unitcell_abbreviate = {'ORT': unitcell_vectors['Orthorhombic'],
                           'CUB': unitcell_vectors['Cubic'],
                           'FCC': unitcell_vectors['Face-centered cubic'],
                           'BCC': unitcell_vectors['Body-centered cubic'],
                           'HEX': unitcell_vectors['Hexagonal']}
    unitcell_vectors.update(unitcell_abbreviate)  # 将记录缩写字典中的键值对更新的基矢字典中，方便外部调用

    # 从晶格常数计算对应晶格primitive cell的基矢，并以字典形式储存
    primitive_vectors = {'Orthorhombic': [[0, b / 2.0, c / 2.0],
                                          [a / 2.0, 0, c / 2.0],
                                          [a / 2.0, b / 2.0, 0]],
                         'Cubic': [[a, 0, 0],
                                   [0, a, 0],
                                   [0, 0, a]],
                         'Face-centered cubic': [[0, a / 2.0, a / 2.0],
                                                 [a / 2.0, 0, a / 2.0],
                                                 [a / 2.0, a / 2.0, 0]],
                         'Body-centered cubic': [[-a / 2.0, a / 2.0, a / 2.0],
                                                 [a / 2.0, -a / 2.0, a / 2.0],
                                                 [a / 2.0, a / 2.0, -a / 2.0]],
                         'Hexagonal': [[a, 0, 0],
                                       [-a / 2.0, a * np.sqrt(3) / 2.0, 0],
                                       [0, 0, c]]}
    # 同样，将缩写的键指向全称的值，并以字典形式记录
    primitve_abbreviate = {'ORT': primitive_vectors['Orthorhombic'],
                           'CUB': primitive_vectors['Cubic'],
                           'FCC': primitive_vectors['Face-centered cubic'],
                           'BCC': primitive_vectors['Body-centered cubic'],
                           'HEX': primitive_vectors['Hexagonal']}
    primitive_vectors.update(primitve_abbreviate)  # 将记录缩写字典中的键值对更新的基矢字典中，方便外部调用

    # 把两个字典分配到不同晶格的模式的键值之下
    lattice_vectors = {'unitcell': unitcell_vectors[lattice],
                       'primitive': primitive_vectors[lattice]}
    return lattice_vectors[lattice_type]

########################################################################################################################
# 晶体学运算核心模块

# 计算实空间的度规张量(Metric Tensor)
def MetricTensor(lattice,lattice_parameter,lattice_type='primitive'):
    a1, a2, a3 = Bravais_lattice(lattice,lattice_parameter,lattice_type)
    g = [[np.dot(a1,a1), np.dot(a1,a2), np.dot(a1,a3)],
         [np.dot(a2,a1), np.dot(a2,a2), np.dot(a2,a3)],
         [np.dot(a3,a1), np.dot(a3,a2), np.dot(a3,a3)]]
    return np.array(g)

# 计算倒易空间基矢
def Reciprocal_lattice(lattice,lattice_parameter,lattice_type='primitive'):
    a1, a2, a3 = Bravais_lattice(lattice,lattice_parameter,lattice_type)  # 计算正空间基矢
    a1_x_a2, a2_x_a3, a3_x_a1 = (np.cross(a1,a2),np.cross(a2,a3), np.cross(a3,a1))  # 提前算好基矢的交叉叉乘结果，方便调用以减少代码计算量

    V = np.inner(a1,a2_x_a3)  # 计算实空间晶胞的体积

    # 倒空间基矢计算公式：b1 = 2*pi*(a2xa3)/[a1·(a2xa3)], b2 = 2*pi*(a3xa1)/[a1·(a2xa3)], b3 = 2*pi*(a1xa2)/[a1·(a2xa3)]
    pi = np.pi
    b1 = [(2.0*pi/V)*a2_x_a3[n] for n in range(len(a2_x_a3))]
    b2 = [(2.0*pi/V)*a3_x_a1[n] for n in range(len(a3_x_a1))]
    b3 = [(2.0*pi/V)*a1_x_a2[n] for n in range(len(a1_x_a2))]

    return np.array([b1,b2,b3])

# 计算倒易空间的度规张量
def Reciprocal_MetricTensor(lattice,lattice_parameter,lattice_type='primitive'):
    b1, b2, b3 = Reciprocal_lattice(lattice,lattice_parameter,lattice_type)
    g_star = [[np.inner(b1,b1), np.inner(b1,b2), np.inner(b1,b3)],
              [np.inner(b2,b1), np.inner(b2,b2), np.inner(b2,b3)],
              [np.inner(b3,b1), np.inner(b3,b2), np.inner(b3,b3)]]
    return np.array(g_star)

########################################################################################################################
# 晶体学运算高阶模块

# 利用度规张量（metric tensor）计算不同空间坐标下向量的长度
def length(vector,metric_tensor=np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])):
    vec = np.array([vector])            # 将输入的向量转变为二维数组，方便利用numpy进行矩阵运算
    d_square = vec@metric_tensor@vec.T  # 利用度规张量计算向量的模（In NumPy, the @ operator means matrix multiplication）
    d = np.sqrt(d_square[0,0])          # 由于numpy二维数组的运算结果仍是二维数组，所以需要先提取元素再开方
    return d

# 计算晶胞的体积
def Volume(lattice,lattice_parameter,lattice_type='primitive',space='real'):
    x, y, z = (np.zeros(3),np.zeros(3),np.zeros(3))  # 初始化晶胞基矢
    if space == 'real':
        x, y, z = Bravais_lattice(lattice,lattice_parameter,lattice_type)
    elif space == 'reciprocal':
        x, y, z = Reciprocal_lattice(lattice,lattice_parameter,lattice_type)

    V = np.inner(x, np.cross(y,z))  # 计算晶胞体积

    return V


if __name__ == '__main__':
    a = [1, 2, 3]
    a2 = [3, 2, 1]

    b = [[1, 1, 1],
         [2, 2, 2],
         [3, 3, 3]]

    c = [[1, 0, 0],
         [0, 2, 0],
         [0, 0, 3]]

    # print(np.outer(a,a2))
    # print(np.cross(a,a2))
    # print(np.inner(a,b))
    # print(np.outer(a,b))

    # print(np.zeros(3))

    print(np.array([a]) @ np.array(c) @ np.array([a]).T)