import numpy as np


# original_lattice跟target_lattice的输入可以是二维数组，列表亦或是numpy矩阵，基本格式为
# [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]
# 其中，如a-axis的基矢[a1, a2, a3]则是由正交直角坐标系表示（Cartesian frame）
def LatticeTransform(fractional_coordinates,original_lattice,target_lattice):
    coordinates_old = np.array(fractional_coordinates)  # 将原子分数坐标列表转换为二维数组
    g1 = np.mat(original_lattice)   # 确保晶格矩阵的格式为numpy矩阵
    g2 = np.mat(target_lattice)     # g1与g2的维度都应该是dim=(3x3)
    g2_inverse = np.linalg.inv(g2)

    coordinates_new = []
    for n in range(len(coordinates_old)):
        r = np.array([coordinates_old[n]])  # 将原子坐标转换成二维数组以便后续计算，dim=(1x3)
        r_projected = np.dot(r,g1)
        r_new = np.dot(r_projected,g2_inverse)  # rt = r·g1·g2^(-1)
        coordinates_new.append(r_new[0])

    return np.array(coordinates_new)


