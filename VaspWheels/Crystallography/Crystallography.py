# This script is designed for crystallography analysis in aid of performing first-principle calculations.
# This code has referred to the article below when developing.
# W. Setyawan, S. Curtarolo. High-throughput electronic band structure calculations: Challenges and tools, Computational Materials Science, 49 (2010) 299-312.
# 此函数包利用numpy进行线性代数相关运算，详见：https://www.runoob.com/numpy/numpy-tutorial.html
# 以及：https://numpy.org/doc/stable/reference/array_api.html

import numpy as np

########################################################################################################################
# 基础模块：晶格常数与晶格基矢
# There are 14 kinds of Bravais lattice within 7 kinds of lattice system. (7大晶系，14种布拉菲晶格）
# Each lattice has its own set of lattice parameters, which is a list consisting with 6 parameters.
# Typical lattice_parameter = [a, b, c, alpha, beta, gamma]
# a, b, c is the three lattice constant, and alpha, beta, gamma is the three interaxial angle.
# There are two types of lattice vectors: unitcell and primitive.
# unitcell - The conventional lattice usually used in crystallography analysis.
# primitive - The lattice consistent with the stoichiometry, used in first-principle calculations.

# 此函数可通过指定晶格类型，以及给定晶格常数，计算出晶格基矢
def LatticeVector(lattice, lattice_parameter, lattice_type='primitive'):
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
    return np.array(lattice_vectors[lattice_type])  # 保证输出的结果为numpy的数组，方面后续矩阵运算

# 这个函数可以通过晶格基矢a, b, c计算晶格常数，但是记得输入必须是个由三个基矢组成的列表：[[a],[b],[c]]
def LatticeParameter(lattice_vector):
    lattice_vector = [np.array(lattice_vector[i]) for i in range(len(lattice_vector))]  # 将晶格基矢转换为数组，防止出错
    a_vec, b_vec, c_vec = lattice_vector                                                # 解压a, b, c基矢
    # 计算三个晶格基矢的长度，向量的二范数即向量的模
    a_len, b_len, c_len = [np.linalg.norm(lattice_vector[i],ord=2) for i in range(len(lattice_vector))]
    alpha = np.arccos(np.dot(b_vec, c_vec) / (b_len * c_len))  # 利用 cos(<a,b>) = a·b/(|a|·|b|)计算向量夹角
    beta = np.arccos(np.dot(a_vec, c_vec) / (a_len * c_len))   # 在python中，向量点乘（内积）可以通过np.dot()函数实现
    gamma = np.arccos(np.dot(a_vec, b_vec) / (a_len * b_len))
    return a_len, b_len, c_len, alpha, beta, gamma

########################################################################################################################
# 晶体学运算核心模块

# 给定晶格基矢(lattice vector)计算该空间的度规常量(Metric Tensor), 输入的晶格矩阵必须是由晶格基矢组成的numpy数组
def MetricTensor_from_LattVec(lattice_matrix): return lattice_matrix@lattice_matrix.T

# 给定晶格常数计算实空间的度规张量
def MetricTensor(lattice,lattice_parameter,lattice_type='primitive'):
    lattice_matrix = LatticeVector(lattice,lattice_parameter,lattice_type)  # LatticeVector()函数的输出已是数组形式
    metric_tensor = lattice_matrix@lattice_matrix.T  # @ - Python 3.5+中的操作，指代矩阵乘法
    return metric_tensor

# 给定晶格常数计算倒易空间基矢
def Reciprocal_Lattice(lattice,lattice_parameter,lattice_type='primitive'):
    a1, a2, a3 = LatticeVector(lattice,lattice_parameter,lattice_type)  # 计算正空间基矢

    V = np.inner(a1,np.cross(a2, a3))  # 计算实空间晶胞的体积

    # 倒空间基矢计算公式：b1 = 2*pi*(a2xa3)/[a1·(a2xa3)], b2 = 2*pi*(a3xa1)/[a1·(a2xa3)], b3 = 2*pi*(a1xa2)/[a1·(a2xa3)]
    reciprocal_lattice = (2.0 * np.pi / V) * np.array([np.cross(a2, a3), np.cross(a3, a1), np.cross(a1, a2)])

    return reciprocal_lattice

# 给定晶格常数计算倒易空间的度规张量
def Reciprocal_MetricTensor(lattice,lattice_parameter,lattice_type='primitive'):
    reciprocal_lattice_matrix = Reciprocal_Lattice(lattice,lattice_parameter,lattice_type)
    reciprocal_metric_tensor = reciprocal_lattice_matrix@reciprocal_lattice_matrix.T
    return reciprocal_metric_tensor

########################################################################################################################
# 晶体学运算高阶模块

# 计算不同空间坐标下向量的长度
def Length(vector,mode='lattice vector',**kwargs):
    # 初始化晶格基矢模式下所需的变量
    lattice_vector = kwargs['lattice_vector'] if 'lattice_vector' in kwargs else np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])
    # 初始化晶格常数模式下所需的变量
    lattice = kwargs['lattice'] if 'lattice' in kwargs else 'CUB'
    lattice_parameter = kwargs['lattice_parameter'] if 'lattice_parameter' in kwargs else [1.0, 1.0, 1.0, 90, 90, 90]
    lattice_type = kwargs['lattice_type'] if 'lattice_type' in kwargs else 'primitive'

    if mode == 'lattice vector':
        metric_tensor = MetricTensor_from_LattVec(lattice_vector)
    elif mode == 'lattice parameter':
        metric_tensor = MetricTensor(lattice,lattice_parameter,lattice_type)
    else:
        print(r'There are two available mode: "lattice parameter" or "lattice vector" .')
        return

    vec = np.array([vector])            # 将输入的向量转变为二维数组，方便利用numpy进行矩阵运算
    l_square = vec@metric_tensor@vec.T  # 利用度规张量计算向量的模（In NumPy, the @ operator means matrix multiplication）
    l = np.sqrt(l_square[0,0])          # 由于numpy二维数组的运算结果仍是二维数组，所以需要先提取元素再开方

    return l

# 此函数用于计算原子键长
def BondLength(atom1_pos,atom2_pos,mode='lattice vector',**kwargs):
    # 初始化晶格基矢模式下所需的变量
    lattice_vector = kwargs['lattice_vector'] if 'lattice_vector' in kwargs else np.array(
        [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])
    # 初始化晶格常数模式下所需的变量
    lattice = kwargs['lattice'] if 'lattice' in kwargs else 'CUB'
    lattice_parameter = kwargs['lattice_parameter'] if 'lattice_parameter' in kwargs else [1.0, 1.0, 1.0, 90, 90, 90]
    lattice_type = kwargs['lattice_type'] if 'lattice_type' in kwargs else 'primitive'

    if mode == 'lattice vector':
        metric_tensor = MetricTensor_from_LattVec(lattice_vector)
    elif mode == 'lattice parameter':
        metric_tensor = MetricTensor(lattice, lattice_parameter, lattice_type)
    else:
        print(r'There are two available mode: "lattice parameter" or "lattice vector" .')
        return

    atom1, atom2 = (np.array(atom1_pos),np.array(atom2_pos))  # 将原子坐标转换为数组，防止运算出错
    l_bond_vec = np.array([atom1-atom2])
    l_bond_sqaure = l_bond_vec@metric_tensor@l_bond_vec.T
    l_bond = np.sqrt(l_bond_sqaure[0][0])

    return l_bond

# 计算晶胞的体积
def Volume(lattice,lattice_parameter,lattice_type='primitive',space='real'):
    x, y, z = (np.zeros(3),np.zeros(3),np.zeros(3))  # 初始化晶胞基矢
    if space == 'real':
        x, y, z = LatticeVector(lattice,lattice_parameter,lattice_type)
    elif space == 'reciprocal':
        x, y, z = Reciprocal_Lattice(lattice,lattice_parameter,lattice_type)

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